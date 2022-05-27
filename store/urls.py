from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns=[
    path('',views.store,name="store"),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('update_item/',views.updateItem,name="update_item"),
    path('main/',views.main,name="main"),
    path('brand/',views.brand,name="brand"),
    path('category/',views.category,name="category"),
    path('product/',views.product,name="product"),
    path('checkin/',views.checkin,name="checkin"),
    path('<int:id>/detail/',views.detail,name="detail"),
    path('product/update/<int:pk>/',views.product_update,name="store-product-update"),
    path('product/delete/<int:pk>/',views.product_delete,name="store-product-delete"),
    path('brand/update/<int:pk>/',views.brand_update,name="store-brand-update"),
    path('brand/delete/<int:pk>/',views.brand_delete,name="store-brand-delete"),
    path('category/update/<int:pk>/',views.category_update,name="store-category-update"),
    path('category/delete/<int:pk>/',views.category_delete,name="store-category-delete"),
    path('password_reset',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('process_order/',views.processOrder,name="process_order"),
    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('login/',auth_views.LoginView.as_view(template_name='store/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='store/logout.html'),name='logout'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)