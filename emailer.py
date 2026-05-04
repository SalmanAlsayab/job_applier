import smtplib
from dotenv import find_dotenv, load_dotenv
from email.message import EmailMessage
import os
import json
import re
import time

try:
    with open('email_job-title.json', encoding='utf-8') as file:
        job_posts = json.load(file)
except:
    print('failed to open file')
    
load_dotenv(find_dotenv())

keywords = ['data', 'ETL', 'Bussiness', 'AI', 'Artificial', 'machine', 'natural', 'NLP', 'ML', 'Large', 'LLM', 'MLOPs', 'BI', 'DBA', 'cloud']
email_address = os.getenv('EMAIL_USER')
email_password = os.getenv('EMAIL_PASSWORD')

try:
    for email in job_posts.keys():
        for job_title in job_posts[email]:
            time.sleep(10)
            if not job_title:
                break
            msg = EmailMessage()
            msg['Subject'] = job_title
            msg['From'] = email_address
            msg['TO'] = email
            msg.set_content(f"""
            Greetings, I would like to express my interest in the {job_title} role.

            You will find me an excellent candidate for this role to know more about me, please read the CV attached.

            Thank you in advance, and best regards

            Salman Alsayab. """)
            flag = [True for element in job_title if element in keywords]
            if flag:
                pdf_path = "cv/Salman Alsayab CV.pdf"
                pdf_name = re.split('/', pdf_path)[-1]
            else:
                pdf_path = "cv/CV_IT.pdf"
                pdf_name = re.split('/', pdf_path)[-1]
            with open(pdf_path, 'rb') as f:
                file_data = f.read()
                msg.add_attachment(
                    file_data,
                    maintype='application',
                    subtype='pdf',
                    filename=pdf_name
                )
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(email_address, email_password)
                smtp.send_message(msg)
except:
    print('error')
            
    