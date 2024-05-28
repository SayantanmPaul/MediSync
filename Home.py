#import lottie
import streamlit as st
import firebase_admin
import json
import requests
from streamlit_lottie import st_lottie
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
import pandas as pd
import numpy as np
import joblib


st.set_page_config(
    page_title="MediSync",
    page_icon="🩺"
)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("drug-prescription-17cba-d6b39273782c.json")
firebase_admin.initialize_app(cred)

#st.sidebar.success("Select a page above")

def page1():
    st.title("Home")
    # Define the columns
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.title("Welcome to MediSync")
        st.header("Your Health, Your Way!")
        description_text = """
        Embrace the future of personalized healthcare. 
        Join MediSync and embark on a journey where 
        your prescriptions are as unique as you are. 
        Your health, personalized. Your journey, empowered. 
        Welcome to MediSync — Where Precision Meets Personalization.
        """

        st.text(description_text)

    #add medicine.py
        if st.button("Explore"):
            st.session_state.page = 'Account'





    with col2:
        #animetion from local machine
        def load_lottiefile(filepath:str):
            with open(filepath, "r") as f:
                return json.load(f)


        #animetion from url
        #def load_lottieurl(url:str):
            #r = requests.get(url)
            #if r.status_code != 200:
             #   return None
            #return r.json()'''

        #hello_lottie_url = load_lottieurl("https://app.lottiefiles.com/animation/0969293e-77d2-4e5a-a2b4-d90c18ca8abe?channel=web&source=public-animation&panel=download")
        hello_lottie_local = load_lottiefile("hello_man.json")

        st_lottie(
            hello_lottie_local,
            speed=1,
            reverse=False,
            loop=True,
            quality="low", #medium,high
            #renderer = "svg", #canvas
            height=500,
            width=300,
            key=None,
        )



def page2():
    st.title('Account')

    # Initialize session state variables
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''
    if "signedout" not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False

    # Firebase REST API endpoints
    api_key = "AIzaSyDw0szPidgs3RmwOLq2136V34Hx36OZchM"
    sign_up_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
    sign_in_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    reset_password_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"

    # Function to sign up user
    def sign_up_with_email_and_password(email, password, username=None):
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        if username:
            payload["displayName"] = username
        response = requests.post(sign_up_url, params={"key": api_key}, data=json.dumps(payload))
        if response.status_code == 200:
            return response.json()['email']
        else:
            st.warning(response.json())

    # Function to sign in user
    def sign_in_with_email_and_password(email, password):
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(sign_in_url, params={"key": api_key}, data=json.dumps(payload))
        if response.status_code == 200:
            data = response.json()
            user_info = {
                'email': data['email'],
                'username': data.get('displayName', '')  # Retrieve username if available
            }
            return user_info
        else:
            st.warning(response.json())

    # Function to reset password
    def reset_password(email):
        payload = {
            "email": email,
            "requestType": "PASSWORD_RESET"
        }
        response = requests.post(reset_password_url, params={"key": api_key}, data=json.dumps(payload))
        if response.status_code == 200:
            return True, "Reset email sent"
        else:
            return False, response.json().get('error', {}).get('message')

    # Login handler
    def handle_login():
        try:
            userinfo = sign_in_with_email_and_password(st.session_state.email_input, st.session_state.password_input)
            st.session_state.username = userinfo['username']
            st.session_state.useremail = userinfo['email']
            st.session_state.signedout = True
            st.session_state.signout = True
        except Exception as e:
            st.warning(f'Login failed: {e}')

    # Logout handler
    def handle_logout():
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ''

    # Reset password handler
    def handle_reset_password():
        email = st.text_input('Email')
        if st.button('Send Reset Link'):
            success, message = reset_password(email)
            if success:
                st.success(message)
            else:
                st.warning(f"Password reset failed: {message}")

    # Main app logic
    if not st.session_state["signedout"]:
        choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')
        st.session_state.email_input = email
        st.session_state.password_input = password

        if choice == 'Sign up':
            username = st.text_input("Enter your unique username")
            if st.button('Create my account'):
                user = sign_up_with_email_and_password(email=email, password=password, username=username)
                st.success('Account created successfully! Please login using your email and password.')
                st.balloons()
        else:
            st.button('Login', on_click=handle_login)
            handle_reset_password()



    #st.title("Welcome")
    if st.session_state.signout:
        st.header(f"Welcome {st.session_state.username}, here's your virtual medical assistant")



        # load datasets
        sym_des = pd.read_csv("Dataset/symtoms_df.csv")
        precautions = pd.read_csv("Dataset/precautions_df.csv")
        workout = pd.read_csv("Dataset/workout_df.csv")
        description = pd.read_csv("Dataset/description.csv")
        medications = pd.read_csv("Dataset/medications.csv")
        diets = pd.read_csv("Dataset/diets.csv")

        # load model
        # svc = pickle.load(open("Model/svc.pkl",'rb'))
        svc = joblib.load(open("Model/svc_model.pkl", 'rb'))

        # model prediction function
        symptoms_dict = {'itching': 0, 'skin_rash': 1, 'nodal_skin_eruptions': 2, 'continuous_sneezing': 3,
                         'shivering': 4, 'chills': 5, 'joint_pain': 6, 'stomach_pain': 7, 'acidity': 8,
                         'ulcers_on_tongue': 9, 'muscle_wasting': 10, 'vomiting': 11, 'burning_micturition': 12,
                         'spotting_ urination': 13, 'fatigue': 14, 'weight_gain': 15, 'anxiety': 16,
                         'cold_hands_and_feets': 17, 'mood_swings': 18, 'weight_loss': 19, 'restlessness': 20,
                         'lethargy': 21, 'patches_in_throat': 22, 'irregular_sugar_level': 23, 'cough': 24,
                         'high_fever': 25, 'sunken_eyes': 26, 'breathlessness': 27, 'sweating': 28, 'dehydration': 29,
                         'indigestion': 30, 'headache': 31, 'yellowish_skin': 32, 'dark_urine': 33, 'nausea': 34,
                         'loss_of_appetite': 35, 'pain_behind_the_eyes': 36, 'back_pain': 37, 'constipation': 38,
                         'abdominal_pain': 39, 'diarrhoea': 40, 'mild_fever': 41, 'yellow_urine': 42,
                         'yellowing_of_eyes': 43, 'acute_liver_failure': 44, 'fluid_overload': 45,
                         'swelling_of_stomach': 46, 'swelled_lymph_nodes': 47, 'malaise': 48,
                         'blurred_and_distorted_vision': 49, 'phlegm': 50, 'throat_irritation': 51,
                         'redness_of_eyes': 52, 'sinus_pressure': 53, 'runny_nose': 54, 'congestion': 55,
                         'chest_pain': 56, 'weakness_in_limbs': 57, 'fast_heart_rate': 58,
                         'pain_during_bowel_movements': 59, 'pain_in_anal_region': 60, 'bloody_stool': 61,
                         'irritation_in_anus': 62, 'neck_pain': 63, 'dizziness': 64, 'cramps': 65, 'bruising': 66,
                         'obesity': 67, 'swollen_legs': 68, 'swollen_blood_vessels': 69, 'puffy_face_and_eyes': 70,
                         'enlarged_thyroid': 71, 'brittle_nails': 72, 'swollen_extremeties': 73, 'excessive_hunger': 74,
                         'extra_marital_contacts': 75, 'drying_and_tingling_lips': 76, 'slurred_speech': 77,
                         'knee_pain': 78, 'hip_joint_pain': 79, 'muscle_weakness': 80, 'stiff_neck': 81,
                         'swelling_joints': 82, 'movement_stiffness': 83, 'spinning_movements': 84,
                         'loss_of_balance': 85, 'unsteadiness': 86, 'weakness_of_one_body_side': 87,
                         'loss_of_smell': 88, 'bladder_discomfort': 89, 'foul_smell_of urine': 90,
                         'continuous_feel_of_urine': 91, 'passage_of_gases': 92, 'internal_itching': 93,
                         'toxic_look_(typhos)': 94, 'depression': 95, 'irritability': 96, 'muscle_pain': 97,
                         'altered_sensorium': 98, 'red_spots_over_body': 99, 'belly_pain': 100,
                         'abnormal_menstruation': 101, 'dischromic _patches': 102, 'watering_from_eyes': 103,
                         'increased_appetite': 104, 'polyuria': 105, 'family_history': 106, 'mucoid_sputum': 107,
                         'rusty_sputum': 108, 'lack_of_concentration': 109, 'visual_disturbances': 110,
                         'receiving_blood_transfusion': 111, 'receiving_unsterile_injections': 112, 'coma': 113,
                         'stomach_bleeding': 114, 'distention_of_abdomen': 115, 'history_of_alcohol_consumption': 116,
                         'fluid_overload.1': 117, 'blood_in_sputum': 118, 'prominent_veins_on_calf': 119,
                         'palpitations': 120, 'painful_walking': 121, 'pus_filled_pimples': 122, 'blackheads': 123,
                         'scurring': 124, 'skin_peeling': 125, 'silver_like_dusting': 126, 'small_dents_in_nails': 127,
                         'inflammatory_nails': 128, 'blister': 129, 'red_sore_around_nose': 130,
                         'yellow_crust_ooze': 131}
        diseases_list = {15: 'Fungal infection', 4: 'Allergy', 16: 'GERD', 9: 'Chronic cholestasis',
                         14: 'Drug Reaction', 33: 'Peptic ulcer diseae', 1: 'AIDS', 12: 'Diabetes ',
                         17: 'Gastroenteritis', 6: 'Bronchial Asthma', 23: 'Hypertension ', 30: 'Migraine',
                         7: 'Cervical spondylosis', 32: 'Paralysis (brain hemorrhage)', 28: 'Jaundice', 29: 'Malaria',
                         8: 'Chicken pox', 11: 'Dengue', 37: 'Typhoid', 40: 'hepatitis A', 19: 'Hepatitis B',
                         20: 'Hepatitis C', 21: 'Hepatitis D', 22: 'Hepatitis E', 3: 'Alcoholic hepatitis',
                         36: 'Tuberculosis', 10: 'Common Cold', 34: 'Pneumonia', 13: 'Dimorphic hemmorhoids(piles)',
                         18: 'Heart attack', 39: 'Varicose veins', 26: 'Hypothyroidism', 24: 'Hyperthyroidism',
                         25: 'Hypoglycemia', 31: 'Osteoarthristis', 5: 'Arthritis',
                         0: '(vertigo) Paroymsal  Positional Vertigo', 2: 'Acne', 38: 'Urinary tract infection',
                         35: 'Psoriasis', 27: 'Impetigo'}

        # user input
        # Extract the keys from symptoms_dict
        symptom_options = list(symptoms_dict.keys())
        # Multiselect for selecting multiple symptoms
        selected_symptoms = st.multiselect('Select Symptoms:', symptom_options)
        # Display the selected symptoms
        #st.write(f'Selected Symptoms: {selected_symptoms}')

        # helper function
        def helper(dis):
            desc = description[description['Disease'] == predicted_disease]['Description']
            desc = " ".join([w for w in desc])

            pre = precautions[precautions['Disease'] == dis][
                ['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
            # pre = [col for col in pre.values]
            pre = pre.values.tolist()  # Convert DataFrame to a list of lists (rows)

            med = medications[medications['Disease'] == dis]['Medication']
            med = [med for med in med.values]

            die = diets[diets['Disease'] == dis]['Diet']
            die = [die for die in die.values]

            wrkout = workout[workout['disease'] == dis]['workout']

            return desc, pre, med, die, wrkout

        def get_predicted_value(patient_symptoms):
            input_vector = np.zeros(len(symptoms_dict))

            for item in patient_symptoms:
                input_vector[symptoms_dict[item]] = 1
            return diseases_list[svc.predict([input_vector])[0]]

        # user_symptoms = [s.strip() for s in selected_symptoms.split(',')]
        user_symptoms = [sym.strip("[]' ") for sym in selected_symptoms]
        predicted_disease = get_predicted_value(user_symptoms)
        desc, pre, med, die, wrkout = helper(predicted_disease)

        if st.button('Show Results'):
            st.write(f'predicted disease: {predicted_disease}')
            st.write(f'description: {desc}')

            # Display results in columns
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.text("Precaution")
                for i, p_i in enumerate(pre[0], 1):
                    st.write(f"{i}: {p_i}")

            with col2:
                st.text("Medication")
                for i, m_i in enumerate(med, 1):
                    st.write(f"{i}: {m_i}")

            with col3:
                st.text("Workout")
                for i, w_i in enumerate(wrkout, 1):
                    st.write(f"{i}: {w_i}")

            with col4:
                st.text("Diet")
                for i, d_i in enumerate(die, 1):
                    st.write(f"{i}: {d_i}")


        st.button('Sign out', on_click=handle_logout)

# Set default page if not already set
if 'page' not in st.session_state:
    st.session_state.page = 'Home'


# Page routing logic
if st.session_state.page == 'Home':
    page1()
elif st.session_state.page == 'Account':
    page2()