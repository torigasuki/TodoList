from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('signup/',views.SignupView.as_view(), name ='signup'),
    path('login/', views.TokenLoginView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('<str:id>/', views.UserView.as_view(), name='user_list'),
]
