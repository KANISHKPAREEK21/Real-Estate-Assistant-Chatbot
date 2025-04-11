from openai import OpenAI
import json
import requests
import pandas as pd
import time
import os
import tempfile
import asyncio
from dotenv import load_dotenv
load_dotenv()

GPT_API_KEY = os.getenv("OPENAI_API_KEY")
OpenAIclient = OpenAI( api_key = GPT_API_KEY)

def handle_file_upload(uploaded_file):
    """
    Handles uploading Streamlit file to OpenAI Assistant in a temp file.
    """
    if uploaded_file is None:
        return None

    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(upload_openai_image(file= tmp_file_path))
    return tmp_file_path

def createThread():
    """
    This funciton is built on top of OPENAI GPT Assistant API
    return:OPENAI GPT Assistant Thread ID
    """
    url = "https://api.openai.com/v1/threads"
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+GPT_API_KEY,
        'OpenAI-Beta': 'assistants=v2',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    final_json = response.json()
    thread_id = final_json.get("id")
    return thread_id


def call_stream_assistant(msg=None,Thread_ID=None, Assistant_id=None, *args, **kwargs):
    
    if(str(Assistant_id)=="None" or str(Assistant_id)==""):
        ASSISTANT_ID='asst_8xx7YssEJLdCLAtR3yjlYxo3'
    else:
        ASSISTANT_ID = Assistant_id

    if(str(msg)=="None" or str(msg)==""):
        msg = "Give me detailed analysis of the image provided"
    def query(msg):
        message= OpenAIclient.beta.threads.messages.create(
           thread_id=Thread_ID,
           role="user",
           content= msg
           )
        return message
    
    query(msg)
    
    stream = OpenAIclient.beta.threads.runs.create(
        thread_id = Thread_ID,
        assistant_id = ASSISTANT_ID,
        stream=True
        )
    
    return stream

async def upload_openai_image(ASSISTANT_ID=None,file=None, *args, **kwargs):
    """
    This funciton is built on top of OpenAI Assistant to upload file
    Call OpenAI Assistant api and upload file in assistant's vector store
    :return: OpenAI Assistant's vector Id and File Id
    """
    if(str(ASSISTANT_ID)=="None" or str(ASSISTANT_ID)==""):
        ASSISTANT_ID='asst_8xx7YssEJLdCLAtR3yjlYxo3'
    else:
        ASSISTANT_ID = ASSISTANT_ID
    
    filedata_id = None
    retrieve_vectorfile_ids = []
    print(type(file))
  
    if file:
        with open(file, "rb") as uploadfile:

            filedata = OpenAIclient.files.create(
                file = uploadfile,
                purpose="assistants"
            )
            filedata_id = filedata.id
    
        my_updated_assistant = OpenAIclient.beta.assistants.update(
            assistant_id = ASSISTANT_ID,
            tool_resources = {
            "code_interpreter": {
                "file_ids": [filedata_id] 
            }}
        )
    return {"success":1}


def delete_assistant_file():
    ASSISTANT_ID='asst_8xx7YssEJLdCLAtR3yjlYxo3'
    

    my_updated_assistant = OpenAIclient.beta.assistants.update(
        assistant_id = ASSISTANT_ID,
        tool_resources = {
        "code_interpreter": {
            "file_ids": [] 
        }}
    )
    return {"success" : 1}