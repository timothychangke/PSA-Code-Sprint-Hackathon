from flask import Blueprint, render_template
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from datetime import datetime
from website.models import Approved_courses, User, User_courses

views = Blueprint('views', __name__)

@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        course_name = request.form.get('course')
        organisation = request.form.get('organisation')
        date = datetime.strptime(request.form.get('datepicker'), '%m/%d/%Y')
        approved_courses = Approved_courses.query.filter_by(course_name=course_name).first()
        if approved_courses and organisation == approved_courses.organisation:
            course_check = User_courses.query.filter_by(course_id=approved_courses.id).first()
            if not course_check:
                new_course = User_courses(course_name=course_name, organisation=organisation, date=date, user_id=current_user.id)
                db.session.add(new_course)
                db.session.commit()
                return render_template("home.html", user=current_user)
            else:
                flash("You have already inputted this course into the website.", category="error")
                return render_template("home.html", user=current_user)
        else:
            flash("The course you have entered is not valid.", category="error")
            return render_template("home.html", user=current_user)
            
            
            
    
    return render_template("home.html", user=current_user)