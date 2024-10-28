#  _____      _                         _      _____ _____   _____                       _ _   _
# /  ___|    | |                       | |    |_   _|_   _| /  __ \                     | | | (_)
# \ `--.  ___| |__  _ __ ___   ___  ___| | __   | |   | |   | /  \/ ___  _ __  ___ _   _| | |_ _ _ __   __ _
#  `--. \/ __| '_ \| '__/ _ \ / _ \/ __| |/ /   | |   | |   | |    / _ \| '_ \/ __| | | | | __| | '_ \ / _` |
# /\__/ / (__| | | | | | (_) |  __/ (__|   <   _| |_  | |   | \__/\ (_) | | | \__ \ |_| | | |_| | | | | (_| |
# \____/ \___|_| |_|_|  \___/ \___|\___|_|\_\  \___/  \_/    \____/\___/|_| |_|___/\__,_|_|\__|_|_| |_|\__, |
#                                                                                                       __/ |
#                                                                                                      |___/

import time

import streamlit as st

from .dynamic_question_logic import generate_suggestions, \
    add_follow_up_questions
from .utils import display_message, display_typing_effect


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

    return query


def handle_predefined_questions():
    """
    Handles asking predefined questions and collecting responses.
    """
    if questions_to_ask := st.session_state.questions_to_ask:
        question_id = questions_to_ask[0]["id"]
        question = questions_to_ask[0]["question"]

        # Replace placeholders in the question with the team name
        if question_id == "teams_involved":
            question = question.format(team=st.session_state.team_name)

        # Display the assistant message with the predefined question
        if not any(message["content"] == question for message in
                   st.session_state.messages):
            st.session_state.messages.append(
                {"role": "assistant", "content": question})
            display_message("assistant", question)

        # Check if clickable suggestions need to be provided
        if question_id in generate_suggestions():
            st.chat_input(disabled=True)
            user_answer = display_clickable_suggestions(question_id)
        else:
            user_answer = st.chat_input("Message")

        # If user has answered, store the response and display it
        if user_answer:
            st.session_state.questions_to_ask.pop(0)
            st.session_state.questions_asked.append(question)
            st.session_state.user_responses.append(user_answer)
            st.session_state.messages.append(
                {"role": "user", "content": user_answer})

            display_message("user", user_answer)
            add_follow_up_questions(question_id)

            # Wait for a short time before asking the next question
            time.sleep(0.5)
            st.rerun()
    else:
        # All predefined questions have been answered, generate the query
        initial_query = project_details_query(st.session_state.questions_asked,
                                              st.session_state.user_responses)
        handle_assistant_response_streaming(initial_query)
        st.session_state.assistant_started = True
        st.rerun()

# this functiion is not used now
def handle_assistant_response(query):
    """
    Handles interaction with the assistant, submitting a query and displaying the response.
    No streaming is used, so the response is displayed after the assistant has finished processing.
    """
    assistant_client = st.session_state.assistant_client
    thread_id = st.session_state.thread_id

    with st.chat_message("assistant"):
        with st.spinner(''):
            run = assistant_client.submit_message(thread_id, query)
            run = assistant_client.wait_on_run(run, thread_id)
            response_messages = assistant_client.get_response_messages(
                thread_id)
            response = assistant_client.extract_assistant_response(
                response_messages)

        display_typing_effect(response)
        st.session_state.messages.append(
            {"role": "assistant", "content": response})

def handle_assistant_response_streaming(query):
    '''
    Handles interaction with the assistant, submitting a query and displaying the response.
    Uses streaming to receive the response in real-time.
    '''
    assistant_client = st.session_state.assistant_client
    thread_id = st.session_state.thread_id
    assistant_client.add_query_to_thread(thread_id, query)

    with st.chat_message("assistant"):
        assistant_reply = assistant_client.stream_assistant_response(thread_id)

        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_reply})

def handle_user_queries():
    """
    Handles user input and communication after assistant interaction has started.
    """
    if user_query := st.chat_input("Message"):
        st.session_state.messages.append(
            {"role": "user", "content": user_query})
        display_message("user", user_query)

        handle_assistant_response_streaming(user_query)


def handle_custom_input(selected_suggestions):
    """
    Handles the custom input logic when 'Add another option...' is selected.
    Multiple options can be entered by the user separated by commas.
    """
    if "Add another option..." in selected_suggestions:
        custom_input = st.text_input("Enter your other option(s)...")
        if custom_input:
            custom_options = [option.strip() for option in
                              custom_input.split(',')]
            selected_suggestions.remove("Add another option...")
            selected_suggestions.extend(custom_options)
    return selected_suggestions


def display_clickable_suggestions(question_id):
    """
    Displays the assistant message with a box of suggestions to choose from
    """
    # Get suggestions based on the question ID
    config = generate_suggestions().get(question_id, {})
    suggestions = config.get("suggestions", [])
    multiple_choice = config.get("multiple_choice")
    selected_suggestions = []

    # Display suggestions and collect user input
    col1, col2, col3 = st.columns([1, 11, 2])
    with col2:
        if suggestions:
            if multiple_choice:
                suggestions = suggestions + ["Add another option..."]
                selected_suggestions = st.multiselect(
                    "Select from suggestions:", suggestions,
                    label_visibility="collapsed")

                # If "None" is selected, remove all other options
                if "None" in selected_suggestions:
                    selected_suggestions = ["None"]

                # Create text input for user entry
                selected_suggestions = handle_custom_input(selected_suggestions)

            else:
                if suggestions != ["Yes", "No"]:
                    suggestions = suggestions + ["Add another option..."]
                selected_suggestions = [
                    st.selectbox("Select option", suggestions,
                                 label_visibility="collapsed")]

                # Create text input for user entry
                selected_suggestions = handle_custom_input(selected_suggestions)

    with col3:
        if st.button("Submit", key=f"{question_id}_submit"):
            # Store Team Name and Stakeholders for future use
            if question_id == "team":
                st.session_state.team_name = ", ".join(selected_suggestions)
            elif question_id == "stakeholders":
                st.session_state.stakeholders = selected_suggestions
            elif question_id == "input_data":
                st.session_state.input_data = ", ".join(selected_suggestions)
            elif question_id == "output_data":
                st.session_state.output_data = ", ".join(selected_suggestions)

            return ", ".join(selected_suggestions)
