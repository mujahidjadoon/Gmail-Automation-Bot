import os
from database_manager import MujahidVault  


class FileManager:
    def __init__(self):
      
        self.vault = MujahidVault()
        self.target_drive = "D:\\"

    def scan_drive(self):
        print(f"MUJAHID BOT: Scanning {self.target_drive}... Please wait.")
        file_count = 0

        # Drive scan karna
        for root, dirs, files in os.walk(self.target_drive):
            for file in files:
                full_path = os.path.join(root, file)

                try:
                    # Aap ki database_manager mein 'save_path' function mojood hai
                    self.vault.save_path(file, full_path)
                    file_count += 1

                    # Terminal par progress dikhana
                    if file_count % 10 == 0:
                        print(f"[*] Secured {file_count} files in the Vault...", end="\r")
                except Exception as e:
                    print(f"\nError securing {file}: {e}")

        print(f"\nMUJAHID BOT: Day 3 Scan Complete! {file_count} system paths indexed.")


if __name__ == "__main__":
    scanner = FileManager()
    scanner.scan_drive()
