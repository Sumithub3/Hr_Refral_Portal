from django.urls import path
from .import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('signup/', views.handleSignup, name='handleSignup'),
    path('login/', views.handleLogin, name='handleLogin'),
    path('logout/', views.handleLogout, name='handleLogout'),
    path('post/', views.postJobs, name='postJobs'),
    path('view/', views.jobView, name='jobView'),
    path('apply/', views.jobApply, name='jobApply'),
    path('applies/', views.viewApply, name='viewApply'),
    path('about/', views.about, name='about'),
    path('contact/', views.contactUs, name='contact'),
    path('search/', views.search, name='search'),
    path('export/', views.exportCSV, name='exportCSV'),
    path('profile/', views.viewProfile, name='viewProfile'),
]