from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogs_list, name="blogs_list"),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('add_blog/', views.add_blog, name="add_blog"),
    path('edit_blog/<int:blog_id>/', views.edit_blog, name="edit_blog"),
    path('delete_blog/<int:del_id>/', views.delete_blog, name='delete_blog'),

]
