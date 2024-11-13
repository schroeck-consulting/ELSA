#  _____      _                         _      _____ _____   _____                       _ _   _
# /  ___|    | |                       | |    |_   _|_   _| /  __ \                     | | | (_)
# \ `--.  ___| |__  _ __ ___   ___  ___| | __   | |   | |   | /  \/ ___  _ __  ___ _   _| | |_ _ _ __   __ _
#  `--. \/ __| '_ \| '__/ _ \ / _ \/ __| |/ /   | |   | |   | |    / _ \| '_ \/ __| | | | | __| | '_ \ / _` |
# /\__/ / (__| | | | | | (_) |  __/ (__|   <   _| |_  | |   | \__/\ (_) | | | \__ \ |_| | | |_| | | | | (_| |
# \____/ \___|_| |_|_|  \___/ \___|\___|_|\_\  \___/  \_/    \____/\___/|_| |_|___/\__,_|_|\__|_|_| |_|\__, |
#                                                                                                       __/ |
#                                                                                                      |___/

import pandas as pd
import streamlit as st

# teams_data = pd.read_csv("teams_data.csv", sep=";")
teams_data = pd.read_csv("updated_teams_and_collaborations_data.csv", sep=",")

# TODO: Pull context from a BLOB Storage


def get_data_by_team(team, column):
    """
    Returns the data for a given team and column.
    """
    row = teams_data.loc[teams_data['Team'] == team]
    return row[column].iloc[0].split(", ") if not row.empty else []


def get_prioritized_data(team_name, column_name):
    """
    For a given team, place the most used options at the top, followed by all other ones.
    """
    # Step 1: Get data for the team
    team_data = get_data_by_team(team_name, column_name)

    # Step 2: Get all unique options from dataset
    all_options = teams_data[column_name].str.split(
        ',').explode().str.strip().unique()

    # Step 3: Create the list of remaining options
    remaining_data = [d for d in all_options if d not in team_data]

    return team_data + remaining_data


def get_suggestions(question_id, team=None):
    """
    Gets suggestions based on the question ID
    """
    if team:
        question_map = {
            "teams_involved": get_prioritized_data(team,
                                                   "Collaborates With") + [
                                  "None"],
            "stakeholders": get_prioritized_data(team, "Stakeholders"),
            "technical_components": get_prioritized_data(team, "Components"),
        }
    else:
        question_map = {
            "team": teams_data['Team'].tolist(),
            "input_data": ["Yes", "No"],
            "output_data": ["Yes", "No"],
        }
    return question_map.get(question_id, [])


def generate_suggestions():
    """
    Generates suggestions for the current question based on the team name.
    """
    # If we already have all suggestions, return them
    if len(st.session_state.question_to_suggestions) > 1:
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
            st.session_state.questions_to_ask.insert(0, {
                "id": f"benefit_{stakeholder}", "question": question_benefit})
            st.session_state.questions_to_ask.insert(0, {
                "id": f"changes_{stakeholder}", "question": question_changes})

    elif question_id == "input_data":
        if st.session_state.input_data == "Yes":
            question_input = "**What new data and from which system is it needed**"
            st.session_state.questions_to_ask.insert(0, {
                "id": "input_data_details", "question": question_input})

    elif question_id == "output_data":
        if st.session_state.output_data == "Yes":
            question_output = "**What new data are you outputting and where is it being sent to**"
            st.session_state.questions_to_ask.insert(0, {
                "id": "output_data_details", "question": question_output})
