"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from shop.forms import MyPasswordResetForm, MySetPasswordForm
from shop import views
from shop import webhook

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('shop.urls', namespace='shop')),


    path('password_reset/', auth_view.PasswordResetView.as_view(template_name='shop/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password_reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='shop/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='shop/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password_reset_complete/', auth_view.PasswordResetCompleteView.as_view(template_name='shop/password_reset_complete.html'), name="password-reset-complete"),

    #Ajax 
    path('pluscart/', views.pluscart, name='plus-cart'),
    path('minuscart/', views.minuscart, name='minus-cart'),
    path('removecart/', views.removecart, name='remove-cart'),
    path('pluswishlist/', views.plus_wishlist, name='plus_wishlist'),
    path('minuswishlist/', views.minus_wishlist, name='minus_wishlist'),
    path('payment/webhook/', webhook.stripe_webhook, name="stripe-webhook"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Neel Shop'
admin.site.site_title = 'Neel shop'
admin.site.site_index_title = 'Neel shop'
