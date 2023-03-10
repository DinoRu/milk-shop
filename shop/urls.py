from django.urls import path
from . import views
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeDoneView, PasswordChangeView, LogoutView
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm

app_name = 'shop'
urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:val>/', views.CategoryView.as_view(), name='category'),
    path('category-title/<str:val>/', views.CategoryTitleView.as_view(), name='category-title'),
    path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('register/', views.CustomerRegisterView.as_view(), name="register"),
    path('account/login/', LoginView.as_view(template_name='shop/login.html', authentication_form=LoginForm), name='login'),
    path('password-reset/', PasswordResetView.as_view(template_name='shop/password_reset.html', form_class=MyPasswordResetForm), name='password-reset'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.AddressView.as_view(), name='address'),
    path('udpdate-profile/<int:pk>/', views.updateProfileView.as_view(), name='update-profile'),
    path('passwordchange/', PasswordChangeView.as_view(template_name='shop/change-password.html', form_class=MyPasswordChangeForm, success_url=reverse_lazy('shop:passwordchangedone')), name='changepassword'),
    path('passwordchangedone/', PasswordChangeDoneView.as_view(template_name='shop/password-change-done.html'), name='passwordchangedone'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('shop:login')), name='logout'),

    # Add to cart
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('show_cart/', views.show_cart, name='cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('process/', views.payment_process, name="process"),
    path('success/', views.payment_success, name="sucess"),
    path('cancel/', views.payment_cancel, name='cancel'),
]