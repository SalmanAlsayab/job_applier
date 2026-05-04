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

try:
    with open('channels.json', 'r') as file:
        data = json.load(file)
        channels_url = data["channel"]

except:
    print("failed to read json file")

channels = list(map(lambda x: re.split('/', x)[-1], channels_url))

load_dotenv(find_dotenv())
gemeni_api= os.getenv("gemeni_api") 
client = genai.Client(api_key=gemeni_api)

prompt = "please extract the email, and job title from the document"

email_title = {}
class email_data(BaseModel):
    email: str = Field(description="Email address in document")
    job_title: str = Field(description="Job title in document")
try:
    for folder in channels:
        dierectory = pathlib.Path(f'{folder}')
        for idx, file in enumerate(dierectory.iterdir()):
            time.sleep(5.5)
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
                move(file, f'job_postings-dump/{folder}{idx}')
            
            data = dict(email_data.model_validate_json(response.text))
            email = data['email']
            job_title = data['job_title']
            if email in email_title.keys():
                if job_title in email_title[email]:
                    pass
                else:
                    email_title[email].append(job_title)
            else:
                email_title[email] = [job_title]
finally:
    json_str = json.dumps(email_title, indent=4, ensure_ascii=False)
    with open('email_job-title.json', 'w', encoding='utf-8') as jsonFile:
        jsonFile.write(json_str)
if __name__ == "__main__":
    print(data.model_dump_json()) 