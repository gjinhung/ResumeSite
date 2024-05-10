from flask import Blueprint, jsonify, request
from ..models import db, Resume, Section, Company, Detail
from flask_login import login_required, current_user
from ..forms.resume_form import ResumeForm
import datetime

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
    else:
        return jsonify({"errors": "Resume is currently unavailable"}), 404

    return {resume_dict["id"]: resume_dict}


@resume_routes.route("/new", methods=["POST"])
@login_required
def new_resume():
    form = ResumeForm()

    form["csrf_token"].data = request.cookies["csrf_token"]

    if form.validate_on_submit():
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
