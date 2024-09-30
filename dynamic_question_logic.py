import streamlit as st
import pandas as pd
from icecream import ic

teams_data = pd.read_csv("teams_data.csv", sep=";")


def get_data_by_team(team, column):
    """
    Returns the data for a given team and column.
    """
    row = teams_data.loc[teams_data['Team'] == team]
    return row[column].iloc[0].split(", ") if not row.empty else []


def get_suggestions(question_id, team=None):
    """
    Gets suggestions based on the question ID
    """
    if question_id == "team":
        return teams_data['Team'].tolist()
    
    if team:
        return {
            "teams_involved": get_data_by_team(team, 'Collaborates With')+["None"],
            "stakeholders": get_data_by_team(team, 'Stakeholders'),
            "technical_components": get_data_by_team(team, 'Components'),
            "input_data": ["Yes", "No"],
            "output_data": ["Yes", "No"],
        }.get(question_id, [])
    
    return []


def generate_suggestions():
    """
    Generates suggestions for the current question based on the team name.
    """
    if st.session_state.question_to_suggestions != {}:
        return st.session_state.question_to_suggestions
    
    team = st.session_state.team_name
    if team == None:
        question_to_suggestions = {
            "team": {
                "suggestions": get_suggestions("team"),
                "multiple_choice": False
            }
        }
    else:
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
            "input_data": {
                "suggestions": get_suggestions("input_data"),
                "multiple_choice": False
            },
            "output_data": {
                "suggestions": get_suggestions("output_data"),
                "multiple_choice": False
            }
        }
        st.session_state.question_to_suggestions = question_to_suggestions
    return question_to_suggestions


def add_follow_up_questions(question_id):
    """
    Adds follow-up questions based on the user's response.
    """
    if question_id == "stakeholders":
        for stakeholder in st.session_state.stakeholders:
            question_benefit = f"**What is the benefit to {stakeholder}?**"
            question_changes = f"**What changes for {stakeholder}?**"
            st.session_state.questions_to_ask.insert(0, {"id": f"benefit_{stakeholder}", "question": question_benefit})
            st.session_state.questions_to_ask.insert(0, {"id": f"changes_{stakeholder}", "question": question_changes})

    elif question_id == "input_data":
        if st.session_state.input_data == "Yes":
            question_input = "**What new data and from which system is it needed**"
            st.session_state.questions_to_ask.insert(0, {"id": "input_data_details", "question": question_input})
    
    elif question_id == "output_data":
        if st.session_state.output_data == "Yes":
            question_output = "**What new data are you outputting and where is it being sent to**"
            st.session_state.questions_to_ask.insert(0, {"id": "output_data_details", "question": question_output})