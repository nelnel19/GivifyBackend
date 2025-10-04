from database import campaigns_collection  # Make sure this points to your MongoDB collection
from bson import ObjectId

class CampaignModel:
    @staticmethod
    def create_campaign(title, description, goal_amount, image):
        campaign = {
            "title": title,
            "description": description,
            "goalAmount": goal_amount,
            "collectedAmount": 0,
            "image": image
        }
        result = campaigns_collection.insert_one(campaign)
        return str(result.inserted_id)

    @staticmethod
    def get_all_campaigns():
        campaigns = campaigns_collection.find()
        return [
            {
                "id": str(campaign["_id"]),
                "title": campaign["title"],
                "description": campaign["description"],
                "goalAmount": campaign["goalAmount"],
                "collectedAmount": campaign["collectedAmount"],
                "image": campaign["image"]
            }
            for campaign in campaigns
        ]
