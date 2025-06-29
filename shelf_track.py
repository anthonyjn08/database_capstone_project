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

# Check for an author table and create if it does not exist.
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS
    author(id INTEGER PRIMARY KEY, name TEXT, country TEXT)
'''
)

# Commit tables to the database
db.commit()

# Create initial list of books in database
books = [
    (3001, "A Tale of Two Cities", 1290, 30),
    (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
    (3003, "The Lion, the Witch and the Wardrobe", 2356, 25),
    (3004, "The Lord of the Rings", 6380, 37),
    (3005, "Alice’s Adventures in Wonderland", 5620, 12),
]

# Check if book database is populated
cursor.execute(
    '''
    SELECT COUNT(*)
    FROM book
'''
)
book_count = cursor.fetchone()

# If book database is empty, insert book data from list
# and then commit changes
if book_count[0] == 0:
    print("adding books")
    cursor.executemany(
        '''
        INSERT INTO book(id, title, authorID, qty)
        VALUES(?, ?, ?, ?)
''', books
    )

    db.commit()

# List of initial authors in the system
authors = [
    (1290, "Charles Dickens", "England"),
    (8937, "J.K. Rowling", "England"),
    (2356, "C.S. Lewis", "Ireland"),
    (6380, "J.R.R. Tolkien", "South Africa"),
    (5620, "Lewis Carroll", "England"),
]

# Check if author database is populated
cursor.execute(
    '''
    SELECT COUNT(*)
    FROM author
'''
)
author_count = cursor.fetchone()

# If author database is empty, insert author data from list
# and then commit changes
if author_count[0] == 0:
    print("adding authors")
    cursor.executemany(
        '''
        INSERT INTO author(id, name, country)
        VALUES(?, ?, ?)
''', authors
    )

    db.commit()


def enter_book():
    '''
    Function: enter_book
    This function allows the user to enter a new book into the database
    taking inputs from the user for the ID, title, authorID and quantity.
    IDs are validated to be 4 digits, not starting with 0 and unique.
    AuthorID is validated to be 4 digits and not start with 0.

    Inputs:
    id: (int) The books ID and primary key
    title: (str) The title of the book
    authorID: The UD of the books author, foriegn key from author table
    qty: The quantity for the book
    '''
    print("\nEnter new book\n")

    # Loop to get valid, unique 4 digit book ID
    while True:
        try:
            id = int(input("Please enter the books 4 digit ID "
                           "(must not start with 0): "))
            
            # Check ID is 4 digits
            if id < 1000 or id > 9999:
                print("\nThe ID must be 4 digits and not start with 0\n")
                continue

            # Check ID does not already exist
            cursor.execute('''
                           SELECT id
                           FROM book
                           WHERE id = ?''',
                           (id,))
            if cursor.fetchone():
                print(f"\nA book with ID {id} already exists. Please use a "
                      "unique ID\n")
                continue
            break
        except ValueError:
            print("\nInvalid input! Please enter a 4 digit number.\n")
            
    title =  input("Please enter the books title: ")
    
    # Loop to get valid authorID
    while True:
        try:
            authorid = int(input("Please enter the 4 digit Author ID "
                                 "(must not start with 0): "))
            if authorid < 1000 or authorid > 9999:
                print("\nThe Author ID must be 4 digits and not start with 0\n")
                continue
            break
        except ValueError:
            print("\nInvalid input! Please enter a 4 digit number.\n")

    # Loop to get valid quantity
    while True:
        try:
            qty = int(input("Please enter the total quantity: "))
            break
        except ValueError:
            print("\nPlease enter a whole number.\n")

    # Insert all validated inputs into database
    try:
        cursor.execute('''INSERT INTO book(id, title, authorID, qty)
                    VALUES(?, ?, ?, ?)''', (id, title, authorid, qty))

        # Commit changes to database
        db.commit()
        print(f"\nBook: {title} added to database\n")
    except sqlite3.IntegrityError as e:
        print("Database integrity error.", e)


def id_search(cursor):
    '''
    Function: id_search
    This function performs a search on the book ID in the book table.
    If the book doesn't exist, users are asked to enter the ID again
    or return to the main menu.
    This is used in any function where a user searches for a book.
    '''

    # Loop to validate ID
    while True:
        try:
            id = int(input("Please enter the book id or '-1' for main menu: "))

            # If user wants to return to main menu
            if id == -1:
                return None
            
            # Validates ID
            elif id < 1000 or id > 9999:
                print("\nThe ID must be 4 digits and not start with 0\n")
                continue

            cursor.execute('''
                           SELECT *
                           FROM book
                           WHERE id = ?''',
                           (id,))
            book = cursor.fetchone()

            # If book doesn't exist, provide error message.
            if book is None:
                print("\nBook not found. Please try again.\n")
                continue

            # Return the book if found.
            return book

        except ValueError:
                print("Please enter data in correct format!")


def update_book(cursor):
    print("\n**** Update book ****\n")

    book = id_search(cursor)

    id = book[0]

    while True:
        print(f"\nUpdating {book[1]}\n")
        confirm = input("Is this correct? (y/n): ").lower()

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
                        
                        print(f"{book[1]} quantity updated to {qty}")

                    authorID_update = input(f"Would you like to update "
                                            f"{book[1]}'s authorID? (y/n): ").lower()
                    if authorID_update == "y":
                        new_auth_ID = int(input("Please enter the new 4 digit author ID "
                                                "(must not start with 0)"))
                        if new_auth_ID < 1000 or new_auth_ID > 9999:
                            print("\nThe ID must be 4 digits and not start with 0\n")
                        else:
                            cursor.execute('''
                                        UPDATE book
                                        SET authorID = ?
                                        WHERE id = ?''',
                                        (new_auth_ID, id))
                            print(f"{book[1]} author ID updated to {new_auth_ID}")

                    title_update = input(f"Would you like to update {book[1]}'s "
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

    book = id_search(cursor)

    while True:

        print(f"Are you sure you wish to delete {book[1]} from the database?")
        choice = input("(y/n): ").lower()
        if choice == "n":
            break
        elif choice == "y":
            cursor.execute('''
                            DELETE FROM book
                            WHERE id = ?''',
                            (id,))
            print(f"{book[1]} has been deleted")
            db.commit()
            break
        else:
            print("Invalid option. Try again.")
            continue


def search_books(cursor):
    while True:
        print("\n**** Search Book ****\n")

        book = id_search(cursor)

        if book is None:
            return

        print(f"\nBook ID:                    {book[0]}")
        print(f"Title:                      {book[1]}")
        print(f"Author ID:                  {book[2]}")
        print(f"Quantity:                   {book[3]}\n")

        while True:
            again = input("\nSearch again? (y/n): ")
            if again == "y":
                break
            elif again == "n":
                return
            else:
                print("\nInvalid option. Try again.\n")


def view_details(cursor):
    cursor.execute('''
        SELECT book.title, author.name, author.country
        FROM book
        INNER JOIN author
        ON book.authorID = author.ID
        ''')
    
    details = cursor.fetchall()

    for title, author, country in details:
        print(f'''
Title:        {title}
Author:       {author}
Country:      {country}''')
        print("-" * 50)
    

   
while True:
    try:
        menu = int(input('''
        Please select and option:
        1. Enter book
        2. Update book
        3. Delete book
        4. Search books
        5. View details of all books
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
        elif menu == 5:
            view_details(cursor)
        elif menu == 0:
            db.close()
            sys.exit()
        else:
            print("Please enter a valid option")
    
    except ValueError:
        print("Please enter a valid option.")