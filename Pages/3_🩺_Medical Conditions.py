import streamlit as st
import pickle
from pandas import DataFrame
import json
from streamlit_lottie import st_lottie

st.title("Pinnacle of Health Challenges")
# Header
st.header("Medical Conditions Faced by Many")

#define cols
col1, col2 = st.columns([1.5,1])

with col1:
    drugs_dict = pickle.load(open('Model/drugs_dict.pkl','rb'))
    drugs = DataFrame(drugs_dict)

    # Slider for selecting the number of top conditions to display
    num_conditions = st.slider('Select the Number of Top Conditions to Display:', min_value=1, max_value=50, value=10)

    # Display the most common conditions
    if st.button('Show most common conditions'):
        top_conditions = drugs['condition'].value_counts().head(num_conditions)
        st.table(top_conditions)


with col2:
    # animetion from local machine
    def load_lottiefile(filepath: str):
        with open(filepath, "r") as f:
            return json.load(f)


    hello_lottie_local = load_lottiefile("medical_conditions.json")

    st_lottie(
        hello_lottie_local,
        speed=1,
        reverse=False,
        loop=True,
        quality="low",  # medium,high
        # renderer = "svg", #canvas
        height=350,
        width=300,
        key=None,
    )