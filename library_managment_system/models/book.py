# models/book.py
class Book:
    def __init__(self, book_id: int, title: str, author: str, category: str, is_issued: bool = False):
        self.book_id = int(book_id)
        self.title = title
        self.author = author
        self.category = category
        self.is_issued = bool(is_issued)

    def issue(self):
        if self.is_issued:
            return False
        self.is_issued = True
        return True

    def return_book(self):
        if not self.is_issued:
            return False
        self.is_issued = False
        return True

    def to_dict(self) -> dict:
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "category": self.category,
            "is_issued": self.is_issued
        }

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            book_id=d.get("book_id"),
            title=d.get("title", ""),
            author=d.get("author", ""),
            category=d.get("category", ""),
            is_issued=d.get("is_issued", False)
        )

    def __str__(self):
        status = "Issued" if self.is_issued else "Available"
        return f"[{self.book_id}] {self.title} — {self.author} | {self.category} | {status}"
