import numpy as np 
import pandas as pd 
import streamlit as st 
import sqlite3
import joblib 


st.title("🏡 House Price Prediction")

model = joblib.load("house5.pkl")




bedrooms = st.text_input("Bedrooms", "")
washrooms = st.text_input("Bathrooms", "")
balcony = st.text_input("Balcony", "")
area_sqft = st.text_input("Area (sq ft)", "")
floor = st.text_input("Floor", "")

furnishing = st.selectbox("Furnishing", ["Fully-Furnished", "Semi-Furnished", "Unfurnished"])
furn_map = {"Unfurnished": 0, "Semi-Furnished": 1, "Fully-Furnished": 2}
furn_val = furn_map[furnishing]

year_built = st.text_input("Built Year", "")

city = st.selectbox("City", ["Mumbai", "Delhi", "Pune", "Chennai", "Hyderabad", "Kolkata", "Bangalore"])
city_map = {"Bangalore": 0, "Chennai": 1, "Delhi": 2, "Hyderabad": 3, "Kolkata": 4, "Mumbai": 5, "Pune": 6}
city_val = city_map[city]

all_filled = all([bedrooms, washrooms, balcony, area_sqft, floor, year_built])

if st.button("₹ Predict Price"):
    if not all_filled:
        st.warning("⚠ Please fill all the fields before predicting price")
    else:
        b = int(bedrooms)
        w = int(washrooms)
        bal = int(balcony)
        area = float(area_sqft)
        fl = int(floor)
        yr = int(year_built)

        input_data = np.array([[b, w, bal, area, fl, furn_val, city_val, yr]])
        price = model.predict(input_data)[0]

        st.success(f"Predicted Price:₹{price:}")

conn = sqlite3.connect("price.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS house_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    area_sqft REAL,
    bedrooms INTEGER,
    washrooms INTEGER,
    balcony INTEGER,
    furnishing TEXT,
    city TEXT,
    year_built INTEGER,
    floor INTEGER
)
""")

if all_filled:
    c.execute("""
    INSERT INTO house_details(area_sqft, bedrooms, washrooms, balcony, furnishing, city, year_built, floor)
    VALUES (?,?,?,?,?,?,?,?)
    """, (area_sqft, bedrooms, washrooms, balcony, furnishing, city, year_built, floor))
    conn.commit()

conn.close()


