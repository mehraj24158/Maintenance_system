#!/usr/bin/python

from django.core.management.base import BaseCommand

from tickManage.email import process_email


class Command(BaseCommand):

    def __init__(self):
        BaseCommand.__init__(self)

    help = 'Process django-tickManage queues and process e-mails via POP3/IMAP or ' \
           'from a local mailbox directory as required, feeding them into the tickManage.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--quiet',
            action='store_true',
            dest='quiet',
            default=False,
            help='Hide details about each queue/message as they are processed',
        )

    def handle(self, *args, **options):
        quiet = options.get('quiet', False)
        process_email(quiet=quiet)


if __name__ == '__main__':
    process_email()
