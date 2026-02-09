import os
from cryptography.fernet import Fernet
import sqlite3

class MujahidVault:
    def __init__(self, db_name="mujahid_vault.db"):
        self.db_name = db_name
        self.key_file = "master.key"
        self.load_key()
        self.init_db()

    def load_key(self):
        # Master Key banana ya load karna
        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(key)
        
        with open(self.key_file, "rb") as f:
            self.key = f.read()
        self.fernet = Fernet(self.key)

    def init_db(self):
        # Simone's Silo Structure: Tables for different data types
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        # Silo 1: System Paths (Encrypted)
        cursor.execute('''CREATE TABLE IF NOT EXISTS system_paths 
                          (id INTEGER PRIMARY KEY, name TEXT, encrypted_path BLOB)''')
        # Silo 2: Habit Logs
        cursor.execute('''CREATE TABLE IF NOT EXISTS habit_logs 
                          (id INTEGER PRIMARY KEY, action TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()

    def encrypt_data(self, data):
        return self.fernet.encrypt(data.encode())

    def decrypt_data(self, encrypted_data):
        return self.fernet.decrypt(encrypted_data).decode()

    def save_path(self, name, path):
        # Data ko silo mein mehfooz karna
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        enc_path = self.encrypt_data(path)
        cursor.execute("INSERT INTO system_paths (name, encrypted_path) VALUES (?, ?)", (name, enc_path))
        conn.commit()
        conn.close()
        print(f"JARVIS: {name} path secured in the Vault.")

# --- Test Day 1 ---
if __name__ == "__main__":
    vault = MujahidVault()
    vault.save_path("D_Drive", "D:\\all apps")
    print("Mujahid Bot: Day 1 Security Layer Completed.")