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
# project = select in sql; lookup = join in sql; unwind = as in SQL; match = where in sql
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


# ==================================================================================
# For many-to-many relationships
from bson import ObjectId

class Student(NamedTuple):
    name: str

class Course(NamedTuple):
    name: str

class Enrollment(NamedTuple):
    studentId: ObjectId
    courseId: ObjectId
    grade: str = None

class EnrollmentResult(NamedTuple):
    id: ObjectId
    studentId: ObjectId
    courseId: ObjectId
    grade: str
    courseName: str
    studentName: str

# Assuming enrollments collection
enrollments = db["enrollments"]
courses = db["courses"]
students = db["students"]

# insert sample data
student = Student("John Doe 2")
student_id = students.insert_one(student._asdict()).inserted_id
course = Course("Math 102")
course_id = courses.insert_one(course._asdict()).inserted_id

enrollment = Enrollment(student_id, course_id, "A")
enrollments.insert_one(enrollment._asdict())

# read_student_courses
pipeline = [
    {"$match": {"studentId": student_id}},
    {
        "$lookup": {
            "from": "courses",
            "localField": "courseId",
            "foreignField": "_id",
            "as": "course"
        }
    },
    {"$unwind": "$course"},
    {
        "$lookup": {  # added lookup for student name
            "from": "students",
            "localField": "studentId",
            "foreignField": "_id",
            "as": "student"
        }
    },
    {"$unwind": "$student"},  # added unwind for student
    {
        "$project": {
            "_id": 0,  # exclude original _id
            "id": "$_id",
            "studentId": "$studentId",
            "courseId": "$courseId",
            "grade": 1,
            "courseName": "$course.name",
            "studentName": "$student.name"  # added student name
        }
    }
]
enrollments_docs_list: list[EnrollmentResult] = [EnrollmentResult(**doc) for doc in enrollments.aggregate(pipeline)]
for edl in enrollments_docs_list:
    print(f"Student {edl.studentName} enrolled in course: {edl.courseName}")

# Remove
enrollments.delete_one({"studentId": student_id, "courseId": course_id})
