from pymongo import MongoClient

# 1️⃣ Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["testdb"]

users_collection = db["users"]
addresses_collection = db["addresses"]

# 2️⃣ Build aggregation pipeline
pipeline = [
    {
        "$lookup": {
            "from": "addresses", # collection to join
            "localField": "addressIds", # field from users collection
            "foreignField": "_id", # field from addresses collection
            "as": "addressesList" # output array field alieass
        }
    },
    { "$unwind": "$addressesList" },  # flatten addresses array
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
            "_id": 1, # include user _id
            "addressId": "$addressesList._id", # include address _id
            "userName": "$name",
            "city": "$addressesList.city"
        }
    }
]

# 3️⃣ Run aggregation
results = users_collection.aggregate(pipeline)

# 4️⃣ Print results
for doc in results:
    print(doc)
