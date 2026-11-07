import sqlite3
import pandas as pd

conn = sqlite3.connect('cities.db')

conn.execute("DROP TABLE IF EXISTS cities")

conn.execute("""
CREATE TABLE cities (
    City_id     INTEGER      PRIMARY KEY,
    City_name   TEXT       NOT NULL UNIQUE,
    Country     TEXT         NOT NULL,
    Population  INTEGER,
    Is_Capital TEXT          DEFAULT 'No'
);
""")
conn.commit()
print("Table created successfully")


conn.execute("INSERT INTO cities VALUES (1, 'New York', 'USA', 8419600, 'Yes');")
conn.execute("INSERT INTO cities VALUES (2, 'Los Angeles', 'USA', 3980400, 'Yes');")
conn.execute("INSERT INTO cities VALUES (3, 'Chicago', 'USA', 2716000, 'No');")
conn.execute("INSERT INTO cities VALUES (4, 'Houston', 'USA', 2328000, 'No');")
conn.execute("INSERT INTO cities VALUES (5, 'Phoenix', 'USA', 1690000, 'Yes');")
conn.execute("INSERT INTO cities (City_id, City_name, Country) VALUES (6, 'Philadelphia', 'USA');")
conn.commit()
print("Rows inserted successfully")

cities = pd.read_sql_query("SELECT * FROM cities", conn)
print(cities)

print("\n--- TESTING PRIMARY KEY ---")
try:
    conn.execute("INSERT INTO cities VALUES (1, 'San Francisco', 'USA', 883305, 'Yes');")
    conn.commit()
except Exception as e:
    conn.rollback()
    print("Error occurred while inserting duplicate primary key:", e)
    print("City_Id 1 already belongs to New York - PRIMARY KEY MUST BE UNIQUE")

print("\n--- TESTING NOT NULL ---")
try:
    conn.execute("INSERT INTO cities VALUES (7, 'Berlin', NULL, 3769000, 'Yes');")
    conn.commit()
except Exception as e:
    conn.rollback()
    print("Error occurred while inserting NULL value in NOT NULL column:", e)
    print("Country cannot be NULL - every row must provide a country value")

print("\n--- TESTING UNIQUE ---")
try:
    conn.execute("INSERT INTO cities VALUES (8, 'New York', 'USA', 8419600, 'Yes');")
    conn.commit()
except Exception as e:
    conn.rollback()
    print("Rejected:", e)
    print("City_name 'New York' already exists - UNIQUE constraint violated")