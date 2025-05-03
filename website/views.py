from flask import Blueprint, render_template, request, flash, redirect, url_for
import os
import requests


# Create a Blueprint for views
views = Blueprint('views', __name__)

@views.route('/')
def home():
    """Home page route"""
    return render_template('home.html')

@views.route('/orders')
def orders():
    """Orders page route"""
    return render_template('orders.html')

@views.route('/settings')
def settings():
    """Settings page route"""
    return render_template('settings.html')

@views.route('/userInit', methods=['GET', 'POST'])
def checkUser():
    if request.method == 'POST':
        # Get email from form
        email = request.form.get('email')
        
        # Check if the user service URL is set
        service_url = os.getenv('USER_CONTROL_SERVICE_URL')
        if not service_url:
            flash('User control service URL is not set', 'error')
            return redirect(url_for('views.home'))
        
        try:
            # Make a request to check if user exists
            response = requests.post(f'{service_url}/check-user', json={'email': email})
            response_data = response.json()
            
            # If user does not exist, redirect to registration with email
            if 'exists' in response_data and response_data['exists'] is False:
                flash('Seems you are new around here. Please complete your registration.', 'info')
                return redirect(url_for('views.userRegister', email=email))
            
            # If user exists, redirect to login with email
            flash('Welcome back! Please enter your password to continue.', 'info')
            return redirect(url_for('views.userLogin', email=email))
            
        except Exception as e:
            flash(f'Error checking user: {str(e)}', 'error')
            return redirect(url_for('views.home'))
    
    # GET request - show the initial form
    return render_template('userInit.html')

@views.route('/login', methods=['GET', 'POST'])
def userLogin():
    if request.method == 'POST':
        # Handle login submission
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Here you would validate credentials with your user service
        service_url = os.getenv('USER_CONTROL_SERVICE_URL')
        if not service_url:
            flash('User control service URL is not set', 'error')
            return redirect(url_for('views.home'))
        
        try:
            # This endpoint would need to exist in your user service
            response = requests.post(f'{service_url}/login', 
                                    json={'email': email, 'password': password})
            
            if response.status_code == 200:
                flash('Login successful!', 'success')
                return redirect(url_for('views.home'))
            else:
                flash('Invalid credentials. Please try again.', 'error')
                return render_template('userLogin.html', email=email)
                
        except Exception as e:
            flash(f'Error during login: {str(e)}', 'error')
            return render_template('userLogin.html', email=email)
            
    # GET request - show the login form, possibly with pre-filled email
    email = request.args.get('email', '')
    return render_template('userLogin.html', email=email)

@views.route('/register', methods=['GET', 'POST'])
def userRegister():
    if request.method == 'POST':
        # Handle registration submission
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Here you would register the user with your user service
        service_url = os.getenv('USER_CONTROL_SERVICE_URL')
        if not service_url:
            flash('User control service URL is not set', 'error')
            return redirect(url_for('views.home'))

        try:
            response = requests.post(f'{service_url}/register', 
                                    json={'email': email, 'password': password})

            if response.status_code == 200:
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('views.userLogin', email=email))
            else:
                flash('Registration failed. Please try again.', 'error')
                return render_template('userRegister.html', email=email)
                
        except Exception as e:
            flash(f'Error during registration: {str(e)}', 'error')
            return render_template('userRegister.html', email=email)

    # GET request - show the registration form, possibly with pre-filled email
    email = request.args.get('email', '')
    return render_template('userRegister.html', email=email)

