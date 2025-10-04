from flask import Blueprint, request, jsonify
from CampaignModel import CampaignModel
from bson import ObjectId
from database import campaigns_collection

campaign_routes = Blueprint("campaign_routes", __name__)

# Get all campaigns
@campaign_routes.route("/campaigns", methods=["GET"])
def get_campaigns():
    campaigns = CampaignModel.get_all_campaigns()
    return jsonify(campaigns), 200

# Create a new campaign
@campaign_routes.route("/campaigns", methods=["POST"])
def create_campaign():
    data = request.json
    title = data.get("title")
    description = data.get("description")
    goal_amount = data.get("goalAmount")
    image = data.get("image")

    if not title or not description or not goal_amount or not image:
        return jsonify({"error": "All fields are required"}), 400

    campaign_id = CampaignModel.create_campaign(title, description, goal_amount, image)
    return jsonify({"message": "Campaign created successfully", "id": campaign_id}), 201

# Update a campaign
@campaign_routes.route("/campaigns/<id>", methods=["PUT"])
def update_campaign(id):
    data = request.json
    update_fields = {}

    if "title" in data:
        update_fields["title"] = data["title"]
    if "description" in data:
        update_fields["description"] = data["description"]
    if "goalAmount" in data:
        update_fields["goalAmount"] = data["goalAmount"]
    if "image" in data:
        update_fields["image"] = data["image"]

    result = campaigns_collection.update_one({"_id": ObjectId(id)}, {"$set": update_fields})
    if result.matched_count == 0:
        return jsonify({"error": "Campaign not found"}), 404

    campaign = campaigns_collection.find_one({"_id": ObjectId(id)})
    return jsonify({
        "id": str(campaign["_id"]),
        "title": campaign["title"],
        "description": campaign["description"],
        "goalAmount": campaign["goalAmount"],
        "collectedAmount": campaign["collectedAmount"],
        "image": campaign["image"]
    }), 200

# Delete a campaign
@campaign_routes.route("/campaigns/<id>", methods=["DELETE"])
def delete_campaign(id):
    result = campaigns_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Campaign not found"}), 404

    return jsonify({"message": "Campaign deleted successfully"}), 200
