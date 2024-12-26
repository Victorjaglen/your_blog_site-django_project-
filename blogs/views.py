from django.shortcuts import render, redirect
from .models import Blog
# Create your views here.
def blogs_list(request):
    blogs = Blog.objects.all().order_by('-date')
    context = {'blogs': blogs}
    return render(request, 'blogs_list.html', context)

def blog_detail(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    context = {'blog': blog}
    return render(request, 'blog_detail.html', context)


def add_blog(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        author = request.POST['author']
        image = request.FILES.get('image')

        if image:
            blog = Blog(title=title, content=content, author=author, image=image)
        else:
            blog = Blog(title=title, content=content, author=author)
        blog.save()

        return redirect('blog_detail', blog_id=blog.id)

    return render(request, 'add_blog.html')


def delete_blog(request, del_id):
    blog = Blog.objects.get(id=del_id)
    if request.method == 'POST':
        blog.delete()
        print(f'Successfully Deleted :{blog}')
    return redirect('blogs_list')


def edit_blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    if request.method == 'POST':
        blog.title = request.POST['title']
        blog.content = request.POST['content']
        blog.author = request.POST['author']
        image = request.FILES.get('image')
        if image:
            blog.image = image
        blog.save()

        return redirect('blog_detail', blog_id=blog.id)

    return render(request, 'edit_blog.html', {'blog': blog})
