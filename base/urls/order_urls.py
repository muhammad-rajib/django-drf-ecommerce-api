from django.urls import path
from base.views import order_views as views


urlpatterns = [
    path('add/', views.addOrderItems, name='order-add'),
    path('myorders/', views.getMyOrders, name='my-orders'),
    path('<str:pk>/', views.getOrderById, name='get-order'),
    path('<str:pk>/pay/', views.updateOrderPay, name='order-pay'),
]