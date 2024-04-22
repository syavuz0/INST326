# imports
import tkinter as tk
from tkinter import ttk
import datetime # one module for working with dates and times
from tkinter import filedialog
import json
import csv

# The MainWindow class creates a custom GUI window based on the tkinter window (tk.Tk)
# It has an __init__() method, and three additional methods (new_note(), open_notebook(), and save_notebook())
# These methods correspond to new, open, and save buttons in the window.
# The new_note method calls the NoteForm class to create a new note form top level window.

class MainWindow(tk.Tk): 
    def __init__(self):
        super().__init__()
        self.geometry("600x400")  
        self.title('Notebook')
        self.notebook = []
        self.notes = []

        blank_text = 'Type Here' #adds default text 

        title_label = tk.Label(self, bg='light gray', text='Note Title:')
        title_label.grid(padx=10, pady=10, row=1, column=0, sticky='e')

        text_label = tk.Label(self, bg='light gray', text='Note Text:')
        text_label.grid(padx=10, pady=10, row=2, column=0, sticky='e')

        # Create our note title entry field
        self.note_title = tk.Entry(self, width=80)
        self.note_title.grid(padx=10, pady=10, row=1, column=1, sticky='w')
        self.note_title.insert(0, 'New note title')  # Adds default text (useful during development)

        # Create our note text entry field
        self.note_text = tk.Text(self, height=10, width=60)
        self.note_text.grid(padx=10, pady=10, row=2, column=1)
        self.note_text.insert('1.0', blank_text)  # Adds default text (useful during development)

        submit_button = tk.Button(self, text="Submit", command=self.submit) #Create a submit button
        submit_button.grid(row=3, column=1)

        save_txt_button = tk.Button(self, text="Save as TXT", command=self.save_txt_note)
        save_txt_button.grid(row=4, column=1)

        save_json_button = tk.Button(self, text="Save as JSON", command=self.save_json_note)
        save_json_button.grid(row=5, column=1)

        save_csv_button = tk.Button(self, text="Save as CSV", command=self.save_csv_note)
        save_json_button.grid(row=6, column=1)

        
        view_saved_button = tk.Button(self, text="View Saved Notes", command=self.view_saved_notes)
        view_saved_button.grid(row=7, column=1)

        self.load_saved_notes() # autoatically load saved notes 

        
        now = datetime.datetime.now() #Current date and time
        local_now = now.astimezone()
        local_tz = local_now.tzinfo #Local Timezone information

        print(now)
        print(local_now)
        print(local_tz)

    def submit(self):
        title = self.note_title.get()
        text = self.note_text.get("1.0", tk.END)
        new_note = {'Title': title, 'Text': text}
        self.notes.append(new_note)
        print("Note submitted successfully!")

    def save_txt_note(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if filename:
            with open(filename, 'w') as file:
                for note in self.notes:
                    file.write(f"Title: {note['Title']}\n")
                    file.write(f"Text:\n{note['Text']}\n")
                    file.write('\n')  # Add a blank line between notes
            print('Notes saved as TXT file successfully!')
    

    def save_json_note(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if filename:
            with open(filename, 'w') as file:
                json.dump(self.notes, file, indent=4)  # Write self.notes to the file in JSON format
            print('Notes saved as JSON file successfully!')

    def save_csv_note(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if filename:
            with open(filename, 'w')as file:
                user = csv.writer(file)
                for note in self.notes:
                    note.get('Title')
                    note.get('Text')
                    
                    L = f'"{title}", "{text}"\n'
                 file.write(L)
            print('Notes saved as CSV file successfully!')


    


                
                
                
                
            
                
    #creats a separate window to view notes 
    def view_saved_notes(self):
        filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if filename:
            with open(filename, 'r') as file:
                content = file.read()
            display_window = tk.Toplevel(self)
            display_window.title("Saved Notes")
            display_text = tk.Text(display_window)
            display_text.insert(tk.END, content)
            display_text.pack(fill="both", expand=True)

# the NoteForm() class creates a Toplevel window that is a note form containing fields for
# data entry for title, text, link, and tags. It also calculates a meta field with date, time, and timezone
# the Noteform class has an __init__() method, and a submit() method that is called by a submit button
# the class may contain additional methods to perform tasks like calculating the metadata, for example
# the submit method calls the MakeNote class that transforms the the entered data into a new note object.


class NoteForm(tk.Toplevel):
    
    def __init__(self, master, notebook, notes):
        super().__init__(master) #toplevel window
        self.title('New Note')
        self.geometry("400x300")
        
        self.submit_button = ttk.Button(self, text="Submit", command=self.submit)
        self.submit_button.pack()
        
        self.save_button = ttk.Button(self, text="Save", command=self.save_note)
        self.save_button.pack()
        
    def submit(self):
        title = self.master.note_title.get()
        text = self.master.note_text.get("1.0", tk.END)
        note_dict = {'Title': title, 'Text': text} # creates a dictionary that matches the structure
        new_note = MakeNote(note_dict)
        self.master.notes.append(new_note)
        print("Note submitted successfully!")
        self.destroy()        
    
    def save_note(self):
        title = self.master.note_title.get()
        text = self.master.note_text.get("1.0", tk.END)
        note_dict = {'Title': title, 'Text': text}
        new_note = MakeNote(note_dict)
        self.master.notes.append(new_note)
        self.master.save_note()

# The MakeNote class takes a dictionary containing the data entered into the form window,
# and transforms it into a new note object.
# At present the note objects have attributes but no methods.

class MakeNote():
    def __init__(self, note_dict):
        self.title = note_dict['Title']
        self.text = note_dict['Text']


if __name__ == '__main__':
    main_window = MainWindow()
    main_window.mainloop() 


# Snippet Class

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
