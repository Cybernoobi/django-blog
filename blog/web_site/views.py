from django.shortcuts import render, HttpResponse, redirect

from .models import Article, Category
from .forms import UserRegistrationForm, UserAuthenticationForm, ArticleForm

from django.contrib.auth import login, logout, authenticate
from django.views.generic import UpdateView, DeleteView, ListView
from django.db.models import Q


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
    context = {
        "article": article
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
