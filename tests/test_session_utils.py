import pytest
from unittest import mock
from src.session_utils import init_session_state  # Adjust import path based on your structure

# Test session state initialization
@mock.patch("streamlit.session_state", new_callable=dict)
def test_session_initialization(mock_session_state):
    init_session_state()
    assert mock_session_state["authentication_status"] is None
    assert mock_session_state["assistant_started"] is False
    assert "messages" in mock_session_state

# Test session state with predefined variables
@mock.patch("streamlit.session_state", new_callable=dict)
def test_session_with_predefined(mock_session_state):
    mock_session_state["authentication_status"] = True
    init_session_state()
    assert mock_session_state["authentication_status"] == True
