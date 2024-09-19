# Epic Builder Copilot

Epic Builder Copilot is a Streamlit-based application that leverages OpenAI's GPT-4 model to assist users in generating and managing epic stories for their projects.

## Prerequisites

- Python 3.8 or higher
- Streamlit
- OpenAI API Key
- `.env` file with the following variables:
  - `ASSISTANT_ID`
  - `OPENAI_API_KEY`

## Installation

1. Clone the repository:
```sh
git clone https://github.com/yourusername/epic-builder-copilot.git
cd epic-builder-copilot
```

2. Create and activate a virtual environment:
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```


3. Install the required packages:
```sh
pip install -r requirements.txt
```

4. Create a .env file in the root directory and add your OpenAI API key and Assistant ID:
```sh
ASSISTANT_ID=your_assistant_id
OPENAI_API_KEY=your_openai_api_key
```

## Usage
1. Run the Streamlit application:
```sh
streamlit run main.py
```
2. Open your web browser and navigate to http://localhost:8501.
3. Interact with the AI assistant by typing your queries in the chat input box.

## Features
- **Interactive Chat Interface:** Communicate with the AI assistant in real-time.
- **Epic Story Generation:** Get suggestions for epic stories based on your input.
- **Session Management:** Maintains the state of the conversation across multiple interactions.