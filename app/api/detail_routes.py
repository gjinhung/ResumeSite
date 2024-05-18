from flask import Blueprint, jsonify, request
from ..models import db, Resume, Section, Company, Detail
from flask_login import login_required, current_user
from ..forms.detail_form import DetailForm
import datetime
from .auth_routes import validation_errors_to_error_messages

detail_routes = Blueprint("sections", __name__)


@detail_routes.route("/")
@login_required
def get_user_details():
    details_list = []
    details = Detail.query.filter_by(user_id=current_user.id)

    if details:
        for detail in details:
            detail_dict = detail.dict()
            tags = detail.tags
            detail_dict["Tags"] = tags
            details_list.append(detail_dict)
    else:
        return jsonify({"errors": "Details is currently unavailable"}), 404

    return {"details": {detail["id"]: detail for detail in details_list}}


@detail_routes.route("/<int:id>")
def get_one_detail(id):
    detail = Detail.query.get(id)
    if detail:
        detail_dict = detail.dict()
        tags = detail.tags
        detail_dict["Tags"] = tags
        return {detail_dict["id"]: detail_dict}
    else:
        return jsonify({"errors": "Detail is currently unavailable"}), 404


@detail_routes.route("/new", methods=["POST"])
@login_required
def new_detail():
    form = DetailForm()

    form["csrf_token"].data = request.cookies["csrf_token"]

    if form.validate_on_submit():
        form.title.data = form.title.data.strip()

        detail = Detail(
            user_id=current_user.id,
            company_id=form.company_id.data,
            description=form.description.data,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )

        db.session.add(detail)
        db.session.commit()

        detail_dict = detail.to_dict()

        return detail_dict
    else:
        return {"errors": "error in post a new Detail"}


@detail_routes.route("/<int:id>", methods=["PUT"])
@login_required
def edit_detail(id):
    form = DetailForm()
    form["csrf_token"].data = request.cookies["csrf_token"]
    detail = Detail.query.get(id)
    if current_user.id != detail.user_id:
        return jsonify({"errors": "Unauthorized to edit this Detail"}), 403

    if form.validate_on_submit():
        form.description.data = form.description.data.strip()

        detail.updated_at = datetime.datetime.utcnow()
        detail.description = form.description.data
        if form.company_id.data != detail.company_id:
            detail.company_id = form.company_id.data
        db.session.commit()

        return detail.to_dict()
    else:
        return {"errors": validation_errors_to_error_messages(form.errors)}


@detail_routes.route("/<int:id>/", methods=["DELETE"])
@login_required
def delete_detail(id):
    detail = Detail.query.get(id)

    if not detail:
        return jsonify({"errors": "Detail not found"}), 404

    try:
        db.session.delete(detail)
        db.session.commit()

        response = {"message": "Detail successfully deleted."}

        return jsonify(response)

    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {
                    "errors": "An error occurred while deleting this Detail",
                    "message": str(e),
                }
            ),
            500,
        )
