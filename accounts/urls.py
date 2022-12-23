from django.urls import path
from accounts.views import UserCreateView, LoginView, LogoutView, \
    ContactListCreateView, DashboardView, UserGetView, ContactListView

urlpatterns = [
    path(r'signup/', UserCreateView .as_view()),
    path(r'login/', LoginView .as_view()),
    path(r'logout/', LogoutView .as_view()),
    path(r'contact/', ContactListCreateView .as_view()),
    path(r'contact/list/', ContactListView.as_view()),
    path(r'dashboard/', DashboardView .as_view()),
    path(r'user-details/<idencode:pk>', UserGetView .as_view())
]