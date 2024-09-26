import streamlit as st
import pandas as pd

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
            "technical_components": get_data_by_team(team, 'Components')
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
        }
        st.session_state.question_to_suggestions = question_to_suggestions
    return question_to_suggestions