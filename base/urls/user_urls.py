from django.urls import path
from base.views import user_views as views


urlpatterns = [
    path('', views.getUsers, name='users'),
    path('register/', views.registerUser, name='registerUser'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', views.getUserProfile, name='users-profile'),
]