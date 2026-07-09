from django.views.generic import DeleteView
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponse


class CustomDeleteView(DeleteView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(status=404)


class UserIsAdminMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
