from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import User
# Create your views here.
def login_page(request): #renders the template for '/'
    return render(request, 'login_reg/index.html')


def register_page(request): #renders template for ''/registration'
    return render(request, 'login_reg/register.html')


def register(request): #validates and saves registration data to database
    if request.method == "POST":
        post_data = {
            "username": request.POST['username'],
            "email": request.POST['email'],
            "password": request.POST['password'],
            "confirm_password": request.POST['confirm_password'],
        }

        result = User.objects.register_account(post_data)
        if result['errors'] == None:
            request.session['id'] = result['user'].id
            return redirect(reverse('home:home_page'))
        else:
            for error in result['errors']:
                messages.error(request, error, extra_tags='signup')
            return redirect('/registration')



def login(request):
    if request.method == "POST":
        login_data = {
            "username": request.POST["username"],
            "password": request.POST["password"]
        }

        result = User.objects.login_account(login_data)
        if result['errors'] == None:
            request.session['id'] = result['user'].id
            return redirect(reverse('home:home_page'))
        else:
            for errors in result['errors']:
                messages.error(request, errors, extra_tags='login')
            return redirect('/')






















#------------end-------------#
