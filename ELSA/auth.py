#  _____      _                         _      _____ _____   _____                       _ _   _
# /  ___|    | |                       | |    |_   _|_   _| /  __ \                     | | | (_)
# \ `--.  ___| |__  _ __ ___   ___  ___| | __   | |   | |   | /  \/ ___  _ __  ___ _   _| | |_ _ _ __   __ _
#  `--. \/ __| '_ \| '__/ _ \ / _ \/ __| |/ /   | |   | |   | |    / _ \| '_ \/ __| | | | | __| | '_ \ / _` |
# /\__/ / (__| | | | | | (_) |  __/ (__|   <   _| |_  | |   | \__/\ (_) | | | \__ \ |_| | | |_| | | | | (_| |
# \____/ \___|_| |_|_|  \___/ \___|\___|_|\_\  \___/  \_/    \____/\___/|_| |_|___/\__,_|_|\__|_|_| |_|\__, |
#                                                                                                       __/ |
#                                                                                                      |___/

import streamlit as st
import streamlit_authenticator as stauth
from streamlit import session_state as ss


def authenticate():
    """
    Handles the authentication using streamlit-authenticate.
    """

    def convert_secrets_to_strings(secrets):
        converted_dict = {}
        for key, value in secrets.items():
            if isinstance(value, dict):
                # Wenn der Wert ein weiteres Dictionary ist, rekursiv aufrufen
                converted_dict[key] = convert_secrets_to_strings(value)
            else:
                # Ansonsten den Wert in einen String umwandeln
                converted_dict[key] = str(value)
        return converted_dict

    secrets = convert_secrets_to_strings(st.secrets)

    # Initialize the authenticator with credentials and cookie settings
    authenticator = stauth.Authenticate(
        secrets['credentials'],
        st.secrets['cookie']['name'],
        st.secrets['cookie']['key'],
        st.secrets['cookie']['expiry_days'],
    )

    # Display the login form and manage authentication status
    authenticator.login()

    # Handle error messages
    if ss["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif ss["authentication_status"] is None:
        st.warning('Please enter your username and password')
