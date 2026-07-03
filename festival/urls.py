from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    path('work/<int:pk>/', views.work_detail, name='work_detail'),
    path('work/<int:pk>/vote/', views.vote, name='vote'),
    path('work/<int:pk>/comment/', views.add_comment, name='add_comment'),
]