from flask import Blueprint, jsonify, request
from ..models import db, Resume, Section, Company, Detail
from flask_login import login_required, current_user
from ..forms.resume_form import ResumeForm
import datetime

resume_routes = Blueprint("resumes", __name__)


@resume_routes.route("/")
def get_user_resumes():
    resumes_list = []
    resumes = Resume.query.filter_by(user_id=current_user.id)

    if resumes:
        for resume in resumes:
            resume_dict = resume.to_dict()
            sections = resume.sections
            sections_list = []
            for section in sections:
                section_id = section.id
                sect_dict = section.to_dict()
                companies = Company.query.filter_by(section_id=section_id)
                companies_list = []
                for company in companies:
                    company_dict = company.to_dict()
                    details = Detail.query.filter_by(company_id=company.id)
                    details_list = []
                    for detail in details:
                        detail_dict = detail.to_dict()
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

    return {"resumes": {resumes["title"]: resumes for resumes in resumes_list}}


# @language_routes.route("/<int:id>")
# def get_one_language(id):
#     language = Language.query.get(id)

#     if not language:
#         return jsonify({"errors": "Language not found"}), 404

#     language_dict = language.to_dict()
#     guides = language.guides
#     guides_list = []
#     for guide in guides:
#         g_dic = guide.to_dict()
#     guides_list.append(g_dic["id"])
#     language_dict["guides_id"] = guides_list

#     return {language_dict["id"]: language_dict}


# @language_routes.route("/new", methods=["POST"])
# @login_required
# def new_language():
#     form = LanguageForm()
#     form["csrf_token"].data = request.cookies["csrf_token"]

#     if form.validate_on_submit():
#         language = Language(
#             language=form.language.data,
#             created_at=datetime.datetime.utcnow(),
#             updated_at=datetime.datetime.utcnow(),
#         )

#         db.session.add(language)
#         db.session.commit()

#         language_dict = language.to_dict()

#         guides = language.guides
#         guides_list = []
#         for guide in guides:
#             g_dic = guide.id
#         guides_list.append(g_dic)
#         language_dict["guides_id"] = guides_list

#         return language_dict
#     else:
#         return {"errors": "error in post a new language"}
