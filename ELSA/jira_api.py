import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import json


JIRA_DOMAIN = st.secrets.get("JIRA_DOMAIN")
EMAIL = st.secrets.get("JIRA_EMAIL")
API_TOKEN = st.secrets.get("JIRA_API_TOKEN")
PROJECT_KEY = st.secrets.get("PROJECT_KEY")

def post_epic_to_jira(epic_title, epic_description):
    '''
    Posts an epic to Jira using the Jira API.
    '''
    api_endpoint = f"{JIRA_DOMAIN}/rest/api/2/issue"
    auth = HTTPBasicAuth(EMAIL, API_TOKEN)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "fields": {
            "project": {
                "key": PROJECT_KEY
            },
            "summary": epic_title,
            "description": epic_description,
            "issuetype": {
                "name": "Epic"
            },
        }
    })

    # Send the request
    response = requests.request(
        method="POST",
        url=api_endpoint,
        auth=auth,
        headers=headers,
        data=payload
    )
    return response
