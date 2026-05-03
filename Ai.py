from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import find_dotenv, load_dotenv
import pathlib
import os
load_dotenv(find_dotenv())

gemeni_api= os.getenv("gemeni_api") 
client = genai.Client(api_key=gemeni_api)

prompt = "please extract the email, and job title from the document"

filepath = pathlib.Path("jobs/job0.txt")

class email_data(BaseModel):
    email: str = Field(description="Email address in document")
    job_title: str = Field(description="Job title in document")

response = client.models.generate_content(
  model="gemini-3-flash-preview",
  contents=[
      types.Part.from_bytes(
        data=filepath.read_bytes(),
        mime_type='text/plain',
      ),
      prompt
  ],
  config={"response_mime_type": "application/json",
          "response_json_schema": email_data.model_json_schema()}
)

data = email_data.model_validate_json(response.text)
print(data.model_dump_json()) 