from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.db import connection, IntegrityError
from .models import Book, Author
#from djangoviz import charts

def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

def book_detail(request, book_id, isbn_prefix=None):
    #return JsonResponse({'isbn_prefix': isbn_prefix})
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'books/book_detail.html', {'book': book, 'isbn_prefix': isbn_prefix})

def api_book(request):
    select_query = "SELECT * FROM books_book INNER JOIN books_author where books_book.author_id = books_author.id"
    with connection.cursor() as cursor:
        cursor.execute(select_query)
        rows = cursor.fetchall()

    # Convert the result into a list of dictionaries
    columns = [col[0] for col in cursor.description]
    books_list = [
        dict(zip(columns, row))
        for row in rows
    ]

    return JsonResponse({'books': books_list})

##############################################333


def api_review(request):
    select_query = "SELECT * FROM books_review INNER JOIN books_book where books_review.book_id = books_book.id"
    #select_query = "SELECT book_id FROM books_review"
    with connection.cursor() as cursor:
        cursor.execute(select_query)
        books = cursor.fetchall()
    return JsonResponse({'books': books})

def books_isbn(request, isbn_prefix):
    tbooks = Book.objects.all()
    select_query = "SELECT * FROM books_book where ISBN LIKE '"+isbn_prefix+"%'"
    with connection.cursor() as cursor:
        cursor.execute(select_query)
        rows = cursor.fetchall()

    # Convert the result into a list of dictionaries
    columns = [col[0] for col in cursor.description]
    books_list = [
        dict(zip(columns, row))
        for row in rows
    ]

#    return JsonResponse(books_list, safe=False)
#    return render(request, 'books/book_list.html', {'books': books_list, 'isbn_prefix': isbn_prefix})
    return JsonResponse({'books': books_list, 'isbn_prefix': isbn_prefix})

def show_author(request):
    tbooks = Book.objects.all()
    select_query = "SELECT * FROM books_author"
    with connection.cursor() as cursor:
        cursor.execute(select_query)
        rows = cursor.fetchall()

    # Convert the result into a list of dictionaries
    columns = [col[0] for col in cursor.description]
    books_list = [
        dict(zip(columns, row))
        for row in rows
    ]

#    return JsonResponse(books_list, safe=False)
#    return render(request, 'books/book_list.html', {'books': books_list, 'isbn_prefix': isbn_prefix})
    return JsonResponse({'books': books_list})


def delete_author(request):
    tbooks = Book.objects.all()
    select_query = "DELETE FROM books_author where id = 3"
    with connection.cursor() as cursor:
        cursor.execute(select_query)
        rows = cursor.fetchall()

    # Convert the result into a list of dictionaries
    columns = [col[0] for col in cursor.description]
    books_list = [
        dict(zip(columns, row))
        for row in rows
    ]

#    return JsonResponse(books_list, safe=False)
#    return render(request, 'books/book_list.html', {'books': books_list, 'isbn_prefix': isbn_prefix})
    return JsonResponse({'books': books_list})

def add_book(request):
    select_query = "INSERT INTO books_book (title, isbn, publication_date, summary, author_id) VALUES (%s, %s, %s, %s, %s)"

    # Define the values to be inserted
    values = ('dummy title 6', '117777', '1988-02-03', 'This is a fake summary 6', 1)

    try:
        with connection.cursor() as cursor:
            cursor.execute(select_query, values)
            # Fetch the number of rows affected

            # Return a success message
            return JsonResponse({'success': True, 'message': 'Insert successful'})

    except IntegrityError as e:
        # Handle any integrity errors, such as duplicate entries
        return JsonResponse({'success': False, 'message': str(e)})

    except Exception as e:
        # Handle other exceptions
        return JsonResponse({'success': False, 'message': str(e)})

    finally:
        # Ensuring the connection is closed properly (optional with `with` statement)
        connection.close()        

def update_book_title(request):
    book_id = 3
    new_title = 'Chopped Down'

    # Ensure both parameters are provided
    if not book_id or not new_title:
        return HttpResponseBadRequest("Missing 'id' or 'title' parameter.")

    # Perform raw SQL update
    with connection.cursor() as cursor:
        # Write your SQL query
        sql = "UPDATE books_book SET title = %s WHERE id = %s"
        # Execute the query
        cursor.execute(sql, [new_title, book_id])
        # Fetch the number of rows affected
        rows_affected = cursor.rowcount

    # Check if any row was updated
    if rows_affected > 0:
        return JsonResponse({'success': True, 'rows_updated': rows_affected})
    else:
        return JsonResponse({'success': False, 'message': 'No rows were updated.'})
