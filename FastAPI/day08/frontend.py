import streamlit as st
import requests
from jedi.inference.compiled import value

API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(layout="wide")

st.title("Insurance  Premium category prediction")

st.markdown("Enter your details below:")

# input fields

age = st.number_input("Age", min_value=5, max_value=100, value=0)
weight = st.number_input("Weight", min_value=0, max_value=100, value=30)
height = st.number_input("Height", min_value=0.5, max_value=3, value=1.7)
income_lpa = st.number_input("Income", min_value=0, max_value=1000, value=0)
smoker = st.selectbox("Smoker", options=[True, False])
city = st.text_input("City", value= "Mumbai")
occupation = st.selectbox("Occupation", options=['retired', 'unemployed', 'business owner', 'government job', 'student', 'freelancer', 'private job'])

if st.button("predict premium category"):
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        response = requests.post(API_URL, json=input_data)
        if response.status_code == 200:
            result_data = response.json()
            st.success(result_data['message'])
        else:
            st.error(f"Request failed with status code {response.status_code}")
    except Exception as e:
        st.error(f"Request failed with status code {response.status_code}")
