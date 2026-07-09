from abc import abstractmethod
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
    

class FormBasedOnType:
    class Meta:
        fields_to_refresh: list | tuple = ()
    
    def __init__(self, *args, **kwargs):
        self.context_type = kwargs.pop("context_type", None)
        super().__init__(*args, **kwargs)
        
    def save(self, commit=True):
        if self.context_type == "edit":
            self.instance.refresh_from_db(fields=self.Meta.fields_to_refresh)
            
            self.edit_refreshed()
            
            self.instance.save()
            return self.instance
        return super().save(commit)
    
    @abstractmethod
    def edit_refreshed(self):
        pass
