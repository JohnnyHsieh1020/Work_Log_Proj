# Create website route for Login, Sign up, Account and Logout.
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


# Login Page -----------------------------------------------------------------
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # If user click 'login' button
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check login info is correct
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect username or password.', category='error')
        else:
            flash('Email does not exsit.', category='error')

    return render_template('access/login.html', user=current_user)
# ----------------------------------------------------------------------------


# Sign Up Page ---------------------------------------------------------------
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # If user click 'submit' button
    if request.method == 'POST':
        name = request.form.get('firstName')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        identity = request.form.get('identity')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exsit.', category='error')
        # Each columns restrictions
        elif len(name) < 3:
            flash('Name must be greater than 3 character.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif password1 != password2:
            flash('Password don\'t match.', category='error')
        elif len(password1) < 5:
            flash('Password must be greater than 5 characters.', category='error')
        elif identity == None:
            flash('You have to choose your identity.', category='error')
        else:
            # Add new user to database
            new_user = User(name=name, email=email,
                            password=generate_password_hash(password1, method='sha256'), identity=identity)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')

            return redirect(url_for('views.home'))

    return render_template('access/sign_up.html', user=current_user)
# ----------------------------------------------------------------------------


# Account Page ---------------------------------------------------------------
@auth.route('/account', methods=['GET', 'POST'])
@login_required  # If user logged in, user may access to the Account Page.
def account():
    found_user = User.query.filter_by(email=current_user.email).first()

    if found_user:
        if request.method == 'POST':
            # Get new info
            name = request.form['name']
            pwd = request.form['password']

            if len(name) < 3:
                flash('Name must be greater than 3 character.', category='error')
            elif pwd == '':
                # Update data
                found_user.name = name
                db.session.commit()

                # Show message
                flash('Saved!', category='success')
            elif len(pwd) < 5:
                # Show message
                flash('Password must be greater than 5 characters.',
                      category='error')
            else:
                # Update data
                found_user.name = name
                found_user.password = generate_password_hash(
                    pwd, method='sha256')
                db.session.commit()

                # Show message
                flash('Saved!', category='success')
            return render_template('user/account.html', user=current_user, name=current_user.name, email=current_user.email)
        else:
            return render_template('user/account.html', user=current_user, name=current_user.name, email=current_user.email)
# ----------------------------------------------------------------------------


@auth.route('/logout')
@login_required  # User can't access to '/logout' if user does not log in.
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
