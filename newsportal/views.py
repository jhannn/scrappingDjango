from django.shortcuts import get_object_or_404, render
from django.db.models import Q

from .models import News

def index(request):
        news_list = News.objects.all()
        context = {
                'news_list': news_list,
        }  
        return render(request, 'home.html', context)

def search(request):
        query = request.GET.get('q')
        results = News.objects.filter(Q(title__icontains=query))
        context = {
                'news_list': results,
        }  
        return render(request, 'home.html', context)