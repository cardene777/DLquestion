from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('login/', views.QuestionLoginView.as_view(), name="login"),
    path('logout/', views.QuestionLogoutView.as_view(), name="logout"),
    path('signup/', views.SignUpView.as_view(), name="signup"),
]
