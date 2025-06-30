# database_capstone_project

HyperionDev Database Capstone Project

This is a project for my HyperionDev Software engineering bootcamp.

The aim is to create a bookshop application to track book inventory.

Developed as part of a practical SQL + Python project to demonstrate database integration, user input handling, and application logic.

# 📚 Shelf Track — Bookstore Inventory Management

## Overview

**Shelf Track** is a command-line Python program designed to assist bookstore clerks in managing book inventory efficiently. It uses a SQLite relational database to store and retrieve data about books and their authors. The system provides full CRUD functionality (Create, Read, Update, Delete), along with integrated data validation and clean, user-friendly display formatting.

This project is divided into three main phases:

1. **Basic inventory control**
2. **Expanded relational data with an author table**
3. **Code refinement, validation, and best practices**

---

## 📁 Features

The program presents the following menu options:

1. Enter book
2. Update book
3. Delete book
4. Search books
5. View details of all books
6. Exit

### 🔧 1. Enter Book

Allows the clerk to:

- Input a **4-digit unique Book ID**
- Provide the **book title**
- Input a **4-digit Author ID** (linked to the author table)
- Enter the **quantity in stock**

### ✏️ 2. Update Book

Default action is to update the quantity of a book. The user can also choose to:

- Update the **title**
- Update the **author ID**
- Update the **author name**
- Update the **author country**

Once a book is selected, the program displays:

- Current book title
- Current book quantity

It then allows updates to:

- Book **title**
- Author **ID**
- Author **name**
- Author **country**

All changes are committed back to the database.

### ❌ 3. Delete Book

Removes a book from the database by ID.

### 🔍 4. Search Books

Allows the clerk to find a book using its ID. Displays:

- Book ID
- Title
- Author ID
- Quantity

User has the option to **search again**.

### 📖 5. View Details of All Books

Displays **title, author name, and author country** in a user-friendly format.  
Data is pulled from both `book` and `author` tables using an `INNER JOIN`.

Example Output:

Title: Harry Potter and the Goblet of Fire
Author: J.K. Rowling
Country: England

---

## 🗃️ Database Structure

Two tables are used:

### `book`

| Column     | Type    | Notes                    |
| ---------- | ------- | ------------------------ |
| `id`       | INTEGER | Primary key (4-digit ID) |
| `title`    | TEXT    | Book title               |
| `authorID` | INTEGER | Foreign key              |
| `qty`      | INTEGER | Stock quantity           |

### `author`

| Column    | Type    | Notes                            |
| --------- | ------- | -------------------------------- |
| `id`      | INTEGER | Primary key (matches `authorID`) |
| `name`    | TEXT    | Author name                      |
| `country` | TEXT    | Author country                   |

---

## ✅ Validation & Error Handling

- Ensures all IDs are **4-digit integers** not starting with 0
- Prevents duplicate book IDs via integrity checks
- All input is wrapped in `try-except` blocks to catch:
  - `ValueError` for invalid input types
  - `sqlite3.IntegrityError` for primary key violations
  - General `sqlite3.Error` for other DB issues

---

## 📦 Technologies Used

- **Python 3.x**
- **SQLite3**
- **Standard Library only** (no external dependencies)

---

## 🧱 Setup

1. Clone the repository
2. Run the Python file:
   ```bash
   python shelf_track.py
   ```
3. The database (books_db.db or similar) will be created if it does not exist.

## 🧼 Best Practices Followed

- Modular code design using reusable functions
- Data validation on all user input
- Clear separation of book and author logic
- Use of INNER JOIN for accurate cross-table queries
- Graceful error handling and feedback for the user

## Feedback

To be added once project has been reviewed.
