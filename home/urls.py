from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
    path("", views.home_view, name="home"),
    path("login/", views.BasicLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
]
