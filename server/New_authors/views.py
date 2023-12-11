import random
from django.shortcuts import render
from users.models import User
from books.models import Book
from categories.models import Category


def menu(request):
    popularAuthor = User.getAllWithStatistics(User).order_by('-reviewsCount')[:12]
    books = Book.getAllWithStatistics(Book)

    newBooks = books.order_by('-publication_date')[:12]
    popularBooks = books.order_by('-reviewsCount')

    categoriesTorandomise = []
    categories = Category.objects.all()

    for category in categories:
        if category.book_set.count() > 0:
            categoriesTorandomise.append(category)

    return render(request, 'menu.html',
                  {'popularAuthor': popularAuthor, 'newBooks': newBooks, 'popularBooks': popularBooks,
                   'category': random.choice(categoriesTorandomise) if categories else []})
