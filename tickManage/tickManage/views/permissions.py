from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from tickManage.decorators import is_tickManage_staff


class MustBeStaffMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return is_tickManage_staff(self.request.user)
