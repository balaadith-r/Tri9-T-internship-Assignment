from database.qa_store import QAStore


class RetrievalService:
    def __init__(self):
        self.qa_store = QAStore()

    def get_latest(self, selection_id: int):
        return self.qa_store.get_latest(selection_id)

    def get_history(self, selection_id: int):
        return self.qa_store.get_history(selection_id)

    def get_by_node_id(self, node_id: int):
        return self.qa_store.get_by_node_id(node_id)