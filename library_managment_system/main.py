# main.py
import os
from models.library import Library


def input_non_empty(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Input cannot be empty. Try again.")


def print_books(books):
    if not books:
        print("No books found.")
        return
    for b in books:
        print(b)


def print_users(users):
    if not users:
        print("No users found.")
        return
    for u in users:
        print(u)


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    library = Library(base_dir=base_dir)

    
    
    
    MENU = """
---- Library Menu ----
1. Add Book
2. Remove Book
3. View All Books
4. Search Books
5. Add User
6. View All Users
7. Issue Book
8. Return Book
9. Save Data
0. Exit
----------------------
"""

    while True:
        print(MENU)
        choice = input("Enter choice: ").strip()

        if choice == "1":
            title = input_non_empty("Title: ")
            author = input_non_empty("Author: ")
            category = input_non_empty("Category: ")
            book = library.add_book(title=title, author=author, category=category)
            print(f"Added: {book}")

        elif choice == "2":
            bid = input_non_empty("Book ID to remove: ")
            try:
                ok = library.remove_book(int(bid))
            except ValueError:
                ok = False
            if ok:
                print("Book removed.")
            else:
                print("Failed to remove book (either not found or issued).")

        elif choice == "3":
            books = library.show_all_books()
            print_books(books)

        elif choice == "4":
            q = input("Search query (title/author/category/id): ").strip()
            results = library.search_books(q)
            print_books(results)

        elif choice == "5":
            name = input_non_empty("User name: ")
            user = library.add_user(name)
            print(f"Added user: {user}")

        elif choice == "6":
            users = library.show_all_users()
            print_users(users)

        elif choice == "7":
            try:
                uid = int(input_non_empty("User ID: "))
                bid = int(input_non_empty("Book ID: "))
            except ValueError:
                print("IDs must be numbers.")
                continue
            ok, msg = library.issue_book(uid, bid)
            print(msg)

        elif choice == "8":
            try:
                uid = int(input_non_empty("User ID: "))
                bid = int(input_non_empty("Book ID: "))
            except ValueError:
                print("IDs must be numbers.")
                continue
            ok, msg = library.return_book(uid, bid)
            print(msg)

        elif choice == "9":
            library.save_data()
            print("Data saved to disk.")

        elif choice == "0":
            library.save_data()
            print("Data saved. Exiting.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
