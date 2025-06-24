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
if book_count == 0:
    cursor.executemany(
        '''
        INSERT INTO book(id, title, authorID, qty)
        VALUES(?, ?, ?, ?)
''', books
    )

while True:
    menu = input('''
    Please select and option:
    1. Enter book
    2. Update book
    3. Delete book
    4. Search books
    0. Exit
    : ''')

    if menu == 1:
        print("1")
    elif menu == 2:
        print("2")
    elif menu == 3:
        print("3")
    elif menu == 4:
        print("4")
    elif menu == 0:
        sys.exit()
    else:
        print("Please enter a valid option")