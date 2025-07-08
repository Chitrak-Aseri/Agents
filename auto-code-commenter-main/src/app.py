import os
import json

class Book:
    """Represents a book in the library system.
    
    Attributes:
        book_id (str): Unique identifier for the book
        title (str): Title of the book
        author (str): Author of the book
        copies (int): Number of available copies
    """
    def __init__(self, book_id, title, author, copies):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.copies = copies

    def to_dict(self):
        """Convert Book object to dictionary for JSON serialization."""
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'copies': self.copies
        }

class Library:
    """Manages the library's book collection and operations.
    
    Attributes:
        db_file (str): Path to JSON database file
        books (list): List of Book objects in the library
    """
    def __init__(self, db_file='library_db.json'):
        self.db_file = db_file
        self.books = self.load_books()

    def load_books(self):
        """Load books from JSON database file. Creates empty file if none exists."""
        if not os.path.exists(self.db_file):
            return []
        with open(self.db_file, 'r') as file:
            data = json.load(file)
            return [Book(**book) for book in data]

    def save_books(self):
        """Save current book collection to JSON database file."""
        with open(self.db_file, 'w') as file:
            json.dump([book.to_dict() for book in self.books], file, indent=4)

    def add_book(self, book):
        """Add a new book or update copies if book already exists.
        
        Args:
            book (Book): Book object to add or update
        """
        for b in self.books:
            if b.book_id == book.book_id:
                b.copies += book.copies
                print(f"Updated existing book: {b.title}")
                self.save_books()
                return
        self.books.append(book)
        self.save_books()
        print(f"Added new book: {book.title}")

    def remove_book(self, book_id):
        """Remove a book from the library by its ID.
        
        Args:
            book_id (str): ID of the book to remove
        """
        for b in self.books:
            if b.book_id == book_id:
                self.books.remove(b)
                self.save_books()
                print(f"Removed book: {b.title}")
                return
        print("Book ID not found.")

    def list_books(self):
        """Display all books in the library with their details."""
        if not self.books:
            print("No books in the library.")
            return
        print("Available Books:")
        for b in self.books:
            print(f"{b.book_id} | {b.title} by {b.author} - {b.copies} copies")

    def borrow_book(self, book_id):
        """Borrow a book by decreasing its available copies.
        
        Args:
            book_id (str): ID of the book to borrow
        """
        for b in self.books:
            if b.book_id == book_id:
                if b.copies > 0:
                    b.copies -= 1
                    self.save_books()
                    print(f"You borrowed: {b.title}")
                    return
                else:
                    print("Sorry, that book is currently unavailable.")
                    return
        print("Book ID not found.")

    def return_book(self, book_id):
        """Return a book by increasing its available copies.
        
        Args:
            book_id (str): ID of the book to return
        """
        for b in self.books:
            if b.book_id == book_id:
                b.copies += 1
                self.save_books()
                print(f"You returned: {b.title}")
                return
        print("Book ID not found.")

def main():
    """Main entry point for the library management system.
    
    Provides a menu-driven interface for library operations.
    """
    library = Library()

    while True:
        print("\n--- Library Menu ---")
        print("1. List Books")
        print("2. Add Book")
        print("3. Remove Book")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            library.list_books()
        elif choice == '2':
            book_id = input("Enter Book ID: ")
            title = input("Enter Title: ")
            author = input("Enter Author: ")
            try:
                copies = int(input("Enter number of copies: "))
                book = Book(book_id, title, author, copies)
                library.add_book(book)
            except ValueError:
                print("Invalid number of copies.")
        elif choice == '3':
            book_id = input("Enter Book ID to remove: ")
            library.remove_book(book_id)
        elif choice == '4':
            book_id = input("Enter Book ID to borrow: ")
            library.borrow_book(book_id)
        elif choice == '5':
            book_id = input("Enter Book ID to return: ")
            library.return_book(book_id)
        elif choice == '6':
            print("Exiting Library System.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()