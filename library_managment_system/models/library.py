# models/library.py
import json
import os
from typing import Dict, List, Tuple, Optional
from .book import Book
from .user import User

class Library:
    """
    Main Library Controller.
    Handles:
    - Books & Users (in dictionaries)
    - JSON persistence
    - Search, Issue, Return operations
    """

    def __init__(self, base_dir: Optional[str] = None):

        # --------------- Fix: Safe Base Directory ---------------
        # Works regardless of where you run main.py from
        if base_dir is None:
            base_dir = os.getcwd()

        self.base_dir = base_dir
        self.data_dir = os.path.join(base_dir, "data")
        os.makedirs(self.data_dir, exist_ok=True)

        self.book_file = os.path.join(self.data_dir, "books.json")
        self.user_file = os.path.join(self.data_dir, "users.json")

        # --------------- Internal Data Containers ---------------
        self.books: Dict[int, Book] = {}
        self.users: Dict[int, User] = {}

        # Load data safely
        self.load_data()

    # ============================================================
    #                         DATA LOADING
    # ============================================================
    def _read_json(self, path: str):
        """Read JSON safely and return list. Handles empty/corrupted files."""
        try:
            if not os.path.exists(path) or os.path.getsize(path) == 0:
                return []  # empty file
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []  # corrupted JSON fallback

    def load_data(self):
        """Load books & users from JSON into dictionaries."""

        # ---------- Load Books ----------
        books_list = self._read_json(self.book_file)
        self.books = {
            book_dict["book_id"]: Book.from_dict(book_dict)
            for book_dict in books_list
            if "book_id" in book_dict
        }

        # ---------- Load Users ----------
        users_list = self._read_json(self.user_file)
        self.users = {
            user_dict["user_id"]: User.from_dict(user_dict)
            for user_dict in users_list
            if "user_id" in user_dict
        }

    # ============================================================
    #                         DATA SAVING
    # ============================================================
    def save_data(self):
        """Save current library state to JSON."""
        # Convert dictionaries → lists
        books_list = [book.to_dict() for book in self.books.values()]
        users_list = [user.to_dict() for user in self.users.values()]

        # Save safely
        with open(self.book_file, "w", encoding="utf-8") as f:
            json.dump(books_list, f, indent=2, ensure_ascii=False)

        with open(self.user_file, "w", encoding="utf-8") as f:
            json.dump(users_list, f, indent=2, ensure_ascii=False)

    # ============================================================
    #                     HELPER / ID GENERATORS
    # ============================================================
    def _next_book_id(self) -> int:
        return max(self.books.keys(), default=0) + 1

    def _next_user_id(self) -> int:
        return max(self.users.keys(), default=0) + 1

    # ============================================================
    #                     BOOK OPERATIONS
    # ============================================================
    def add_book(self, title: str, author: str, category: str) -> Book:
        bid = self._next_book_id()
        book = Book(bid, title, author, category)
        self.books[bid] = book
        self.save_data()
        return book

    def remove_book(self, book_id: int) -> bool:
        try:
            book_id = int(book_id)
        except ValueError:
            return False

        book = self.books.get(book_id)
        if not book or book.is_issued:
            return False

        del self.books[book_id]
        self.save_data()
        return True

    def get_book(self, book_id: int) -> Optional[Book]:
        try:
            return self.books.get(int(book_id))
        except ValueError:
            return None

    def show_all_books(self) -> List[Book]:
        return list(self.books.values())

    # ============================================================
    #                     USER OPERATIONS
    # ============================================================
    def add_user(self, name: str) -> User:
        uid = self._next_user_id()
        user = User(uid, name)
        self.users[uid] = user
        self.save_data()
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        try:
            return self.users.get(int(user_id))
        except ValueError:
            return None

    def show_all_users(self) -> List[User]:
        return list(self.users.values())

    # ============================================================
    #                          SEARCH
    # ============================================================
    def search_books(self, query: str) -> List[Book]:
        query = (query or "").strip().lower()
        if not query:
            return []

        results = []
        for book in self.books.values():
            if (
                query in str(book.book_id).lower()
                or query in book.title.lower()
                or query in book.author.lower()
                or query in book.category.lower()
            ):
                results.append(book)
        return results

    # ============================================================
    #                     ISSUE / RETURN LOGIC
    # ============================================================
    def issue_book(self, user_id: int, book_id: int) -> Tuple[bool, str]:
        user = self.get_user(user_id)
        if not user:
            return False, "User not found."

        book = self.get_book(book_id)
        if not book:
            return False, "Book not found."

        if book.is_issued:
            return False, "Book is already issued."

        # Book issue attempt
        if not book.issue():
            return False, "Failed to issue the book."

        # User borrow attempt
        if not user.borrow_book(book_id):
            book.return_book()  # rollback
            return False, "User already borrowed this book."

        self.save_data()
        return True, "Book issued successfully."

    def return_book(self, user_id: int, book_id: int) -> Tuple[bool, str]:
        user = self.get_user(user_id)
        if not user:
            return False, "User not found."

        book = self.get_book(book_id)
        if not book:
            return False, "Book not found."

        if book_id not in user.borrowed_books:
            return False, "This user did not borrow this book."

        # Remove from user
        if not user.return_book(book_id):
            return False, "Failed to return the book from user."

        # Change book state
        if not book.return_book():
            user.borrow_book(book_id)  # rollback
            return False, "Failed to update book return status."

        self.save_data()
        return True, "Book returned successfully."
