# models/user.py
class User:
    def __init__(self, user_id: int, name: str, borrowed_books=None):
        self.user_id = int(user_id)
        self.name = name
        # store as list of ints
        self.borrowed_books = list(borrowed_books) if borrowed_books else []

    def borrow_book(self, book_id: int) -> bool:
        book_id = int(book_id)
        if book_id in self.borrowed_books:
            return False
        self.borrowed_books.append(book_id)
        return True

    def return_book(self, book_id: int) -> bool:
        book_id = int(book_id)
        if book_id not in self.borrowed_books:
            return False
        self.borrowed_books.remove(book_id)
        return True
    
    # Object → Dictionary
    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "borrowed_books": self.borrowed_books
        }
        
    # Dictionary → Object
    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            user_id=d.get("user_id"),
            name=d.get("name", ""),
            borrowed_books=d.get("borrowed_books", [])
        )

    def __str__(self):
        return f"[{self.user_id}] {self.name} — Borrowed: {self.borrowed_books}"
