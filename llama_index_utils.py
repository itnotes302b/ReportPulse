import os
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
from prompts import SUMMARY_PROMPT
import redis
import hashlib
from llama_index import StorageContext, load_index_from_storage

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

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

        # rebuild storage context
        try:
            storage_context = StorageContext.from_defaults(persist_dir='./storage')
            index = load_index_from_storage(storage_context)
        except Exception as e:
            index = GPTVectorStoreIndex.from_documents(documents)
            index.storage_context.persist()
        
        return index

    def get_next_message(self, prompt=SUMMARY_PROMPT, lang="ENGLISH"):

        input = f"{prompt}. Return the result in {lang} language."

        md5_hash = hashlib.md5(input.encode()).hexdigest()

        if r.exists(md5_hash):
            response = r.get(md5_hash).decode('utf-8')
            return response
        else:
            response = self.chat_engine.chat(input)
            r.set(md5_hash, response.response)
             
        return response.response


    



