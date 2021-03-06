from django.urls import path
from rango import views
from django.conf.urls import url

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    # path('search/', views.search, name='search'),
    path('category/<slug:category_name_slug>/add_comment/', views.add_comment, name='add_comment'),
    path('suggest/', views.CategorySuggestionView.as_view(), name='suggest'),
    url(r'^goto/$', views.track_url, name='goto'),
    url(r'^like/$', views.like_category, name='like_category'),
]