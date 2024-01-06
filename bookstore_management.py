# Import SQLite library
import sqlite3


# Connect to SQLite database called 'ebookstore.db'
# Get a cursor object
db = sqlite3.connect("ebookstore.db")
cursor = db.cursor()


# Function to create the database and table called 'books'
# If table does not exist, execute SQL query to create table with columns called 'id', 'title', 'author', 'quantity'
# Commit changes to the database
# Rollback and raise e if any change if something goes wrong
def create_books_table():
    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT,
            author TEXT,
            quantity INTEGER
            )
        """
        )
        db.commit()
        populate_table()
    except Exception as e:
        db.rollback()
        raise e


# Function to populate 'books' table
# Commit changes to the database
# Rollback and raise e if any change if something goes wrong
def populate_table():
    try:
        cursor.executemany(
            """
            INSERT INTO books(id, title, author, quantity)
            VALUES (?, ?, ?, ?)
            """,
            [
                (3001, "A Tale of Two Cities", "Charles Dickens", 30),
                (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
                (3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25),
                (3004, "The Lord of the Rings", "J.R.R. Tolkien", 37),
                (3005, "Alice in Wonderland", "Lewis Carroll", 12),
            ],
        )
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


# Function to add a new book to the database
# Obtain input from user
# Execute SQL query to insert new book into table
# Commit changes to the database
# Display success message
# Rollback and raise e if any change if something goes wrong
def add_book():
    try:
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        quantity = int(input("Enter quantity: "))

        cursor.execute(
            """
            INSERT INTO books(title, author, quantity)
            VALUES (?, ?, ?)
            """,
            (title, author, quantity),
        )
        db.commit()
        print("Book added successfully!")
    except Exception as e:
        db.rollback()
        raise e


# Function to update book information in the database
# Obtain input from user
# Execute SQL query to update book in table
# Commit changes to the database
# Display success message
# Rollback and raise e if any change if something goes wrong
def update_book():
    try:
        book_id = int(input("Enter the ID of the book to update: "))
        new_title = input("Enter new title (press Enter to skip): ")
        new_author = input("Enter new author(press Enter to skip): ")
        new_quantity = input("Enter new quantity (press Enter to skip): ")

        update_query = "UPDATE books SET"
        update_values = []

        if new_title:
            update_query += "title=?, "
            update_values.append(new_title)
        if new_author:
            update_query += "author=?, "
            update_values.append(new_author)
        if new_quantity:
            update_query += "quantity=?"
            update_values.append(new_quantity)

        if not update_values:
            print("No values provided for update.")
            return

        update_values.append(book_id)
        update_query = update_query.rstrip(",") + " WHERE id=?"

        cursor.execute(update_query, update_values)
        db.commit()
        print("Book updated successfully!")
    except Exception as e:
        db.rollback()
        raise e


# Function to delete a book from the database
# Obtain input from user
# Execute SQL query to delete book from table
# Commit changes to the database
# Display success message
# Rollback and raise e if any change if something goes wrong
def delete_book():
    try:
        book_id = int(input("Enter the ID of the book to delete: "))
        cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
        db.commit()
        print("Book deleted successfully!")
    except Exception as e:
        db.rollback()
        raise e


# Function to search for a specific book in the database
# Obtain input from user
# Execute SQL query to search book in table
# Rollback and raise e if any change if something goes wrong
def search_book():
    try:
        search_term = input("Enter title or author to search: ")
        cursor.execute(
            "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
            ("%" + search_term + "%", "%" + search_term + "%"),
        )
        books = cursor.fetchall()

        if not books:
            print("No books found.")
        else:
            for book in books:
                print("ID:", book[0])
                print("Title:", book[1])
                print("Author:", book[2])
                print("Quantity:", book[3])
                print()
    except Exception as e:
        db.rollback()
        raise e


# Main function to present the user with a menu
# Display menu options to user
# Proceed based on user input
# Close database connection when exiting program
def main():
    create_books_table()
    print("\n*** Welcome to the Bookstore Database Management System! ***")
    while True:
        print("\nMenu:")
        print("1. Enter book")
        print("2. Update book")
        print("3. Delete book")
        print("4. Search books")
        print("0. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_book()
            db.commit()
        elif choice == "2":
            update_book()
            db.commit()
        elif choice == "3":
            delete_book()
            db.commit()
        elif choice == "4":
            search_book()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please enter a valid option.")

    db.close()

if __name__ == "__main__":
    main()