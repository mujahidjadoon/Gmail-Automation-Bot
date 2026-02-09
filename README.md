# 🤖 Gmail Automation & Local File Retrieval Bot

A **100% Local** and secure Python-based AI assistant that allows you to search and retrieve system files remotely via Gmail commands.

### 🛡️ Key Features
- **Local-First Architecture:** All indexing and file management happen on your local machine.
- **Remote Retrieval:** Use simple Gmail triggers to locate files from anywhere.
- **AES-256 Encryption:** Securely stores 400,000+ system paths in an encrypted local vault.
- **Zero-Trust Security:** Requires a pre-set password for any data access.

### 🚀 Local Setup & Installation
1. **Clone the Project:**
   `git clone https://github.com/mujahidjadoon/Gmail-Automation-Bot.git`
2. **Setup Google API:**
   Place your `credentials.json` in the root folder (keep it private!).
3. **Run Indexer:**
   Execute `python file_manager.py` to scan your local drives.
4. **Start Assistant:**
   Run `python gmail_controller.py` to begin the remote listener.


<img width="1088" height="960" alt="Gemini_Generated_Image_pqold3pqold3pqol" src="https://github.com/user-attachments/assets/cf52751a-657f-468c-8ad7-fa3ed192efed" />


---
## 📸 Project Screenshots & Demo

### 1. Bot Initialization & Listening
![System Start](scan_demo.png)
*Terminal showing the bot successfully starting and waiting for Gmail triggers.*

### 2. Remote File Search & Email Delivery
![Email Proof](bot_reply.png)
*Proof of the bot finding the file locally and sending it back via encrypted email.*
