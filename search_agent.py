import sqlite3
import os
from database_manager import MujahidVault


def universal_search():
    # Initializing the vault with MujahidVault class
    vault = MujahidVault()
    conn = sqlite3.connect(vault.db_name)
    cursor = conn.cursor()

    print("\n--- MUJAHID BOT: UNIVERSAL FILE ACCESS ---")
    query = input("What are you looking for? (Enter file name or extension): ").strip().lower()

    if not query:
        print("[!] Input cannot be empty. Please enter a search term.")
        return

    # Fetching all indexed records from the system_paths table
    cursor.execute("SELECT name, encrypted_path FROM system_paths")
    results = cursor.fetchall()

    found_items = []
    for name, enc_path in results:
        try:
            # Decrypting the path using AES-256 logic from MujahidVault
            decrypted_path = vault.decrypt_data(enc_path)

            # Checking if query exists in the filename or the full path
            if query in name.lower() or query in decrypted_path.lower():
                found_items.append((name, decrypted_path))
        except Exception as e:
            continue

    if not found_items:
        print(f"[-] No results found for '{query}'.")
        print("Tip: If the file is new, please run 'python file_manager.py' to update the index.")
    else:
        print(f"\n[+] Mujahid Bot found {len(found_items)} matches:")
        # Displaying the first 20 results for clarity
        for i, (name, path) in enumerate(found_items[:20]):
            print(f"{i + 1}. {name}")
            print(f"   Location: {path}\n")

        choice = input("Which file would you like to OPEN? (Enter Number or press Enter to Exit): ")

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(found_items):
                file_path = found_items[idx][1]

                # Verification before opening
                if os.path.exists(file_path):
                    print(f"[*] Mujahid Bot: Opening file... Please wait.")
                    os.startfile(file_path)  # Command to open the file with its default application
                else:
                    print("[-] Error: File not found at the original path. It might have been moved.")
            else:
                print("[!] Invalid selection.")

    conn.close()


if __name__ == "__main__":
    universal_search()