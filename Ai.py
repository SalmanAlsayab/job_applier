from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import find_dotenv, load_dotenv
import pathlib
import os
import json
import re
from shutil import move
import time

load_dotenv(find_dotenv())
gemeni_api = os.getenv("gemeni_api") 
client = genai.Client(api_key=gemeni_api)

prompt = "please extract the email, and job title from the document"

class email_data(BaseModel):
    email: str = Field(description="Email address in document")
    job_title: str = Field(description="Job title in document")

def run_ai():
    email_title = {}
    pathlib.Path('job_postings-dump').mkdir(exist_ok=True)
    try:
        directory = "new_messages"
        for idx, file in enumerate(directory.iterdir()):
            if not file.is_file():
                continue
            time.sleep(5.5)  # Rate limiting
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite-preview",
                contents=[
                    types.Part.from_bytes(
                        data=file.read_bytes(),
                        mime_type='text/plain',
                    ),
                    prompt
                ],
                config={"response_mime_type": "application/json",
                        "response_json_schema": email_data.model_json_schema()}
            )
            if response.text:
                move(str(file), f'job_postings-dump/job{idx}.txt')
                try:
                    data = dict(email_data.model_validate_json(response.text))
                    email = data['email']
                    job_title = data['job_title']
                    if email in email_title:
                        if job_title not in email_title[email]:
                            email_title[email].append(job_title)
                    else:
                        email_title[email] = [job_title]
                except Exception as e:
                    print(f"Error processing {file}: {e}")
    finally:    
        json_str = json.dumps(email_title, indent=4, ensure_ascii=False)
        with open('email_job-title.json', 'w', encoding='utf-8') as jsonFile:
            jsonFile.write(json_str)

