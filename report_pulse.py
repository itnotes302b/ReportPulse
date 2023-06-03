import streamlit as st
from pathlib import Path
from streamlit_chat import message
from llama_index_utils import ReportPulseAssistent
import os
import json

st.set_page_config(
    page_title="Report Pulse",
    page_icon="favicon.ico",
)

path = os.path.dirname(__file__)

# Load translations from JSON file
with open(path+"/Assets/translations.json") as f:
    transl = json.load(f)

# Trick to preserve the state of your widgets across pages
for k, v in st.session_state.items():
    st.session_state[k] = v 
##

os.environ["OPENAI_API_KEY"] = st.secrets["openai_api_key"]


st.title('Report pulse ChatBot')

file_uploaded = st.file_uploader(label="Upload your report here")

styl = f"""
<style>
    .stTextInput {{
      position: fixed;
      bottom: 3rem;
      z-index: 2;
    }}
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.css-1y4p8pa {{
        display: flex !important;
        float:left;
        overflow-y: auto;
        flex-direction: column-reverse;
    }}
</style>
"""
st.markdown(styl, unsafe_allow_html=True)


# Add the language selection dropdown    
if 'lang_tmp' not in st.session_state:
    st.session_state['lang_tmp'] = 'English'

if 'lang_changed' not in st.session_state:
    st.session_state['lang_changed'] = False

if 'lang_select' in st.session_state:
    #st.sidebar.markdown("<h3 style='text-align: center; color: black;'>{}</h3>".format(transl[st.session_state['lang_select']]["language_selection"]), unsafe_allow_html=True)
    lang = st.sidebar.selectbox(transl[st.session_state['lang_select']]["language_selection"], options=list(transl.keys()), key='lang_select')
else:
    #st.sidebar.markdown("<h3 style='text-align: center; color: black;'>{}</h3>".format(transl[st.session_state['lang_tmp']]["language_selection"]), unsafe_allow_html=True)
    lang = st.sidebar.selectbox(transl[st.session_state['lang_tmp']]["language_selection"], options=list(transl.keys()), key='lang_select')

if lang != st.session_state['lang_tmp']:
    st.session_state['lang_tmp'] = lang
    st.session_state['lang_changed'] = True
else:
    st.session_state['lang_changed'] = False

st.title(transl[lang]["title"])

file_uploaded = st.file_uploader(label=transl[lang]["title"])

styl = f"""
<style>
    .stTextInput {{
      position: fixed;
      bottom: 3rem;
    }}
</style>
"""
st.markdown(styl, unsafe_allow_html=True)

if file_uploaded is not None:
    def display_messages():
        
        for i, (msg, is_user) in enumerate(st.session_state["messages"]):
            #message( msg, is_user=is_user, key=str(i), allow_html = True )
            message( msg, is_user=is_user, key=str(i), allow_html = True )
        st.session_state["thinking_spinner"] = st.empty()
    
    def process_input():
        if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
            user_text = st.session_state["user_input"].strip()
            with st.session_state["thinking_spinner"], st.spinner(f"Thinking"):
                agent_text = generate_response(user_text)

            st.session_state["messages"].append((user_text, True))
            st.session_state["messages"].append((agent_text, False))
            
    # Storing the chat
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    def showmessage(output):
        st.session_state["messages"].append((output, False))

    def upload_file(uploadedFile):
        
        # Save uploaded file to 'content' folder.
        save_folder = '/app/reportsData/'
        save_path = Path(save_folder, uploadedFile.name)
        
        with open(save_path, mode='wb') as w:
            w.write(uploadedFile.getvalue())

        if save_path.exists():
            st.success(f'File {uploadedFile.name} is successfully saved!')
        
        return ReportPulseAssistent(save_folder)
        
    reportPulseAgent = upload_file(file_uploaded)    
    r_response = reportPulseAgent.get_next_message().response
    st.sidebar.markdown(r_response)
    

    def generate_response(user_query):
        response = reportPulseAgent.get_next_message(user_query)
        return response.response

    # We will get the user's input by calling the get_text function

    st.text_input(transl[lang]['ask_question'],key="user_input", on_change=process_input)
    display_messages()