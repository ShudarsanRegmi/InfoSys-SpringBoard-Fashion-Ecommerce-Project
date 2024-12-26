import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText




ema = "songs.trendify@gmail.com"


def send_token_email(to_email, user_name, verification_link):
    global ema
    from_email = ema
    subject = "Reset Password Request"
    smtp_server = "smtp.gmail.com"
    smtp_port = 465  # SSL port
    smtp_user = ema
    smtp_password = p  # Use the app password generated

    # Create the email
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Create the HTML content
    html_content = f"""
    <html>
    <head></head>
    <body>
        <p>Hi {user_name},</p>
        <p>You have requested for a password change so here is your password reset link:</p>
        <h2><a href = '{verification_link}'>{verification_link}</a></h2>
        <p><strong>Important Information:</strong></p>
        <ul>
            <li>This clink is for one-time use and will expire after 1 Hour.</li>
            <li>For your security, please keep this code confidential.</li>
            <li>If you encounter any issues, contact our support team at <a href="mailto:support@example.com">support@example.com</a>.</li>
        </ul>
        <p>Best regards,</p>
        <p>OUR APP NAME<br/>
        <a href="mailto:support@example.com">support@example.com</a> | (123) 456-7890</p>
    </body>
    </html>
    """

    # Attach the HTML content to the email
    msg.attach(MIMEText(html_content, 'html'))

    # Set the email headers
    msg.add_header('X-Priority', '1')  # High priority
    msg.add_header('X-Mailer', 'Python SMTP')

    # Send the email
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(from_email, to_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")