import streamlit as st
import requests

API_URL = "http://localhost:8000"
def main():
    st.title("कल्याणम समाजिक स्वास्थ्य सेवा API")
    st.sidebar.title("Menu")

    menu = ['Home', 'View Patients', 'Add Patient', 'Update Patient', 'Delete Patient']
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == 'Home':
        st.subheader("कल्याणम समाज स्वस्त सेवा में आपका स्वागत है")
        st.write("Dr. B.K. Jha (Founder, Kalyanam Samajik Swasthya Seva)")
        st.write("This is a simple Patient Management System.")
        st.write("You can view, add, update, and delete patient details.")

    elif choice == 'View Patients':
        st.subheader("View Patients")
        response = requests.get(f"{API_URL}/view")
        if response.status_code == 200:
            data = response.json()
            st.write(data)
        else:
            st.error("Failed to fetch patient details.")

    elif choice == 'Add Patient':
        st.subheader("Add New Patient")
        patient_id = st.text_input("Patient ID")
        name = st.text_input("Name")
        father_name = st.text_input("Father's Name")
        mother_name = st.text_input("Mother's Name")
        grandfather_name = st.text_input("Grandfather's Name")
        grandmother_name = st.text_input("Grandmother's Name")
        phone = st.text_input("Phone Number")
        address = st.text_input("Address")
        age = st.number_input("Age", min_value=0, max_value=120)
        gender = st.text_input("Gender")
        bp = st.number_input("Blood Pressure (mmHg)", min_value=0.0, format="%.2f")
        sugar = st.number_input("Sugar Level (mg/dL)", min_value=0.0, format="%.2f")
        temperature = st.number_input("Temperature (Celsius)", min_value=0.0, format="%.2f")
        reason = st.text_input("Reason for Visit")

        if st.button("Add Patient"):
            patient_data = {
                "id": patient_id,
                "name": name,
                "father_name": father_name,
                "mother_name": mother_name,
                "grandfather_name": grandfather_name,
                "grandmother_name": grandmother_name,
                "phone": phone,
                "address": address,
                "age": age,
                "gender": gender,
                "bp": bp,
                "sugar": sugar,
                "temperature": temperature,
                "reason": reason
            }
            response = requests.post(f"{API_URL}/create", json=patient_data)
            if response.status_code == 201:
                st.success("Patient added successfully!")
            else:
                st.error("Failed to add patient. Please check the details and try again.")

    elif choice == 'Update Patient':
        st.subheader("Update Patient")
        patient_id = st.text_input("Patient ID to Update")
        if patient_id:
            response = requests.get(f"{API_URL}/patients/{patient_id}")
            if response.status_code == 200:
                patient_data = response.json()
                name = st.text_input("Name", value=patient_data.get("name", ""))
                father_name = st.text_input("Father's Name", value=patient_data.get("father_name", ""))
                mother_name = st.text_input("Mother's Name", value=patient_data.get("mother_name", ""))
                grandfather_name = st.text_input("Grandfather's Name", value=patient_data.get("grandfather_name", ""))
                grandmother_name = st.text_input("Grandmother's Name", value=patient_data.get("grandmother_name", ""))
                phone = st.text_input("Phone Number", value=patient_data.get("phone", ""))
                address = st.text_input("Address", value=patient_data.get("address", ""))
                age = st.number_input("Age", min_value=0, max_value=120, value=patient_data.get("age", 0))
                gender = st.text_input("Gender", value=patient_data.get("gender", ""))
                bp = st.number_input("Blood Pressure (mmHg)", min_value=0.0, format="%.2f", value=patient_data.get("bp", 0.0))
                sugar = st.number_input("Sugar Level (mg/dL)", min_value=0.0, format="%.2f", value=patient_data.get("sugar", 0.0))
                temperature = st.number_input("Temperature (Celsius)", min_value=0.0, format="%.2f", value=patient_data.get("temperature", 0.0))
                reason = st.text_input("Reason for Visit", value=patient_data.get("reason", ""))

                if st.button("Update Patient"):
                    updated_data = {
                        "name": name,
                        "father_name": father_name,
                        "mother_name": mother_name,
                        "grandfather_name": grandfather_name,
                        "grandmother_name": grandmother_name,
                        "phone": phone,
                        "address": address,
                        "age": age,
                        "gender": gender,
                        "bp": bp,
                        "sugar": sugar,
                        "temperature": temperature,
                        "reason": reason
                    }
                    response = requests.put(f"{API_URL}/edit/{patient_id}", json=updated_data)
                    if response.status_code == 200:
                        st.success("Patient updated successfully!")
                    else:
                        st.error("Failed to update patient. Please check the details and try again.")
            else:
                st.error("Patient not found. Please check the Patient ID and try again.")

    elif choice == 'Delete Patient':
        st.subheader("Delete Patient")
        patient_id = st.text_input("Patient ID to Delete")
        if st.button("Delete Patient"):
            response = requests.delete(f"{API_URL}/delete/{patient_id}")
            if response.status_code == 200:
                st.success("Patient deleted successfully!")
            else:
                st.error("Failed to delete patient. Please check the Patient ID and try again.")
if __name__ == "__main__":
    main()
