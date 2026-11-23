"""
Public Library Management System
A simple OOP implementation based on a class diagram.

Author: Michael Delight Simon
Program: Information System Engineering
University: Near East University
"""

from datetime import datetime, timedelta


class Author:
    def __init__(self, author_id: str, name: str, nationality: str):
        self.author_id = author_id
        self.name = name
        self.nationality = nationality
        self.books = []

    def add_book(self, book):
        if book not in self.books:
            self.books.append(book)

    def get_books(self):
        return self.books

    def __str__(self):
        return f"{self.name} ({self.nationality})"


class Category:
    def __init__(self, category_id: str, name: str, description: str = ""):
        self.category_id = category_id
        self.name = name
        self.description = description

    def __str__(self):
        return self.name


class Book:
    def __init__(self, isbn: str, title: str, author: Author, publisher: str, year: int, category: Category, copies: int = 1):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publisher = publisher
        self.year = year
        self.category = category
        self.available_copies = copies
        author.add_book(self)

    def is_available(self) -> bool:
        return self.available_copies > 0

    def decrease_copies(self):
        if self.available_copies > 0:
            self.available_copies -= 1

    def increase_copies(self):
        self.available_copies += 1

    def __str__(self):
        return f"'{self.title}' by {self.author.name} ({self.year})"


class Loan:
    def __init__(self, loan_id: str, member, book: Book, borrow_days: int = 14):
        self.loan_id = loan_id
        self.member = member
        self.book = book
        self.borrow_date = datetime.now()
        self.due_date = self.borrow_date + timedelta(days=borrow_days)
        self.return_date = None
        self.fine_amount = 0.0

    def is_overdue(self) -> bool:
        if self.return_date:
            return self.return_date > self.due_date
        return datetime.now() > self.due_date

    def calculate_fine(self, fine_per_day: float = 0.50) -> float:
        if not self.is_overdue():
            return 0.0
        if self.return_date:
            overdue_days = (self.return_date - self.due_date).days
        else:
            overdue_days = (datetime.now() - self.due_date).days
        self.fine_amount = max(0, overdue_days) * fine_per_day
        return self.fine_amount

    def return_book(self):
        self.return_date = datetime.now()
        self.book.increase_copies()
        self.calculate_fine()

    def __str__(self):
        status = "Returned" if self.return_date else "Active"
        return f"Loan {self.loan_id}: {self.book.title} | {status} | Due: {self.due_date.strftime('%Y-%m-%d')}"


class Member:
    def __init__(self, member_id: str, name: str, email: str, phone: str, address: str, membership_type: str = "Regular"):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.membership_type = membership_type
        self.join_date = datetime.now()
        self.loans = []

    def borrow_book(self, book: Book) -> Loan | None:
        if not book.is_available():
            print(f"Sorry, '{book.title}' is currently not available.")
            return None
        loan_id = f"LN-{len(self.loans) + 1:04d}"
        loan = Loan(loan_id, self, book)
        book.decrease_copies()
        self.loans.append(loan)
        print(f"{self.name} successfully borrowed '{book.title}'.")
        return loan

    def return_book(self, loan: Loan):
        if loan in self.loans and not loan.return_date:
            loan.return_book()
            print(f"{self.name} returned '{loan.book.title}'. Fine: ${loan.fine_amount:.2f}")

    def view_loans(self):
        if not self.loans:
            print(f"{self.name} has no loans.")
            return
        print(f"\nLoans for {self.name}:")
        for loan in self.loans:
            print(f"  - {loan}")

    def pay_fine(self, amount: float):
        total_fine = sum(loan.fine_amount for loan in self.loans if not loan.return_date)
        if amount >= total_fine:
            print(f"Fine of ${total_fine:.2f} paid successfully.")
        else:
            print(f"Partial payment of ${amount:.2f} received. Remaining: ${total_fine - amount:.2f}")

    def __str__(self):
        return f"Member {self.member_id}: {self.name} ({self.membership_type})"


class Librarian:
    def __init__(self, employee_id: str, name: str, email: str):
        self.employee_id = employee_id
        self.name = name
        self.email = email
        self.managed_books = []
        self.registered_members = []

    def add_book(self, book: Book):
        self.managed_books.append(book)
        print(f"Librarian {self.name} added book: {book.title}")

    def remove_book(self, book: Book):
        if book in self.managed_books:
            self.managed_books.remove(book)
            print(f"Book '{book.title}' removed from catalog.")

    def register_member(self, member: Member):
        self.registered_members.append(member)
        print(f"Member '{member.name}' registered successfully.")

    def process_return(self, loan: Loan):
        if loan.member in self.registered_members:
            loan.member.return_book(loan)

    def __str__(self):
        return f"Librarian {self.employee_id}: {self.name}"


# ==================== DEMO / SAMPLE USAGE ====================
def demo():
    print("=" * 60)
    print("PUBLIC LIBRARY MANAGEMENT SYSTEM - DEMO")
    print("=" * 60)

    # Create author and category
    author1 = Author("A001", "George Orwell", "British")
    category1 = Category("C001", "Fiction", "Novels and short stories")

    # Create a book
    book1 = Book(
        isbn="978-0451524935",
        title="1984",
        author=author1,
        publisher="Signet Classics",
        year=1949,
        category=category1,
        copies=3
    )

    # Create librarian and member
    librarian = Librarian("L001", "Sarah Johnson", "sarah@library.org")
    member1 = Member(
        member_id="M001",
        name="Michael Delight Simon",
        email="michael.simon@neu.edu.tr",
        phone="+90 123 456 7890",
        address="Near East University, Nicosia",
        membership_type="Student"
    )

    # Librarian actions
    librarian.add_book(book1)
    librarian.register_member(member1)

    print("\n" + "-" * 40)
    print("BORROWING PROCESS")
    print("-" * 40)

    # Member borrows the book
    loan1 = member1.borrow_book(book1)
    member1.view_loans()

    print(f"\nBook availability after borrowing: {book1.available_copies} copies left")

    print("\n" + "-" * 40)
    print("RETURNING PROCESS")
    print("-" * 40)

    # Return the book
    if loan1:
        librarian.process_return(loan1)
        member1.view_loans()

    print("\n" + "=" * 60)
    print("DEMO COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    demo()
