"""
django-tickManage - A Django powered ticket tracker for small enterprise.

(c) Copyright 2008 Jutda. All Rights Reserved. See LICENSE for details.

views/public.py - All public facing views, eg non-staff (no authentication
                  required) views.
"""
import logging

from django.core.exceptions import (
    ObjectDoesNotExist, PermissionDenied, ImproperlyConfigured,
)
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.http import urlquote
from django.utils.translation import ugettext as _
from django.conf import settings
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from tickManage import settings as tickManage_settings
from tickManage.decorators import protect_view, is_tickManage_staff
import tickManage.views.staff as staff
import tickManage.views.abstract_views as abstract_views
from tickManage.forms import PublicTicketForm
from tickManage.lib import text_is_spam
from tickManage.models import CustomField, Ticket, Queue, UserSettings, KBCategory, KBItem
from tickManage.user import huser_from_request

logger = logging.getLogger(__name__)


def create_ticket(request, *args, **kwargs):
    if is_tickManage_staff(request.user):
        return staff.CreateTicketView.as_view()(request, *args, **kwargs)
    else:
        return CreateTicketView.as_view()(request, *args, **kwargs)


class BaseCreateTicketView(abstract_views.AbstractCreateTicketMixin, FormView):
    form_class = PublicTicketForm

    def dispatch(self, *args, **kwargs):
        request = self.request
        if not request.user.is_authenticated and tickManage_settings.TICKMANAGE_REDIRECT_TO_LOGIN_BY_DEFAULT:
            return HttpResponseRedirect(reverse('login'))

        if is_tickManage_staff(request.user) or \
                (request.user.is_authenticated and
                 tickManage_settings.TICKMANAGE_ALLOW_NON_STAFF_TICKET_UPDATE):
            try:
                if request.user.usersettings_tickManage.login_view_ticketlist:
                    return HttpResponseRedirect(reverse('tickManage:list'))
                else:
                    return HttpResponseRedirect(reverse('tickManage:dashboard'))
            except UserSettings.DoesNotExist:
                return HttpResponseRedirect(reverse('tickManage:dashboard'))
        return super().dispatch(*args, **kwargs)

    def get_initial(self):
        initial_data = super().get_initial()

        # add pre-defined data for public ticket
        if hasattr(settings, 'TICKMANAGE_PUBLIC_TICKET_QUEUE'):
            # get the requested queue; return an error if queue not found
            try:
                initial_data['queue'] = Queue.objects.get(
                    slug=settings.TICKMANAGE_PUBLIC_TICKET_QUEUE,
                    allow_public_submission=True
                ).id
            except Queue.DoesNotExist as e:
                logger.fatal(
                    "Public queue '%s' is configured as default but can't be found",
                    settings.TICKMANAGE_PUBLIC_TICKET_QUEUE
                )
                raise ImproperlyConfigured("Wrong public queue configuration") from e
        if hasattr(settings, 'TICKMANAGE_PUBLIC_TICKET_PRIORITY'):
            initial_data['priority'] = settings.TICKMANAGE_PUBLIC_TICKET_PRIORITY
        if hasattr(settings, 'TICKMANAGE_PUBLIC_TICKET_DUE_DATE'):
            initial_data['due_date'] = settings.TICKMANAGE_PUBLIC_TICKET_DUE_DATE
        return initial_data

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        if '_hide_fields_' in self.request.GET:
            kwargs['hidden_fields'] = self.request.GET.get('_hide_fields_', '').split(',')
        kwargs['readonly_fields'] = self.request.GET.get('_readonly_fields_', '').split(',')
        return kwargs

    def form_valid(self, form):
        request = self.request
        if text_is_spam(form.cleaned_data['body'], request):
            # This submission is spam. Let's not save it.
            return render(request, template_name='tickManage/public_spam.html')
        else:
            ticket = form.save(user=self.request.user if self.request.user.is_authenticated else None)
            try:
                return HttpResponseRedirect('%s?ticket=%s&email=%s&key=%s' % (
                    reverse('tickManage:public_view'),
                    ticket.ticket_for_url,
                    urlquote(ticket.submitter_email),
                    ticket.secret_key)
                )
            except ValueError:
                # if someone enters a non-int string for the ticket
                return HttpResponseRedirect(reverse('tickManage:home'))

    def get_success_url(self):
        request = self.request


class CreateTicketIframeView(BaseCreateTicketView):
    template_name = 'tickManage/public_create_ticket_iframe.html'

    @csrf_exempt
    @xframe_options_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        if super().form_valid(form).status_code == 302:
            return HttpResponseRedirect(reverse('tickManage:success_iframe'))


class SuccessIframeView(TemplateView):
    template_name = 'tickManage/success_iframe.html'

    @xframe_options_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CreateTicketView(BaseCreateTicketView):
    template_name = 'tickManage/public_create_ticket.html'


class Homepage(CreateTicketView):
    template_name = 'tickManage/public_homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kb_categories'] = huser_from_request(self.request).get_allowed_kb_categories()
        return context


def search_for_ticket(request, error_message=None):
    if hasattr(settings, 'TICKMANAGE_VIEW_A_TICKET_PUBLIC') and settings.TICKMANAGE_VIEW_A_TICKET_PUBLIC:
        email = request.GET.get('email', None)
        return render(request, 'tickManage/public_view_form.html', {
            'ticket': False,
            'email': email,
            'error_message': error_message,
            'tickManage_settings': tickManage_settings,
        })
    else:
        raise PermissionDenied("Public viewing of tickets without a secret key is forbidden.")


@protect_view
def view_ticket(request):
    ticket_req = request.GET.get('ticket', None)
    email = request.GET.get('email', None)
    key = request.GET.get('key', '')

    if not (ticket_req and email):
        if ticket_req is None and email is None:
            return search_for_ticket(request)
        else:
            return search_for_ticket(request, _('Missing ticket ID or e-mail address. Please try again.'))

    queue, ticket_id = Ticket.queue_and_id_from_query(ticket_req)
    try:
        if hasattr(settings, 'TICKMANAGE_VIEW_A_TICKET_PUBLIC') and settings.TICKMANAGE_VIEW_A_TICKET_PUBLIC:
            ticket = Ticket.objects.get(id=ticket_id, submitter_email__iexact=email)
        else:
            ticket = Ticket.objects.get(id=ticket_id, submitter_email__iexact=email, secret_key__iexact=key)
    except (ObjectDoesNotExist, ValueError):
        return search_for_ticket(request, _('Invalid ticket ID or e-mail address. Please try again.'))

    if is_tickManage_staff(request.user):
        redirect_url = reverse('tickManage:view', args=[ticket_id])
        if 'close' in request.GET:
            redirect_url += '?close'
        return HttpResponseRedirect(redirect_url)

    if 'close' in request.GET and ticket.status == Ticket.RESOLVED_STATUS:
        from tickManage.views.staff import update_ticket
        # Trick the update_ticket() view into thinking it's being called with
        # a valid POST.
        request.POST = {
            'new_status': Ticket.CLOSED_STATUS,
            'public': 1,
            'title': ticket.title,
            'comment': _('Submitter accepted resolution and closed ticket'),
        }
        if ticket.assigned_to:
            request.POST['owner'] = ticket.assigned_to.id
        request.GET = {}

        return update_ticket(request, ticket_id, public=True)

    # redirect user back to this ticket if possible.
    redirect_url = ''
    if tickManage_settings.TICKMANAGE_NAVIGATION_ENABLED:
        redirect_url = reverse('tickManage:view', args=[ticket_id])

    return render(request, 'tickManage/public_view_ticket.html', {
        'key': key,
        'mail': email,
        'ticket': ticket,
        'tickManage_settings': tickManage_settings,
        'next': redirect_url,
    })


def change_language(request):
    return_to = ''
    if 'return_to' in request.GET:
        return_to = request.GET['return_to']

    return render(request, 'tickManage/public_change_language.html', {'next': return_to})
