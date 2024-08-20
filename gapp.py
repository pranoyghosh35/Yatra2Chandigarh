import streamlit as st
from frontend.app_st_ui import setup_ui, display_openai_api_key_input
from backend.qa_setup import ask_setup  # Import the function to initialize the agent
from backend.google_system import get_system_info  # Import the system information fetching logic

# Get the API key from user input
api_key = display_openai_api_key_input()




# Get the system information
system_info = get_system_info()

# Determine the greeting based on the current time
current_hour = int(system_info["current_time"].split(":")[0])

#Morning: 12:00 AM to 11:59 AM
#Noon: 12:00 PM
#Afternoon: 12:01 PM to 5:59 PM
#Evening: 6:00 PM to 8:59 PM
#Night: 9:00 PM to 11:59 PM


if "AM" in system_info["current_time"]:
    if current_hour < 12:
        greeting = "Good morning 🌅"
else:  # PM times
    if current_hour < 6:
        greeting = "Good afternoon 🌞"
    elif current_hour < 9:
        greeting = "Good evening 🌇"
    elif current_hour == 12:
        greeting = "Good noon ☀️"
    else:
        greeting = "Good night 🌙"

# Show the information in a textbox with a greeting
with st.sidebar:  # Positioning on the right side
    st.text_area(
        label="🔍 Websearched the latest information...",
        value=(
            f"{greeting}! \n\n"
            f"📅 {system_info['date']}\n"
            f"🕒 {system_info['current_time']}\n"
            f"☁️ {system_info['weather']}\n"
            f"🌡️ Season: {system_info['season']}\n"
            "\n... Also may edit your notes here ...\n"
        ),
        height=200,
    )
    
# Set up the UI
setup_ui()

# Initialize chat history and agent if API key is provided
if api_key:
    # Initialize the LangChain agent with the API key
    agent = ask_setup(api_key)  # Pass the API key to setup the agent

    # Set a default model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o-mini"

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Add system message if not already present
    if not any(msg["role"] == "system" for msg in st.session_state.messages):
        # Fetch system information like date, time, weather, etc.
        #system_info = get_system_info()
        
        # Construct the system message with dynamic context
        system_message = (
            f"Date: {system_info['date']}\n"
            f"Month: {system_info['month']}\n"
            f"Current Time: {system_info['current_time']}\n"
            f"Current Weather: {system_info['weather']}\n"
            f"Weather upto 6 hrs before and later and details: {system_info['weather_details']}\n"
            f"Season: {system_info['season']}\n"
            """You are virtual travel guide to city beautiful Chandigarh. you may help plan itinerary but ask user about preferences. While planning itinerary "let's think step by step" suggest places which is inaccessible that day for weather or hour or out of budget to try another day.
            You should be polite, avoid giving wrong information if not confident, and should not be biased.
            Politely decline any offensive queries and all queries not related to Chandigarh 
            (including math or reasoning question or puzzle) You should search the internet only if provided context from vector database don't answer the query\n"""
        )

        # Insert the system message into chat history
        st.session_state.messages.insert(0, {"role": "system", "content": system_message})

    # Display chat messages from history on app rerun, skipping the system message
    for message in st.session_state.messages:
        if message["role"] != "system":  # Skip displaying the system message
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input(f"{greeting}!  How can I help you today?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Construct a context-aware prompt including the system message
        context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
        context_prompt = f"{context}\nuser: {prompt}\nassistant:"
        
        # Query the LangChain agent for a response
        response = agent.run(context_prompt)
        
        # Add assistant's response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Display user message and bot response
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            st.markdown(response)

else:
    # If no API key is provided, prompt the user
    st.write("Please enter your OpenAI API key on the left to proceed.")
