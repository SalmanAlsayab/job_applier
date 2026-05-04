import smtplib
from dotenv import find_dotenv, load_dotenv
from email.message import EmailMessage
import os
import json


with open('email_job-title.json', encoding='utf-8') as file:
    job_posts = json.load(file)


# for idx, email in enumerate(job_posts.keys()):
#     for job_title in job_posts[email]:
#         print(job_title)
#         print('-'*20)
#         print(job_posts[email])
#         ('-'*20)
#         job_posts[email].remove(job_title)
#     if idx == 2:
#         break
        