from django.shortcuts import render, redirect
from .models import Category, Article


# Create your views here.
def new_view(request):
    # get 요청으로 들어오면 form 태그 있는 html 을 보여주고
    # post 요청이 들어오면 request.POST 변수들 받아서 글 생성
    if request.method == 'POST':
        title = request.POST.get('title', None)
        content = request.POST.get('content', None)
        # '영화'라는 카테고리로 글을 썼다면 category_name 에는 '영화'가 할당될것
        category_name = request.POST.get('category', None)
        # 아래 코드에서 category_name 도 '영화'
        category = Category.objects.get(name=category_name)
        article = Article.objects.create(title=title, content=content, category=category)
        # django 는 자동으로 PK 라는 필드를 만들어준다
        # 첫번째 글을 썼다 -> pk = 1
        # 두번째 글을 썼다 -> pk = 2
        return redirect('detail', article.pk)
    elif request.method == 'GET':
        # 새 글을 쓸때 현재 category 모델에 존재하는 것만 사용자가 선택할 수 있어야함
        categories = Category.objects.all()
        return render(request, 'new.html', {'categories':categories})


# 카테고리 이름, 해당 카테고리 글 개수
# {movie: 1, drama: 0, entertain: 0}
def category_view(request):
    categories = Category.objects.all()
    infos = {}
    for category in categories:
        infos[category.name] = Article.objects.filter(category=category).count()
    return render(request, 'category.html', {'infos': infos})


# '127.0.0.1/movie' -> name='movie'
def article_view(request, name):
    category = Category.objects.get(name=name)
    articles = Article.objects.filter(category=category)
    return render(request, 'article.html', {'articles': articles})


# '127.0.0.1/detail/1' -> pk = 1
def detail_view(request, pk):
    article = Article.objects.get(pk=pk) # pk=1
    return render(request, 'detail.html', {'article': article})
