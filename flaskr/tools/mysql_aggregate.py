import pymysql
from typing import NamedTuple

# Constants for dates
START_DATE = '2025-08-01'
END_DATE = '2025-10-31'

class Result(NamedTuple):
    id: str
    name: str
    city: str

# Connect to MySQL
connection = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="yanivc77",
    database="testdb"
)

cursor = connection.cursor()

# First filter users by date do it before run query
query = f"""
SELECT u.Id, u.Name, a.City
FROM (
  SELECT *
  FROM users
  WHERE CreatedAt BETWEEN '{START_DATE}' AND '{END_DATE}'
) AS u
JOIN addresses a ON a.UserId = u.Id
WHERE a.city = 'Los Angeles'
  AND u.name = 'David';
"""

# Execute the query
cursor.execute(query)

# Fetch and cast results to Result[]
results: list[Result] = [Result(id=row[0], name=row[1], city=row[2]) for row in cursor.fetchall()]

# Print the first user name
if results:
    print("First user name:", results[0].name)
else:
    print("No results found")

# Print all results
for row in results:
    print(row)

# Close connection
cursor.close()
connection.close()
