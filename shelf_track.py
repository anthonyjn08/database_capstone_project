import sqlite3, sys

# Create database called ebookstore
db = sqlite3.connect("ebookstore.db")

# Create a cursor object
cursor = db.cursor()

# Check for table called book and creates if it does not exist
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS
    book(id INTEGER PRIMARY KEY, title TEXT, authorID INTEGER, qty INTEGER)
'''
)


# Create initial list of books in database
books = [
    (3001, "A Tale of Two Cities", 1290, 30),
    (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
    (3003, "The Lion, the Witch and the Wardrobe", 2356, 25),
    (3004, "The Lord of the Rings", 6380, 37),
    (3005, "Alice’s Adventures in Wonderland", 5620, 12)
]
cursor.execute(
    '''
    SELECT COUNT(*)
    FROM book
'''
)
book_count = cursor.fetchone()
if book_count[0] == 0:
    print("adding books")
    cursor.executemany(
        '''
        INSERT INTO book(id, title, authorID, qty)
        VALUES(?, ?, ?, ?)
''', books
    )

    db.commit()


def enter_book():
    '''
    Function: enter_book
    This function allows the user to enter a new book into the database
    taking inputs from the user for the ID, title, authorID and quantity.

    Inputs:
    id: (int) The books ID and primary key
    title: (str) The title of the book
    authorID: The UD of the books author
    qty: The quantity for the book
    '''
    print("\nEnter new book\n")
    while True:
        try:

            id = int(input("Please enter the books 4 digit ID "
                           "(must not start with 0): "))
            title =  input("Please enter the books title: ")
            authorid = int(input("Please enter the 4 digit Author ID "
                                 "(must not start with 0): "))
            qty = int(input("Please enter the total quantity: "))

            if id < 1000 or id > 9999:
                print("\nThe ID must be 4 digits and not start with 0\n")
            elif authorid < 1000 or authorid > 9999:
                print("\nThe Author ID must be 4 digits and not start with 0\n")
            else:
                cursor.execute('''INSERT INTO book(id, title, authorID, qty)
                            VALUES(?, ?, ?, ?)''', (id, title, authorid, qty))

                db.commit()
                print(f"\nBook: {title} added to database\n")
                break

        except sqlite3.IntegrityError:
            print(f"A book with ID {id} already exists. Please use a unique ID.")
        except ValueError:
            print("Please enter data in correct format!")


def id_search(cursor):
    while True:
        try:
            id = int(input("Please enter the book id or '-1' for main menu: "))

            if id == -1:
                return None
            elif id < 1000 or id > 9999:
                print("\nThe ID must be 4 digits and not start with 0\n")
                continue

            cursor.execute('''
                           SELECT *
                           FROM book
                           WHERE id = ?''',
                           (id,))
            book = cursor.fetchone()

            if book is None:
                print("\nBook not found. Please try again.\n")
                continue

            return book
            

        except ValueError:
                print("Please enter data in correct format!")


def update_book(cursor):
    print("\n**** Update book ****\n")

    book = id_search(cursor)

    while True:
        print(f"\nUpdating {book[1]}\n")
        confirm = input("Please enter 'y' if this is the right book or 'n': ").lower()

        if confirm == "y":
            while True:
                try:
                    qty = int(input("Please enter the new quantity "
                                    "or '-1' to proceed to update title or authorID: "))
                    if qty == -1:
                        pass
                    else:
                        cursor.execute('''
                                    UPDATE book
                                    SET qty = ?
                                    WHERE id = ?''',
                                    (qty, id))
                        
                        print(f"{book[0]} quantity updated to {qty}")

                    authorID_update = input(f"Would you like to update "
                                            f"{book[0]}'s authorID? 'y' or 'n': ").lower()
                    if authorID_update == "y":
                        new_auth_ID = int(input("Please enter the new 4 digit author ID "
                                                "(must not start with 0)"))
                        if new_auth_ID < 1000:
                            print("\nThe ID must be 4 digits and not start with 0\n")
                        else:
                            cursor.execute('''
                                        UPDATE book
                                        SET authorID = ?
                                        WHERE id = ?''',
                                        (new_auth_ID, id))
                            print(f"{book[0]} author ID updated to {new_auth_ID}")

                    title_update = input(f"Would you like to update {book[0]}'s "
                                        f"title? 'y' or 'n': ").lower
                    if title_update == "y":
                        new_title = input("Please enter the new book title: ")
                        cursor.execute('''
                                    UPDATE book
                                    SET title = ?
                                    WHERE id = ?''',
                                    (new_title, id))
                        
                        print(f"Title updated to {new_title}")
                    return
                except ValueError:
                    print("Please try again.")
        elif confirm == "n":
            id_search(cursor)
        else:
            print("Invalid Option. Try again")
        db.commit()
        break


def delete_book(cursor):
    print("\n**** Delete Book ****\n")
    while True:
        try:
            id = int(input("Please enter the ID of the book you wish to delete "
                        " or '0' to return to main menu: "))
            
            if id == 0:
                return
            
            elif id < 1000:
                print("\nPlease make sure ID does not start with 0 and "
                        "is four digits long.\n")
                break
            
            cursor.execute('''
                            SELECT title
                            FROM book
                            WHERE ID = ?''',
                            (id,))
            book = cursor.fetchone()

            while True:
                if book:
                    print(f"Are you sure you wish to delete {book[0]} from the database?")
                    choice = input("Enter 'y' or 'n': ").lower()
                    if choice == "n":
                        break
                    elif choice == "y":
                        cursor.execute('''
                                        DELETE FROM book
                                        WHERE id = ?''',
                                        (id,))
                        print(f"{book[0]} has been deleted")
                        db.commit()
                        break
                    else:
                        print("Invalid option. Try again.")
                        continue
                    
                else:
                    print("Book does not exist. Please try again.")

        except ValueError:
            print("\n*Invalid input. Please tray again.*\n")


def search_books():
    print("\n**** Search Book ****\n")

    while True:
        try:
            id = int(input("Please enter the book ID or '0' to return to main menu: "))
            cursor.execute('''
                           SELECT *
                           FROM book
                           WHERE id = ?''',
                           (id,))
            book = cursor.fetchone()

            if id == 0:
                break

            while True:
                if book:
                    print(f"\nBook ID:                  {book[0]}")
                    print(f"Title:                      {book[1]}")
                    print(f"Author ID:                  {book[2]}")
                    print(f"Quantity:                   {book[3]}\n")
                    break
                else:
                    print("Invalid option]")
                    break
        except ValueError:
            print("\n*Invalid input. Please tray again.*\n")
            
while True:
    try:
        menu = int(input('''
        Please select and option:
        1. Enter book
        2. Update book
        3. Delete book
        4. Search books
        0. Exit
        : '''))

        if menu == 1:
            enter_book()
        elif menu == 2:
            update_book(cursor)
        elif menu == 3:
            delete_book(cursor)
        elif menu == 4:
            search_books(cursor)
        elif menu == 0:
            db.close()
            sys.exit()
        else:
            print("Please enter a valid option")
    
    except ValueError:
        print("Please enter a valid option.")