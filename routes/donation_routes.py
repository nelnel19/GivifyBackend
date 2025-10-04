from flask import Blueprint, request, jsonify
from DonationModel import DonationModel

donation_routes = Blueprint("donation_routes", __name__)

# ✅ Create a new donation
@donation_routes.route("/donate", methods=["POST"])
def donate():
    data = request.json
    try:
        # Create donation
        donation_id = DonationModel.create_donation(data)
        
        # Update campaign collected amount
        DonationModel.update_campaign_collected_amount(
            data["campaign_id"], data["donation_amount"]
        )
        
        return jsonify({"message": "Donation successful", "donation_id": donation_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ✅ Get donations by user email
@donation_routes.route("/donations/<email>", methods=["GET"])
def get_donations_by_user(email):
    try:
        donations = DonationModel.get_donations_by_user(email)
        return jsonify(donations), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ✅ Get all donations (Admin / Management)
@donation_routes.route("/donations", methods=["GET"])
def get_all_donations():
    try:
        donations = DonationModel.get_all_donations()
        return jsonify(donations), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ✅ Update donation status
@donation_routes.route("/donations/<donation_id>/status", methods=["PUT"])
def update_status(donation_id):
    data = request.json
    new_status = data.get("status")

    if not new_status:
        return jsonify({"error": "Status is required"}), 400

    try:
        updated = DonationModel.update_status(donation_id, new_status)
        if updated:
            return jsonify({"message": "Status updated successfully"}), 200
        else:
            return jsonify({"error": "Failed to update status"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400
