import streamlit as st
import base64
from Yatra2Chandigarh import ask_setup

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
        unsafe_allow_html=True
    )
def ask(query, qa, chat_history=None):
    # Get response
    result = qa({"query": query, "chat_history": chat_history})
    #chat_history.extend([query, result["result"]])  # Append the response to chat history
    return result["result"]

def main():
    st.image("chandigarh_data/chandigarh_hand_symbol.jpg", width=300)
    st.title("Welcome to Chandigarh! Traveller, how can I help you today?")
    chat_history = []  # Initialize chat history
    qa=ask_setup()
    # Input box for user query
    user_query = st.text_input("You:", "")

    # Button to submit query
    if st.button("Ask"):
        response = ask(user_query,qa,chat_history)
        st.text_area("MaQuery:", value=response, height=200)
        chat_history.extend([(user_query, response)])

if __name__ == "__main__":
    add_bg_from_local('chandigarh_data/chandi_bg.png')  # Add background image
    main()
