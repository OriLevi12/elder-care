import streamlit as st
from api_client import fetch_data

def view_data():
    st.subheader("📊 View Data")
    data_type = st.selectbox("Select data type", ["Elderly", "Caregivers"])

    if st.button("Fetch Data"):
        try:
            # Fetch data from the API
            data = fetch_data(data_type.lower())

            # Display Elderly data with tasks and medications
            if data_type == "Elderly":
                st.write("Elderly:")
                for entry in data:
                    with st.expander(f"{entry['name']} (ID: {entry['id']})"):
                        st.markdown(f"**Name:** {entry['name']}")
                        st.markdown(f"**ID:** {entry['id']}")
                        st.markdown("**Tasks:**")
                        for task in entry.get("tasks", []):
                            st.write(f"- {task['description']} ({task['status']})")
                        st.markdown("**Medications:**")
                        for med in entry.get("medications", []):
                            st.write(f"- {med['name']} ({med['dosage']}, {med['frequency']})")

            # Display Caregiver data
            elif data_type == "Caregivers":
                st.write("Caregivers:")
                for caregiver in data:
                    with st.expander(f"{caregiver['name']} (ID: {caregiver['id']})"):
                        st.markdown(f"**Bank Name:** {caregiver['bank_name']}")
                        st.markdown(f"**Bank Account:** {caregiver['bank_account']}")
                        st.markdown(f"**Branch Number:** {caregiver['branch_number']}")
                        salary_data = caregiver.get('salary', {})
                        st.markdown(f"**Salary:** Base: {salary_data.get('price', 'N/A')}, Amount: {salary_data.get('amount', 'N/A')}, Total: {salary_data.get('total', 'N/A')}")

        except RuntimeError as e:
            st.error(str(e))
