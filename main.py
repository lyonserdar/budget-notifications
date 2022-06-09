import os
import requests
import json
import smtplib
from datetime import datetime
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()

url = os.getenv("URL")
token = os.getenv("ACCESS_TOKEN")
budget_id = os.getenv("BUDGET_ID")
gmail_email = os.getenv("GMAIL_EMAIL")
gmail_password = os.getenv("GMAIL_PASSWORD")
to = os.getenv("TO").split(",")

categories = [
    "ec899102-c5f8-40da-8efb-537691cef505", 
    "73572037-0948-43f4-a9c4-00453d0ff07d", 
    "03052592-1c50-4ef6-9b98-28b7c11959c7", 
    "fd6e07ed-d765-4f4f-ac06-89fecfccac4d", 
    "906ec2ba-5616-4611-b273-4a8c470b63c9", 
    "8fdb4c2f-60e2-44aa-ad4b-529755759e48", 
    "0ee1838f-84d4-4e80-b27c-a0d949cd8dc3", 
    "07a97762-8c79-4047-8a21-f4da610bfd20"
]

output = []

for category in categories:
    response = requests.get(
        f"{url}/budgets/{budget_id}/categories/{category}",
        headers={
            "accept": "application/json",
            "Authorization": f"Bearer {token}"
        })
    data = response.json()["data"]["category"]
    obj = {"name": data["name"], "remaining": f'${data["balance"] / 1000:.2f}'} 
    output.append(obj)

message = EmailMessage()
text = ""

for x in output:
    text += f'{x["name"]}, {x["remaining"]} \n'

message.set_content(text)
message["Subject"] = "Daily Budget Remaining Balances"
message["From"] = gmail_email
message["To"] = to

print(datetime.now())
print("Sending Email")
try:
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    server.login(gmail_email, gmail_password)
    server.send_message(message)
    server.quit()
except:
    print("Something went wrong sending email")
