from datetime import datetime, timezone
from pymongo import MongoClient
from typing import NamedTuple

# 1️⃣ Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["testdb"]

users_collection = db["users"]
addresses_collection = db["addresses"]

startDate = datetime(2025, 10, 1, 0, 0, 0, tzinfo=timezone.utc)
endDate = datetime(2025, 10, 31, 23, 59, 59, tzinfo=timezone.utc)

class Result(NamedTuple):
    id: str
    addressId: str
    userName: str
    city: str

# 2️⃣ Build aggregation pipeline
pipeline = [
    { # First filter by date do it before run query
        "$match": {
          "createdAt": {
              "$gte": startDate,
              "$lte": endDate
          }
        }
    },
    {
        "$lookup": { #
            "from": "addresses", # collection to join
            "localField": "addressIds", # field from users collection
            "foreignField": "_id", # field from addresses collection
            "as": "addressesList" # output array field alieass
        }
    },
    { "$unwind": "$addressesList" },  # flatten addresses array
    # {
    #     "$lookup": {  # New lookup for kids
    #         "from": "kids",  # collection to join
    #         "localField": "kidIds",  # field from users collection (assuming it exists)
    #         "foreignField": "_id",  # field from kids collection
    #         "as": "kidsList"  # output array field
    #     }
    # },
    # { "$unwind": "$kidsList" },  # flatten kids array
    {
        "$match": {
            "$and": [
                {"addressesList.city": "Los Angeles"},
                {"name": "David"}
            ]
        }
    },
    {
        "$project": {
            "_id": 0,  # exclude original _id
            "id": "$_id",  # alias _id to id
            "addressId": "$addressesList._id", # include address _id
            "userName": "$name",
            "city": "$addressesList.city"
          # "kidName": "$kidsList.name"
        }
    }
]

# 3️⃣ Run aggregation
results: list[Result] = [Result(**doc) for doc in users_collection.aggregate(pipeline)]

if results:
    print("user name:", results[0].userName)
else:
    print("No results found")

# 4️⃣ Print results
for doc in results:
    print(doc)


# For many-to-many relationships
# from bson import ObjectId

# class Enrollment(NamedTuple):
#     _id: str
#     studentId: str
#     courseId: str
#     grade: str = None  # optional

# # Assuming enrollments collection
# enrollments = db["enrollments"]

# # Insert
# student_id = ObjectId()  # replace with actual student ObjectId
# course_id = ObjectId()   # replace with actual course ObjectId

# enrollment = {
#     "studentId": student_id,
#     "courseId": course_id
# }
# enrollments.insert_one(enrollment)

# # Read
# enrollments_docs = list(enrollments.find({"studentId": student_id}))
# results: list[Enrollment] = [Enrollment(**doc) for doc in enrollments_docs]
# print("grade:", results[0].grade)
# for enrollment in results:
#     print(enrollment)

# # Remove
# enrollments.delete_one({"studentId": student_id, "courseId": course_id})
