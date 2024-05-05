from .db import db, environment, SCHEMA, add_prefix_for_prod
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

details_tags = db.Table(
    "details_tags",
    db.Model.metadata,
    db.Column(
        "detail_id",
        db.Integer,
        db.ForeignKey(add_prefix_for_prod("details.id")),
        primary_key=True,
    ),
    db.Column(
        "tag_id",
        db.Integer,
        db.ForeignKey(add_prefix_for_prod("tags.id")),
        primary_key=True,
    ),
)

if environment == "production":
    details_tags.schema = SCHEMA


class User(db.Model, UserMixin):
    __tablename__ = "users"

    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    joined_on = db.Column(db.DateTime(), nullable=False)
    profile_pic = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime(), nullable=False)
    updated_at = db.Column(db.DateTime(), nullable=False)

    resumes = db.relationship("Resume", back_populates="user")
    companies = db.relationship("Company", back_populates="user")
    tags = db.relationship("Tag", back_populates="user")

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "joined_on": self.joined_on,
            "profile_pic": self.profile_pic,
            "phone": self.phone,
            "location": self.location,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class Resume(db.Model):
    __tablename__ = "resumes"

    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_prod("users.id")), nullable=False
    )
    title = db.Column(db.String(40), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    updated_at = db.Column(db.DateTime(), nullable=False)

    user = db.relationship("User", back_populates="resumes")
    sections = db.relationship("Section", back_populates="resume")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class Section(db.Model):
    __tablename__ = "sections"

    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=True)
    resume_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_prod("resumes.id")), nullable=False
    )
    created_at = db.Column(db.DateTime(), nullable=False)
    updated_at = db.Column(db.DateTime(), nullable=False)

    resume = db.relationship("Resume", back_populates="sections")
    companies = db.relationship("Company", back_populates="section")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "resume_id": self.resume_id,
            # "created_at": self.created_at,
            # "updated_at": self.updated_at,
        }


class Detail(db.Model):
    __tablename__ = "details"

    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(40), nullable=False, unique=True)
    company_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_prod("companies.id")), nullable=False
    )
    created_at = db.Column(db.DateTime(), nullable=False)
    updated_at = db.Column(db.DateTime(), nullable=False)

    company = db.relationship("Company", back_populates="details")
    tags = db.relationship("Tag", secondary=details_tags, back_populates="details")

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "company_id": self.company_id,
            # "created_at": self.created_at,
            # "updated_at": self.updated_at,
        }


class Company(db.Model):
    __tablename__ = "companies"

    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    organization = db.Column(db.String(40), nullable=False, unique=False)
    title = db.Column(db.String(40), nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_prod("users.id")), nullable=False
    )
    section_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_prod("sections.id")), nullable=False
    )
    start_date = db.Column(db.String(40), nullable=True)
    end_date = db.Column(db.String(40), nullable=True)
    created_at = db.Column(db.DateTime(), nullable=False)
    updated_at = db.Column(db.DateTime(), nullable=False)

    section = db.relationship("Section", back_populates="companies")
    details = db.relationship("Detail", back_populates="company")
    user = db.relationship("User", back_populates="companies")

    def to_dict(self):
        return {
            "id": self.id,
            "organization": self.organization,
            "title": self.title,
            "user_id": self.user_id,
            "section_id": self.section_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            # "created_at": self.created_at,
            # "updated_at": self.updated_at,
        }


class Tag(db.Model):
    __tablename__ = "tags"

    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(40), nullable=False, unique=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_prod("users.id")), nullable=False
    )
    created_at = db.Column(db.DateTime(), nullable=False)
    updated_at = db.Column(db.DateTime(), nullable=False)

    user = db.relationship("User", back_populates="tags")
    details = db.relationship("Detail", secondary=details_tags, back_populates="tags")

    def to_dict(self):
        return {
            "id": self.id,
            "tag": self.tag,
            "user_id": self.user_id,
            # "created_at": self.created_at,
            # "updated_at": self.updated_at,
        }
