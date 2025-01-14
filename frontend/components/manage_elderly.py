import streamlit as st
from api_client import fetch_data, add_data, delete_data, update_task_status

def manage_elderly():
    st.subheader("👴 Manage Elderly")
    try:
        elderly_data = fetch_data("elderly")
        for elderly in elderly_data:
            # Create an expander for each elderly person
            with st.expander(f"{elderly['name']} (ID: {elderly['id']})"):
                # Layout: Delete button on the right
                col1, col2 = st.columns([8, 2])  # Adjust column width ratios
                with col1:
                    st.markdown(f"### {elderly['name']} (ID: {elderly['id']})")
                with col2:
                    if st.button(f"❌ Delete", key=f"delete_elderly_{elderly['id']}"):
                        delete_data(f"elderly/{elderly['id']}")
                        st.success(f"Elderly {elderly['name']} deleted successfully!")
                        continue  # Skip rendering tabs for deleted elderly

                # Tabs for managing elderly content
                tab1, tab2, tab3, tab4 = st.tabs(["Tasks", "Medications", "Add Task", "Add Medication"])

                # Tasks Tab
                with tab1:
                    st.markdown("**Tasks:**")
                    for task in elderly.get("tasks", []):
                        st.write(f"- {task['id']}: {task['description']} ({task['status']})")

                        new_status = st.text_input(f"Update Status for Task {task['id']}", value=task['status'], key=f"update_status_{task['id']}")
                        if st.button(f"Update Task {task['id']} Status", key=f"update_task_status_{task['id']}"):
                            update_task_status(elderly['id'], task['id'], new_status)
                            st.success(f"Task {task['id']} status updated to {new_status}!")

                        if st.button(f"Delete Task {task['id']}", key=f"delete_task_{task['id']}"):
                            delete_data(f"elderly/{elderly['id']}/tasks/{task['id']}")
                            st.success(f"Task {task['id']} deleted successfully!")

                # Medications Tab
                with tab2:
                    st.markdown("**Medications:**")
                    for med in elderly.get("medications", []):
                        st.write(f"- {med['name']} ({med['dosage']}, {med['frequency']})")

                        if st.button(f"Delete Medication {med['name']}", key=f"delete_medication_{med['id']}"):
                            delete_data(f"elderly/{elderly['id']}/medications/{med['id']}")
                            st.success(f"Medication {med['name']} deleted successfully!")

                # Add Task Tab
                with tab3:
                    description = st.text_input(f"Task Description for {elderly['name']}", key=f"task_description_{elderly['id']}")
                    status = st.text_input("Task Status", value="pending", key=f"task_status_{elderly['id']}")
                    if st.button(f"Add Task to {elderly['name']}", key=f"add_task_{elderly['id']}"):
                        payload = {"description": description, "status": status}
                        add_data(f"elderly/{elderly['id']}/tasks", payload)
                        st.success(f"Task added successfully to {elderly['name']}!")

                # Add Medication Tab
                with tab4:
                    name = st.text_input(f"Medication Name for {elderly['name']}", key=f"medication_name_{elderly['id']}")
                    dosage = st.text_input(f"Dosage for {elderly['name']}", key=f"medication_dosage_{elderly['id']}")
                    frequency = st.text_input(f"Frequency for {elderly['name']}", key=f"medication_frequency_{elderly['id']}")
                    if st.button(f"Add Medication to {elderly['name']}", key=f"add_medication_{elderly['id']}"):
                        payload = {"name": name, "dosage": dosage, "frequency": frequency}
                        add_data(f"elderly/{elderly['id']}/medications", payload)
                        st.success(f"Medication {name} added successfully to {elderly['name']}!")

    except RuntimeError as e:
        st.error(str(e))