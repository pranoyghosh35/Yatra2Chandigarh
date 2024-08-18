import streamlit as st
import base64

# Set page configuration as the first Streamlit command
st.set_page_config(layout="wide")

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"jpeg"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True)

def setup_ui():
    """
    Set up the Streamlit UI components.
    """
    st.image("backend/images/chandigarh_hand_symbol.jpg", width=300)
    #add_bg_from_local('backend/images/chandi_bg.png')
    st.title("🏞️ Welcome Traveller to Chandigarh!")
    st.sidebar.title("ℹ️ About")
    
    # Path to the README.html file
    readme_path = "https://pranoyghosh35.github.io/yatra2chandigarh/"

    # Provide a link to open the README.html content in a new window
    st.sidebar.markdown(
        f'<a href="{readme_path}" target="_blank" style="text-decoration: none;"><img src="https://img.icons8.com/color/48/000000/help.png" width="20"/> Help</a>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            width: 300px;
        }
        [data-testid="stSidebar"] .css-1d391kg {
            width: 300px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.info(
        """
        ## Example Questions

        If you are unsure of its capabilities, try asking about itself and what topics or example questions it can answer.
        """
    )
    
    # Display file uploader in sidebar
    #st.sidebar.info("Optional: Upload any additional/latest information about Chandigarh.")
    #uploaded_file = display_file_uploader(clear_submit)
    
    #if uploaded_file:
    #    st.sidebar.write(f"Uploaded file: {uploaded_file.name}")

def display_file_uploader(clear_submit):
    """
    Display the file uploader widget.
    """
    uploaded_file = st.sidebar.file_uploader(
        "Choose a file",
        type=['txt', 'doc', 'docx', 'pdf'],
        on_change=clear_submit,
    )
    return uploaded_file

def display_openai_api_key_input():
    """
    Display the input for the OpenAI API key.
    """
    st.sidebar.info("""
    Please enter your OpenAI API key securely.
    """)
    return st.sidebar.text_input("OpenAI API Key", type="password")

def clear_submit():
    """
    Clear the Submit Button State
    """
    st.session_state["submit"] = False
