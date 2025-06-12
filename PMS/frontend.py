import streamlit as st
import requests

API_URL = "http://localhost:8000"
def main():
    st.title("कल्याणम समाजिक स्वास्थ्य सेवा API")
    st.sidebar.title("Menu")
    st.sidebar.image('file.enc')
    

    menu = ['Home', 'view Patients', 'Add Patient', 'Update Patient', 'Delete Patient']
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == 'Home':
        st.subheader("कल्याणम समाज स्वस्त सेवा में आपका स्वागत है")
        st.write("Dr. B.K. Jha (Founder, Kalyanam Samajik Swasthya Seva)")
        st.write("This is a simple Patient Management System.")
        st.write("You can view, add, update, and delete patient details.")

    elif choice == 'view Patients':
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
        city = st.text_input("City")
        age = st.number_input("Age", min_value=0, max_value=120)
        gender = st.text_input("Gender")
        height = st.number_input("Height (cm)", min_value=0.0, format="%.2f")
        weight = st.number_input("Weight (kg)", min_value=0.0, format="%.2f")
        if st.button("Add Patient"):
            patient_data = {
                "id": patient_id,
                "name": name,
                "city": city,
                "age": age,
                "gender": gender,
                "height": height,
                "weight": weight
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
                city = st.text_input("City", value=patient_data.get("city", ""))
                age = st.number_input("Age", min_value=0, max_value=120, value=patient_data.get("age", 0))
                gender = st.text_input("Gender", value=patient_data.get("gender", ""))
                height = st.number_input("Height (cm)", min_value=0.0, format="%.2f", value=patient_data.get("height", 0.0))
                weight = st.number_input("Weight (kg)", min_value=0.0, format="%.2f", value=patient_data.get("weight", 0.0))
                if st.button("Update Patient"):
                    updated_data = {
                        "name": name,
                        "city": city,
                        "age": age,
                        "gender": gender,
                        "height": height,
                        "weight": weight
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
