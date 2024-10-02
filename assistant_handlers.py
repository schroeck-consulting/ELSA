import streamlit as st
import time
import re
from icecream import ic
from utils import display_message, display_typing_effect
from dynamic_question_logic import generate_suggestions, add_follow_up_questions



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
    if questions_to_ask:=st.session_state.questions_to_ask:
        question_id = questions_to_ask[0]["id"]
        question = questions_to_ask[0]["question"]

        # Replace placeholders in the question with the team name
        if question_id == "teams_involved":
            question = question.format(team=st.session_state.team_name)
        
        # Display the assistant message with the predefined question
        if not any(message["content"] == question for message in st.session_state.messages):
            st.session_state.messages.append({"role": "assistant", "content": question})
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
            st.session_state.messages.append({"role": "user", "content": user_answer})

            display_message("user", user_answer)
            add_follow_up_questions(question_id)

            # Wait for a short time before asking the next question
            time.sleep(0.5)
            st.rerun()
    else:
        # All predefined questions have been answered, generate the query
        initial_query = project_details_query(st.session_state.questions_asked, st.session_state.user_responses)
        handle_assistant_response(initial_query)
        st.session_state.assistant_started = True
        st.rerun()


# def split_epic_text(epic_text):
#     """
#     Splits the generated epic into three parts:
#     - start: Everything before EPIC_START
#     - epic: Everything between EPIC_START and EPIC_END
#     - end: Everything after EPIC_END
#     """
#     # Split the text at EPIC_START
#     parts = re.split(r"EPIC_START", epic_text, maxsplit=1)
#     start = parts[0].strip() if len(parts) > 0 else ""
    
#     # Further split at EPIC_END to extract the epic and end parts
#     if len(parts) > 1:
#         epic_parts = re.split(r"EPIC_END", parts[1], maxsplit=1)
#         epic = epic_parts[0].strip() if len(epic_parts) > 0 else ""
#         end = epic_parts[1].strip() if len(epic_parts) > 1 else ""
#     else:
#         epic = ""
#         end = ""

#     return start, epic, end


# def display_generated_epic(user_response):
#     """
#     Displays the generated epic and allows the user to modify it.
#     """
#     start_text, epic_text, end_text = split_epic_text(user_response)
    
#     # Display the epic in the text area for modification
#     display_typing_effect(start_text)
#     modified_epic = st.text_area("Modify the epic if needed:", value=epic_text, height=500)
#     display_typing_effect(end_text)
    
#     # If user submits the modified epic, display a confirmation message
#     if st.button("Submit", key="submit_epic"):
#         content = "Here is the modified epic:\n\n" + modified_epic + "\n\nAre you happy with it?" # if yes, store it and send to Jira
#         st.markdown(content)
#         st.session_state.modified_epic = modified_epic


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

        display_typing_effect(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

        # if "EPIC_START" in response:
        #     display_generated_epic(response)
        #     if st.session_state.modified_epic != "":
        #         content = "Here is the modified epic:\n\n" + st.session_state.modified_epic + "\n\nAre you happy with it?"
        #         st.markdown(content)
        #         st.session_state.messages.append({"role": "assistant", "content": content})
        # else:
        #     display_typing_effect(response)
        #     st.session_state.messages.append({"role": "assistant", "content": response})


def handle_user_queries():
    """
    Handles user input and communication after assistant interaction has started.
    """
    if user_query := st.chat_input("Message"):
        st.session_state.messages.append({"role": "user", "content": user_query})
        display_message("user", user_query)
        
        handle_assistant_response(user_query)


def handle_custom_input(selected_suggestions):
    """
    Handles the custom input logic when 'Add another option...' is selected.
    """
    if "Add another option..." in selected_suggestions:
        custom_input = st.text_input("Enter your other option...")
        if custom_input:
            selected_suggestions.remove("Add another option...")
            selected_suggestions.append(custom_input)
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
                selected_suggestions = st.multiselect("Select from suggestions:", suggestions, label_visibility="collapsed")
                
                # If "None" is selected, remove all other options
                if "None" in selected_suggestions:
                    selected_suggestions = ["None"]

                # Create text input for user entry
                selected_suggestions = handle_custom_input(selected_suggestions)

            else:
                if suggestions != ["Yes", "No"]:
                    suggestions = suggestions + ["Add another option..."]
                selected_suggestions = [st.selectbox("Select option", suggestions, label_visibility="collapsed")]

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
        