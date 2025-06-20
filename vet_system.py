import sqlite3
import datetime
from pet_management import add_pet, search_pets
from visit_management import add_visit, search_visits


def create_tables():
    connection = sqlite3.connect('vet.db')
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fname TEXT,
        lname TEXT,
        phone TEXT,
        email TEXT,
        address TEXT,
        city TEXT,
        postalcode TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        type TEXT CHECK(type IN ('dog', 'cat')),
        breed TEXT,
        birthdate DATE,
        ownerID INTEGER,
        FOREIGN KEY (ownerID) REFERENCES customers(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS visits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ownerid INTEGER,
        petid INTEGER,
        details TEXT,
        cost REAL,
        paid REAL,
        visit_date DATE DEFAULT CURRENT_DATE,
        FOREIGN KEY (ownerid) REFERENCES customers(id),
        FOREIGN KEY (petid) REFERENCES pets(id)
    )
    """)

    connection.commit()
    connection.close()


def add_customer():
    print("\n=== Add new customer ===")
    fname = input("Enter first name: ")
    lname = input("Enter last name: ")
    phone = input("Enter phone number: ")
    email = input("Enter email: ")
    address = input("Enter address: ")
    city = input("Enter city: ")
    postalcode = input("Enter postal code: ")

    connection = sqlite3.connect('vet.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM customers WHERE phone=?", (phone,))
    if cursor.fetchone():
        print("\n This phone number already exits！")
        return

    cursor.execute("SELECT * FROM customers WHERE email=?", (email,))
    if cursor.fetchone():
        print("\n This email already exists！")
        return

    cursor.execute("SELECT * FROM customers WHERE lname=?", (lname,))
    same_lastname = cursor.fetchall()
    if same_lastname:
        print("\n Found customer with the same last name：")
        for customer in same_lastname:
            print(f"ID: {customer[0]}, Name: {customer[2]} {customer[1]}, Phone number: {customer[3]}")
        confirm = input("\n Continue？(y/n): ")
        if confirm.lower() != 'y':
            return

    cursor.execute("""
    INSERT INTO customers (fname, lname, phone, email, address, city, postalcode)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (fname, lname, phone, email, address, city, postalcode))

    connection.commit()
    print("\n Customer added successfully！")
    connection.close()


def search_customer():
    print("\n=== Search customer ===")
    print("1. By name")
    print("2. By phone number")
    print("3. By email")
    print("4. By city")
    choice = input(" Please enter number (1-4): ")

    connection = sqlite3.connect('vet.db')
    cursor = connection.cursor()

    if choice == '1':
        lname = input("Enter last name: ")
        cursor.execute("SELECT * FROM customers WHERE lname LIKE ?", (f"%{lname}%",))
    elif choice == '2':
        phone = input("Enter phone number: ")
        cursor.execute("SELECT * FROM customers WHERE phone LIKE ?", (f"%{phone}%",))
    elif choice == '3':
        email = input("Enter email: ")
        cursor.execute("SELECT * FROM customers WHERE email LIKE ?", (f"%{email}%",))
    elif choice == '4':
        city = input("Enter city: ")
        cursor.execute("SELECT * FROM customers WHERE city LIKE ?", (f"%{city}%",))
    else:
        print("Invalid entry！")
        return

    results = cursor.fetchall()
    if results:
        print("\n Information：")
        for customer in results:
            print(f"ID: {customer[0]}")
            print(f"Name: {customer[2]} {customer[1]}")
            print(f"Phone: {customer[3]}")
            print(f"Email: {customer[4]}")
            print(f"Address: {customer[5]}")
            print(f"City: {customer[6]}")
            print(f"Postal code: {customer[7]}")
            print("-" * 30)
    else:
        print("\n No matched customer！")

    connection.close()


def main_menu():
    while True:
        print("\n=== Vet system ===")
        print("1. Customer management")
        print("2. Pet management")
        print("3. Visit history")
        print("4. Exit")

        choice = input("Please select from (1-4): ")

        if choice == '1':
            while True:
                print("\n=== Customer management ===")
                print("1. Add new customer")
                print("2. Search customer")
                print("3. Return to main menu")
                sub_choice = input("Select from (1-3): ")
                if sub_choice == '1':
                    add_customer()
                elif sub_choice == '2':
                    search_customer()
                elif sub_choice == '3':
                    break
                else:
                    print("Invalid entry！")

        elif choice == '2':
            while True:
                print("\n=== Pet management ===")
                print("1. Add new pet")
                print("2. Search pet")
                print("3. Return to main menu")
                sub_choice = input("Select from (1-3): ")
                if sub_choice == '1':
                    add_pet()
                elif sub_choice == '2':
                    search_pets()
                elif sub_choice == '3':
                    break
                else:
                    print("Invalid entry！")

        elif choice == '3':
            while True:
                print("\n=== Visit history ===")
                print("1. Add visits")
                print("2. Search visits")
                print("3. Return to main menu")
                sub_choice = input("Select from (1-3): ")
                if sub_choice == '1':
                    add_visit()
                elif sub_choice == '2':
                    search_visits()
                elif sub_choice == '3':
                    break
                else:
                    print("Invalid entry！")

        elif choice == '4':
            print("Bye bye！")
            break
        else:
            print("Invalid entry！")


if __name__ == "__main__":
    create_tables()
    main_menu()
