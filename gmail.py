import smtplib
from email.message import EmailMessage

smtp_server = "smtp.example.com"
smtp_port = 587
smtp_user = "zoom.main21@gmail.com"
smtp_password = "andreilly20023"

smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
smtp_connection.starttls()
smtp_connection.login(smtp_user, smtp_password)

msg = EmailMessage()
msg["Subject"] = "Тема вашего письма"
msg["From"] = smtp_user
msg["To"] = "andrewbasilew@gmail.com"
msg.set_content("Текст вашего письма")

smtp_connection.sendmail(smtp_user, "recipient@example.com", msg.as_string())

smtp_connection.quit()