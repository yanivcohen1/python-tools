import streamlit as st

# run once
if "init" not in st.session_state:
    # Initialize 'options' variable
    st.session_state["init"] = True
    st.session_state["options"] = []

# Create a button that populates the 'options' variable when clicked
if st.button('Load options'):
    st.session_state["options"] = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Create a button that clears the 'options' variable when clicked
if st.button('Clear options'):
    st.session_state["options"] = []

# Use 'options' as input to st.multiselect
selected_options = st.multiselect('Select options', st.session_state["options"])

# Display the selected options
if selected_options:
    st.write(f"You have selected {selected_options}")

    # Also print each selected option
    for option in selected_options:
        st.write(f"Option: {option}")
