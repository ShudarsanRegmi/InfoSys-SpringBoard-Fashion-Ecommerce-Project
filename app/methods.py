import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .models import OrderItems, Product, User
from flask import url_for


with open('app/secret.txt') as fh:
    p = fh.read()

ema = "shudarsanregmi555@gmail.com"


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

def send_approval_email(to_email, user_name, approved):
    global ema, p
    from_email = ema
    subject = "Account Approval"
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
        <p>Your account has been {'approved' if approved else 'rejected'}.</p>
        <p>Best regards,</p>
        <p>OUR APP NAME<br/>
    </body>
    </html>
    """

    # Attach the HTML content to the email
    msg.attach(MIMEText(html_content, 'html'))
    
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

def send_thankyou_email(order_id):
    global ema
    from_email = ema
    to_email = ""
    user_name = ""
    subject = "Thank you for shopping"
    smtp_server = "smtp.gmail.com"
    smtp_port = 465  # SSL port
    smtp_user = ema
    smtp_password = p  # Use the app password generated

    # Fetch all products in the order
    order_items = OrderItems.query.filter_by(OrderID=order_id).all()
    # Get the user ID from the first order item (assuming all items in the order belong to the same user)
    user_id = order_items[0].UserID if order_items else None

    # Fetch the user's email and name from the User model (assuming a User model exists)
    if user_id:
        user = User.query.get(user_id)
        if user:
            to_email = user.email
            user_name = user.firstname
    
    # Generate rating links for each product
    rating_links = ""
    for item in order_items:
        product = Product.query.get(item.ProductID)  # Assuming a Product model exists
        if product:
            rating_url = url_for('views.rate_product', product_id=item.ProductID, _external=True)
            rating_links += f"<li><a href='{rating_url}'>{product.name}</a></li>\n"

    # Create the HTML content
    html_content = f"""<html>
    <body>
    <p>Dear {user_name},</p>

    <p>Thank you for shopping with us! We hope you are happy with your purchase.</p>
    
    <p>We would love to hear your feedback! Please take a moment to rate the products you purchased:</p>

    <ul>
    {rating_links}
    </ul>

    <p>If you have any questions or need assistance, feel free to contact us.</p>

    <p>Best regards,<br>Your Company Name</p>
    </body>
    </html>
    """

    # Create the email
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))

    # Set the email headers
    msg.add_header('X-Priority', '1')  # High priority
    msg.add_header('X-Mailer', 'Python SMTP')

    # Send the email
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.set_debuglevel(1)  # Enable debugging
            server.login(smtp_user, smtp_password)
            server.sendmail(from_email, to_email, msg.as_string())
        print("Thank you Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


def send_order_deleted_mail(to_email, user_name, products):
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
        <p>Sorry to inform you that your order with the products - {products} has been canceled. due to technical reasons.</p>
        <p><strong>Important Information:</strong></p>
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