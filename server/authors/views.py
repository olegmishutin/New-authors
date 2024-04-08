from django.views import generic
from django.http import HttpResponse
from users.models import User
from New_authors.otherFunctions.functions import filterContext


class Authors(generic.ListView):
    model = User
    template_name = 'authors.html'
    context_object_name = 'authors'
    paginate_by = 24

    def get_queryset(self):
        checkboxesFilters = {'hightRatingAuthors': '-rating', 'lowRatingAuthors': 'rating',
                             'newAuthors': '-date_joined', 'popularAuthors': '-reviewsCount'}

        self.authors = User.getAuthors()
        self.filteredContext = filterContext(self.request, self.authors, checkboxesFilters)
        return self.filteredContext.get('queryset')

    def get_context_data(self, *, object_list=None, **kwargs):
        self.context = super().get_context_data(**kwargs)
        self.context['isAdmin'] = False
        self.context.update(self.filteredContext.get('context'))
        return self.context


class AuthorsAdmin(Authors):
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        return HttpResponse(status=403)

    def get_context_data(self, *, object_list=None, **kwargs):
        super().get_context_data(**kwargs)
        self.context['isAdmin'] = True
        self.context['authorsNumber'] = self.authors.count()
        return self.context
