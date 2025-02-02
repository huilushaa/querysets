import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'queryset.settings')
django.setup()

from methods.models import Book, Author, Category
from datetime import date

author1 = Author.objects.create(name='Пушкин', age=40, country='Россия')
author2 = Author.objects.create(name='Толстой', age=70, country='Казахстан')
author3 = Author.objects.create(name='Киргизов', age=19, country='США')
#//////////////////////////////////////////////////////////////////////////////
scientific = Category.objects.create(name='Scientific')
drama = Category.objects.create(name='Drama')
thriller = Category.objects.create(name='Thriller')
fantastic = Category.objects.create(name='Fantastic')
mystery = Category.objects.create(name='Mystery')
#//////////////////////////////////////////////////////////////////////////////
book1 = Book.objects.create(title='Капитанская дочка',
                            published_date=date(1836, 12, 10),
                            price=120.99,
                            bestseller=True,
                            author=author1)
book1.categories.set(drama)

book2 = Book.objects.create(title='Золотая рыбка',
                            published_date=date(1833, 2,10),
                            price=70.99,
                            bestseller=False,
                            author=author1)
book2.categories.set(fantastic, drama)

book3 = Book.objects.create(title='Война и мир',
                            published_date=date(1724, 4,11),
                            price=250.99,
                            bestseller=True,
                            author=author2)
book3.categories.set(drama)

book4 = Book.objects.create(title='Детство',
                            published_date=date(1733, 11,11),
                            price=99.99,
                            bestseller=False,
                            author=author2)
book4.categories.set(drama)

book5 = Book.objects.create(title='Как я провел лето',
                            published_date=date(2019, 9,12),
                            price=10.99,
                            bestseller=False,
                            author=author3)
book5.categories.set(fantastic, mystery, thriller)

book6 = Book.objects.create(title='Курсовой проект',
                            published_date=date(2024, 12,24),
                            price=5000,
                            bestseller=True,
                            author=author3)
book6.categories.set(scientific, drama, thriller)
#//////////////////////////////////////////////////////////////////////////////

#фильтрации по датам публикации раньше 1800 года.
print("\n1. all() - :")
books = Book.objects.filter(published_date__lt=date(1800, 1, 1))
print(books)
