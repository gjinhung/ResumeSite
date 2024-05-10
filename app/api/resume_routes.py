from flask import Blueprint, jsonify, request
from ..models import db, Resume, Section, Company, Detail
from flask_login import login_required, current_user
from ..forms.resume_form import ResumeForm
import datetime
from .auth_routes import validation_errors_to_error_messages

resume_routes = Blueprint("resumes", __name__)


@resume_routes.route("/")
@login_required
def get_user_resumes():
    resumes_list = []
    resumes = Resume.query.filter_by(user_id=current_user.id)

    if resumes:
        for resume in resumes:
            resume_dict = {}
            resume_dict["id"] = resume.id
            sections = resume.sections
            sections_list = []
            for section in sections:
                section_id = section.id
                sect_dict = {}
                sect_dict["id"] = section.id
                companies = Company.query.filter_by(section_id=section_id)
                companies_list = []
                for company in companies:
                    company_dict = {}
                    company_dict["id"] = company.id
                    details = Detail.query.filter_by(company_id=company.id)
                    details_list = []
                    for detail in details:
                        detail_dict = {}
                        detail_dict["id"] = detail.id
                        tags = detail.tags
                        detail_dict["Tags"] = tags
                        details_list.append(detail_dict)
                    company_dict["Details"] = details_list
                    companies_list.append(company_dict)
                sect_dict["Companies"] = companies_list
                sections_list.append(sect_dict)
            resume_dict["Sections"] = sections_list
            resumes_list.append(resume_dict)
    else:
        return jsonify({"errors": "Resume is currently unavailable"}), 404

    return {"resumes": {resumes["id"]: resumes for resumes in resumes_list}}


@resume_routes.route("/<int:id>")
def get_one_resume(id):
    resume = Resume.query.get(id)
    if resume:
        resume_dict = resume.to_dict()
        resume_dict["id"] = resume.id
        sections = resume.sections
        sections_list = []
        for section in sections:
            section_id = section.id
            sect_dict = section.to_dict()
            sect_dict["id"] = section.id
            companies = Company.query.filter_by(section_id=section_id)
            companies_list = []
            for company in companies:
                company_dict = company.to_dict()
                company_dict["id"] = company.id
                details = Detail.query.filter_by(company_id=company.id)
                details_list = []
                for detail in details:
                    detail_dict = detail.to_dict()
                    detail_dict["id"] = detail.id
                    tags = detail.tags
                    detail_dict["Tags"] = tags
                    details_list.append(detail_dict)
                company_dict["Details"] = details_list
                companies_list.append(company_dict)
            sect_dict["Companies"] = companies_list
            sections_list.append(sect_dict)
        resume_dict["Sections"] = sections_list
    else:
        return jsonify({"errors": "Resume is currently unavailable"}), 404

    return {resume_dict["id"]: resume_dict}


@resume_routes.route("/new", methods=["POST"])
@login_required
def new_resume():
    form = ResumeForm()

    form["csrf_token"].data = request.cookies["csrf_token"]

    if form.validate_on_submit():
        form.title.data = form.title.data.strip()
        if not form.title.data:
            untitledResume = Resume.query.filter_by(title="Resume").count()
            if not untitledResume:
                form.title.data = "Resume"
            else:
                resumeNum = 1
                untitledResume = Resume.query.filter_by(
                    title=f"Resume {resumeNum}"
                ).count()
                while untitledResume:
                    print(f"resumeNum = {resumeNum}")
                    resumeNum = resumeNum + 1
                    untitledResume = Resume.query.filter_by(
                        title=f"Resume {resumeNum}"
                    ).count()

                form.title.data = f"Resume {resumeNum}"

        else:
            existingResume = Resume.query.filter_by(title=form.title.data).count()
            if existingResume:
                resumeNum = 1
                untitledResume = Resume.query.filter_by(
                    title=f"{form.title.data} {resumeNum}"
                ).count()
                while untitledResume:
                    resumeNum = resumeNum + 1
                    untitledResume = Resume.query.filter_by(
                        title=f"{form.title.data}  {resumeNum}"
                    ).count()

                form.title.data = f"{form.title.data} {resumeNum}"

        resume = Resume(
            user_id=current_user.id,
            title=form.title.data,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )

        db.session.add(resume)
        db.session.commit()

        resume_dict = resume.to_dict()

        return resume_dict
    else:
        return {"errors": "error in post a new Resume"}


@resume_routes.route("/<int:id>", methods=["PUT"])
@login_required
def edit_resume(id):
    form = ResumeForm()
    form["csrf_token"].data = request.cookies["csrf_token"]
    resume = Resume.query.get(id)
    if current_user.id != resume.user_id:
        return jsonify({"errors": "Unauthorized to edit this Resume"}), 403

    if form.validate_on_submit():
        form.title.data = form.title.data.strip()
        if form.title.data:
            existingResume = Resume.query.filter_by(title=form.title.data).count()
            if existingResume:
                return {"errors": f"{form.title.data} already exist"}
            else:
                resume.title = form.title.data
                resume.updated_at = datetime.datetime.utcnow()

        db.session.commit()

        return resume.to_dict()
    else:
        return {"errors": validation_errors_to_error_messages(form.errors)}


@resume_routes.route("/<int:id>/", methods=["DELETE"])
@login_required
def delete_resume(id):
    resume = Resume.query.get(id)

    if not resume:
        return jsonify({"errors": "Review not found"}), 404

    try:
        db.session.delete(resume)
        db.session.commit()

        response = {"message": "Resume successfully deleted."}

        return jsonify(response)

    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {
                    "errors": "An error occurred while deleting the Resume",
                    "message": str(e),
                }
            ),
            500,
        )
