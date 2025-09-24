import pandas as pd
import mysql.connector
from pymongo import MongoClient
import matplotlib.pyplot as plt

# ==========================
# Connect to MySQL
# ==========================
mydb = mysql.connector.connect(
    host="localhost",
    user="root",             
    password="Bhargavi@2005", 
    database="food_delivery"
)

query = """
SELECT o.order_id, u.name AS user_name, r.name AS restaurant_name, 
       r.cuisine, o.order_time, o.delivery_time, o.amount
FROM orders o
JOIN users u ON o.user_id = u.user_id
JOIN restaurants r ON o.restaurant_id = r.restaurant_id;
"""
orders_df = pd.read_sql(query, mydb)

print("Orders Data:")
print(orders_df.head())

# ==========================
# MySQL Analysis
# ==========================
# Average delivery time
avg_time = orders_df['delivery_time'].mean()
print("\nAverage Delivery Time:", avg_time)

# Revenue by restaurant
orders_df.groupby('restaurant_name')['amount'].sum().plot(kind='bar')
plt.title("Revenue by Restaurant")
plt.xlabel("Restaurant")
plt.ylabel("Total Revenue")
plt.show()

# ==========================
# Connect to MongoDB
# ==========================
client = MongoClient("mongodb://localhost:27017/")
db = client["food_reviews"]
reviews_df = pd.DataFrame(list(db.reviews.find()))

print("\nReviews Data:")
print(reviews_df.head())

# ==========================
# MongoDB Analysis
# ==========================
# Average rating by restaurant
avg_rating = reviews_df.groupby("restaurant_id")["rating"].mean()
print("\nAverage Rating by Restaurant:")
print(avg_rating)

avg_rating.plot(kind='bar', color='orange')
plt.title("Average Ratings by Restaurant")
plt.xlabel("Restaurant ID")
plt.ylabel("Average Rating")
plt.show()
