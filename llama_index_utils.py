import os
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
from prompts import SUMMARY_PROMPT

class ReportPulseAssistent:

    def __init__(self, data_dir) -> None:
        # on initialization 
        self.documents = self.get_docs(data_dir)
        self.index = self.get_index(self.documents)
        self.chat_engine = self.index.as_chat_engine(verbose=True)


    def get_docs(self, data_dir):
        # data_dir = '../data'
        documents = SimpleDirectoryReader(data_dir).load_data()
        return documents


    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
    def get_index(self, documents):
        index = GPTVectorStoreIndex.from_documents(documents)
        return index

    def get_next_message(self, prompt=SUMMARY_PROMPT):
        response = self.chat_engine.chat(prompt)
        return response


    



