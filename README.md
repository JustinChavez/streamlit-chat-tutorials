# streamlit-chat-tutorials

## Setup

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/).

2. Clone this repository.

3. Create a new virtual environment:

   ```bash
   $ python -m venv venv
   $ . venv/bin/activate
   ```

4. Navigate into the project directory + desired tutorial:

   ```bash
   $ cd streamlit-chat-tutorials/01_streamlit_chatgpt_frontend
   ```

5. Install the requirements:

   ```bash
   $ pip install -r requirements.txt
   ```

6. Make a copy of the example environment variables file:

   ```bash
   $ cp .env.example .env
   ```

7. Fill out the new environment variables file with your keys

8. `app.py` contains the code we built in the video. Feel free to clear the file and follow along. Run it with:
```
streamlit run app.py
```