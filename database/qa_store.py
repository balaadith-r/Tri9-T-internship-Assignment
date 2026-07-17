from bson import ObjectId

from database.mongodb import db


class QAStore:
    def __init__(self):
        self.collection = db.generated_test_suites

    def save(self, qa_document: dict) -> str:
        result = self.collection.insert_one(qa_document)
        return str(result.inserted_id)

    def get_latest(self, selection_id: int):
        return self.collection.find_one(
            {"selection_id": selection_id},
            sort=[("generated_at", -1)],
        )

    def get_history(self, selection_id: int):
        return list(
            self.collection.find(
                {"selection_id": selection_id}
            ).sort("generated_at", -1)
        )

    def mark_stale_by_id(self, mongo_id: str):
        self.collection.update_one(
            {"_id": ObjectId(mongo_id)},
            {
                "$set": {
                    "stale": True
                }
            },
        )

    def delete_by_id(self, mongo_id: str):
        self.collection.delete_one(
            {"_id": ObjectId(mongo_id)}
        )
        
    def get_by_node_id(self, node_id: int):
        return list(
            self.collection.find(
                {
                    "test_cases.source_node_ids": node_id
                }
            ).sort("generated_at", -1)
        )