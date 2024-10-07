import yaml
import streamlit_authenticator as stauth
import streamlit as st
from yaml.loader import SafeLoader
from streamlit import session_state as ss

CONFIG_FILENAME = 'config.yaml'

def authenticate():
    """
    Handles the authentication using streamlit-authenticate.
    """
    # Load the configuration from the YAML file
    with open(CONFIG_FILENAME) as file:
        config = yaml.load(file, Loader=SafeLoader)

    # Initialize the authenticator with credentials and cookie settings
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
    )

    # Display the login form and manage authentication status
    authenticator.login()

    # Handle error messages
    if ss["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif ss["authentication_status"] is None:
        st.warning('Please enter your username and password')

    # Save the hashed passwords back to the config file (if needed)
    with open(CONFIG_FILENAME, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

