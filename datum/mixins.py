from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from datum.models import Profile, Preference

class ProfileUpdatePermissionMixin(LoginRequiredMixin, PermissionRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and Profile.objects.get(
            user=self.request.user,
            pk=self.request.user.profile.pk
        ):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class PreferenceUpdatePermissionMixing(LoginRequiredMixin, PermissionRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and Preference.objects.get(
            user=self.request.user,
            pk=self.request.user.user_preference.pk
        ):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)