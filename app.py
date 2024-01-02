import streamlit as st
import json
from datetime import datetime
import os
import openai
from openai import OpenAI
import base64

def safe_json_serialize(data):
    try:
        return json.dumps(data, default=str)  # Converts to JSON, with a default handler for non-serializable types
    except TypeError as e:
        print(f"Error in JSON serialization: {e}")
        return "{}"

def save_data_as_json(file_name):
    if os.path.exists(file_name):
        with open(file_name,"r") as file:
             return json.load(file)
    return []

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


def clear_form_fields():
    """Clears all fields in st.session_state."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]

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

    # st.json(user_data)


    with st.form("user_info_form"):
        name = st.text_input("Name", key="name")
        age = st.number_input("Age", key="age")
        gender = st.radio("Gender", ["Male", "Female", "Other"], key="gender")
        interest = st.text_area("Interest", key="interest")
        work = st.text_input("Work", key="work")
        salary = st.number_input("Salary", key="salary")
        dob = st.date_input("Date of Birth", key="dob")
        religion = st.text_input("Religion", key="religion")
        photo = st.file_uploader("Upload a photo", key="photo")
        planetary_position = st.text_input("Planetary Position", key="planetary_position")
        horoscope_chart = st.file_uploader("Upload your horoscope chart", key="horoscope_chart")
        star = st.selectbox("Star", options=['Ashwini','Bharani','Krittika','Rohini','Mrighasira','Ardra','Punarvasu','Pushya','Ashlesha','Magha','Purva Phalguni','Uttara Phalguni','Hasta','Chitra','Swati','Vishaka','Anuradha','Jyestha','Moola','Purvashada','Uttarashada','Sharavan','Dhanishta','Shatabisha','Purvabhadra','Uttarabhadra','Revat'], key="star")  # add all star names
        

        # submit= st.form_submit_button("Submit")

        all_fields_filled = all([name, age > 0, gender, interest, work, salary > 0, dob, religion, planetary_position, star])
        if all_fields_filled:
            st.write(f"All fields filled: {all_fields_filled}")
        submitted = st.form_submit_button("Submit", disabled=not (all_fields_filled and photo is not None and horoscope_chart is not None))

        if submitted:
            encoded_photo = base64.b64encode(photo.read()).decode() if photo else None
            encoded_horoscope_chart = base64.b64encode(horoscope_chart.read()).decode() if horoscope_chart else None

            user_data = {
                    "name": name,
                    "age":age,
                    "gender": gender,
                    "interest": interest,
                    "work":work,
                    "salary":salary,
                    "dob": dob.strftime("%Y-%m-%d"),
                    "religion": religion,
                    "photo": encoded_photo,
                    "Planetary_position":planetary_position,
                    "horoscope_chart": encoded_horoscope_chart,
                    "star":star 
                }
            save_data(user_data)
            st.success("Data Saved Successfully!")

            clear_form_fields()
            st.rerun() 
        else:
             st.warning("Please fill in all required fields.")

    try:
        with open("user_data.json", "r") as file:
            user_data_json_content = file.read()
    except FileNotFoundError:
         user_data_json_content = "{}"
    st.download_button(
        label="Download JSON file",
        data=user_data_json_content,
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
