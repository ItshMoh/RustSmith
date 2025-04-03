"""
MongoDB connection and operations for Rustsmith
"""
import pymongo
from config import MONGODB_URI, MONGODB_DB, MONGODB_COLLECTION

class MongoDB:
    def __init__(self, uri=MONGODB_URI):
        self.client = pymongo.MongoClient('mongodb+srv://mohcodes:SitARam%40108@mlproject.yu0js.mongodb.net/?retryWrites=true&w=majority&appName=MlProject')
        self.db = self.client['rustsmith']
        self.collection = self.db['user_contexts']
    
    def get_user_context(self, user_id):
        """
        Retrieve user context from MongoDB
        
        Args:
            user_id (str): The unique identifier for the user
            
        Returns:
            list: List of dictionaries containing question, answer, and error
        """
        user_record = self.collection.find_one({"user_id": user_id})
        if user_record:
            return user_record.get("context", [])
        return []
    
    def update_user_context(self, user_id, context):
        """
        Update user context in MongoDB
        
        Args:
            user_id (str): The unique identifier for the user
            context (list): List of dictionaries with question, answer, and error
            
        Returns:
            bool: True if update was successful
        """
        self.collection.update_one(
            {"user_id": user_id},
            {"$set": {"context": context}},
            upsert=True
        )
        return True