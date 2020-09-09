from django.shortcuts import render, redirect
from . import models
from .models import User, Book
from django.contrib import messages
import bcrypt
from datetime import datetime


def checklogin(request):
    errors = {}
    if "username" not in request.session:
        errors['email'] = "<div class='ohno'>Please log in</div>"
        return False
    return True


def index(request):
    if "username" in request.session:
        return render(request, "books.html")
    else:
        return render(request, "index.html")


def register(request):
    errors = User.objects.basic_validator(request.POST)
    if errors:
        request.session['first_name'] = request.POST['first_name']
        request.session['last_name'] = request.POST['last_name']
        request.session['email'] = request.POST['email']
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        hash = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],
                            email=request.POST['email'], birthdate=datetime.strptime(request.POST['birthdate'], '%Y-%m-%d'), password=hash)
        request.session['username'] = request.POST['email']
        User.objects.get(email=request.POST['email'])
        return redirect("/books")


def books(request):
    if not checklogin(request):
        return redirect('/')
    if request.method == "GET":
        context = {
            "all_books": Book.objects.all(),
            "user_info": User.objects.get(email=request.session['username']),
        }
        return render(request, "books.html", context)
    if request.method == "POST":
        errors = Book.objects.book_validate(request.POST)
        if errors:
            request.session['title'] = request.POST['title']
            request.session['description'] = request.POST['description']
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/books")
        else:
            uploaded_by = User.objects.get(id=int(request.POST['uploaded_by']))
            new_book_info = Book.objects.create(
                title=request.POST['title'], description=request.POST['description'], uploaded_by=uploaded_by)
            new_book_info.users_who_like.add(uploaded_by)
            return redirect("/books")


def edit(request, book_id):
    if request.method == "GET":
        context = {
            "user_info": User.objects.get(email=request.session['username']),
            "book_info": Book.objects.get(id=book_id)
        }
        return render(request, context, "edit.html")
    if request.method == "POST":
        book_to_update: Book.objects.get(id=book_id)
        book_to_update.description = request.POST['description']
        book_to_update.save()
        return redirect(f"/books/{book_id}")


def show(request, book_id):
    if request.method == "GET":
        context = {
            "user_info": User.objects.get(email=request.session['username']),
            "book_info": Book.objects.get(id=book_id),
            "users_who_like_this": Book.objects.get(id=book_id).users_who_like.all(),
        }
        return render(request, "show.html", context)
    if request.method == "POST":
        errors = Book.objects.edit_book_validate(request.POST)
        return redirect(f"/books/{book_id}")


def delete(request, book_id):
    Book.objects.get(id=book_id).delete()
    return redirect("/books")


def favorite(request, book_id):
    user = User.objects.get(email=request.session['username'])
    book = Book.objects.get(id=book_id)
    user.liked_books.add(book)
    return redirect(f"/books/{book_id}")


def unfavorite(request, book_id):
    user = User.objects.get(email=request.session['username'])
    book = Book.objects.get(id=book_id)
    book.users_who_like.remove(user)
    return redirect(f"/books/{book_id}")


def logout(request):
    if "email" in request.session:
        del request.session["username"]
    if "first_name" in request.session:
        del request.session["first_name"]
    if "last_name" in request.session:
        del request.session["last_name"]
    return redirect("/")


def login(request):
    errors = User.objects.login_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        request.session['username'] = request.POST['email']
        return redirect("/books")
