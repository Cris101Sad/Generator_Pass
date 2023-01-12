import random
import string
import sqlite3
from sqlite3 import Error
from termcolor import colored
import sys
import os
import textwrap
import time
import halo
from tqdm import tqdm
from colorama import init
from prettytable import PrettyTable

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('data.db')
        print(f'successful connection with sqlite version {sqlite3.version}')
    except Error as e:
        print(e)
    
    if conn:
        return conn


def generate_password(length):
    # check if length is a valid number
    if not str(length).isnumeric():
        print("Invalid input, password length should be a number.")
        return None
    # check if length is within a specific range
    elif int(length) < 8 or int(length) > 32:
        print("Invalid input, password length should be between 8 and 32.")
        return None
    # generate a secure password if input is valid
    letters_and_digits = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(letters_and_digits) for i in range(int(length)))
    return password

def generate_password_for_username(conn):
    username = input("Enter the username: ")
    length = input("Enter the password length (between 8 and 32): ")
    password = generate_password(length)
    if password:
        c = conn.cursor()
        c.execute("SELECT id FROM passwords WHERE username = ?", (username,))
        row = c.fetchone()
        if row:
            c.execute(f"UPDATE passwords SET password = '{password}' WHERE username = '{username}'")
            conn.commit()
            print("Record updated successfully")
        else:
            print(f"Username '{username}' does not exist.")

def create_table(conn):
    sql_create_table = """CREATE TABLE IF NOT EXISTS passwords (
                                id integer PRIMARY KEY,
                                username text NOT NULL UNIQUE,
                                password text NOT NULL
                            );"""
    try:
        c = conn.cursor()
        c.execute(sql_create_table)
    except Error as e:
        print(e)

def insert_data(conn,username, password):
    c = conn.cursor()
    c.execute("SELECT id FROM passwords WHERE username = ?", (username,))
    row = c.fetchone()
    if row:
        print(f"Username '{username}' already exists. Please enter a different username.")
    else:
        sql_insert_query = "INSERT INTO passwords (username, password) VALUES (?, ?)"
        try:
            c.execute(sql_insert_query, (username, password))
            conn.commit()
            print("Record created successfully")
        except Error as e:
            print(e)

def update_password_by_username(conn):
    username = input("Enter the username: ")
    new_password = input("Enter the new password: ")
    c = conn.cursor()
    c.execute(f"SELECT id FROM passwords WHERE username='{username}'")
    row = c.fetchone()
    if row:
        c.execute(f"UPDATE passwords SET password = '{new_password}' WHERE username = '{username}'")
        conn.commit()
        print("Record updated successfully")
    else:
        print(f"Username '{username}' does not exist.")

def update_username_by_password(conn):
    password = input("Enter the current password: ")
    new_username = input("Enter the new username: ")
    c = conn.cursor()
    c.execute(f"SELECT id FROM passwords WHERE password='{password}'")
    row = c.fetchone()
    if row:
        c.execute(f"UPDATE passwords SET username = '{new_username}' WHERE password = '{password}'")
        conn.commit()
        print("Record updated successfully")
    else:
        print(f"Password does not exist.")



def retrieve_all_data(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM passwords")
    rows = c.fetchall()
    if rows:
        table = PrettyTable()
        table.field_names = ["ID", "Username", "Password"]
        for row in rows:
            table.add_row([row[0], row[1], row[2]])
        print(table)
    else:
        print("No data found.")
        
def retrieve_password(conn, username):
    c = conn.cursor()
    c.execute(f"SELECT password FROM passwords WHERE username='{username}'")
    row = c.fetchone()
    if row:
        return row[0]
    else:
        return None

def read_data(conn):
    c = conn.cursor()
    c.execute("SELECT * from passwords ORDER BY username")
    rows = c.fetchall()
    print("ID\tUsername\tPassword")
    print("--\t--------\t--------")
    for row in rows:
        print(f"{row[0]}\t{row[1]}\t\t{row[2]}")


def menu():
  
    init()

    print("+----------------------------------+")
    print("|           MAIN MENU              |")
    print("+----------------------------------+")
    for i in tqdm(range(7), desc="Loading Menu",  bar_format="{l_bar}{bar} | 🔥 {n_fmt}/{total_fmt} 🔥"):
        time.sleep(0.5)
        with halo.Halo(text="Loading Menu", spinner="dots") as spinner:
            spinner.start()
            spinner.stop()
    print(textwrap.fill(colored("[1] Update password by username", "cyan"), width=40))
    print(textwrap.fill(colored("[2] Update username by password", "cyan"), width=40))
    print(textwrap.fill(colored("[3] Generate password for username", "cyan"), width=40))
    print(textwrap.fill(colored("[4] Retrieve all data", "cyan"), width=40))
    print(textwrap.fill(colored("[5] Insert new data", "cyan"), width=40))
    print(textwrap.fill(colored("[6] Delete data", "cyan"), width=40))
    print(textwrap.fill(colored("[7] Exit", "red"), width=40))
    print("+----------------------------------+")
    print("Please select an option (1-7):")
    print("Press Enter to continue...")
    print()

def main():
    while True:
        print("="*40)
        print(colored("    Welcome to the Password Manager    ", "green", attrs=["bold"]))
        print(colored("Created by Cristian Mar Q. De Guzman  ", "green", attrs=["bold"]))
        print("="*40)
        print("🔒 This code will help you generate a secure password and store it with a corresponding username.")
        print("📱 If you are on a phone, make sure you are using a command line interface or terminal to run the code.")
        print() 
        print(colored("🔌 Connecting to database...", "yellow", attrs=["bold"]))
        conn = create_connection()
        if conn:
            print(colored("✔ Successful connection with SQLite version " + sqlite3.version + "!", "green", attrs=["bold"]))
        else:
            print(colored("❌ Error: Connection failed!", "red", attrs=["bold"]))
        print() 
        print(colored("💾 Creating table 'passwords'...", "blue"))
        create_table(conn)
        print() 

        password_prompt = input("🔑 Please enter the password for this script: ")
        if password_prompt != "your_password":
            print("❌ Access Denied, Incorrect password.")
            sys.exit()
        else:
            print("\n")
            menu()
            option = input("Enter your choice [1-7]: ")
            if option == "1":
                conn = create_connection()
                if conn:
                    update_password_by_username(conn)
                else:
                    print("No database connection.")
            elif option == "2":
                conn = create_connection()
                if conn:
                    update_username_by_password(conn)
                else:
                    print("No database connection.")
            elif option == "3":
                conn = create_connection()
                if conn:
                    generate_password_for_username(conn)
                else:
                    print("No database connection.")
            elif option == "4":
                conn = create_connection()
                if conn:
                    retrieve_all_data(conn)
                else:
                    print("No database connection.")
            elif option == "5":
                conn = create_connection()
                if conn:
                    username = input("Enter a new username: ")
                    password = input("Enter a new password: ")
                    insert_data(conn, username, password)
                else:
                    print("No database connection.")
            elif option == "6":
                conn = create_connection()
                if conn:
                    choice = input("Enter '1' to delete by username or '2' to delete by password: ")
                    if choice == "1":
                        username = input("Enter the username: ")
                        c = conn.cursor()
                        c.execute("SELECT id FROM passwords WHERE username = ?", (username,))
                        row = c.fetchone()
                        if row:
                            c.execute("DELETE FROM passwords WHERE username = ?", (username,))
                            conn.commit()
                            print("Record deleted successfully.")
                        else:
                            print("Username not found.")
                    elif choice == "2":
                        password = input("Enter the password: ")
                        c = conn.cursor()
                        c.execute("SELECT id FROM passwords WHERE password = ?", (password,))
                        row = c.fetchone()
                        if row:
                            c.execute("DELETE FROM passwords WHERE password = ?", (password,))
                            conn.commit()
                            print("Record deleted successfully.")
                        else:
                            print("Password not found.")
                    else:
                        print("Invalid choice. Please enter '1' to delete by username or '2' to delete by password.")
            elif option == "7":
                print("Exiting the program.")
                sys.exit()
            else: 
                print("Invalid option. Please enter a valid option [1-7].")

if __name__ == '__main__':
    main()
