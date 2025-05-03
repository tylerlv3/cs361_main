from flask import Blueprint, render_template, request, flash, redirect, url_for
import os
import requests


# Create a Blueprint for views
views = Blueprint('views', __name__)

@views.route('/')
def home():
    """Home page route"""
    return render_template('home.html')

@views.route('/userInit', methods=['GET', 'POST'])
def checkUser():

    if request.method == 'POST':
        # Handle login logic here
        email = request.form.get('email')
        
        service_url = os.getenv('USER_CONTROL_SERVICE_URL')
        if not service_url:
            flash('User control service URL is not set', 'error')
            return redirect(url_for('views.home'))
        # Here you would typically make a request to the user control service

        response = requests.post(f'{service_url}/check-user', json={'email': email})

        print(response.json())
        if response.json()['exists'] is False:
            flash('Seems you are new around here. Please register below.', 'message')
            return redirect(url_for('views.userRegister'))



        return redirect(url_for('views.home'))
    
    return render_template('userInit.html')

@views.route('/register', methods=['GET', 'POST'])
def userRegister():
    if request.method == 'POST':
        # Handle registration logic here
        email = request.form.get('email')
        # Here you would typically make a request to the user control service to register the user

        service_url = os.getenv('USER_CONTROL_SERVICE_URL')
        if not service_url:
            flash('User control service URL is not set', 'error')
            return redirect(url_for('views.home'))

        response = requests.post(f'{service_url}/register', json={'email': email})

        if response.status_code == 200:
            flash('Registration successful!', 'success')
            return redirect(url_for('views.home'))
        else:
            flash('Registration failed. Please try again.', 'error')

    return render_template('userRegister.html')

