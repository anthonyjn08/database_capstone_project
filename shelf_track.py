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

    Input:
    id: (int) this is the book ID and primary key

    Output:
    book: returns the data of the book if found.
    '''

    # Loop to validate ID
    while True:
        try:
            id = int(input("\nPlease enter the book id or '-1' for main menu: "))

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
                           INNER JOIN author
                           ON book.authorid = author.id
                           WHERE book.id = ?''',
                           (id,))
            book = cursor.fetchone()

            # If book doesn't exist, provide error message.
            if book is None:
                print("\nBook not found. Please try again.\n")
                continue

            # Return the book if found.
            return book

        except ValueError:
                print("\nPlease enter data in correct format!\n")


def update_book(cursor):
    '''
    Function update_book
    This function allows users to update the book quantity, title, authorID
    from the book table, and an inner join on the book authorID to the field
    to the author ID field in the author table. The user can then update the
    author name and country. If authorID is updated in the book table, the data
    is refreshed to ensure it re-syncs with the author table.

    Inputs:
    qty: (int) new quantity if updated
    new_auth_ID: (int) new author ID. Checked and validated
    new_title: (TEXT) new title of book.
    new_name: (TEXT) new author name
    new_ctry: (TEXT) new author country
    '''
    print("\n**** Update book ****\n")

    # Create book object using id_search function
    book = id_search(cursor)

    # Variables for ID and authorID for inner join on tables
    id = book[0]
    authorid = book[4]

    # Create new_auth_id variable to use to check if book data needs refreshing
    new_auth_ID = None


    while True:
        try:
            # Print book title to ensure this is the correct book before progressing
            print(f"\n** Updating {book[1]} **\n")

            # Allow user to confirm and proceed or make another selection
            confirm = input("\nIs this correct? (y/n): ").lower()

            if confirm == "y":
                while True:
                    try:
                        # Show current quantity. Ask user to enter number to update
                        # Or progress to other updates if they enter -1
                        qty = int(input(f"Current quantity: {book[3]}. Enter new quantity "
                                        "or '-1' to proceed to more update choices: "))
                        if qty == -1:
                            pass
                        else:
                            cursor.execute('''
                                        UPDATE book
                                        SET qty = ?
                                        WHERE id = ?''',
                                        (qty, id))
                            
                            # Print confirmation message and save changes
                            print(f"{book[1]} quantity updated to {qty}")
                            db.commit()
                    except ValueError:
                        print("\nInvalid input! Please enter a whole number or -1.\n")
                        continue
                    break

                # AuthorID update
                authorID_update = input(f"{book[1]} authorID is {authorid}? "
                                                    f" Update? (y/n): ").lower()

                # Create loop to validate authorID is int and 4 digits
                while True:
                    try:
                        if authorID_update == "y":
                            new_auth_ID = int(input("Please enter the new 4 "
                                                    "digit author ID "
                                                    "(must not start with 0)"))
                            if new_auth_ID < 1000 or new_auth_ID > 9999:
                                print("\nThe ID must be 4 digits and "
                                      "not start with 0\n")
                            else:
                                cursor.execute('''
                                            UPDATE book
                                            SET authorID = ?
                                            WHERE id = ?''',
                                            (new_auth_ID, id))
                                print(f"\n{book[1]} author ID updated to "
                                      "{new_auth_ID}.\n")
                                db.commit()
                                break
                        elif authorID_update == "n":
                            break
                        else:
                            print("\nInvalid option. Try again.\n")
                            continue

                    except ValueError:
                        print("\nInvalid input. Author ID must be a "
                            "4 digit number not starting with 0.\n")
                        continue

                # Title update

                while True:
                    title_update = input(f"\nBook title: {book[1]}. "
                                         "Update? (y/n): ").lower()
                    if title_update == "y":
                        new_title = input("\nPlease enter the new book title: ")
                        cursor.execute('''
                                    UPDATE book
                                    SET title = ?
                                    WHERE id = ?''',
                                    (new_title, id))
                        
                        print(f"\nTitle updated to {new_title}.\n")
                        db.commit()
                        break
                    elif title_update == "n":
                        break
                    else:
                        print("\nInvalid option. Try again.\n")
                        continue

                # Refresh author ID and book data if authorID has been changed
                if new_auth_ID is not None:
                    authorid = new_auth_ID
                    cursor.execute('''
                                SELECT *
                                FROM book
                                INNER JOIN author
                                ON book.authorID = author.id
                                WHERE book.id = ?''',
                                (id,))
                    book = cursor.fetchone()

                # Author name update

                while True:
                    author_name = input(f"\nAuthor name is: {book[5]}. "
                                        "Update (y/n): ").lower()
                    if author_name == "y":
                        new_name = input("\nPlease enter author name: ")
                        cursor.execute('''
                                        UPDATE author
                                        SET name = ?
                                        WHERE id = ?''',
                                        (new_name, authorid))
                        print(f"\n{book[1]} author name updated to {new_name}\n")
                        db.commit()
                        break
                    elif author_name == "n":
                        break
                    else:
                        print("\nInvalid option. Try again.\n")
                        continue

                # Author country update 
                while True:
                    author_ctry = input(f"\nAuthor country is {book[6]}. "
                                        "Update? (y/n): ").lower()
                    if author_ctry == "y":
                        new_ctry = input("\nPlease enter author country: ")
                        cursor.execute('''
                                        UPDATE author
                                        SET country = ?
                                        WHERE id = ?''',
                                        (new_ctry, authorid))
                        print(f"\n{book[1]} author country updated to {new_ctry}\n")
                        db.commit()
                        break
                    elif author_ctry == "n":
                        break
                    else:
                        print("\nInvalid option. Try again.\n")
                        continue
                                
                return
            
            # If id provided is not the right one, asks for ID again
            # or provides option to return to main meny
            elif confirm == "n":
                id_search(cursor)
            else:
                print("\nInvalid Option. Try again.\n")
            
            break
        except sqlite3.IntegrityError as e:
            print("Database integrity error.", e)


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
            print(f"\n{book[1]} has been deleted\n")
            db.commit()
            break
        else:
            print("\nInvalid option. Try again.\n")
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

    print("**** View all book details ****")
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
            print("\nPlease enter a valid option\n")
    
    except ValueError:
        print("\nPlease enter a valid option.\n")