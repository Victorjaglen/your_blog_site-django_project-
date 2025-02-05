from django.shortcuts import render, redirect

def homepage(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    return redirect('login_register')
    # return render(request, 'home.html')
