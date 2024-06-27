from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

class Author(models.Model):
    firstname = models.CharField(max_length=50, null=True)
    lastname = models.CharField(max_length=50, null=True)
    biography = models.TextField()
    birth_year = models.IntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.now().year)
        ],
        default=2000
    )
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_date = models.DateField()
    ISBN = models.CharField(max_length=13, unique=True)
    summary = models.TextField()
    content = models.TextField(null=True, blank=True)  # Allows null values and optional content

    def __str__(self):
        return self.title

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reviewer_name = models.CharField(max_length=100)
    review_text = models.TextField()
    rating = models.IntegerField()  # assuming rating is between 1 and 5
    review_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.reviewer_name} for {self.book.title}'
