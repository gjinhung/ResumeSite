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


@company_routes.route("/<int:id>")
def get_one_company(id):
    company = Company.query.get(id)
    if company:
        company_dict = company.to_dict()
        details = Detail.query.filter_by(company_id=company.id)
        details_list = []
        for detail in details:
            detail_dict = detail.to_dict()
            detail_dict["id"] = detail.id
            tags = detail.tags
            detail_dict["Tags"] = tags
            details_list.append(detail_dict)
        company_dict["Details"] = details_list
        return {company_dict["id"]: company_dict}
    else:
        return jsonify({"errors": "Section is currently unavailable"}), 404


@company_routes.route("/new", methods=["POST"])
@login_required
def new_company():
    form = CompanyForm()

    form["csrf_token"].data = request.cookies["csrf_token"]

    if form.validate_on_submit():
        form.title.data = form.title.data.strip()
        form.organization.data = form.organization.data.strip()

        company = Company(
            user_id=current_user.id,
            organization=form.organization.data,
            title=form.title.data,
            section_id=form.section_id.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )

        db.session.add(company)
        db.session.commit()

        company_dict = company.to_dict()

        return company_dict
    else:
        return {"errors": "error in post a new Company"}


@company_routes.route("/<int:id>", methods=["PUT"])
@login_required
def edit_company(id):
    form = CompanyForm()
    form["csrf_token"].data = request.cookies["csrf_token"]
    company = Company.query.get(id)
    if current_user.id != company.user_id:
        return jsonify({"errors": "Unauthorized to edit this Company"}), 403

    if form.validate_on_submit():
        form.title.data = form.title.data.strip()
        form.organization.data = form.organization.data.strip()
        company.organization = form.organization.data
        company.title = form.title.data
        company.section_id = form.section_id.data
        company.start_date = form.start_date.data
        company.end_date = form.end_date.data
        company.updated_at = datetime.datetime.utcnow()
        db.session.commit()

        return company.to_dict()
    else:
        return {"errors": validation_errors_to_error_messages(form.errors)}


@company_routes.route("/<int:id>/", methods=["DELETE"])
@login_required
def delete_company(id):
    company = Company.query.get(id)

    if not company:
        return jsonify({"errors": "Company not found"}), 404

    try:
        db.session.delete(company)
        db.session.commit()

        response = {"message": "Company successfully deleted."}

        return jsonify(response)

    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {
                    "errors": "An error occurred while deleting this Company",
                    "message": str(e),
                }
            ),
            500,
        )
