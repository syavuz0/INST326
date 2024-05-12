import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import font 
import datetime
import json
import csv

class MainWindow(tk.Tk): 
    def __init__(self):
        super().__init__()
        self.geometry("800x600")  # bigger window size 
        self.title('Notebook and Snippets')  # Combined title
        self.configure(bg = 'light blue')
        self.items = []  # combined storage for notes and snippets
        self.key = b'your_secret_key_here' # key for encryption
        self.cipher = Fernet(self.key) # ciphering a message

        self.load_default_notebook()  # Load default notebook when program starts

        title_label = tk.Label(self, bg='light blue', text='Note Title:')
        title_label.grid(padx=10, pady=10, row=1, column=0, sticky='e')

        text_label = tk.Label(self, bg='light gray', text='Note Text:')
        text_label.grid(padx=10, pady=10, row=2, column=0, sticky='e')

        #creating dropdown menu
        color_label = tk.Label(self, text = "Background Color:")
        color_label.grid = (row=3, column=0, sticky='e', padx=10, pady=10)
        self.color_options = ["light blue", "pale green", "lemon chiffon", "rosy brown", "honeydew"]
        self.color_dropdown = ttk.Combobox(self, values=self.color_options, state="readonly")
        self.color_dropdown.grid(row=3, column=1, sticky='w', padx=10)
        self.color_dropdown.current(0)  
        self.color_dropdown.bind("<<ComboboxSelected>>", self.change_color)

        self.note_title = tk.Entry(self, width=80)
        self.note_title.grid(padx=10, pady=10, row=1, column=1, sticky='w')
        self.note_title.insert(0, 'New note title')

        self.note_text = tk.Text(self, height=20, width=80)  # bigger text widget size
        self.note_text.grid(padx=10, pady=10, row=2, column=1)
        self.note_text.insert('1.0', 'Type Here')

        submit_button = tk.Button(self, text="Submit", command=self.submit)
        submit_button.grid(row=3, column=1)

        save_txt_button = tk.Button(self, text="Save as TXT", command=self.save_txt_note)
        save_txt_button.grid(row=4, column=1)

        save_json_button = tk.Button(self, text="Save as JSON", command=self.save_json_note)
        save_json_button.grid(row=5, column=1)

        save_csv_button = tk.Button(self, text="Save as CSV", command=self.save_csv_note)
        save_csv_button.grid(row=6, column=1)

        view_saved_button = tk.Button(self, text="View and Edit Notes", command=self.view_saved_notes)
        view_saved_button.grid(row=7, column=1)


    def load_default_notebook(self):
        # Load default notebook from a file
        default_notebook = [{'Type': 'Note', 'Title': 'Default Note', 'Content': 'This is a default note.', 'Created': '2024-05-12T12:00:00', 'Updated': '2024-05-12T12:00:00'}]
        self.items.extend(default_notebook)

    def submit(self):
        created = datetime.datetime.now().isoformat()
        title = self.item_title.get()
        content = self.item_content.get("1.0", tk.END)
        new_item = {'Type': 'Note', 'Title': title, 'Content': content, 'Created': created, 'Updated': created}  # combined format
        self.items.append(new_item)
        messagebox.showinfo("Submit", "Item submitted successfully!")

    def save_txt_note(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if filename:
            with open(filename, 'w') as file:
                for note in self.notes:
                    file.write(f"Title: {note['Title']}\nText: {note['Text']}\nCreated: {note['Created']}\nUpdated: {note['Updated']}\n\n")
            messagebox.showinfo("Save", "Notes saved as TXT file successfully!")

    def save_json_note(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if filename:
            with open(filename, 'w') as file:
                json.dump(self.notes, file, indent=4)
            messagebox.showinfo("Save", "Notes saved as JSON file successfully!")

    def save_csv_note(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if filename:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Title', 'Text', 'Created', 'Updated'])
                for note in self.notes:
                    writer.writerow([note['Title'], note['Text'], note['Created'], note['Updated']])
            messagebox.showinfo("Save", "Notes saved as CSV file successfully!")

    def view_saved_notes(self):
        view_window = tk.Toplevel(self)
        view_window.title("View/Edit Notes")
        view_window.geometry("800x600")  # bigger window size

        listbox = tk.Listbox(view_window, width=100, height=15)
        listbox.pack(pady=20)

        for index, note in enumerate(self.notes):
            listbox.insert(tk.END, f"{index + 1}: {note['Title']} - Last Updated: {note['Updated']}")

        def edit_note():
            selected_index = int(listbox.curselection()[0])
            edit_window = tk.Toplevel(view_window)
            edit_window.title("Edit Note")
            edit_window.geometry("400x300")

            tk.Label(edit_window, text="Title:").pack()
            title_entry = tk.Entry(edit_window, width=50)
            title_entry.pack()
            title_entry.insert(0, self.notes[selected_index]['Title'])

            tk.Label(edit_window, text="Text:").pack()
            text_entry = tk.Text(edit_window, width=50, height=10)
            text_entry.pack()
            text_entry.insert('1.0', self.notes[selected_index]['Text'])

            def save_changes():
                self.notes[selected_index]['Title'] = title_entry.get()
                self.notes[selected_index]['Text'] = text_entry.get("1.0", tk.END)
                self.notes[selected_index]['Updated'] = datetime.datetime.now().isoformat()
                messagebox.showinfo("Update", "Note updated successfully!")
                view_window.destroy()
                self.view_saved_notes()

            save_button = tk.Button(edit_window, text="Save Changes", command=save_changes)
            save_button.pack()

            # Note Encryption
            self.root.bind("<Control-n>", self.create_new_note)
            self.root.bind("<Control-s>", self.save_note)

        edit_button = tk.Button(view_window, text="Edit Selected Note", command=edit_note)
        edit_button.pack()

    def change_color(self, event):
        color = self.color_dropdown.get()
        self.configure(bg = color)
        

        

if __name__ == '__main__':
    main_window = MainWindow()
    main_window.mainloop()

class Snippets():
    def __init__(self, file_path):
        self.file_path = file_path
        self.snippets = self.load_snippets()

    def load_snippets(self):
            with open(self.file_path, 'r') as file:
                return json.load(file)
       
    def save_snippets(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.snippets, file, indent=4)

    def create_snippet(self, name, code):
        snippet = {'name': name, 'code': code}
        self.snippets.append(snippet)
        self.save_snippets()

    def display_snippets(self):
        for idx, snippet in enumerate(self.snippets, 1):
            print(f"{idx}. {snippet['name']}:\n{snippet['code']}\n")

    def edit_snippet(self, index, name=None, code=None):
        snippet = self.snippets[index]
        if name:
            snippet['name'] = name
        if code:
            snippet['code'] = code
        self.save_snippets()

    def delete_snippet(self, index):
        del self.snippets[index]
        self.save_snippets()


class RichTextEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rich Text Editor")
        self.text = tk.Text(self)
        self.text.pack()

        # Define custom font styles 
        self.bold_font = font.Font(self.text, self.text.cget("font"))
        self.bold_font.configure(weight="bold")
        self.text.tag_configure("bold", font=self.bold_font)

        self.italic_font = font.Font(self.text, self.text.cget("font"))
        self.italic_font.configure(slant="italic")
        self.text.tag_configure("italic", font=self.italic_font)

        self.underline_font = font.Font(self.text, self.text.cget("font"))
        self.underline_font.configure(underline=True)
        self.text.tag_configure("underline", font=self.underline_font)

        # Create buttons 
        self.bold_button = tk.Button(self, text="Bold", command=self.bold_text)
        self.bold_button.pack(side="left", padx=5)

        self.italic_button = tk.Button(self, text="Italic", command=self.italic_text)
        self.italic_button.pack(side="left", padx=5)

        self.underline_button = tk.Button(self, text="Underline", command=self.underline_text)
        self.underline_button.pack(side="left", padx=5)

    def bold_text(self):
        current_tags = self.text.tag_names("sel.first")
        if "bold" in current_tags:
            self.text.tag_remove("bold", "sel.first", "sel.last")
        else:
            self.text.tag_add("bold", "sel.first", "sel.last")

    def italic_text(self):
        current_tags = self.text.tag_names("sel.first")
        if "italic" in current_tags:
            self.text.tag_remove("italic", "sel.first", "sel.last")
        else:
            self.text.tag_add("italic", "sel.first", "sel.last")

    def underline_text(self):
        current_tags = self.text.tag_names("sel.first")
        if "underline" in current_tags:
            self.text.tag_remove("underline", "sel.first", "sel.last")
        else:
            self.text.tag_add("underline", "sel.first", "sel.last")

