from django.urls import path
from accounts.views import UserCreateView, LoginView, LogoutView,  UserGetView

urlpatterns = [
    path(r'create/user/', UserCreateView .as_view()),
    path(r'login/', LoginView .as_view()),
    path(r'logout/', LogoutView .as_view()),
    path(r'user-details/<idencode:pk>', UserGetView .as_view()),
    path(r'user/list/', UserGetView .as_view())
]