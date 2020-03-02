# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, reverse, get_object_or_404

from book_rental.models import BookCategory, Book, Coustomer
from django.http import HttpResponseRedirect, HttpResponse
from book_rental.forms import BookCategoryForm,BookForm, CoustomerForm


def index(request):
    category_list = BookCategory.objects.all()
    return render(request, 'book_rental/index.html', {'category_list': category_list})


def createcategoryform(request):
    if request.method == "POST":
        form = BookCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('book_rental:index'))
    form = BookCategoryForm()
    return render(request, "book_rental/categoryform.html", {'form': form})


def book_selection(request, category_id):
    bookcategory = get_object_or_404(BookCategory, id=category_id)
    if request.method == 'POST':
        days=request.POST['days']
        check_values = request.POST.getlist('books[]')
        number_of_books=len(check_values)
        result=number_of_books*bookcategory.cost
        result*= int(days)
        return render(request, 'book_rental/calculate.html', {'result': result})
        # return HttpResponseRedirect(reverse('book_rental:calculate'))
    books = Book.objects.filter(book_category=bookcategory)
    return render(request, 'book_rental/bookcategory.html', {'bookcategory': bookcategory, 'books': books})

# def book_selection(request, category_id):
#     bookcategory = get_object_or_404(BookCategory, id=category_id)
#     if request.method == "POST":
#         bookcategory.book_set.create(
#             book_name=request.POST['book_name'],
#             author_name=request.POST['author_name'],
#         )
#
#
#     return render(request, 'book_rental/bookcategory.html', {'bookcategory': bookcategory})


def add_book(request, category_id):
    bookcategory = get_object_or_404(BookCategory, id=category_id)
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.book_category = bookcategory
            instance.save()
            return HttpResponseRedirect(reverse('book_rental:book_selection', args=[category_id, ]))
    form = BookForm()
    return render(request,'book_rental/add_book.html', {'form': form})


def calculate(request, category_id):
    return HttpResponse('success')


def create_coustomer(request):
    if request.method == "POST":
        form = CoustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('book_rental:index'))
    form = CoustomerForm()
    return render(request, "book_rental/customerform.html", {'form': form})