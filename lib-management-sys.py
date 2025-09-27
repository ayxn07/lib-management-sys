import customtkinter as ctk
import mysql.connector as conc
from tkinter import StringVar, Listbox, END, messagebox


def mainloop():
    global window
    window = ctk.CTk()
    window.title("Library Management System")
    window.geometry("600x600")

    title = ctk.CTkEntry(master=window, height=40, width=220, placeholder_text="Title")
    title.place(relx=0.55, rely=0.2, anchor="center")
    author = ctk.CTkEntry(master=window, height=40, width=220, placeholder_text="Author")
    author.place(relx=0.55, rely=0.3, anchor="center")
    genre = ctk.CTkEntry(master=window, height=40, width=220, placeholder_text="Genre")
    genre.place(relx=0.55, rely=0.4, anchor="center")
    year = ctk.CTkEntry(master=window, height=40, width=220, placeholder_text="Year")
    year.place(relx=0.55, rely=0.5, anchor="center")

    def open_search_window():
        window.withdraw()

        search_window = ctk.CTkToplevel(window)
        search_window.title("Search Book")
        search_window.geometry("600x600")

        book_details = ctk.CTkLabel(master=search_window, text="Search Title:", font=("Arial", 20, "bold"))
        book_details.place(relx=0.25, rely=0.2, anchor="center")
        title1 = ctk.CTkEntry(master=search_window, height=40, width=220)
        title1.place(relx=0.55, rely=0.2, anchor="center")

        search_var = StringVar()
        title1.configure(textvariable=search_var)
        search_var.trace_add("write", lambda name, index, mode, sv=search_var: update_search_results(sv, search_window))

        results_listbox = Listbox(search_window, height=5, width=30, fg="white")
        results_listbox.place(relx=0.55, rely=0.4, anchor="center")
        results_listbox.configure(background=search_window.cget('background'))

        def update_search_results(sv, search_window):
            query = sv.get()
            results_listbox.delete(0, END)

            if len(query) >= 2:
                try:
                    mydb = conc.connect(host="localhost", user="root", passwd="OIS@12345", database="library")
                    mycursor = mydb.cursor()
                    mycursor.execute("SELECT title FROM librarySet WHERE title LIKE %s", (f"%{query}%",))
                    results = mycursor.fetchall()
                    for book in results:
                        results_listbox.insert(END, book[0])
                    mydb.close()
                except conc.Error as e:
                    print(f"Error accessing database: {e}")

        def show_book_details(event):
            selection = results_listbox.curselection()
            if selection:
                selected_book_title = results_listbox.get(selection[0])
                open_book_details_window(selected_book_title)

        results_listbox.bind("<<ListboxSelect>>", show_book_details)

        search_window.protocol("WM_DELETE_WINDOW", lambda: close_search_window(search_window))

    def close_search_window(search_window):
        window.deiconify()
        search_window.destroy()

    def open_book_details_window(book_title):
        details_window = ctk.CTkToplevel(window)
        details_window.title("Book Details")
        details_window.geometry("600x600")

        try:
            mydb = conc.connect(host="localhost", user="root", passwd="OIS@12345", database="library")
            mycursor = mydb.cursor()
            mycursor.execute("SELECT Title, Author, Genre, Year FROM librarySet WHERE title = %s", (book_title,))
            book = mycursor.fetchone()
            mydb.close()
            if book:
                Title, Author, Genre, Year = book
                details_text = f"Title: {Title}\nAuthor: {Author}\nGenre: {Genre}\nYear: {Year}"
                book_details = ctk.CTkLabel(master=details_window, text=details_text, font=("Arial", 35, "bold"))
                book_details.place(relx=0.5, rely=0.4, anchor="center")

                btn_edit = ctk.CTkButton(master=details_window, text="Edit Book",
                                         command=lambda: open_edit_window(book_title), height=50, width=200)
                btn_edit.place(relx=0.5, rely=0.6, anchor="center")

                btn_delete = ctk.CTkButton(master=details_window, text="Delete Book",
                                           command=lambda: delete_book(book_title, details_window), height=50,
                                           width=200)
                btn_delete.place(relx=0.5, rely=0.7, anchor="center")

        except conc.Error as e:
            print(f"Error accessing database: {e}")

    def open_edit_window(book_title):
        edit_window = ctk.CTkToplevel(window)
        edit_window.title("Edit Book Details")
        edit_window.geometry("600x600")

        try:
            mydb = conc.connect(host="localhost", user="root", passwd="OIS@12345", database="library")
            mycursor = mydb.cursor()
            mycursor.execute("SELECT title, author, genre, year FROM librarySet WHERE title = %s", (book_title,))
            book = mycursor.fetchone()
            mydb.close()

            if book:
                Title, Author, Genre, Year = book

                title_entry = ctk.CTkEntry(master=edit_window, height=40, width=220)
                title_entry.insert(0, Title)
                title_entry.place(relx=0.55, rely=0.2, anchor="center")

                author_entry = ctk.CTkEntry(master=edit_window, height=40, width=220)
                author_entry.insert(0, Author)
                author_entry.place(relx=0.55, rely=0.3, anchor="center")

                genre_entry = ctk.CTkEntry(master=edit_window, height=40, width=220)
                genre_entry.insert(0, Genre)
                genre_entry.place(relx=0.55, rely=0.4, anchor="center")

                year_entry = ctk.CTkEntry(master=edit_window, height=40, width=220)
                year_entry.insert(0, Year)
                year_entry.place(relx=0.55, rely=0.5, anchor="center")

                def save_changes():
                    new_title = title_entry.get()
                    new_author = author_entry.get()
                    new_genre = genre_entry.get()
                    new_year = year_entry.get()

                    if new_title == "" or new_author == "" or new_genre == "" or new_year == "":
                        messagebox.showerror("Error", "Please fill all fields")
                        return

                    try:
                        mydb = conc.connect(host="localhost", user="root", passwd="OIS@12345", database="library")
                        mycursor = mydb.cursor()
                        update_query = """
                        UPDATE librarySet
                        SET title = %s, author = %s, genre = %s, year = %s
                        WHERE title = %s
                        """
                        mycursor.execute(update_query, (new_title, new_author, new_genre, new_year, book_title))
                        mydb.commit()
                        mydb.close()
                        messagebox.showinfo("Success", "Book details updated successfully")
                        edit_window.destroy()
                    except conc.Error as e:
                        print(f"Error accessing database: {e}")

                btn_save = ctk.CTkButton(master=edit_window, text="Save Changes", command=save_changes, height=50,
                                         width=200)
                btn_save.place(relx=0.55, rely=0.6, anchor="center")

        except conc.Error as e:
            print(f"Error accessing database: {e}")

    def delete_book(book_title, details_window):
        confirm = messagebox.askyesno("Confirm Delete",
                                      f"Are you sure you want to delete the book titled '{book_title}'?")
        if confirm:
            try:
                mydb = conc.connect(host="localhost", user="root", passwd="OIS@12345", database="library")
                mycursor = mydb.cursor()
                delete_query = "DELETE FROM librarySet WHERE title = %s"
                mycursor.execute(delete_query, (book_title,))
                mydb.commit()
                mydb.close()
                messagebox.showinfo("Success", "Book deleted successfully")
                details_window.destroy()
            except conc.Error as e:
                print(f"Error accessing database: {e}")

    def add_record():
        titleGot = title.get()
        authorGot = author.get()
        genreGot = genre.get()
        yearGot = year.get()
        if titleGot == "" or authorGot == "" or genreGot == "" or yearGot == "":
            label3 = ctk.CTkLabel(master=window, text="Please fill all fields", font=("Arial", 15), text_color="red")
            label3.place(relx=0.55, rely=0.66, anchor="center")
        else:
            try:
                mydb = conc.connect(host="localhost", user="root", passwd="OIS@12345", database="library")
                mycursor = mydb.cursor()
                addrec = "INSERT INTO librarySet (title, author, genre, year) VALUES (%s, %s, %s, %s)"
                studentInto2 = (titleGot, authorGot, genreGot, yearGot)
                mycursor.execute(addrec, studentInto2)
                mydb.commit()
                mydb.close()
                label3 = ctk.CTkLabel(master=window, text=" ", font=("Arial", 15), text_color="red")
                label3.place(relx=0.55, rely=0.66, anchor="center")
                label4 = ctk.CTkLabel(master=window, text="Record added successfully", font=("Arial", 15),
                                      text_color="green")
                label4.place(relx=0.55, rely=0.66, anchor="center")
            except conc.Error as e:
                print(f"Error accessing database: {e}")

    def show_all_books():
        all_books_window = ctk.CTkToplevel(window)
        all_books_window.title("All Books")
        all_books_window.geometry("600x600")

        results_listbox = Listbox(all_books_window, height=20, width=50, fg="white",font=("Arial", 20))
        results_listbox.pack(expand=True, fill="both")
        results_listbox.configure(background=all_books_window.cget('background'))

        try:
            mydb = conc.connect(host="localhost", user="root", passwd="OIS@12345", database="library")
            mycursor = mydb.cursor()
            mycursor.execute("SELECT title FROM librarySet")
            results = mycursor.fetchall()
            for book in results:
                results_listbox.insert(END, book[0])
            mydb.close()
        except conc.Error as e:
            print(f"Error accessing database: {e}")

    label1 = ctk.CTkLabel(master=window, text="Title: ", font=("Arial", 25))
    label1.place(relx=0.28, rely=0.2, anchor="center")
    label2 = ctk.CTkLabel(master=window, text="Author: ", font=("Arial", 25))
    label2.place(relx=0.28, rely=0.3, anchor="center")
    label3 = ctk.CTkLabel(master=window, text="Genre: ", font=("Arial", 25))
    label3.place(relx=0.28, rely=0.4, anchor="center")
    label4 = ctk.CTkLabel(master=window, text="Year: ", font=("Arial", 25))
    label4.place(relx=0.28, rely=0.5, anchor="center")
    label5 = ctk.CTkLabel(master=window, text="Search Title: ", font=("Arial", 25))
    label5.place(relx=0.23, rely=0.75, anchor="center")

    btn1 = ctk.CTkButton(master=window, text="Add Book", command=add_record)
    btn1.place(relx=0.55, rely=0.6, anchor="center")
    btn2 = ctk.CTkButton(master=window, text="Search Book", command=open_search_window, height=50, width=200,
                         font=("Arial", 16))
    btn2.place(relx=0.55, rely=0.75, anchor="center")
    btn3 = ctk.CTkButton(master=window, text="Show All Books", command=show_all_books, height=50, width=200,
                         font=("Arial", 16))
    btn3.place(relx=0.55, rely=0.85, anchor="center")

    window.mainloop()
mainloop()
