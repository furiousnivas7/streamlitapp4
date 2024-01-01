import streamlit as st
import json
from datetime import datetime
import os
import openai
from openai import OpenAI

def save_data_as_json(file_name):
    if os.path.exists(file_name):
        with open(file_name,"r") as file:
            return json.dumps(json.load(file))
    return json.dumps([])

def call_gbt3(prompt):
    openai.api_key = os.environ['OPEN_API_KEY']
    client=OpenAI()

    response = client.completinons.create(
        model="gpt-3.5-turbo-instruct",  
        prompt=prompt,  
        max_tokens = 1000 
    )

    return response.choices[0].text
# Function to save data to a JSON file
def save_data(data, filename="user_data.json"):
    try:
        with open(filename, "r") as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []

    existing_data.append(data)

    with open(filename, "w") as file:
        json.dump(existing_data, file, indent=12)

# Streamlit app
def main():
    if 'full_prompt' not in st.session_state:
        st.session_state.full_prompt=""
    if 'gpt3_response' not in st.session_state:
        st.session_state.gpt3_response=""

    if 'user_data.json' not in st.session_state:
        file_name="user_data.json"
        st.session_state.user_data_json = ""


    st.title("User Information Form")
    file_name = "user_data.json"
    st.session_state.user_data_json = str(save_data_as_json(file_name))
    user_data = save_data(file_name)

    


    with st.form("user_info_form",clear_on_submit=True):
        name = st.text_input("Name")
        st.write("Welcome",name)
        age  =st.number_input("Age" ,placeholder="insert the age",value=None)
        gender = st.radio("Gender", ["Male", "Female", "Other"])
        interest = st.text_area("Interest",placeholder=" You enter your requirments like salary religion gender work")
        work =st.text_input("work" ,placeholder="goverment or private")
        salary=st.number_input("salary",placeholder="enter your salary")
        dob = st.date_input("Date of Birth")
        religion = st.text_input("Religion")
        photo = st.file_uploader("Upload a photo")
        Planetary_position =st.text_input("Planetary_position" ,placeholder="enter your Planetary_position")
        star =st.selectbox("star" ,('Ashwini','Bharani','Krittika','Rohini','Mrighasira','Ardra','Punarvasu','Pushya','Ashlesha','Magha','Purva Phalguni','Uttara Phalguni','Hasta','Chitra','Swati','Vishaka','Anuradha','Jyestha','Moola','Purvashada','Uttarashada','Sharavan','Dhanishta','Shatabisha','Purvabhadra','Uttarabhadra','Revat'))
        horoscope_chart =st.file_uploader("Upload a photo of your horoscope_chart")
        
        # submit= st.form_submit_button("Submit")

        # if name and age and gender and interest and work and salary and dob and religion and photo:
        submitted = st.form_submit_button("Submit")
        if submitted:
                user_data = {
                    "name": name,
                    "age":age,
                    "gender": gender,
                    "interest": interest,
                    "work":work,
                    "salary":salary,
                    "dob": dob.strftime("%Y-%m-%d"),
                    "religion": religion,
                    "photo": photo.read(),
                    "Planetary_position":Planetary_position,
                    "star":star,
                    "horoscope_chart":horoscope_chart.read()    
                }
                save_data(user_data)
                st.success("Data Saved Successfully!")
        # else:
        #     st.warning("Please fill in all required fields.")

    with open("user_data.json", "r") as json_file:
        st.download_button(
            label="Download JSON file",
            data=json_file,
            file_name="user_data.json",
            mime="application/json"
        )
    user_prompt = st.text_input("Enter your prompt here")  
    button = st.button("Send Data to GPT-3.5") 

    if button:
        full_prompt = str(st.session_state.user_data_json) + user_prompt  
        gpt3_response = call_gbt3(full_prompt)  
    
        user_data = {
                "interest": user_prompt,
                "gpt3_response": gpt3_response,
                "photo": st.file_uploader("Upload a photo").read()
            }

        save_data(user_data)
        st.write("OpenAI Response:", gpt3_response)
        st.success("Data Saved Successfully!") 

if __name__ == "__main__":
    main()
