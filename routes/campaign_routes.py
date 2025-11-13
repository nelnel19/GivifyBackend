from flask import Blueprint, request, jsonify
from CampaignModel import CampaignModel
from bson import ObjectId
from database import campaigns_collection
import base64
import os
from werkzeug.utils import secure_filename

campaign_routes = Blueprint("campaign_routes", __name__)

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Create uploads directory if it doesn't exist
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        return f"/{UPLOAD_FOLDER}/{filename}"
    return None

# Get all campaigns
@campaign_routes.route("/campaigns", methods=["GET"])
def get_campaigns():
    campaigns = CampaignModel.get_all_campaigns()
    return jsonify(campaigns), 200

# Create a new campaign
@campaign_routes.route("/campaigns", methods=["POST"])
def create_campaign():
    try:
        # Check if form data contains file
        if 'image' in request.files:
            file = request.files['image']
            image_path = save_image_file(file)
        else:
            image_path = None

        # Get form data
        title = request.form.get("title")
        description = request.form.get("description")
        goal_amount = request.form.get("goalAmount")

        if not title or not description or not goal_amount:
            return jsonify({"error": "Title, description, and goal amount are required"}), 400

        campaign_id = CampaignModel.create_campaign(title, description, goal_amount, image_path)
        return jsonify({"message": "Campaign created successfully", "id": campaign_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update a campaign
@campaign_routes.route("/campaigns/<id>", methods=["PUT"])
def update_campaign(id):
    try:
        update_fields = {}

        # Handle file upload if present
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:  # Only update image if a new file is provided
                image_path = save_image_file(file)
                if image_path:
                    update_fields["image"] = image_path

        # Get other form data
        if "title" in request.form:
            update_fields["title"] = request.form["title"]
        if "description" in request.form:
            update_fields["description"] = request.form["description"]
        if "goalAmount" in request.form:
            update_fields["goalAmount"] = request.form["goalAmount"]

        if not update_fields:
            return jsonify({"error": "No fields to update"}), 400

        result = campaigns_collection.update_one({"_id": ObjectId(id)}, {"$set": update_fields})
        if result.matched_count == 0:
            return jsonify({"error": "Campaign not found"}), 404

        campaign = campaigns_collection.find_one({"_id": ObjectId(id)})
        return jsonify({
            "id": str(campaign["_id"]),
            "title": campaign["title"],
            "description": campaign["description"],
            "goalAmount": campaign["goalAmount"],
            "collectedAmount": campaign.get("collectedAmount", 0),
            "image": campaign.get("image")
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a campaign
@campaign_routes.route("/campaigns/<id>", methods=["DELETE"])
def delete_campaign(id):
    try:
        result = campaigns_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            return jsonify({"error": "Campaign not found"}), 404

        return jsonify({"message": "Campaign deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500