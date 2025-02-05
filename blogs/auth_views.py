# Import necessary modules and classes
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

# Register view to handle user registration
class Register_view(APIView):

    permission_classes = [AllowAny]

    # POST method to register a new user
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        # Checking if the username already exist
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error_message': 'Username already exists, try again'})

        # Checking if the email already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error_message': 'Email Already exists, try again'})

        # Create a new user if username is available
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        # Generate authentication token for the new user
        token, _ = Token.objects.get_or_create(user=user)
        request.session['auth_token'] = token.key
        return redirect('login_page')


# Login and logout view to handle user authentication
class Login_Logout_view(APIView):
    permission_classes = [AllowAny]  # Allow any user to log in or log out

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        # Authenticate user with provided username and password
        if user is not None:
            # Generate authentication token for the user
            token, _ = Token.objects.get_or_create(user=user)
            login(request, user)  # Log in the user
            request.session['auth_token'] = token.key  # Store token in session
            return redirect('blogs_list')  # Redirect to blogs list after successful login
        else:
            return render(request, 'login.html', {'error_message': 'Wrong credentials, try again'})

    # GET request to log out a user
    def get(self, request):
        request.session.flush()
        logout(request)
        return redirect('login_register')
