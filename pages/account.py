import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import streamlit as st
from streamlit import session_state as ss

CONFIG_FILENAME = 'config.yaml'

with open(CONFIG_FILENAME) as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

login_tab, register_tab, account_tab = st.tabs(['Login', 'Register', "Account"])

# Display the login form
with login_tab:
    authenticator.login()

    if ss["authentication_status"]:
        st.write(f'Welcome *{ss["name"]}*')
        authenticator.logout()

    elif ss["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif ss["authentication_status"] is None:
        st.warning('Please enter your username and password')

    # Display the forgot password form
    if not ss["authentication_status"]:
        try:
            username_of_forgotten_password, \
            email_of_forgotten_password, \
            new_random_password = authenticator.forgot_password()
            if username_of_forgotten_password:
                st.success('New password to be sent securely')
                # The developer should securely transfer the new password to the user.
            elif username_of_forgotten_password == False:
                st.error('Username not found')
        except Exception as e:
            st.error(e)
        
    # Display the forgot username form
    try:
        username_of_forgotten_username, \
        email_of_forgotten_username = authenticator.forgot_username()
        if username_of_forgotten_username:
            st.success('Username to be sent securely')
            # The developer should securely transfer the username to the user.
        elif username_of_forgotten_username == False:
            st.error('Email not found')
    except Exception as e:
        st.error(e)

# Display the register form
with register_tab:
    if not ss["authentication_status"]:
        try:
            email_of_registered_user, \
            username_of_registered_user, \
            name_of_registered_user = authenticator.register_user(captcha=False)#pre_authorized=config['pre-authorized'])
            if email_of_registered_user:
                st.success('User registered successfully')
        except Exception as e:
            st.error(e)

# Display the account form
with account_tab:
    if st.session_state['authentication_status']:
        try:
            if authenticator.reset_password(st.session_state['username']):
                st.success('Password modified successfully')
        except Exception as e:
            st.error(e)

# Save the hashed passwords back to the config file
with open(CONFIG_FILENAME, 'w') as file:
    yaml.dump(config, file, default_flow_style=False)

    
    