import smtplib
from dotenv import find_dotenv, load_dotenv
from email.message import EmailMessage
import os
import json
import re
import time

load_dotenv(find_dotenv())

keywords = ['data', 'ETL', 'Business', 'AI', 'Artificial', 'machine', 'natural', 'NLP', 'ML', 'Large', 'LLM', 'MLOps', 'BI', 'DBA', 'cloud']
email_address = os.getenv('EMAIL_USER')
email_password = os.getenv('EMAIL_PASSWORD')

def run_emailer():
    try:
        with open('email_job-title.json', encoding='utf-8') as file:
            job_posts = json.load(file)
    except FileNotFoundError:
        print('email_job-title.json not found')
        return
    
    # Load sent emails to avoid duplicates
    sent_file = 'sent_emails.json'
    sent = {}
    if os.path.exists(sent_file):
        try:
            with open(sent_file, encoding='utf-8') as f:
                content = f.read()
                if content.strip():
                    sent = json.loads(content)
        except json.JSONDecodeError:
            pass
    
    for email in job_posts.keys():
        for job_title in job_posts[email]:
            if not job_title:
                continue
            key = f"{email}:{job_title}"
            if key in sent:
                continue  # Already sent
            time.sleep(10)  # Rate limiting
            msg = EmailMessage()
            msg['Subject'] = job_title
            msg['From'] = email_address
            msg['To'] = email
            msg.set_content(f"""
Greetings, I would like to express my interest in the {job_title} role.

You will find me an excellent candidate for this role. To know more about me, please read the CV attached.

Thank you in advance, and best regards

Salman Alsayab.""")
            flag = any(element.upper() in map(str.upper, keywords) for element in job_title.split())
            if flag:
                pdf_path = "cv/Salman Alsayab CV.pdf"
                pdf_name = "Salman Alsayab CV.pdf"
            else:
                pdf_path = "cv/CV_IT.pdf"
                pdf_name = "CV_IT.pdf"
            try:
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
                print(f"Email sent to {email} for {job_title}")
                sent[key] = True
            except Exception as e:
                print(f"Error sending email to {email}: {e}")
    
    # Save sent emails
    with open(sent_file, 'w', encoding='utf-8') as f:
        json.dump(sent, f, indent=4, ensure_ascii=False)


if __name__=='__main__':
    run_emailer()