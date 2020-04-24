from django.shortcuts import render,HttpResponse,redirect,get_object_or_404,reverse
from .forms import ArticleForm,usersForm
from django.contrib import messages
from .models import Article,Comment
from usersabout.models import usersAbout
import sqlite3
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):  
    keyword = request.GET.get("keyword")
    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        userabout = usersAbout.objects.filter()
        return render(request,"index.html",{"articles":articles,"userabout":userabout})
    articles = Article.objects.filter()
    userabout = usersAbout.objects.filter()
    context = {
        "articles":articles,
        "userabout":userabout,
    }
    return render(request,"index.html",context)
def oprofil(request,id):
    usersabout = usersAbout.objects.filter(user_id=id)
    connect = sqlite3.connect("db.sqlite3")
    cur = connect.cursor()
    cur.execute("Select * From auth_user where id = ?",(id,))
    first = cur.fetchone()
    a=0
    for i in first:
        if(a==0):
            id=i
        elif(a==3):
            superid=i
        elif(a==4):
            username=i
        elif(a==5):
            ad=i
        elif(a==6):
            email=i
        elif(a==10):
            soyad=i
        a+=1
    articles = Article.objects.filter(author_id = id)
    if (id==request.user.id):
        return redirect("profil")
    
    bilgiler = {
        "username":username,
        "name":ad,
        "email":email,
        "surname":soyad,
        "superid":superid,
        "articles":articles,
        "userabout":usersabout
    } 
    return render(request,"oprofil.html",bilgiler)

@login_required(login_url="/user/login/")
def profil(request):
    articles = Article.objects.filter(author = request.user)
    usersabout = usersAbout.objects.filter(user_id=request.user.id)
    ls=["1","2","3"]
    context = {
        "articles":articles,
        "usersabout":usersabout,
        "ls":ls,
    }
    return render(request,"profil.html",context)

@login_required(login_url="/user/login/")
def message(request):
    return render(request,"messages.html")

@login_required(login_url="/user/login/")
def update(request):
    usersabout=get_object_or_404(usersAbout,user_id=request.user.id)
    form = usersForm(request.POST or None,request.FILES or None,instance=usersabout)
    if form.is_valid():
        userabout = form.save(commit=False)
        userabout.user_id=request.user.id
        userabout.save()
        messages.success(request,"Profil Güncellendi.")
        return redirect("profil")
    context = {
        "form":form
    }
    return render(request,"updateabout.html",context)

@login_required(login_url="/user/login/")
def edit(request):
    usersabout = usersAbout.objects.filter(user_id=request.user.id)
    if str(usersabout)!="<QuerySet []>":
        return redirect("update")
    form = usersForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        userabout = form.save(commit=False)
        userabout.user_id=request.user.id
        userabout.save()
        messages.success(request,"Profil Güncellendi.")
        return redirect("profil")
    context = {
        "form":form
    }
    return render(request,"edit.html",context)

@login_required(login_url="/user/login/")
def addarticle(request):
    form = ArticleForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        article = form.save(commit=False)
        article.author=request.user
        article.save()
        messages.success(request,"Makale Oluşturuldu.")
        return redirect("index")
    return render(request,"addarticle.html",{"form":form})
def detail(request,id): 
    #article = Article.objects.filter(id=id).first()
    article = get_object_or_404(Article,id=id)
    userabout = usersAbout.objects.filter(user_id=article.author_id)
    comments = article.comments.all()
    a=0
    for i in comments:
        a+=1

    return render(request,"detail.html",{"article":article,"comments":comments,"sayi":a,"userabout":userabout})
        

@login_required(login_url="/user/login/")
def updateArticle(request,id):
    article = get_object_or_404(Article,id=id)
    if request.user.id == article.author_id:
        form = ArticleForm(request.POST or None,request.FILES or None,instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.author=request.user
            article.save()
            messages.success(request,"Makale Güncellendi.")
            return redirect("index")
        return render(request,"update.html",{"form":form})
    else:
        messages.warning(request,"Bu işlemi yapmaya izniniz yok.")
        return redirect("index")

@login_required(login_url="/user/login/")
def deleteArticle(request,id):
    article = get_object_or_404(Article,id=id)
    if request.user.id == article.author_id:
        article.delete()
        messages.success(request,"Makale Silindi")
        return redirect("profil")
    else:
        messages.warning(request,"Bu işlemi yapmaya izniniz yok.")
        return redirect("index")
def articles(request):
    keyword = request.GET.get("keyword")
    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        return render(request,"articles.html",{"articles":articles})
    articles = Article.objects.filter()
    context = {
        "articles":articles
    }
    return render(request,"articles.html",context)

def addComment(request,id):
    article = get_object_or_404(Article,id=id)
    if request.method=="POST":
        comment_content = request.POST.get("comment")
        if str(request.user)!="AnonymousUser":
            comment_author = request.user
        else:
            comment_author = "Ziyaretçi"
        newComment = Comment(comment_author=comment_author,comment_content=comment_content) 
        newComment.article=article
        newComment.save()
    return redirect(reverse("article:detail",kwargs={"id":id}))
