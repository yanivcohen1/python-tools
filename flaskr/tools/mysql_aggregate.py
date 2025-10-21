import pymysql

# Constants for dates
START_DATE = '2025-10-01'
END_DATE = '2025-10-31'

# Connect to MySQL
connection = pymysql.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="your_database"
)

cursor = connection.cursor()

# SQL query with f-string formatting
query = f"""
SELECT u.id, u.name, a.city
FROM (
  SELECT *
  FROM users
  WHERE created_at BETWEEN '{START_DATE}' AND '{END_DATE}'
) AS u
JOIN addresses a ON a.id = u.address_id
WHERE a.city = 'LA'
  AND u.name = 'David';
"""

# Execute the query
cursor.execute(query)

# Fetch and print results
results = cursor.fetchall()
for row in results:
    print(row)

# Close connection
cursor.close()
connection.close()
