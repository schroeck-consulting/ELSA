import pandas as pd

teams_data = pd.read_csv("teams_data.csv", sep=";")

# Utility function to get data by team and column
def get_data_by_team(team, column):
    row = teams_data.loc[teams_data['Team'] == team]
    return row[column].iloc[0].split(", ") if not row.empty else []

# Main function to get suggestions based on the question ID
def get_suggestions(question_id, team=None):
    if question_id == "team":
        return teams_data['Team'].tolist()
    
    if team:
        return {
            "teams_involved": get_data_by_team(team, 'Collaborates With')+["None"],
            "stakeholders": get_data_by_team(team, 'Stakeholders'),
            "technical_components": get_data_by_team(team, 'Components')
        }.get(question_id, [])
    
    return []