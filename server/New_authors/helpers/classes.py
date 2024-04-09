from django.views.generic import DeleteView, ListView
from django.http import HttpResponse


class CustomDeleteView(DeleteView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(status=404)


class AdminListView(ListView):
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        return HttpResponse(status=403)
