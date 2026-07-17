from pprint import pprint

from database.mongodb import db

for doc in db.generated_test_suites.find():
    pprint(doc)