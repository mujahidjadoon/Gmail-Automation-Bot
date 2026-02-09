import time
import base64
import os
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from gmail_agent import get_gmail_service
from database_manager import SecureVault

# --- SECURITY CONFIGURATION ---
# Users must define their own password here for remote access.
# On GitHub, we keep this as a placeholder for security.
BOT_PASSWORD = "YOUR_SECRET_PASSWORD"


def search_files_in_vault(query):
    """Searches the local database for files matching the query string."""
    print(f"[*] Deep scanning database for: {query}...")
    vault = SecureVault()
    conn = sqlite3.connect(vault.db_name)
    cursor = conn.cursor()

    # Executing search across the entire indexed system
    cursor.execute("SELECT name, encrypted_path FROM system_paths")

    matches = []
    while True:
        row = cursor.fetchone()
        if row is None: break

        name, enc_path = row
        # Case-insensitive search logic
        if query.lower() in name.lower():
            try:
                dec_path = vault.decrypt_data(enc_path)
                if os.path.exists(dec_path):
                    matches.append((name, dec_path))
                if len(matches) >= 5:  # Limit results for security/performance
                    break
            except Exception:
                continue
    conn.close()
    return matches


def send_secure_email(service, to, subject, body, file_path=None):
    """Handles the construction and delivery of secure email responses."""
    try:
        # Security: Prevent loop-backs by ignoring system/automated emails
        if "mailer-daemon" in to.lower() or "google" in to.lower():
            print(f"[*] Ignoring automated system email: {to}")
            return

        print(f"[*] Preparing secure response for {to}...")
        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = f"Re: {subject}"
        message.attach(MIMEText(body))

        if file_path and os.path.exists(file_path):
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # Size in MB
            if file_size < 25:  # Standard Gmail attachment limit
                filename = os.path.basename(file_path)
                with open(file_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename= {filename}")
                    message.attach(part)
            else:
                message.attach(MIMEText("\n\n[SYSTEM]: File exceeds 25MB. Attachment blocked for security."))

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        service.users().messages().send(userId='me', body={'raw': raw}).execute()
        print(f"[SUCCESS] Response sent successfully.")

    except Exception as e:
        print(f"[ERROR] Delivery failed: {e}")


def listen_as_assistant():
    """Main monitor loop for processing unread Gmail commands."""
    service = get_gmail_service()
    print("\n" + "=" * 45)
    print("--- AI ASSISTANT: SECURE SYSTEM ACTIVE ---")
    print("=" * 45)

    while True:
        try:
            # Query unread messages only
            results = service.users().messages().list(userId='me', q='is:unread').execute()
            messages = results.get('messages', [])

            if messages:
                for msg in messages:
                    txt = service.users().messages().get(userId='me', id=msg['id']).execute()
                    sender = ""
                    subject = ""
                    snippet = txt.get('snippet', '').lower()

                    for header in txt['payload']['headers']:
                        if header['name'] == 'From': sender = header['value']
                        if header['name'] == 'Subject': subject = header['value']

                    print(f"\n[!] Valid Request: '{subject}' from {sender}")

                    if "search" in subject.lower():
                        # Password verification (Check subject or body)
                        has_password = BOT_PASSWORD.lower() in subject.lower() or BOT_PASSWORD.lower() in snippet

                        # Extract query (e.g., "search: report" -> "report")
                        query = subject.lower().split("search")[1].replace(":", "").replace(BOT_PASSWORD.lower(),
                                                                                            "").strip()

                        matches = search_files_in_vault(query)

                        if not matches:
                            reply_body = f"Welcome! I am your AI Assistant.\n\nI could not find any matches for '{query}' in the system."
                            send_secure_email(service, sender, subject, reply_body)
                        elif not has_password:
                            reply_body = (f"Welcome! I am your AI Assistant.\n\n"
                                          f"Match found for '{query}'. However, I cannot share details without the security password.\n\n"
                                          f"Please provide the correct password to gain access.")
                            send_secure_email(service, sender, subject, reply_body)
                        else:
                            # Access Granted - Attach top match
                            name, path = matches[0]
                            reply_body = (f"Access Granted!\n\n"
                                          f"File: {name}\n"
                                          f"Status: Attaching to this email.")

                            send_secure_email(service, sender, subject, reply_body, file_path=path)

                    # Mark message as read to prevent reprocessing
                    service.users().messages().batchModify(
                        userId='me', body={'removeLabelIds': ['UNREAD'], 'ids': [msg['id']]}
                    ).execute()
        except Exception as e:
            print(f"[SYSTEM ERROR]: {e}")

        time.sleep(10)


if __name__ == "__main__":
    listen_as_assistant()