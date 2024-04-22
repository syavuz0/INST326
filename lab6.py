import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import datetime
import json
import csv

class MainWindow(tk.Tk): 
    def __init__(self):
        super().__init__()
        self.geometry("600x400")  
        self.title('Notebook')
        self.notes = []

        title_label = tk.Label(self, bg='light gray', text='Note Title:')
        title_label.grid(padx=10, pady=10, row=1, column=0, sticky='e')

        text_label = tk.Label(self, bg='light gray', text='Note Text:')
        text_label.grid(padx=10, pady=10, row=2, column=0, sticky='e')

        self.note_title = tk.Entry(self, width=80)
        self.note_title.grid(padx=10, pady=10, row=1, column=1, sticky='w')
        self.note_title.insert(0, 'New note title')

        self.note_text = tk.Text(self, height=10, width=60)
        self.note_text.grid(padx=10, pady=10, row=2, column=1)
        self.note_text.insert('1.0', 'Type Here')

        submit_button = tk.Button(self, text="Submit", command=self.submit)
        submit_button.grid(row=3, column=1)

        save_txt_button = tk.Button(self, text="Save TXT", command=self.save_txt_note)
        save_txt_button.grid(row=4, column=1)

        save_json_button = tk.Button(self, text="Save JSON", command=self.save_json_note)
        save_json_button.grid(row=5, column=1)

        save_csv_button = tk.Button(self, text="Save CSV", command=self.save_csv_note)
        save_csv_button.grid(row=6, column=1)

        view_saved_button = tk.Button(self, text="View and Edit Notes", command=self.view_saved_notes)
        view_saved_button.grid(row=7, column=1)

    def submit(self):
        created = datetime.datetime.now().isoformat()
        title = self.note_title.get()
        text = self.note_text.get("1.0", tk.END)
        new_note = {'Title': title, 'Text': text, 'Created': created, 'Updated': created}
        self.notes.append(new_note)
        messagebox.showinfo("Submit", "Note submitted successfully!")

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
        view_window.geometry("600x400")

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

        edit_button = tk.Button(view_window, text="Edit Selected Note", command=edit_note)
        edit_button.pack()

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
