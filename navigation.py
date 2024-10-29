import streamlit as st
import pages as pg
from streamlit_navigation_bar import st_navbar

st.set_page_config(initial_sidebar_state="collapsed")

pages = ["Epics", "User Stories", "Settings"]
logo_path = "images/Dominik_Schroeck_Logo_RGB_Schwarz.svg"

styles = {
    "nav": {
        "background-color": "  #25abef",
        "display": "flex",
        "align-items": "center",
        "justify-content": "center",  # Center the pages
        "position": "relative",
        "height": "60px",  # You can adjust the height if necessary
    },
    "img": {
        "padding-right": "14px",
        "position": "absolute",
        "left": "0",  # Position the logo on the left-most side
        "top": "50%",  # Move the logo to the middle of the nav bar
        "transform": "translateY(-50%)",  # Center it vertically
        "padding-left": "10px",
        "height": "40px",  # Adjust the logo height to fit in the navbar
    },
    "span": {
        "border-radius": "0.5rem",
        # "color": "rgb(49, 51, 63)",
        "color": "white",
        "margin": "0 0.125rem",
        "padding": "0.4375rem 0.625rem",
    },
    # "active": {
    #     "background-color": "rgba(255, 255, 255, 0.25)",
    # },
    "hover": {
        "background-color": "rgba(255, 255, 255, 0.35)",
    },
}
options = {
    "show_menu": True,
    "show_sidebar": True,
}
page = st_navbar(
    pages,
    logo_path=logo_path,
    styles=styles,
    options=options,
)


if page == "Epics":
    pg.epics()
elif page == "User Stories":
    st.write("User Stories")
elif page == "Settings":
    st.write("Settings")