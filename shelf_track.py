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
    print("\nEnter new book\n")
    while True:
        try:

            id = int(input("Please enter the books 4 digit ID (must not start with 0): "))
            title =  input("Please enter the books title: ")
            authorid = int(input("Please enter the 4 digit Author ID (must not start with 0): "))
            qty = int(input("Please enter the total quantity: "))

            if id < 1000:
                print("The ID must be 4 digits and not start with 0")
            elif authorid < 1000:
                print("The Author ID must be 4 digits and not start with 0")
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

while True:
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
        print("2")
    elif menu == 3:
        print("3")
    elif menu == 4:
        print("4")
    elif menu == 0:
        db.close()
        sys.exit()
    else:
        print("Please enter a valid option")