from flask import Blueprint, render_template, request, flash, redirect
from .models import Queries, About, Skills, Project
import re
from .const import *

routes = Blueprint("route", __name__)


def validate_email(email):
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_pattern, email):
       return False

    return True


@routes.route('/')
@routes.route('/home')
def home():

    about = About.query.first()
    project = Project.query.limit(3).all()
    skills = Skills.query.limit(4).all()

    return render_template("home.html"
                           , projects=project
                           , skills=skills
                           , about=about)


@routes.route('/projects')
def projects():

    projects = Project.query.order_by(Project.id.desc())

    return render_template("projects.html"
                           , my_project=projects)


@routes.route("/skills")
def skills():
    my_skill = Skills.query.all()
    return render_template("skills.html"
                           , my_skills=my_skill)


@routes.route("/about")
def about():
    about = About.query.first()
    return render_template("about.html"
                           , about=about)


@routes.route("/contact", methods=['GET', 'POST'])
def contact():

    if request.method == 'POST':
        invalid_form_tracker = False
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        location = request.form.get('location')
        message = request.form.get('message')

        if not name:
            invalid_form_tracker = True
            flash("Name is Required", "error")

        if not email or not validate_email(email):
            invalid_form_tracker = True
            flash("Invalid Email Address", "error")

        if not phone:
            invalid_form_tracker = True
            flash("Phone Number is Required", "error")

        if not location or location not in CITIES:
            invalid_form_tracker = True
            flash("Location doesn't exist in database!", "error")

        if not message:
            invalid_form_tracker = True
            flash("Message is required", "error")

        if not invalid_form_tracker:
            flash("Thankyou for contacting me!", "success")

            new_query = Queries(full_name=name
                                , email=email
                                , phone=phone
                                , location=location
                                , message=message)

            db.session.add(new_query)
            db.session.commit()

        return redirect("/contact")

    return render_template("contact.html"
                           , locations=CITIES)

if __name__ == '__main__':
    app.run(debug=True, port=8080)