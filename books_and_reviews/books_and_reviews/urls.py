"""
URL configuration for books_and_reviews project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from books import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.book_list, name='book_list'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('book/<int:book_id>/<str:isbn_prefix>/', views.book_detail, name='book_detail'),
    path('books/isbn/<str:isbn_prefix>/', views.books_isbn, name='books_isbn'),
    path('show/books/', views.show_books, name='show_books'),
    path('show/reviews/', views.show_reviews, name='show_reviews'),    
    path('show/authors/', views.show_authors, name='show_authors'),    
    path('show/authors/fname', views.show_authors_fname, name='show_authors_fname'),    
    path('show/authors/lname', views.show_authors_lname, name='show_authors_lname'),    
    path('delete/author/', views.delete_author, name='delete_author'),    
    path('add/book/', views.add_book, name='add_book'),    
    path('add/author/', views.add_author, name='add_author'),    
    path('add/review/', views.add_review, name='add_review'),
    path('update/book/title', views.update_book_title, name='update_book_title'),    
    path('update/authors/name', views.update_authors_name, name='update_authors_name'),        
]




