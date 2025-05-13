from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session, g
import os
import requests
import json # Added import
from .forms import RegistrationForm, LoginForm, CheckUserForm

# Create a Blueprint for views
views = Blueprint('views', __name__)



def verify_session():
    if 'session_token' not in session:
        return False
    service_url = os.getenv('USER_CONTROL_SERVICE_URL')
    if not service_url:
        return False

    try:
        response = requests.post(f'{service_url}/verify-session', json={'session_token': session['session_token']})
        session['email'] = response.json().get('email', session.get('email'))
        return response.status_code == 200
    except Exception as e:
        return False

@views.before_app_request
def load_logged_in_user():
    print("Before request: session =", dict(session))
    g.is_logged_in = False
    if 'session_token' in session:
        service_url = os.getenv('USER_CONTROL_SERVICE_URL')
        if service_url:
            try:
                response = requests.post(
                    f'{service_url}/verify-session',
                    json={'session_token': session['session_token']}
                )
                print("Verify session response:", response.status_code, response.text)
                if response.status_code == 200:
                    data = response.json()
                    g.is_logged_in = True
                    # Update session with latest info from microservice
                    session['email'] = data.get('email', session.get('email'))
                    session['name'] = data.get('name', session.get('name', ''))
            except Exception as e:
                print("Exception in verify-session:", e)


@views.app_context_processor
def inject_user():
    return {'is_logged_in': getattr(g, 'is_logged_in', False),
            'name': session.get('name', '')
    }

@views.route('/')
def home():
    """Home page route"""
    products = []
    try:
        # Construct the absolute path to items.json
        # Assuming 'static' is at the same level as 'templates' and this 'views.py' file's directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(base_dir, 'static', 'items.json')
        with open(json_file_path, 'r') as f:
            products = json.load(f)
    except FileNotFoundError:
        flash('Products file not found.', 'error')
    except json.JSONDecodeError:
        flash('Error decoding products JSON.', 'error')
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
    return render_template('home.html', products=products)

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
    form = CheckUserForm()
    if form.validate_on_submit():
        email = form.email.data
        service_url = os.getenv('USER_CONTROL_SERVICE_URL')
        if not service_url:
            flash('User control service URL is not set', 'error')
            return redirect(url_for('views.home'))
        try:
            response = requests.post(f'{service_url}/check-user', json={'email': email})
            response_data = response.json()
            if 'exists' in response_data and response_data['exists'] is False:
                flash('Seems you are new around here. Please complete your registration.', 'info')
                return redirect(url_for('views.userRegister', email=email))
            flash('Welcome back! Please enter your password to continue.', 'info')
            return redirect(url_for('views.userLogin', email=email))
        except Exception as e:
            flash(f'Error checking user: {str(e)}', 'error')
            return redirect(url_for('views.home'))
    return render_template('userInit.html', form=form)

@views.route('/login', methods=['GET', 'POST'])
def userLogin():
    form = LoginForm()
    email = request.args.get('email', '')
    if request.method == 'GET' and email:
        form.email.data = email
    if form.validate_on_submit():
        service_url = os.getenv('USER_CONTROL_SERVICE_URL')
        if not service_url:
            flash('User control service URL is not set', 'error')
            return redirect(url_for('views.home'))
        try:
            response = requests.post(
                f'{service_url}/login',
                json={'email': form.email.data, 'password': form.password.data}
            )
            response_data = response.json()
            print("Login response data:", response_data)
            if response.status_code == 200:
                session['session_token'] = response_data.get('session_token')
                session['user_id'] = response_data.get('user_id')
                session['email'] = response_data.get('email', '')
                session['name'] = response_data.get('name', '')
                flash('Login successful!', 'success')
                return redirect(url_for('views.home'))
            else:
                error_message = response_data.get('error', 'Invalid credentials. Please try again.')
                flash(error_message, 'error')
        except Exception as e:
            flash(f'Error during login: {str(e)}', 'error')
    return render_template('userLogin.html', form=form, email=email)

@views.route('/logout')
def userLogout():
    if 'session_token' in session:
        service_url = os.getenv('USER_CONTROL_SERVICE_URL')
        if not service_url:
            flash('User control service URL is not set', 'error')
            return redirect(url_for('views.home'))
        try:
            response = requests.post(f'{service_url}/logout', json={'session_token': session['session_token']})
            if response.status_code == 200:
                flash('Logged out successfully', 'success')
                session.clear()
                return redirect(url_for('views.home'))
            else:
                flash('Failed to log out', 'error')
                session.clear()
                return redirect(url_for('views.home'))
        except Exception as e:
            flash(f'Error during logout: {str(e)}', 'error')
            session.clear()
            return redirect(url_for('views.home'))


@views.route('/register', methods=['GET', 'POST'])
def userRegister():
    form = RegistrationForm()
    email = request.args.get('email', '')
    if request.method == 'GET' and email:
        form.email.data = email
    if form.validate_on_submit():
        service_url = os.getenv('USER_CONTROL_SERVICE_URL')
        if not service_url:
            flash('User control service URL is not set', 'error')
            return redirect(url_for('views.home'))
        try:
            response = requests.post(f'{service_url}/register', 
                                    json={
                                        'email': form.email.data,
                                        'password': form.password.data,
                                        'name': form.name.data
                                    })
            if response.status_code in [200, 201]:
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('views.userLogin', email=form.email.data))
            else:
                try:
                    response_data = response.json()
                    error_message = response_data.get('error', 'Registration failed. Please try again.')
                except ValueError:
                    error_message = f'Registration failed. Server returned: {response.text}'
                flash(error_message, 'error')
        except Exception as e:
            flash(f'Error during registration: {str(e)}', 'error')
    return render_template('userRegister.html', form=form, email=email)



@views.route('/metadata/<int:fileID>', methods=['POST', 'GET'])
def forwardMetadata(fileID):
    service_url = os.getenv('META_SERVICE_URL')
    if not service_url:
        flash('Metadata service URL is not set', 'error')
        return redirect(url_for('views.home'))
    try:
        if request.method == 'POST':
            data = request.get_json()
            if not data or 'metadata' not in data:
                return jsonify({"error": "Data or metadata Missing"}), 400
            response = requests.post(f'{service_url}/metadata/{fileID}', json=data)
            return jsonify(response.json()), response.status_code
        elif request.method == 'GET':
            response = requests.get(f'{service_url}/metadata/{fileID}')
            return jsonify(response.json()), response.status_code
        else:
            return jsonify({"error": "Method not allowed"}), 405
    except requests.exceptions.ConnectionError:
        response_data = {"error": "Failed to connect to the metadata microservice"}
        status_code = 503 # Service Unavailable
    except requests.exceptions.Timeout:
        response_data = {"error": "Request to the metadata microservice timed out"}
        status_code = 504 # Gateway Timeout
    except requests.exceptions.RequestException as e:
        # Catch other general request exceptions
        response_data = {"error": f"Error communicating with metadata microservice: {str(e)}"}
        status_code = 500
    except ValueError: # If res.json() fails to parse (e.g., microservice returned non-JSON)
            response_data = {"error": "Invalid JSON response from metadata microservice"}
            # Keep status_code from the microservice if available
            status_code = res.status_code if 'res' in locals() and res.status_code >= 400 else 502 # Bad Gateway

    return jsonify(response_data), status_code


@views.route('/product/<int:productID>', methods=['GET', 'POST'])
def product(productID):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(base_dir, 'static', 'items.json')
        with open(json_file_path, 'r') as f:
            products = json.load(f)
        product = next((item for item in products if item['id'] == productID), None)
        if product is None:
            flash('Product not found.', 'error')
            return redirect(url_for('views.home'))

    except FileNotFoundError:
        flash('Products file not found.', 'error')
    
    return render_template('productPage.html', product=product)