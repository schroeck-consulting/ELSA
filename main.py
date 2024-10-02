import streamlit as st
from assistant_handlers import handle_predefined_questions, handle_user_queries
from session_utils import init_session_state, init_assistant_client

def display_logo():
    # To make logo bigger
    st.html("""
    <style>
        [alt=Logo] {
        height: 3rem;
        }
    </style>
        """)
    
    # Display the logo at the sidebar
    LOGO = "images/Dominik_Schroeck_Logo_RGB_Schwarz.svg"
    st.logo(LOGO, icon_image=LOGO)
    st.sidebar.markdown("")


def main():
    init_session_state()
    init_assistant_client()
    
    display_logo()    
    
    # Display the title
    st.title("ELSA - Epic Lifecycle Support Assistant")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Handle predefined questions or chat input based on interaction state
    if not st.session_state.assistant_started:
        handle_predefined_questions()
    else:
        handle_user_queries()

if __name__ == "__main__":
    main()
