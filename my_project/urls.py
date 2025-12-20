"""
URL configuration for my_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from coffee_Shop import views as shop_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('coffee_Shop/', include('coffee_Shop.urls')),
    path('coffee_login/', include('coffee_user_login.urls')),
    path('api/menu/', shop_views.menu_api, name='api_menu_root'),
    path('api/menu/add_to_order/<int:item_id>/', shop_views.add_to_order_api, name='api_add_to_order_root'),
    path('api/order/', shop_views.order_api, name='api_order_root'),
    path('api/order/delete/<int:item_id>/', shop_views.delete_item_api, name='api_order_delete_root'),
    path('api/order/remove/<int:item_id>/', shop_views.remove_item_api, name='api_order_remove_root'),
    path('api/order/confirm/', shop_views.confirm_order_api, name='api_order_confirm_root'),
    path('api/orders/history/', shop_views.order_history_api, name='api_orders_history_root'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
