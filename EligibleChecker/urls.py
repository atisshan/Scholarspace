from . import views
from django.urls import path

urlpatterns=[
    
    
    path('', views.home_view, name='home'),
    path('signup/', views.signUp_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('universities/', views.universities, name='university_list'),
    path('university/<int:university_id>/', views.programs, name='programs'),
    path('saved_programs/<int:program_id>', views.saved_programs,name='saved_programs'),
    path('home_search_results/', views.home_search_results, name='home_search_results'),
    path("download-program/<int:program_id>/", views.download_program_pdf, name="download_program"),
    path("about/", views.AboutView, name="about"),
    path("contact/", views.contact, name='contact'),
    path('contact/success/', views.contact_success_view, name='contact_success'),
   
   
]
