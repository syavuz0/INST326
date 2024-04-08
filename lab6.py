# imports
import tkinter as tk
from tkinter import ttk
import datetime # one module for working with dates and times
from tkinter import filedialog

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

        save_button = tk.Button(self, text="Save", command=self.save_note)
        save_button.grid(row=4, column=1)

        view_saved_button = tk.Button(self, text="View Saved Notes", command=self.view_saved_notes)
        view_saved_button.grid(row=5, column=1)

        now = datetime.datetime.now()
        local_now = now.astimezone()
        local_tz = local_now.tzinfo

        print(now)
        print(local_now)
        print(local_tz)

    def submit(self):
        title = self.note_title.get()
        text = self.note_text.get("1.0", tk.END)
        new_note = {'Title': title, 'Text': text}
        self.notes.append(new_note)
        print("Note submitted successfully!")

    def save_note(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if filename:
            with open(filename, 'w') as file:
                for note in self.notes:
                    file.write(f"Title: {note['Title']}\n")
                    file.write(f"Text:\n{note['Text']}\n")
                    file.write('\n')  # Add a blank line between notes
            print('Notes saved successfully!')

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


