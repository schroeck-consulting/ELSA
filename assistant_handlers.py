import streamlit as st
import time
from utils import display_typing_effect
from dynamic_question_logic import get_suggestions

team="QA Team"####зберігаємо команду з першої відповіді

question_to_suggestions = {
    "team": {
        "suggestions": get_suggestions("team"),
        "multiple_choice": False
    },
    "teams_involved": {
        "suggestions": get_suggestions("teams_involved", team),
        "multiple_choice": True
    },
    "stakeholders": {
        "suggestions": get_suggestions("stakeholders", team),
        "multiple_choice": True
    },
    "technical_components": {
        "suggestions": get_suggestions("technical_components", team),
        "multiple_choice": True
    },
}


def display_message(role, content):
    """
    Utility function to display a chat message.
    """
    with st.chat_message(role):
        if role == "user":
            st.markdown(content)
        elif role == "assistant":
            # st.markdown(content)
            display_typing_effect(content)


def project_details_query(questions, answers):
    """
    Formats the predefined questions and answers into a query for the OpenAI assistant.
    """
    query = "Here is the most important information about epic:\n\n"
    for i, (question, answer) in enumerate(zip(questions, answers), start=1):
        query += f"{i}. **{question}**\n"
        query += f"   - Answer: {answer}\n\n"
    
    query += "Now, based on the above details, help me generate an epic for this project.\n"
    query += "Please also ask for any clarifications or missing information if needed."
    # print(query)
    return query


def handle_predefined_questions(predefined_questions):
    """
    Handles asking predefined questions and collecting responses.
    """
    if st.session_state.current_question_index < len(predefined_questions):
        question_id = predefined_questions[st.session_state.current_question_index]["id"]
        question = predefined_questions[st.session_state.current_question_index]["question"]
        
        # Display the assistant message with the predefined question
        if not any(message["content"] == question for message in st.session_state.messages):
            st.session_state.messages.append({"role": "assistant", "content": question})
            display_message("assistant", question)
        
        # Check if clickable suggestions need to be provided
        if question_id in question_to_suggestions:
            st.chat_input(disabled=True)
            user_answer = display_clickable_suggestions(question_id)
        else:
            user_answer = st.chat_input("Message")

        # If user has answered, store the response and display it
        if user_answer:
            st.session_state.predefined_responses.append(user_answer)
            st.session_state.messages.append({"role": "user", "content": user_answer})
            st.session_state.current_question_index += 1
            display_message("user", user_answer)

            # Wait for a short time before asking the next question
            time.sleep(0.5)
            st.rerun()
    else:
        # All predefined questions have been answered, generate the query
        initial_query = project_details_query(predefined_questions, st.session_state.predefined_responses)
        handle_assistant_response(initial_query)
        st.session_state.assistant_started = True
        st.rerun()
        

def handle_assistant_response(query):
    """
    Handles interaction with the assistant, submitting a query and displaying the response.
    """
    assistant_client = st.session_state.assistant_client
    thread_id = st.session_state.thread_id
    
    with st.chat_message("assistant"):
        with st.spinner(''):
            run = assistant_client.submit_message(thread_id, query)
            run = assistant_client.wait_on_run(run, thread_id)
            response_messages = assistant_client.get_response_messages(thread_id)
            response = assistant_client.extract_assistant_response(response_messages)
        # display_typing_effect(response)
        st.session_state.messages.append({"role": "assistant", "content": response})


def handle_user_queries():
    """
    Handles user input and communication after assistant interaction has started.
    """
    if user_query := st.chat_input("Message"):
        st.session_state.messages.append({"role": "user", "content": user_query})
        display_message("user", user_query)
        
        handle_assistant_response(user_query)



def display_clickable_suggestions(question_id):
    """
    Displays the assistant message with a box of suggestions to choose from
    """
    config = question_to_suggestions.get(question_id, {})
    suggestions = config.get("suggestions", [])
    multiple_choice = config.get("multiple_choice", False)
    selected_suggestions = []
    
    col1, col2, col3 = st.columns([1, 11, 2])

    with col2:
        if suggestions:
            if multiple_choice:
                options = suggestions + ["Add another option..."]
                selected_suggestions = st.multiselect("Select from suggestions:", options, label_visibility="collapsed")

                # Create text input for user entry
                if "Add another option..." in selected_suggestions:
                    custom_input = st.text_input("Enter your other option...")
                    if custom_input:
                        selected_suggestions.remove("Add another option...")
                        selected_suggestions.append(custom_input)
            
            else:
                options = suggestions + ["Another option..."]
                selected_suggestions = [st.selectbox("Select option", options=options, label_visibility="collapsed")]

                # Create text input for user entry
                if selected_suggestions == ["Another option..."]: 
                    selected_suggestions = [st.text_input("Enter your other option...")]
    
        
    with col3:
        if st.button("Submit"):
            if selected_suggestions:
                # Store the user's selected teams and add them to the session messages
                user_response = ", ".join(selected_suggestions)
                st.session_state.predefined_responses.append(user_response)
                st.session_state.messages.append({"role": "user", "content": user_response})

                # Move to the next question or action
                st.session_state.current_question_index += 1
                time.sleep(0.5)
                st.rerun()
            else:
                st.warning("Please select at least one team.")