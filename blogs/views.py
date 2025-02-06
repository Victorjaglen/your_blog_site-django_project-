# Imported necessary modules and classes
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Blog, Comment
from .serializers import BlogSerializer
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from .serializers import CommentSerializer

# Blog view class with multiple actions: list, create, update, and retrieve
class BlogMixinView(mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    generics.GenericAPIView):

    queryset = Blog.objects.all().order_by('-date')
    serializer_class = BlogSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]

    # Get the list of blogs written by the current user
    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user).order_by('-date')

    # Handle GET requests to render various blog pages (list, detail, add, and edit)
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_register')  # Redirect to login if not authenticated

        blog_id = kwargs.get('pk')  # Get blog ID from URL parameters
        try:
            # Render the 'add_blog' page for adding a new blog
            if 'add_blog' in request.path:
                return render(request, 'add_blog.html')

            # Render the 'edit_blog' page for editing an existing blog
            if 'edit_blog' in request.path:
                context = {'blog': Blog.objects.get(id=blog_id)}
                return render(request, 'edit_blog.html', context)

            # Show blog details and its comments
            if blog_id is not None:
                response = self.retrieve(request, *args, **kwargs)
                data = response.data
                blog = Blog.objects.get(id=blog_id)
                comments = Comment.objects.filter(blog=blog).order_by('-created_at')
                comments_serializer = CommentSerializer(comments, many=True)
                context = {'blog': data, 'comments': comments_serializer.data}
                return render(request, 'blog_detail.html', context)

            # Show all blogs if no specific blog ID
            response = self.list(request, *args, **kwargs)
            data = response.data
            context = {'blogs': data}
            return render(request, 'blogs_list.html', context)

        except Exception as e:
            print(e)
            messages.error(request, 'An unexpected error occurred.')
            return render(request, 'blogs_list.html', {'error_message': 'Blog not found, try again'})
            # return render(request, 'blogs_list.html')

    # Handle POST requests for creating or updating a blog
    def post(self, request, *args, **kwargs):
        blog_id = kwargs.get('pk')
        data = request.data.copy()

        if blog_id is not None:
            response = self.update(request, *args, **kwargs)  # Update blog if ID is provided
        else:
            response = self.create(request, *args, **kwargs)  # Create new blog

        data = response.data
        context = {'blog': data}
        return render(request, 'blog_detail.html', context)

    # Save the blog with the logged-in user as the author
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Function to delete a specific blog
def delete_blog(request, pk):
    try:
        blog = Blog.objects.get(id=pk)
    except Blog.DoesNotExist:
        messages.error(request, 'Blog not found.')
        return redirect('blogs_list')

    if request.method == 'POST':
        blog.delete()
        print(f'Successfully Deleted :{blog}')
    return redirect('blogs_list')

# Comment view class for handling comments on blogs (list, create)
class CommentMixinView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Comment.objects.all()  # Get all comments from the model
    serializer_class = CommentSerializer  # Use CommentSerializer for comment data
    permission_classes = [IsAuthenticated]  # Only authenticated users can comment
    lookup_field = 'pk'  # Use primary key as identifier for each comment

    # Save a new comment with the associated blog and logged-in user
    def perform_create(self, serializer):
        blog_id = self.kwargs.get('pk')
        blog = Blog.objects.get(id=blog_id)  # Got the associated blog
        serializer.save(blog=blog, user=self.request.user)  # Save comment with user and blog

    # Handle POST requests to add a comment to a blog
    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)  # Created the comment
        blog_id = self.kwargs.get('pk')  # Got blog ID from URL parameters
        blog = Blog.objects.get(id=blog_id)  # Got the blog object
        blog_data = BlogSerializer(blog).data  # Serialized blog data
        comments = Comment.objects.filter(blog_id=blog_id).order_by('-created_at')  # Get all comments for the blog
        comments_serializer = CommentSerializer(comments, many=True)  # Serialized comments data
        context = {'blog': blog_data, 'comments': comments_serializer.data}  # Passed serialized blog and comment data to the template
        return render(request, 'blog_detail.html', context)


# Function to delete a specific comment from a blog
def delete_comment(request, blog_pk, pk):
    comment = get_object_or_404(Comment, pk=pk, blog_id=blog_pk)  # Retrieved the comment, or return a 404 error if not found
    blog_id = comment.blog_id  # Got the blog ID for redirection

    # Checking if the user is the comment owner or the blog author
    if request.user == comment.user or request.user == comment.blog.author:
        comment.delete()  # Delete the comment
        messages.success(request, 'Comment deleted successfully.')
    else:
        messages.error(request, 'You do not have permission to delete this comment.')

    # Redirected to the blog detail page after deletion
    return redirect('blog_detail', blog_id)


def register_page(request):
    return render(request, 'register.html')


def login_page(request):
    return render(request, 'login.html')


def login_register(request):
    return render(request, 'login-register_page.html')
