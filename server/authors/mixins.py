from django.contrib.auth.mixins import AccessMixin

class IsAuthMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_author:
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()