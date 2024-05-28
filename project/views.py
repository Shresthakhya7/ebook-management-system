from django.shortcuts import render, get_object_or_404, redirect,HttpResponse
from .models import Ebook, UserReading
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def home(request):
    ebooks = Ebook.objects.all()
    return render(request, 'home.html', {'ebooks': ebooks})

@login_required(login_url='/login/')
def ebook_list(request):
    ebooks = Ebook.objects.all()
    categories = ebooks.values_list('category', flat=True).distinct()
    return render(request, 'ebook_list.html', {'categories': categories, 'ebooks': ebooks})


@login_required(login_url='/login/')
def ebook_detail(request, pk):
    ebook = get_object_or_404(Ebook, pk=pk)
    return render(request, 'ebook_detail.html', {'ebook': ebook})

@login_required(login_url='/login/')
def read_ebook(request, pk):
    ebook = get_object_or_404(Ebook, pk=pk)
    if not request.user.is_staff:
        user_reading, created=UserReading.objects.get_or_create(user=request.user,ebook=ebook)
        user_reading.read_count+=1
        user_reading.save()
    return redirect('ebook_detail',pk=pk)

    

def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not (first_name and last_name and username and password):
            messages.error(request, "All fields must be filled.")
            return redirect('/register/')

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already taken.")
            return redirect('/register/')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.set_password(password)
        user.save()
        messages.success(request, "User registered successfully.")
        return redirect('/login/')
    return render(request, 'register.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home/')  
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

@login_required(login_url='/login/')
def ebook_upload(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        category = request.POST.get('category')
        cover = request.FILES.get('cover')
        file = request.FILES.get('file')

        if not (title and author and description and category and cover and file):
            messages.error(request, "All fields must be filled.")
            return redirect('/ebook_upload/')

        if Ebook.objects.filter(title=title, author=author).exists():
            messages.info(request, "Ebook already exists.")
            return redirect('/ebook_upload/')
        
        Ebook.objects.create(
            title=title,
            author=author,
            description=description,
            category=category,
            cover=cover,
            file=file,
        )

        messages.success(request, "Ebook added successfully.")
        return redirect('/ebook_upload/')
    
    return render(request, 'ebook_upload.html')

@login_required(login_url='/login/')
def update_book(request, pk):
    queryset= Ebook.objects.get(pk=pk)

    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        cover = request.FILES.get('cover')
        file = request.FILES.get('file')


        queryset.title=title
        queryset.author=author
        queryset.description=description


        if cover:
            queryset.cover=cover
        if file:
            queryset.file=file

        queryset.save()
        return redirect('/home/')

    context={'ebook': queryset}

    return render(request, 'update.html', context)

@login_required(login_url='/login/')
def delete_book(request, pk):
    queryset= Ebook.objects.get(pk=pk)
    queryset.delete()
    return redirect('/ebook_list/')

def logout_page(request):
    logout(request)
    return redirect('/home/')
