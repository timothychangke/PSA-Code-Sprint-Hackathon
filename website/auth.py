from nis import cat
from flask import Blueprint, render_template, request, flash, redirect, url_for
import re
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else: 
                flash("Incorrect password. Please try again.", category="error")
        else:
            flash("Incorrect email. Please try again.", category="error")  
    data = request.form
    print(data)
    return render_template("login.html", user=current_user)
    
@auth.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@auth.route("/sign-up", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exist", category="error")
        elif not re.match("^.+@.+\.com$", email):
            flash("Please enter a proper email address.", category='error')
        elif not firstName:
            flash('Please enter a valid first name.', category='error')
        
        elif not re.search("(?=.*\d)", password1):
            flash("Password should contain at least one digit.", category="error")
        elif not re.search("(?=.*[a-z])", password1):
            flash("Password should contain at least one lowercase letter.", category="error")
        elif not re.search("(?=.*[A-Z])", password1):
            flash("Password should contain at least one uppercase letter.", category="error")
        elif not re.search("(?=.*\W)", password1):
            flash("Password should contain at least one special character.", category="error")
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=firstName, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
        
        
    return render_template("signup.html", user=current_user)