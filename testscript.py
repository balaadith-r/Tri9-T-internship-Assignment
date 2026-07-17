# from database.database import SessionLocal
# from database.selection_repository import SelectionRepository

# from services.prompt_builder import PromptBuilder
# from services.llm.gemini_client import GeminiClient


# def main():
#     db = SessionLocal()

#     try:
#         selection_repo = SelectionRepository(db)

#         # Change if your selection has a different ID
#         selection_id = 1

#         nodes = selection_repo.get_selection_nodes(selection_id)

#         if not nodes:
#             print(f"No nodes found for selection {selection_id}")
#             return

#         prompt = PromptBuilder().build(nodes)

#         print("\nGenerating QA test suite...\n")

#         llm = GeminiClient()

#         suite = llm.generate_test_suite(prompt)

#         print(suite.model_dump_json(indent=2))

#     finally:
#         db.close()


# if __name__ == "__main__":
#     main()

from datetime import datetime, timedelta

from database.qa_store import QAStore

store = QAStore()

# yesterday
store.save({
    "selection_id": 1,
    "generated_at": datetime.now() - timedelta(days=1),
    "stale": False,
    "test_cases": []
})

# today
store.save({
    "selection_id": 1,
    "generated_at": datetime.now(),
    "stale": False,
    "test_cases": []
})

latest = store.get_latest(1)

print("Latest:")
print(latest["generated_at"])

history = store.get_history(1)

print("\nHistory:")

for doc in history:
    print(doc["generated_at"])