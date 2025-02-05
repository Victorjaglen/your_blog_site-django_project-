from django.urls import path
from . import views
from . import auth_views

urlpatterns = [
    # Blog-related URLs
    path('', views.BlogMixinView.as_view(), name="blogs_list"),
    path('blog/<int:pk>/', views.BlogMixinView.as_view(), name='blog_detail'),
    path('add_blog/', views.BlogMixinView.as_view(), name="add_blog"),
    path('edit_blog/<int:pk>/', views.BlogMixinView.as_view(), name="edit_blog"),
    path('delete_blog/<int:pk>/', views.delete_blog, name='delete_blog'),

    # Authentication-related URLs
    path('register/', views.register_page, name="register_page"),
    path('api/register', auth_views.Register_view.as_view(), name="register"),
    path('login/', views.login_page, name="login_page"),
    path('api/login/', auth_views.Login_Logout_view.as_view(), name="login"),
    path('logout/', auth_views.Login_Logout_view.as_view(), name="logout"),
    path('login_register_page/', views.login_register, name="login_register"),

    # Comment-related URLs
    path('blog/<int:pk>/comments/', views.CommentMixinView.as_view(), name='comments'),
    path('blog/<int:blog_pk>/comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),

]
