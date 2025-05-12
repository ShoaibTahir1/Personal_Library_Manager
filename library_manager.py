import json
import os
import sys
from colorama import init, Fore, Style
import streamlit as st

# Initialize colorama for colored terminal output
init()

data_file = 'library.txt'

# Function to load the library data from a file
def load_library():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    else:
        return []

# Function to save the library data to a file
def save_library(library):
    with open(data_file, 'w') as file:
        json.dump(library, file)

# Function to add a new book to the library
def add_book(library):
    print("\n" + Fore.CYAN + "=== Add a Book ===" + Style.RESET_ALL)
    title = input("Enter the book title: ")
    author = input("Enter the author: ")

    # Validate publication year input
    while True:
        try:
            year = int(input("Enter the publication year: "))
            break
        except ValueError:
            print(Fore.RED + "Please enter a valid year (number)." + Style.RESET_ALL)

    genre = input("Enter the genre: ")
    read_input = input("Have you read this book? (yes/no): ").lower()
    read = read_input == "yes"

    # Create a new book dictionary
    new_book = {
        'title': title,
        'author': author,
        'year': year,
        'genre': genre,
        'read': read
    }
    
    # Add book to the library
    library.append(new_book)
    save_library(library)
    print(Fore.GREEN + "Book added successfully!" + Style.RESET_ALL)

# Function to remove a book by title
def remove_book(library):
    print("\n" + Fore.CYAN + "=== Remove a Book ===" + Style.RESET_ALL)
    title = input("Enter the title of the book to remove: ")
    initial_length = len(library)

    # Remove book if title matches
    library = [book for book in library if book['title'].lower() != title.lower()]
    if len(library) < initial_length:
        save_library(library)
        print(Fore.GREEN + "Book removed successfully!" + Style.RESET_ALL)
    else:
        print(Fore.RED + f"Book '{title}' not found!" + Style.RESET_ALL)

    return library

# Function to search for a book by title or author
def search_library(library):
    print("\n" + Fore.CYAN + "=== Search for a Book ===" + Style.RESET_ALL)
    print("Search by:")
    print("1. Title")
    print("2. Author")

    search_choice = input("Enter your choice: ")

    if search_choice == "1":
        search_by = "title"
    elif search_choice == "2":
        search_by = "author"
    else:
        print(Fore.RED + "Invalid choice." + Style.RESET_ALL)
        return

    search_term = input(f"Enter the {search_by}: ").lower()

    # Find matching books
    results = [book for book in library if search_term in book[search_by].lower()]

    if results:
        print("\n" + Fore.YELLOW + "Matching Books:" + Style.RESET_ALL)
        for i, book in enumerate(results, 1):
            status = "Read" if book['read'] else "Unread"
            print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
    else:
        print(Fore.RED + f"No books found matching '{search_term}' in {search_by} field" + Style.RESET_ALL)

# Function to display all books
def display_all_books(library):
    print("\n" + Fore.CYAN + "=== Your Library ===" + Style.RESET_ALL)
    if library:
        for i, book in enumerate(library, 1):
            status = "Read" if book['read'] else "Unread"
            print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
    else:
        print(Fore.YELLOW + "Library is empty!" + Style.RESET_ALL)

# Function to display statistics
def display_statistics(library):
    print("\n" + Fore.CYAN + "=== Library Statistics ===" + Style.RESET_ALL)
    total_books = len(library)
    read_books = len([book for book in library if book['read']])
    percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0

    print(f"Total books: {total_books}")
    print(f"Percentage read: {percentage_read:.1f}%")

# Function to display the main menu
def display_menu():
    print("\n" + Fore.CYAN + "Menu" + Style.RESET_ALL)
    print("1. Add a book")
    print("2. Remove a book")
    print("3. Search for a book")
    print("4. Display all books")
    print("5. Display statistics")
    print("6. Exit")

# CLI Main function
def cli_main():
    library = load_library()

    print(Fore.YELLOW + "\n===================================")
    print("  Welcome to Personal Library Manager")
    print("===================================" + Style.RESET_ALL)

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            add_book(library)
        elif choice == "2":
            library = remove_book(library)
        elif choice == "3":
            search_library(library)
        elif choice == "4":
            display_all_books(library)
        elif choice == "5":
            display_statistics(library)
        elif choice == "6":
            save_library(library)
            print("\n" + Fore.GREEN + "Library saved to file. Goodbye!" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)

# Streamlit Main function
def streamlit_main():
    st.set_page_config(page_title="📚 Personal Library Manager", layout="centered")

    st.title("📚 Personal Library Manager")
    st.markdown("Manage your book collection easily!")

    library = load_library()

    # --- Dark Mode Support (auto via Streamlit theme settings) ---
    # --- Reset Option ---
    if st.button("🧹 Reset Entire Library"):
        library.clear()
        save_library(library)
        st.success("Library has been reset!")

    st.sidebar.header("Choose Action")
    action = st.sidebar.radio("Select", ["Add Book", "Remove Book", "Search", "Display All", "Statistics"])

    # --- Add Book ---
    if action == "Add Book":
        st.subheader("➕ Add a Book")
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=0, step=1)
        genre = st.text_input("Genre")
        read = st.checkbox("Have you read this book?")

        if st.button("Add Book"):
            new_book = {
                'title': title,
                'author': author,
                'year': int(year),
                'genre': genre,
                'read': read
            }
            library.append(new_book)
            save_library(library)
            st.success(f"✅ '{title}' added to your library!")

    # --- Remove Book ---
    elif action == "Remove Book":
        st.subheader("❌ Remove a Book")
        titles = [book['title'] for book in library]
        if titles:
            book_to_remove = st.selectbox("Select book to remove", titles)
            if st.button("Remove Book"):
                library = [book for book in library if book['title'] != book_to_remove]
                save_library(library)
                st.success(f"🗑️ '{book_to_remove}' removed!")
        else:
            st.warning("Library is empty!")

    # --- Search ---
    elif action == "Search":
        st.subheader("🔍 Search Library")
        search_by = st.radio("Search by", ["Title", "Author"])
        query = st.text_input("Enter search term")

        if query:
            field = "title" if search_by == "Title" else "author"
            results = [book for book in library if query.lower() in book[field].lower()]

            if results:
                st.write(f"### Results ({len(results)} found):")
                for book in results:
                    st.write(f"**{book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
            else:
                st.warning("No matching books found.")

    # --- Display All + Genre Filter ---
    elif action == "Display All":
        st.subheader("📚 Your Library")

        if library:
            genres = list(set(book['genre'] for book in library if book['genre']))
            selected_genre = st.selectbox("Filter by genre", ["All"] + sorted(genres))

            filtered_books = library if selected_genre == "All" else [book for book in library if book['genre'] == selected_genre]

            for book in filtered_books:
                st.write(f"**{book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
        else:
            st.warning("Library is empty!")

    # --- Statistics ---
    elif action == "Statistics":
        st.subheader("📊 Library Statistics")
        total_books = len(library)
        read_books = len([book for book in library if book['read']])
        unread_books = total_books - read_books
        percent_read = (read_books / total_books) * 100 if total_books else 0

        st.metric("📚 Total Books", total_books)
        st.metric("✅ Books Read", read_books)
        st.metric("❌ Books Unread", unread_books)
        st.metric("📈 Percentage Read", f"{percent_read:.1f}%")

# Entry point for the program
if len(sys.argv) > 1 and sys.argv[1] == "cli":
    cli_main()
else:
    streamlit_main()


