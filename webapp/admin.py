import datetime
import os
import uuid

from flask import Blueprint, render_template, redirect, request, flash, session
from .models import *
from werkzeug.utils import secure_filename
from .const import LEVELS

admin = Blueprint("admin", __name__, url_prefix="/admin")
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'images')


def generate_unique_filename(filename):
    unique_identifier = str(uuid.uuid4())
    _, file_extension = os.path.splitext(filename)
    unique_filename = f"{secure_filename(unique_identifier)}{file_extension}"
    return unique_filename


@admin.route("/", methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        check_user = Credential.query.filter(Credential.email == email).first()
        if not check_user:
            flash(f"User with <b>{email}</b> not found!", "error")
            return redirect("/admin/")

        if check_user.password != password:
            flash(f"Incorrect Password!", "error")
            return redirect("/admin/")

        session['id'] = check_user.id

        return redirect("/admin/queries")

    return render_template("login.html")


@admin.route("/logout")
def logout():
    if 'id' in session:
        session.pop('id')
    return redirect("/")


@admin.route("/queries")
def queries():
    all_queries = Queries.query.order_by(Queries.id.desc())
    return render_template("queries.html"
                           , all_queries=all_queries)


@admin.route("/update_profile", methods=['POST', 'GET'])
def update_profile():
    cred = Credential.query.first()
    about = About.query.first()

    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name")
        about_me = request.form.get("about")
        linkedin = request.form.get("linkedin")
        instagram = request.form.get("instagram")

        if "profile_pic" in request.files:
            file = request.files.get('profile_pic')

            unique_filename = generate_unique_filename(file.filename)

            file.save(os.path.join(UPLOAD_FOLDER, unique_filename))
            about.profile_pic = unique_filename

        cred.email = email
        cred.password = password
        about.full_name = name
        about.about = about_me
        about.linked_in = linkedin
        about.instagram = instagram

        db.session.commit()

    return render_template("update_profile.html"
                           , cred=cred
                           , about=about)


@admin.route("/skills", methods=['GET', 'POST'])
def skills():

    if request.method == 'POST':
        name = request.form.get('skill_name')
        experience = request.form.get('skill_experience')

        skill = Skills.query.filter(Skills.name == name.lower()).first()
        if skill:
            flash("Skill Already Exist!", "error")
            return redirect("/admin/skills")

        new_skill = Skills(name=name.lower()
                           , level=experience)

        db.session.add(new_skill)
        db.session.commit()

        flash("Skill Added Successfully", "success")
        return redirect("/admin/skills")

    my_skills = Skills.query.order_by(Skills.id.desc())

    return render_template("manage_skills.html"
                           , levels=LEVELS
                           , my_skills=my_skills)


@admin.route("/skills/delete/<int:skill_id>")
def delete_skill(skill_id):

    skill = Skills.query.get(skill_id)
    db.session.delete(skill)
    db.session.commit()

    flash("Skill Removed Successfully!", "success")
    return redirect("/admin/skills")


@admin.route("/projects")
def projects():

    projects = Project.query.order_by(Project.id.desc())

    return render_template("manage_projects.html"
                           , projects=projects)


@admin.route("/add_new_project", methods=['GET', "POST"])
def add_new_project():

    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        link = request.form.get('link')
        date_complete = request.form.get('date_completed')

        date_obj = datetime.datetime.strptime(date_complete, "%Y-%m-%d")

        new_project = Project(title=title
                              , desc=desc
                              , completed_on=date_obj
                              , repo_link=link)

        db.session.add(new_project)
        db.session.commit()

        flash("Project Added Successfully", "success")

        return redirect("/admin/projects")

    return render_template("add_project.html")


@admin.route("/delete_project/<int:project_id>")
def delete_project(project_id):
    project = Project.query.get(project_id)
    db.session.delete(project)
    db.session.commit()

    flash("Project Removed Successfully!", "success")
    return redirect("/admin/projects")