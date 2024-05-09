import os
import smtplib
import streamlit as st
from email.message import EmailMessage
import imghdr

EMAIL_ADDRESS = os.environ.get("EMAIL_USER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASS")

st.title("Email Sender")

num_recipients = st.number_input("Number of Recipients:", min_value=1, step=1, value=1)

recipient_emails = []
for i in range(num_recipients):
    recipient_email = st.text_input(f"Recipient {i+1}'s Email Address:")
    recipient_emails.append(recipient_email)

subject = st.text_input("Subject:")

default_body_templates = [
    "Hello,\n\nI hope this email finds you well.",
    "Hi there,\n\nJust checking in to see how you're doing.",
    "Dear colleague,\n\nI wanted to share some updates with you.",
    "Hey,\n\nI have attached some documents for your review."
]

selected_template_index = st.selectbox("Select Email Body Template:", options=list(range(len(default_body_templates))), index=0)
body_template = default_body_templates[selected_template_index]

body = st.text_area("Body:", value=body_template)

num_attachments = st.number_input("Number of Attachments:", min_value=0, step=1, value=0)

attachments = []
for i in range(num_attachments):
    attachment_type = st.selectbox(f"Attachment {i+1} Type:", ["Text", "Image"])
    if attachment_type == "Text":
        attachment = st.file_uploader(f"Upload Text File for Attachment {i+1}:", type="txt")
    else:
        attachment = st.file_uploader(f"Upload Image for Attachment {i+1}:", type=["jpg", "jpeg", "png"])
    if attachment is not None:
        attachments.append((attachment_type, attachment))

if st.button("Send Email"):
    for recipient_email in recipient_emails:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient_email
        msg.set_content(body)

        for attachment_type, attachment in attachments:
            if attachment_type == "Text":
                file_data = attachment.getvalue()
                file_name = attachment.name
                msg.add_attachment(file_data, maintype='text', subtype='plain', filename=file_name)
            else:
                file_data = attachment.getvalue()
                file_type = imghdr.what(None, h=file_data)
                file_name = attachment.name
                msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
    st.success("Email(s) sent successfully!")
