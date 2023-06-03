import streamlit as st
from pathlib import Path
from streamlit_chat import message
import os

os.environ["OPENAI_API_KEY"] = "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"

st.title('Report pulse ChatBot')

file_uploaded = st.file_uploader(label="Upload your report here")

if file_uploaded is not None:
    #def upload_file(uploadedFile):
        # Save uploaded file to 'content' folder.
        #save_folder = 'content'
        #save_path = Path(save_folder, uploadedFile.name)
        #with open(save_path, mode='wb') as w:
        #    w.write(uploadedFile.getvalue())

        #if save_path.exists():
        #    st.success(f'File {uploadedFile.name} is successfully saved!')
            
    #upload_file(file_uploaded)
    
    # Create an index using the loaded documents
    #index_creator = VectorstoreIndexCreator()
    #docsearch = index_creator.from_loaders([loader])

    # Create a question-answering chain using the index
    #chain = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.vectorstore.as_retriever(), input_key="question")

    #Creating the chatbot interface
    st.title("Chat wtih your Reports")

    # Storing the chat
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    def generate_response(user_query):
        response =  {'result': "Hello" } #chain({"question": user_query})
        return response['result']
    
    
    # We will get the user's input by calling the get_text function
    def get_text():
        input_text = st.text_input("You: ","Ask Question From your Document?", key="input")
        return input_text
    user_input = get_text()

    if user_input:
        output = generate_response(user_input)
        # store the output 
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)
    
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')