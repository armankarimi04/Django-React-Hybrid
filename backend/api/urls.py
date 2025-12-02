from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path("login/", views.login_view, name="api_login"),
    path("logout/", views.logout_view, name="api_logout"),
    path("session/", views.session_view, name="api_session"),
    path("whoami/", views.whoami_view, name="api_whoami"),
    
    path('employees-list/', views.EmployeeView.as_view(), name='employees_list'),
    path('', views.index, name='index'),
]