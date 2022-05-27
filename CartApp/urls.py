"""CartApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from CartInventory.views import ItemViews, OrderItemUpdateView, AllUserOrderItemView,OrderItemView,OrderViews,CategoryViews,CartView,CartDeleteItemView,CartUpdateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('rest_framework.urls')),
    path('',include('accounts.urls')),
    path('api/Item',ItemViews.as_view()),
    path('api/Order',OrderViews.as_view(),name="order"),
    path('api/Order/<int:order_id>',OrderItemView.as_view()),
    path('api/Order/items',AllUserOrderItemView.as_view()),
    path('api/Order/Update/<int:order_id>',OrderItemUpdateView.as_view()),
    path('api/category',CategoryViews.as_view()),
    path('api/category/<int:cat_id>',CategoryViews.as_view()),
    path('api/cart/<int:user_id>',CartView.as_view()),
    path('api/cart/delete/<int:user_id>/<int:cart_id>',CartDeleteItemView.as_view()),
    path('api/cart/update/<int:cart_id>',CartUpdateView.as_view()),
    path('jwt/token',TokenObtainPairView.as_view()),
    path('jwt/token/refresh',TokenRefreshView.as_view()),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
