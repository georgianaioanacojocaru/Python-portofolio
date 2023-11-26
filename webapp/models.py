from .const import db


class Credential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    password = db.Column(db.String(20))


class About(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_pic = db.Column(db.String(255))
    full_name = db.Column(db.String(255))
    about = db.Column(db.Text)
    linked_in = db.Column(db.String(255))
    instagram = db.Column(db.String(255))


class Skills(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    level = db.Column(db.String(20))


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    desc = db.Column(db.Text)
    completed_on = db.Column(db.Date)
    repo_link = db.Column(db.String(255))


class Queries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(30))
    email = db.Column(db.String(30))
    phone = db.Column(db.String(30))
    location = db.Column(db.String(20))
    message = db.Column(db.Text)