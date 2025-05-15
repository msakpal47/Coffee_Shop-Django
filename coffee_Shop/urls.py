from django.urls import path
from coffee_Shop import views



app_name = 'coffee_Shop'

urlpatterns = [
    path('home/', views.home, name="home"),
    path('menu/', views.menu, name='menu'),
    path('menu/add/', views.add_menu_item, name='add_menu_item'),
    path('menu/add_to_order/<int:item_id>/', views.add_to_order, name='add_to_order'),
    path('menu/delete/<int:item_id>/', views.delete_item, name='delete_item'),

    path('order/', views.order_view, name='order'),
    #path('add_item/', views.add_item, name='add_item'),
    #path('order/', views.order_view, name='order'),
    path('order/remove/<int:item_id>/', views.remove_item, name='remove_item'),
    path('order/confirm/', views.confirm_order, name='confirm_order'),
    #path('menu/delete/<int:item_id>/', views.delete_item, name='delete_item')
    #path('order/', views.order_view, name='order')




    #path('add-item/', views.add_menu_item, name='add_item'),
    #path('add_to_order/<int:item_id>/', views.add_to_order, name='add_to_order'),
    #path('remove-item/<int:item_id>/', views.remove_item, name='remove_item'),
    #path('delete-item/<int:item_id>/', views.delete_item, name='delete_item')
]
