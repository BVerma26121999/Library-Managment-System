# Library-Managment-System
Library Management System (CLI) Simple command-line library management system written in Python. Provides basic functionality to add/remove/search books, manage users, issue and return books, and persist data as JSON.

Features

Add and remove books. Search and list books. Add and list users. Issue and return books to/from users. Persist data to books.json and users.json. Requirements

Python 3.8 or newer No external dependencies (standard library only) Project Structure

main.py: CLI entry point and menu loop. book.py: Book model. user.py: User model. library.py: Core library logic (add/search/issue/return/save). books.json: Stored books data (created/updated by the app). users.json: Stored users data (created/updated by the app). Setup

(Optional) Create and activate a virtual environment: Windows PowerShell: No packages to install. Run From the project root run:

Follow the menu to perform actions.

Usage Example

Start the app: python main.py Choose 1 to add a book, enter Title/Author/Category. Choose 5 to add a user. Choose 7 to issue a book (provide User ID and Book ID). Choose 8 to return a book. Choose 9 to save data manually, or 0 to save and exit. Data Files

books.json and users.json are used for persistence. If those files are missing, the application will create them when saving.
