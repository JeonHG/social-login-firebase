from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("", views.UsersView.as_view()),
    path("token/", views.login),
    path("me/", views.MeView.as_view()),
    path("<int:pk>/", views.user_detail),
    path("<slug:uidb64>/<slug:token>/", views.activate_user),
    # path("test/", views.TestView.as_view()),
]