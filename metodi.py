import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'queryset.settings')
django.setup()

from methods.models import Book, Author, Category
from datetime import date
from django.db import transaction
from decimal import Decimal
from django.db.models import Count, Q, Sum

# author1 = Author.objects.create(name='Пушкин', age=40, country='Россия')
# author2 = Author.objects.create(name='Толстой', age=70, country='Казахстан')
# author3 = Author.objects.create(name='Киргизов', age=19, country='США')
#
# scientific = Category.objects.create(name='Scientific')
# drama = Category.objects.create(name='Drama')
# thriller = Category.objects.create(name='Thriller')
# fantastic = Category.objects.create(name='Fantastic')
# mystery = Category.objects.create(name='Mystery')
#
# book1 = Book.objects.create(title='Капитанская дочка',
#                             published_date=date(1836, 12, 10),
#                             price=120.99,
#                             bestseller=True,
#                             author=author1)
# book1.categories.set([drama])
#
# book2 = Book.objects.create(title='Золотая рыбка',
#                             published_date=date(1833, 2, 10),
#                             price=70.99,
#                             bestseller=False,
#                             author=author1)
# book2.categories.set([fantastic, drama])
#
# book3 = Book.objects.create(title='Война и мир',
#                             published_date=date(1724, 4, 11),
#                             price=250.99,
#                             bestseller=True,
#                             author=author2)
# book3.categories.set([drama])
#
# book4 = Book.objects.create(title='Детство',
#                             published_date=date(1733, 11, 11),
#                             price=99.99,
#                             bestseller=False,
#                             author=author2)
# book4.categories.set([drama])
#
# book5 = Book.objects.create(title='Как я провел лето',
#                             published_date=date(2019, 9, 12),
#                             price=10.99,
#                             bestseller=False,
#                             author=author3)
# book5.categories.set([fantastic, mystery, thriller])
#
# book6 = Book.objects.create(title='Курсовой проект',
#                             published_date=date(2024, 12, 24),
#                             price=5000,
#                             bestseller=True,
#                             author=author3)
# book6.categories.set([scientific, drama, thriller])

# filter() книг по датам публикации раньше 1800 года.
print("\n1. filter() - :")
books = Book.objects.filter(published_date__lt=date(1800, 1, 1))
print(books)

# exclude() книг, не являющихся бестселлерами
print("\n2. exclude() - :")
books = Book.objects.exclude(bestseller=True)
print(books)

# annotate() кол-ва книг для каждого автора
print("\n3. annotate() - :")
authors = Author.objects.annotate(count_of_books=Count('books'))
for author in authors:
    print(f'{author.name} написал(-a) {author.count_of_books} книг(-у)')

# alias() для добавления псевдонима для суммы цен книг, которые являются бестселлерами
print("\n4. alias() - :")
authors = Author.objects.alias(total=Sum('books__price', filter=Q(books__bestseller=True)))
authors = authors.filter(total__gt=200)
for a in authors:
    print(f'{a.name} имеет бестселлеры дороже 200 рублей')

# order_by() книг по убыванию цены и возрастанию названия
print("\n5. order_by() - :")
books = Book.objects.order_by('-price', 'title')
print(books)

# reverse() книг по убыванию айди
print("\n6. reverse() - :")
books = Book.objects.all().order_by('id').reverse()
for b in books:
    print(f'{b.title}, а айди {b.id}')

# distinct() для проблемного случая вывода "уникальных" авторов из-за сортировки по связанным полям
print("\n7. distinct() - :")
authors = Author.objects.order_by('books__title').distinct()
print(authors)

# values() для вывода полей айди и тайтла книг
print("\n8. values() - :")
books = Book.objects.values('id', 'title')
print(books)

# values_list() для вывода айди авторов
print("\n9. values_list() - :")
authors = Author.objects.values_list('id', 'name').order_by('-id')
print(authors)

# dates() для вывода уникальных дат, усеченных до недель
print("\n10. dates() - :")
books = Book.objects.dates('published_date', 'week')
print(books)

# datetimes() для вывода годов публикации книг по убыванию. По сути то же самое. что и дейт, но усечение до времени
# rint("\n11. datetimes() - :")
# books = Book.objects.datetimes('published_date', 'year')
# print(books)

# none() для вызова пустого кверисета
print("\n12.none() - :")
books = Book.objects.filter(bestseller=True).none()
print(books)

# all() для вывода все женров книг
print("\n13. all() - :")
catregories = Category.objects.all()
print(catregories)

# union() для объединения названия книг с именами авторов и категорий
print("\n14. union() - :")
authors = Author.objects.values('name')
books = Book.objects.values('title')
categories = Category.objects.values('name')
books = books.union(categories, authors)
print(books)

# intersection() для возврата общих элементов из прошлого объединения юнион с моделью писателей
print("\n15. intersection() - :")
authors = Author.objects.values('name')
books = Book.objects.values('title')
categories = Category.objects.values('name')
books = books.union(categories, authors)
print(authors.intersection(books))

# difference() для возврата отличных элементов кверисета модели книг, которые не являются бестселлерами
print("\n16. difference() - :")
books = Book.objects.all()
books2 = Book.objects.filter(bestseller=True)
print(books.difference(books2))

# select_related() для получения авторов. связанных с моделью книги
print("\n17. select_related() - :")
authors = Book.objects.select_related('author').all()
for book in authors:
    print(f'Книга: {book.title}, Автор: {book.author.name}')

# prefetch_related() для получения всех категорий из модели книг
print("\n18. prefetch_related() - :")
books = Book.objects.prefetch_related('categories')
for book in books:
    print(f'Книга "{book.title}" имеет жанры: {", ".join(category.name for category in book.categories.all())}')

# extra() устаревшее. не имеет больше смыысла

# defer() для ленивого извлечения полей title и price из модели Book
print("\n19. defer() - :")
books = Book.objects.defer('title', 'price')
for book in books:
    print(f'{book.title}, {book.price}')

# only() противоположный прошлому методу
print("\n20. only() - :")
books = Book.objects.only('title')
print([book.title for book in books])

# using() для выбора базы данных (к сожалению. тут только одна, так что использовать буду default)
print("\n21. using() - :")
books = Book.objects.using('default').all()
print(books)


# select_for_update() для блокировки транзакции по изменению цены книги
print("\n22. select_for_update() - :")

def update_book_price(book_id, new_price):
    try:
        with transaction.atomic():
            book = Book.objects.select_for_update().get(pk=book_id)
            print(f'Блокировка книги: {book.title}, текущая цена: {book.price}')
            book.price = new_price
            book.save()
            print(f'Цена книги {book.title} успешно обновлена до {new_price}!')
    except Book.DoesNotExist:
        print('Книга с указанным айди не найдена')


print(update_book_price(3, 267))
print(update_book_price(53, 270))

#raw() для получения всех тайтлов книг
print("\n23. raw() - :")
query = 'SELECT id, title FROM methods_book'
books = Book.objects.raw(query)
print([book.title for book in books])

#get_or_create() для создания автора
print("\n24. get_or_create() - :")
author, created = Author.objects.get_or_create(name='Киргизов',
                                      age=19,
                                      country='США')
if created:
    print(f'Автор {author} был создан')
else:
    print(f'Автор {author} уже существовал')

#update_or_create() для обновления или создания автора
print("\n25. update_or_create() - :")
author, created = Author.objects.update_or_create(
    name='Блуд',
    defaults={'age': '38'},
    create_defaults={'name': 'Блуд', 'age': 38, 'country': 'Россия'},
)
if created:
    print(f'Был создан автор {author}')
else:
    print(f'Для автора {author} было обновлено поле age на {author.age}')

#bulk_create() для массового создания авторов
print("\n26. bulk_create() - :")
authors = [
    Author(name='aaa', age=10, country='AAA'),
    Author(name='bbb', age=11, country='BBB'),
    Author(name='ccc', age=12, country='CCC'),
]
Author.objects.bulk_create(authors, batch_size=2)
print(Author.objects.order_by('-id')[:3])

#bulk_update() для массового обновления возраста у авторов
print("\n27. bulk_update() - :")
authors = Author.objects.order_by('-id')[:3]
for author in authors:
    author.age += 10
Author.objects.bulk_update(authors, ['age'])
print([author.age for author in authors])

#in_bulk для массового извлечений категорий книг по их айди
print("\n28. bulk_update() - :")
ids = [56, 57, 58]
catregories = Category.objects.in_bulk(ids)
print(catregories)

#iterator() для уменьшения нагрузки на БД при выводе данных о всех авторах
print("\n29. iterator() - :")
authors = Author.objects.all().iterator(chunk_size=10)
print([a for a in authors])

#latest() для возвращения последней выпущенной книги по дате выпуска
print("\n30. latest() - :")
book = Book.objects.latest('published_date')
print(book)

#earliest(), самый ранний объект, first() первый объеке, last() последний
print("\n31-33. earliest(), first(), last()  - :")
print("\n31-33. earliest(), first(), last()  - :")
books = Book.objects.all()
print([books.earliest('published_date'), books.order_by('id').first(), books.order_by('author__age').last()])

#aggregate() для вывода общей суммы всех книг
print("\n34. aggregate() - :")
books_total_sum = Book.objects.aggregate(Sum('price'))
print(books_total_sum)

#exists() для проверки существования книг. выпущенных позднее или в дату 01.01.2024
print("\n35. exists() - :")
print(Book.objects.filter(published_date__gte=date(2024, 1, 1)).exists())

#contains() для проверки содержит ли наш кверисет книг книгу с названием капитанская дочка
print("\n36. contains() - :")
print(Book.objects.contains(Book.objects.get(title='Капитанская дочка')))

#update() для обновления полей в объектах. полученных по фильтру
print("\n37. update() - :")
Book.objects.filter(published_date__year=2024).update(bestseller=False)
book = Book.objects.get(published_date__year=2024)
print(book.bestseller)
Book.objects.filter(published_date__year=2024).update(bestseller=True)
book = Book.objects.get(published_date__year=2024)
print(book.bestseller)

#as_manager() для получения всхе бестселлеров (в модели книги создали его)
print("\n38. as_manager() - :")
books = Book.objects.bestselling_book()
print(books)

#explain(). чтобы увидеть, как наша ORM обращается к базе данных
print("\n39. explain() - :")
print(Book.objects.all().explain())

