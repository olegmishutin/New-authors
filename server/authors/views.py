from django.views import generic
from users.models import User
from New_authors.helpers.functions import filterContext
from New_authors.helpers.classes import UserIsAdminMixin


class Authors(generic.ListView):
    model = User
    template_name = "authors.html"
    context_object_name = "authors"
    paginate_by = 24

    def get_queryset(self):
        checkboxesFilters = {
            "hightRatingAuthors": "-rating",
            "lowRatingAuthors": "rating",
            "newAuthors": "-date_joined",
            "popularAuthors": "-reviewsCount",
        }

        self.authors = User.getAuthors()
        queryset, self.filters_context = filterContext(
            self.request, self.authors, checkboxesFilters
        )
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        self.context = super().get_context_data(**kwargs)
        self.context["isAdmin"] = False
        self.context.update(self.filters_context)
        return self.context


class AuthorsAdmin(UserIsAdminMixin, Authors):
    def get_context_data(self, *, object_list=None, **kwargs):
        super().get_context_data(**kwargs)
        self.context["isAdmin"] = True
        self.context["authorsNumber"] = self.authors.count()
        return self.context
