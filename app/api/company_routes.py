from flask import Blueprint, jsonify, request
from ..models import db, Resume, Section, Company, Detail
from flask_login import login_required, current_user
from ..forms.company_form import CompanyForm
import datetime
from .auth_routes import validation_errors_to_error_messages

company_routes = Blueprint("companies", __name__)


@company_routes.route("/")
@login_required
def get_user_company():
    companies_list = []
    companies = Company.query.filter_by(user_id=current_user.id)

    if companies:
        for company in companies:
            company_dict = company.dict()
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
    else:
        return jsonify({"errors": "Sections is currently unavailable"}), 404

    return {"companies": {company["id"]: company for company in companies_list}}


@section_routes.route("/<int:id>")
def get_one_section(id):
    section = Section.query.get(id)
    if section:
        section_id = section.id
        sect_dict = section.to_dict()
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
        return {sect_dict["id"]: sect_dict}
    else:
        return jsonify({"errors": "Section is currently unavailable"}), 404


@section_routes.route("/new", methods=["POST"])
@login_required
def new_section():
    form = SectionForm()

    form["csrf_token"].data = request.cookies["csrf_token"]

    if form.validate_on_submit():
        form.title.data = form.title.data.strip()

        section = Section(
            user_id=current_user.id,
            title=form.title.data,
            resume_id=form.resume_id.data,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )

        db.session.add(section)
        db.session.commit()

        section_dict = section.to_dict()

        return section_dict
    else:
        return {"errors": "error in post a new Section"}


@section_routes.route("/<int:id>", methods=["PUT"])
@login_required
def edit_section(id):
    form = SectionForm()
    form["csrf_token"].data = request.cookies["csrf_token"]
    section = Section.query.get(id)
    if current_user.id != section.user_id:
        return jsonify({"errors": "Unauthorized to edit this Section"}), 403

    if form.validate_on_submit():
        form.title.data = form.title.data.strip()
        section.title = form.title.data
        section.updated_at = datetime.datetime.utcnow()
        db.session.commit()

        return section.to_dict()
    else:
        return {"errors": validation_errors_to_error_messages(form.errors)}


@section_routes.route("/<int:id>/", methods=["DELETE"])
@login_required
def delete_section(id):
    section = Section.query.get(id)

    if not section:
        return jsonify({"errors": "Section not found"}), 404

    try:
        db.session.delete(section)
        db.session.commit()

        response = {"message": "Section successfully deleted."}

        return jsonify(response)

    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {
                    "errors": "An error occurred while deleting this Section",
                    "message": str(e),
                }
            ),
            500,
        )
