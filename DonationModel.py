from database import donations_collection
from bson import ObjectId
from datetime import datetime

class DonationModel:
    @staticmethod
    def create_donation(donation_data):
        donation = {
            "user_email": donation_data["user_email"],
            "user_name": donation_data["user_name"],
            "campaign_id": donation_data["campaign_id"],
            "campaign_name": donation_data["campaign_name"],
            
            # Payment Method Section
            "payment_method": donation_data["payment_method"],
            "card_number": donation_data["card_number"],
            "expiry_date": donation_data["expiry_date"],
            "cvv": donation_data["cvv"],
            "billing_address": donation_data.get("billing_address", ""),
            
            # Donation Details Section
            "donation_amount": donation_data["donation_amount"],
            "donation_type": donation_data.get("donation_type", ""),
            "message": donation_data.get("message", ""),
            
            # Verification Section
            "age_requirement_accepted": donation_data["age_requirement_accepted"],
            "identity_verified": donation_data.get("identity_verified", False),
            "privacy_policy_accepted": donation_data["privacy_policy_accepted"],
            
            "donation_date": datetime.now(),
            "status": "completed"
        }
        
        result = donations_collection.insert_one(donation)
        return str(result.inserted_id)
    
    @staticmethod
    def update_campaign_collected_amount(campaign_id, donation_amount):
        from database import campaigns_collection
        campaigns_collection.update_one(
            {"_id": ObjectId(campaign_id)},
            {"$inc": {"collectedAmount": donation_amount}}
        )
    
    @staticmethod
    def get_donations_by_user(email):
        donations = donations_collection.find({"user_email": email})
        return [
            {
                "id": str(donation["_id"]),
                "campaign_name": donation["campaign_name"],
                "donation_amount": donation["donation_amount"],
                "donation_date": donation["donation_date"],
                "payment_method": donation["payment_method"],
                "status": donation.get("status", "completed")
            }
            for donation in donations
        ]

    # ✅ Get all donations
    @staticmethod
    def get_all_donations():
        donations = donations_collection.find()
        return [
            {
                "id": str(donation["_id"]),
                "user_name": donation["user_name"],
                "campaign_name": donation["campaign_name"],
                "donation_amount": donation["donation_amount"],
                "donation_date": donation["donation_date"],
                "payment_method": donation["payment_method"],
                "status": donation.get("status", "completed")
            }
            for donation in donations
        ]
    
    # ✅ Update donation status
    @staticmethod
    def update_status(donation_id, new_status):
        result = donations_collection.update_one(
            {"_id": ObjectId(donation_id)},
            {"$set": {"status": new_status}}
        )
        return result.modified_count > 0
