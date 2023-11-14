from django.shortcuts import render, HttpResponse, redirect

from .models import Article, Category, Comment, ArticleCountView
from .forms import UserRegistrationForm, UserAuthenticationForm, ArticleForm, CommentForm

from django.contrib.auth import login, logout, authenticate
from django.views.generic import UpdateView, DeleteView, ListView
from django.db.models import Q
from django.contrib.auth.models import User


class ArticleListView(ListView):
    model = Article
    template_name = "web_site/index.html"
    context_object_name = "articles"


class SearchResult(ArticleListView):
    def get_queryset(self):
        query = self.request.GET.get('q')
        return Article.objects.filter(
            Q(title__iregex=query) | Q(short_description__iregex=query)
        )


class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'web_site/article_form.html'


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = "/"


def home_view(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }
    return render(request, 'web_site/index.html', context)


def category_articles(request, category_id):
    category = Category.objects.get(pk=category_id)
    articles = Article.objects.filter(category=category)
    context = {
        'articles': articles
    }
    return render(request, 'web_site/index.html', context)


def article_detail(request, article_id):
    article = Article.objects.get(pk=article_id)

    if request.method == 'POST':
        # request.POST
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.article = article
            form.author = request.user
            form.save()
            return redirect('article_detail', article.pk)
    else:
        form = CommentForm()

   
    comments = Comment.objects.filter(article=article)
    print(comments)

    if not request.session.session_key:
        request.session.save()

    session_id = request.session.session_key

    viewed = ArticleCountView.objects.filter(article=article, session_id=session_id)
    if viewed.count() == 0 and str(session_id) != 'None':
        obj = ArticleCountView()
        obj.session_id = session_id
        obj.article = article
        obj.save()

        # изменение кол-ва просмотров
        article.views += 1
        article.save()

    context = {
        "article": article,
        "form": form,
        "comments": comments
    }
    return render(request, "web_site/article_detail.html", context)


def login_view(request):
    if request.method == "POST":
        form = UserAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = UserAuthenticationForm()
    context = {
        "form": form
    }
    return render(request, "web_site/login.html", context)


def registration_view(request):
    if request.method == "POST":
        print(request.POST)

        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserRegistrationForm()
    context = {
        "form": form
    }
    return render(request, "web_site/registration.html", context)


def user_logout(request):
    logout(request)
    return redirect('home')


def created_article(request):
    if request.method == 'POST':
        form = ArticleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            return redirect('article_detail', form.pk)
    else:
        form = ArticleForm()

    context = {
        'form': form
    }

    return render(request, 'web_site/article_form.html', context)


def profile_view(request, username):
    user = User.objects.get(username=username)
    articles = user.articles.all()

    context = {
        "user": user,
        "total_views": 0,
        "total_comments": 0,
        "articles": articles
    }
    return render (request, "web_site/profile.html", context)
