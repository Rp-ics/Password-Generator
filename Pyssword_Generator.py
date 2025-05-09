import random
import string
import json
import os
import time
from colorama import init, Fore, Style

# Inizializza Colorama per i colori nel terminale
init(autoreset=True)

# File di salvataggio password
DATA_FILE = "passwords.json"


# ───────────────────────────── UTILS ─────────────────────────────

def clear_screen():
    """Pulisce lo schermo del terminale in modo cross-platform."""
    os.system("cls" if os.name == "nt" else "clear")


def fancy_title(title):
    """Stampa un titolo stilizzato."""
    print(Style.BRIGHT + Fore.MAGENTA + "\n" + "-" * 40)
    print(Fore.MAGENTA + f"{title.center(40)}")
    print("-" * 40)


def pause_and_clear():
    """Aspetta un input dell'utente prima di pulire lo schermo."""
    input(Fore.CYAN + "\nPress Enter to continue...")
    clear_screen()


# ───────────────────────────── GESTIONE DATI ─────────────────────────────

def load_data():
    """Carica le password dal file JSON."""
    time.sleep(0.2)
    return {} if not os.path.exists(DATA_FILE) else json.load(open(DATA_FILE, "r"))


def save_data(data):
    """Salva le password nel file JSON."""
    time.sleep(0.2)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def show_all_names(data):
    """Mostra tutti i nomi delle password salvate."""
    time.sleep(0.2)
    if not data:
        print(Fore.YELLOW + "No saved passwords yet.")
        return False
    print(Fore.MAGENTA + "\nSaved entries:")
    for name in sorted(data.keys()):
        print(Fore.MAGENTA + f" → {name}")
    return True


# ───────────────────────────── GENERAZIONE PASSWORD ─────────────────────────────

LEVELS = {
    "1": ("basic", "Lowercase letters only"),
    "2": ("medium", "Letters (upper/lower) + digits"),
    "3": ("advanced", "Letters + digits + symbols"),
    "4": ("uppercase", "Uppercase letters only"),
    "5": ("lowercase", "Lowercase letters only"),
    "6": ("numbers", "Digits only"),
    "7": ("symbols", "Symbols only"),
}


def choose_level():
    """Permette all'utente di scegliere il livello di complessità della password."""
    while True:
        fancy_title("Password Level")
        for key, (level, desc) in LEVELS.items():
            print(f"{Fore.BLUE}{key}. {Fore.GREEN}{level.capitalize()} → {desc}")
        choice = input(Fore.CYAN + "\nYour choice: ").strip()
        if choice in LEVELS:
            return LEVELS[choice][0]
        print(Fore.RED + "Invalid choice. Try again.")


def generate_password(level, length):
    """Genera una password basata sul livello e lunghezza specificati."""
    time.sleep(0.2)
    char_sets = {
        "basic": string.ascii_lowercase,
        "medium": string.ascii_letters + string.digits,
        "advanced": string.ascii_letters + string.digits + string.punctuation,
        "uppercase": string.ascii_uppercase,
        "lowercase": string.ascii_lowercase,
        "numbers": string.digits,
        "symbols": string.punctuation,
    }
    chars = char_sets.get(level, "")
    return ''.join(random.choice(chars) for _ in range(length))


# ───────────────────────────── MENU PRINCIPALE ─────────────────────────────

def add_password(data):
    """Aggiunge una nuova password al database."""
    name = input(Fore.CYAN + "\nEnter the name (e.g., Gmail): ").strip()
    if name in data:
        print(Fore.RED + "Name already exists. Use update instead.")
        return

    while True:
        level = choose_level()

        while True:
            length_input = input(Fore.CYAN + "Enter desired password length (1-999): ").strip()
            if length_input.isdigit():
                length = int(length_input)
                if 1 <= length <= 999:
                    break
            print(Fore.RED + "Invalid length. Please enter a number between 1 and 999.")

        while True:
            password = generate_password(level, length)
            print(Fore.GREEN + f"\nGenerated password: {password}")
            print(Fore.YELLOW + "\n1 → Save\n2 → Generate Again\n3 → Change Options")
            sub_choice = input(Fore.CYAN + "Your choice: ").strip()

            if sub_choice == "1":
                data[name] = {"level": level, "length": length, "password": password}
                save_data(data)
                print(Fore.GREEN + f"✅ Password for '{name}' saved.")
                return
            elif sub_choice == "2":
                continue
            elif sub_choice == "3":
                break
            else:
                print(Fore.RED + "Invalid option. Try again.")


def view_password(data):
    """Visualizza i dettagli di una password esistente."""
    if not show_all_names(data):
        return
    name = input(Fore.CYAN + "Enter the name to search: ").strip()
    if name in data:
        entry = data[name]
        print(Fore.GREEN + f"\nName: {name}")
        print(Fore.GREEN + f"Level: {entry['level']}")
        print(Fore.GREEN + f"Length: {entry.get('length', 'unknown')}")
        print(Fore.GREEN + f"Password: {entry['password']}")
    else:
        print(Fore.RED + "Name not found.")


def update_password(data):
    """Aggiorna una password esistente."""
    if not show_all_names(data):
        return
    name = input(Fore.CYAN + "Enter the name to update: ").strip()
    if name not in data:
        print(Fore.RED + "Name not found.")
        return

    print(Fore.YELLOW + "\nWhat do you want to update?")
    print("1. Name")
    print("2. Password")
    choice = input("Choice (1 or 2): ").strip()

    if choice == "1":
        new_name = input(Fore.CYAN + "Enter new name: ").strip()
        if new_name in data:
            print(Fore.RED + "Name already exists.")
            return
        data[new_name] = data.pop(name)
        save_data(data)
        print(Fore.GREEN + "✅ Name updated.")
    elif choice == "2":
        level = choose_level()
        while True:
            length_input = input(Fore.CYAN + "Enter desired password length (1-999): ").strip()
            if length_input.isdigit():
                length = int(length_input)
                if 1 <= length <= 999:
                    break
            print(Fore.RED + "Invalid length.")
        password = generate_password(level, length)
        print(Fore.GREEN + f"New password: {password}")
        data[name] = {"level": level, "length": length, "password": password}
        save_data(data)
        print(Fore.GREEN + "✅ Password updated.")
    else:
        print(Fore.RED + "Invalid choice.")


def delete_password(data):
    """Elimina una password esistente."""
    if not show_all_names(data):
        return
    name = input(Fore.CYAN + "Enter the name to delete: ").strip()
    if name in data:
        confirm = input(Fore.RED + f"Are you sure you want to delete '{name}'? (yes/no): ").strip().lower()
        if confirm == "yes":
            del data[name]
            save_data(data)
            print(Fore.GREEN + "🗑️ Deleted successfully.")
        else:
            print(Fore.YELLOW + "Deletion cancelled.")
    else:
        print(Fore.RED + "Name not found.")


# ───────────────────────────── MAIN ─────────────────────────────

def main():
    data = load_data()
    clear_screen()

    while True:
        fancy_title("PASSWORD MANAGER")
        print(f"{Fore.BLUE}1.{Fore.LIGHTYELLOW_EX} Add new password")
        print(f"{Fore.BLUE}2.{Fore.LIGHTYELLOW_EX} View password")
        print(f"{Fore.BLUE}3.{Fore.LIGHTYELLOW_EX} Update password")
        print(f"{Fore.BLUE}4.{Fore.LIGHTYELLOW_EX} Delete password")
        print(f"{Fore.BLUE}5.{Fore.LIGHTYELLOW_EX} Exit")
        choice = input(Fore.CYAN + "\nChoose an option: ").strip()

        clear_screen()
        if choice == "1":
            add_password(data)
        elif choice == "2":
            view_password(data)
        elif choice == "3":
            update_password(data)
        elif choice == "4":
            delete_password(data)
        elif choice == "5":
            print(Fore.YELLOW + "👋 Exiting. Bye!")
            break
        else:
            print(Fore.RED + "❌ Invalid option. Try again.")
        pause_and_clear()


if __name__ == "__main__":
    main()