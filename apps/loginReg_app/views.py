from django.shortcuts import render, redirect, HttpResponse
from time import localtime, strftime, gmtime
from django.contrib import messages
from apps.loginReg_app.models import *
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'loginReg_app/index.html')

def login_process(request):
    print("\n"+"*-"*15,"This is login process", "*-"*15+"\n")
    try:
        user = User.objects.get(email=request.POST['email'])
        print("TRY IN LOGING" *12)
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['name'] = User.objects.get(email=request.POST['email']).first_name
            return redirect('/success')
    except:
        messages.error(request, "Invalid Login", "login")
        return redirect('/')

def reg_process(request):
    print("\n"+"*-"*15, "This is the registration process, redirect('/reg_success') or redirect('/reg')", "*-"*15+"\n")
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, "registration")
        return redirect('/')
    else:
        hashIt = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'],password=hashIt)
        request.session['name'] = request.POST['first_name']
    return redirect('/success')

def success(request):
    if 'name' in request.session:
        return render(request, 'loginReg_app/success.html')
    else:
        return redirect('/')