import schedule
import time

def notify_upcoming_reservations():
    print("Checking for upcoming reservations...")
    # Add logic to fetch reservations 1 day before the event and notify users
    return

def notify_pending_matches():
    print("Checking for pending matches...")
    # Add logic to notify users about matches pending acceptance
    return
import smtplib

def send_email(to_email, subject, body):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("your_email@gmail.com", "your_password")
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail("your_email@gmail.com", to_email, message)
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

# Schedule periodic checks
schedule.every(1).minute.do(notify_upcoming_reservations)
schedule.every(1).minute.do(notify_pending_matches)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
