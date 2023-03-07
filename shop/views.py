from django.shortcuts import render
from django.views import View
from .models import Product

def home(request):
    return render(request, 'shop/home.html', locals())


class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        titles = product.values('title')
        return render(request, 'shop/category.html', locals())