from django.shortcuts import render,redirect
from .forms import RegisterForm,LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
import sqlite3
# Create your views here.
def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data.get("name")
        surname = form.cleaned_data.get("surname")
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        newUser = User(first_name=name,last_name=surname,username=username,email=email)
        newUser.set_password(password)
        newUser.save()
        login(request,newUser)
        messages.success(request,"Kayıt Başarılı.")
        return redirect("index")
    context = {
        "form":form
    }
    return render(request,"register.html",context)
def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
        "form" : form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        connect = sqlite3.connect("db.sqlite3")
        cur = connect.cursor()
        cur.execute("Select * From auth_user where username = ?",(username,))
        first = cur.fetchone()
        user =  authenticate(username=username,password=password,bilgiler = first)
        if user is None:
            messages.info(request,"Kullanıcı Adı veya Parola Yanlış")
            return render(request,"login.html",context)
        messages.success(request,"Giriş Başarılı.")
        login(request,user)
        return redirect("index")
    return render(request,"login.html",context)
def logoutUser(request):
    logout(request)
    messages.warning(request,"Oturum Kapatıldı.")
    return redirect("index")