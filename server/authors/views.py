from django.views import generic
from django.http import HttpResponse
from django.core.paginator import Paginator
from users.models import User


class Authors(generic.ListView):
    model = User
    template_name = 'authors.html'
    context_object_name = 'authors'

    def get_context_data(self, *, object_list=None, **kwargs):
        self.context = super().get_context_data(**kwargs)
        self.context['isAdmin'] = False

        authors = User.getAuthors(User)
        self.context['authorsNumber'] = authors.count()

        filters = []
        checkboxesFilters = {'hightRatingAuthors': '-rating', 'lowRatingAuthors': 'rating',
                             'newAuthors': '-date_joined', 'popularAuthors': '-reviewsCount'}

        for checkbox, filter in checkboxesFilters.items():
            if self.request.GET.get(checkbox):
                filters.append(filter)
                self.context[checkbox] = 'checked'

        authors = authors.order_by(*filters)
        self.context['page_obj'] = Paginator(authors, 24).get_page(self.request.GET.get('page'))
        return self.context


class AuthorsAdmin(Authors):
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        return HttpResponse(status=403)

    def get_context_data(self, *, object_list=None, **kwargs):
        super().get_context_data(**kwargs)
        self.context['isAdmin'] = True
        return self.context
