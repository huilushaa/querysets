from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class BookQuerySet(models.QuerySet):
    def bestselling_book(self):
        return self.filter(bestseller=True)


class Book(models.Model):
    title = models.CharField(max_length=200)
    published_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bestseller = models.BooleanField(default=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    categories = models.ManyToManyField('Category', related_name='categories')

    objects = BookQuerySet.as_manager()

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
