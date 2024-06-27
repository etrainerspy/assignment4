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

def show_books(request):
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

def show_reviews(request):
    select_query = "SELECT * FROM books_review INNER JOIN books_book where books_review.book_id = books_book.id"
    #select_query = "SELECT book_id FROM books_review"
    with connection.cursor() as cursor:
        cursor.execute(select_query)
        rows = cursor.fetchall()

    # Convert the result into a list of dictionaries
    columns = [col[0] for col in cursor.description]
    review_list = [
        dict(zip(columns, row))
        for row in rows
    ]

    return JsonResponse({'reviews': review_list})


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

def show_authors(request):
    tbooks = Book.objects.all()
    select_query = "SELECT * FROM books_author"
    with connection.cursor() as cursor:
        cursor.execute(select_query)
        rows = cursor.fetchall()

    # Convert the result into a list of dictionaries
    columns = [col[0] for col in cursor.description]
    author_list = [
        dict(zip(columns, row))
        for row in rows
    ]

#    return JsonResponse(books_list, safe=False)
#    return render(request, 'books/book_list.html', {'books': books_list, 'isbn_prefix': isbn_prefix})
    return JsonResponse({'authors': author_list})

def show_authors_fname(request):
    select_query = "SELECT CASE " \
                           " WHEN INSTR(name, ' ') = 0 THEN name " \
                           " ELSE SUBSTR(name, 1, INSTR(name, ' ') - 1) " \
                       " END AS parsed_fname " \
                    " FROM books_author"

    with connection.cursor() as cursor:
        cursor.execute(select_query)
        rows = cursor.fetchall()

    # Convert the result into a list of dictionaries
    columns = [col[0] for col in cursor.description]
    author_list = [
        dict(zip(columns, row))
        for row in rows
    ]

    return JsonResponse({'author': author_list})

def show_authors_lname(request):
    select_query = "SELECT substr(name, instr(name, ' ') + 1) AS parsed_lanme FROM books_author"
    with connection.cursor() as cursor:
        cursor.execute(select_query)
        rows = cursor.fetchall()

    # Convert the result into a list of dictionaries
    columns = [col[0] for col in cursor.description]
    author_list = [
        dict(zip(columns, row))
        for row in rows
    ]

    return JsonResponse({'author': author_list})

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
    select_query = "INSERT INTO books_book (title, isbn, publication_date, summary, author_id, content) VALUES (%s, %s, %s, %s, %s, %s)"

    # Define the values to be inserted
    values = ('If you build it', '2134680', '1992-02-03', 'This is a fake summary 9', 2, "This is the story text about distances.")

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

def add_review(request):
    select_query = "INSERT INTO books_review (book_id, reviewer_name, review_text, rating, review_date) VALUES (%s, %s, %s, %s, %s)"

    # Define the values to be inserted
    values = (5, 'Charles Dickens', 'too technical', '1', '2024-06-15')

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

def add_author(request):
    select_query = "INSERT INTO books_author (name, biography) VALUES (%s, %s)"

    # Define the values to be inserted
    values = ("Ted Glendale", "bio 3")

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
    book_id = 11
    new_title = 'Travelling Across the Country'

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

def update_authors_name(request):
    # Write your SQL query
    sql_queryX = "UPDATE books_author " \
                    " SET firstname = '', "\
                    "     lastname = '' "\
                    " WHERE name LIKE '% %' " \

    sql_query = "UPDATE books_author " \
                    " SET firstname = substr(name, 1, instr(name, ' ') - 1), "\
                    "     lastname = substr(name, instr(name, ' ') + 1) "\
                    " WHERE name LIKE '% %' " \

    # Ensure both parameters are provided
    if not sql_query:
        return HttpResponseBadRequest("Missing sql query")

    # Perform raw SQL update
    with connection.cursor() as cursor:
        # Execute the query
        cursor.execute(sql_query)
        # Fetch the number of rows affected
        rows_affected = cursor.rowcount

    # Check if any row was updated
    if rows_affected > 0:
        return JsonResponse({'success': True, 'rows_updated': rows_affected})
    else:
        return JsonResponse({'success': False, 'message': 'No rows were updated.'})

def show_authors_lname(request):
    select_query = "SELECT substr(name, instr(name, ' ') + 1) AS parsed_lanme FROM books_author"
    with connection.cursor() as cursor:
        cursor.execute(select_query)
        rows = cursor.fetchall()

    # Convert the result into a list of dictionaries
    columns = [col[0] for col in cursor.description]
    author_list = [
        dict(zip(columns, row))
        for row in rows
    ]

    return JsonResponse({'author': author_list})


