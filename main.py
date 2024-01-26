import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import TKinterModernThemes as TKMT
import random
import threading
import time
from tkinter import font
import json
import pyperclip
import webbrowser

def createToolTip(widget, text):
    try:
        def enter(event):
            widget._after_id = widget.after(600, show_tooltip, event)

        def leave(event):
            widget.after_cancel(widget._after_id)
            tooltip = getattr(widget, "_tooltip", None)
            if tooltip:
                tooltip.destroy()
                widget._tooltip = None

        def show_tooltip(event):
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root}+{event.y_root}")
            label = tk.Label(tooltip, text=text, background="black", foreground="white")
            label.grid()
            widget._tooltip = tooltip

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

class App(TKMT.ThemedTKinterFrame):
    def __init__(self):
        try:
            super().__init__("RandomPicker", "Sun-valley", "dark")
            self.master.iconbitmap('RandomPicker.ico')
            self.master.resizable(False, False)

            self.main_frame = ttk.Frame(self.master)
            self.main_frame.grid(row=0, column=0, sticky="nsew")

            self.left_frame = ttk.Frame(self.main_frame, width=200, height=400)
            self.left_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ns")

            self.right_frame = ttk.Frame(self.main_frame)
            self.right_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

            self.input_frame = ttk.Frame(self.right_frame)
            self.input_frame.grid(row=0, column=0, sticky="ew")

            self.input_frame.columnconfigure(0, weight=1)
            self.input_frame.columnconfigure(1, weight=1)

            self.name_input = ttk.Entry(self.input_frame, font=("Arial", 12))
            createToolTip(self.name_input, "Enter a name to add to the list")
            self.name_input.grid(row=0, column=0, sticky="ew", padx=5, pady=10)

            self.add_button = ttk.Button(self.input_frame, text="Add Name", command=self.add_name)
            createToolTip(self.add_button, "Click to add the name entered in the entry box to the list")
            self.add_button.grid(row=0, column=1, sticky="ew", padx=5, pady=10)

            self.add_range_button = ttk.Button(self.input_frame, text="Add Range", command=self.add_range)
            createToolTip(self.add_range_button, "Click to add the range of numbers entered in the entry boxes to the list")
            self.add_range_button.grid(row=2, column=1, sticky="ew", padx=5, pady=10)

            self.start_input = ttk.Entry(self.input_frame, font=("Arial", 12))
            createToolTip(self.start_input, "Enter the start value of the range")
            self.start_input.grid(row=2, column=0, sticky="w", padx=5, pady=10)
            self.end_input = ttk.Entry(self.input_frame, font=("Arial", 12))
            createToolTip(self.end_input, "Enter the end value of the range")
            self.end_input.grid(row=2, column=0, sticky="e", padx=5, pady=10)

            self.start_input.config(width=20)
            self.end_input.config(width=20)

            self.name_list = tk.Listbox(self.right_frame, font=("Arial", 12), width=80, height=30)
            createToolTip(self.name_list, "Double-click a name to delete it\nCtrl + Click a name to duplicate it with a custom count\nRight-click a name to edit it\nCtrl + Right-Click to shuffle names\nThis shows the names you have added")
            self.name_list.grid(row=2, column=0, sticky="nsew", pady=10)
            self.name_list.bind("<Double-Button-1>", self.delete_name)
            self.name_list.bind("<Control-Button-1>", self.add_name_with_copy_count)

            self.scrollbar = ttk.Scrollbar(self.right_frame, orient="vertical", command=self.name_list.yview)
            createToolTip(self.scrollbar, "Use this to scroll through the list")
            self.scrollbar.grid(row=2, column=1, sticky="ns", pady=10)
            self.name_list.config(yscrollcommand=self.scrollbar.set)

            self.pick_button = ttk.Button(self.right_frame, text="Pick Randomly", command=self.pick_randomly)
            createToolTip(self.pick_button, "Click to pick a name randomly from the list")
            self.pick_button.grid(row=3, column=0, sticky="ew", pady=10)

            self.auto_select_button = ttk.Button(self.left_frame, text="Automatic Selection", command=self.auto_select)
            createToolTip(self.auto_select_button, "Click to start automatic selection")
            self.auto_select_button.grid(row=0, column=0, sticky="ew", pady=10, padx=5)

            self.auto_select_symbol = ttk.Button(self.left_frame, text="⮞", command=self.auto_select_with_time)
            createToolTip(self.auto_select_symbol, "Click to enter the number of seconds for automatic selection")
            self.auto_select_symbol.grid(row=0, column=1, sticky="ew", pady=10, padx=5)

            self.delete_and_copy_button = ttk.Button(self.left_frame, text="Delete and Copy", command=self.delete_and_copy_selected_name)
            createToolTip(self.delete_and_copy_button, "Click to delete and copy the selected name in the list")
            self.delete_and_copy_button.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10, padx=5)

            self.delete_selected_button = ttk.Button(self.left_frame, text="Delete Selected", command=self.delete_selected_name)
            createToolTip(self.delete_selected_button, "Click to delete the selected name in the list")
            self.delete_selected_button.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10, padx=5)

            self.clear_all_button = ttk.Button(self.left_frame, text="Clear All", command=self.clear_all_names)
            createToolTip(self.clear_all_button, "Click to clear all names in the list")
            self.clear_all_button.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10, padx=5)

            self.remove_duplicates_button = ttk.Button(self.left_frame, text="Remove Duplicates", command=self.remove_duplicates)
            createToolTip(self.remove_duplicates_button, "Click to remove all duplicate names in the list, keeping only one instance")
            self.remove_duplicates_button.grid(row=4, column=0, columnspan=2, sticky="ew", pady=10, padx=5)

            self.history_button = ttk.Button(self.left_frame, text="History", command=self.show_history)
            createToolTip(self.history_button, "Click to view the history of the names picked")
            self.history_button.grid(row=5, column=0, columnspan=2, sticky="ew", pady=10, padx=5)

            self.save_options_button = ttk.Button(self.left_frame, text="Save Options", command=self.save_options)
            createToolTip(self.save_options_button, "Click to save options to a file")
            self.save_options_button.grid(row=6, column=0, columnspan=2, sticky="ew", pady=10, padx=5)

            self.load_options_button = ttk.Button(self.left_frame, text="Load Options", command=self.load_options)
            createToolTip(self.load_options_button, "Click to load options from a file")
            self.load_options_button.grid(row=7, column=0, columnspan=2, sticky="ew", pady=10, padx=5)

            self.send_feedback_button = ttk.Button(self.left_frame, text="Send Feedback", command=self.send_feedback)
            createToolTip(self.send_feedback_button, "Click to open the GitHub issues page and send feedback")
            self.send_feedback_button.grid(row=8, column=0, columnspan=2, sticky="ew", pady=10, padx=5)  

            self.shortcuts_button = ttk.Button(self.left_frame, text="Show Shortcuts", command=self.show_shortcuts)
            createToolTip(self.shortcuts_button, "Click to view keyboard shortcuts")
            self.shortcuts_button.grid(row=9, column=0, columnspan=2, sticky="ew", pady=10, padx=5)           

            self.history_file = "history.json"
            self.history_list = []
            self.load_history()

            self.remove_on_pick_var = tk.BooleanVar()
            self.remove_on_pick_var.set(False)

            self.remove_on_pick_checkbox = ttk.Checkbutton(self.right_frame, text="Remove on Pick", variable=self.remove_on_pick_var)
            createToolTip(self.remove_on_pick_checkbox, "Check to remove the picked name from the list")
            self.remove_on_pick_checkbox.grid(row=3, column=0, sticky="w", pady=10)

            self.result_label = ttk.Label(self.right_frame, text="The name picked is", font=("Arial", 12), anchor="w", width=30)
            createToolTip(self.result_label, "This displays the randomly picked name")
            self.result_label.grid(row=4, column=0, sticky="ew", pady=10)

            self.copy_selected_button = ttk.Button(self.right_frame, text="Copy Selected", command=self.copy_selected_name)
            createToolTip(self.copy_selected_button, "Click to copy the selected name")
            self.copy_selected_button.grid(row=4, column=0, sticky="e", pady=10, padx=(0, 10))

            self.name_list.bind("<Button-3>", self.edit_name)
            self.name_list.bind("<Control-Button-3>", self.shuffle_names)

            self.master.bind("<Control-n>", lambda event: self.add_name())
            self.master.bind("<Control-r>", lambda event: self.add_range())
            self.master.bind("<Control-d>", lambda event: self.delete_selected_name())
            self.master.bind("<Control-c>", lambda event: self.clear_all_names())
            self.master.bind("<Control-p>", lambda event: self.pick_randomly())
            self.master.bind("<Control-a>", lambda event: self.auto_select())
            self.master.bind("<Control-m>", lambda event: self.stop_auto_select(None))
            self.master.bind("<Control-BackSpace>", lambda event: self.clear_history())
            self.master.bind("<Control-q>", lambda event: self.copy_all_history())
            self.master.bind("<Control-e>", lambda event: self.export_history())
            self.master.bind("<Control-s>", lambda event: self.save_options())
            self.master.bind("<Control-l>", lambda event: self.load_options())
            self.master.bind("<Control-d>", lambda event: self.delete_and_copy_selected_name())
            self.master.bind("<Control-f>", lambda event: self.send_feedback())

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def add_name(self):
        try:
            name = self.name_input.get()
            if name:
                self.name_list.insert(0, name)
                self.name_input.delete(0, "end")
            else:
                messagebox.showwarning("Warning", "Please enter a name")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def add_range(self):
        try:
            start = int(self.start_input.get())
            end = int(self.end_input.get())
            if start <= end:
                for i in range(start, end + 1):
                    self.name_list.insert(0, str(i))
                self.start_input.delete(0, "end")
                self.end_input.delete(0, "end")
            else:
                messagebox.showerror("Error", "The start value must be less than or equal to the end value")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers for the range")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def delete_name(self, event):
        try:
            selected_index = self.name_list.curselection()
            if selected_index:
                self.name_list.delete(selected_index)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def clear_all_names(self):
        try:
            self.name_list.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def remove_duplicates(self):
        try:
            names = self.name_list.get(0, "end")
            if not names:
                messagebox.showinfo("Info", "The list is already empty.")
                return
            seen = set()
            unique_names = []
            for name in names:
                if name not in seen:
                    seen.add(name)
                    unique_names.append(name)
            if len(names) == len(unique_names):
                messagebox.showinfo("Info", "The list does not contain any duplicate names.")
                return
            self.name_list.delete(0, "end")
            for name in unique_names:
                self.name_list.insert("end", name)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def copy_selected_name(self):
        try:
            result_text = self.result_label.cget("text")
            if result_text == "The name picked is":
                messagebox.showwarning("No Selected Name", "There is no selected name to copy.")
                return

            selected_name = result_text[len("The name picked is "):]
            pyperclip.copy(selected_name)
            messagebox.showinfo("Copy Selected", f"The selected name '{selected_name}' has been copied to the clipboard.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def add_name_with_copy_count(self, event):
        try:
            selected_index = self.name_list.nearest(event.y)
            if selected_index >= 0:
                name = self.name_list.get(selected_index)
                copy_count = simpledialog.askinteger("Enter Copy Count", f"Enter the number of copies for '{name}':", minvalue=1)
                if copy_count is not None:
                    for _ in range(copy_count):
                        self.name_list.insert("end", name)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def edit_name(self, event):
        try:
            selected_index = self.name_list.nearest(event.y)
            if selected_index >= 0:
                name_to_edit = self.name_list.get(selected_index)
                edited_name = simpledialog.askstring("Edit Name", f"Edit the name:", initialvalue=name_to_edit)
                if edited_name is not None:
                    self.name_list.delete(selected_index)
                    self.name_list.insert(selected_index, edited_name)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def pick_randomly(self):
        try:
            names = self.name_list.get(0, "end")
            if names:
                name = random.choice(names)
                self.result_label.config(text=f"The name picked is {name}")
                if self.remove_on_pick_var.get():
                    self.name_list.delete(self.name_list.get(0, "end").index(name))
                self.save_history(name)
            else:
                messagebox.showerror("Error", "There are no names in the list")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def auto_select(self):
        try:
            names = self.name_list.get(0, "end")
            if names:
                self.auto_selecting = True
                self.dim_frame = ttk.Frame(self.master, width=self.master.winfo_width(), height=self.master.winfo_height())
                self.dim_frame.place(x=0, y=0)
                self.dim_frame.bind("<Button-1>", self.stop_auto_select)
                self.dim_label = ttk.Label(self.dim_frame, text="Click anywhere to stop", foreground="red", font=font.Font(size=20))
                self.dim_label.place(relx=0.5, rely=0.5, anchor="center")
                self.auto_select_thread = threading.Thread(target=self.auto_select_loop)
                self.auto_select_thread.start()
            else:
                messagebox.showerror("Error", "There are no names in the list")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def auto_select_loop(self):
        try:
            while self.auto_selecting:
                names = self.name_list.get(0, "end")
                if names:
                    name = random.choice(names)
                    self.master.after(0, self.update_result_label, name)
                    if self.remove_on_pick_var.get():
                        self.master.after(0, self.remove_selected_name, name)
                    self.save_history(name)
                else:
                    messagebox.showerror("Error", "There are no names in the list")
                time.sleep(0.1)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def update_result_label(self, name):
        self.result_label.config(text=f"The name picked is {name}")

    def remove_selected_name(self, name):
        self.name_list.delete(self.name_list.get(0, "end").index(name))

    def stop_auto_select(self, event):
        try:
            self.auto_selecting = False
            self.dim_frame.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def auto_select_with_time(self):
        try:
            names = self.name_list.get(0, "end")
            if names:
                self.auto_selecting = True
                self.dim_frame = ttk.Frame(self.master, width=self.master.winfo_width(), height=self.master.winfo_height())
                self.dim_frame.place(x=0, y=0)
                self.dim_frame.bind("<Button-1>", self.stop_auto_select)
                self.dim_label = ttk.Label(self.dim_frame, text="", foreground="red", font=font.Font(size=20))
                self.dim_label.place(relx=0.5, rely=0.5, anchor="center")
                self.time_input = simpledialog.askinteger("Enter Time", "Enter the number of seconds for automatic selection:", minvalue=1)
                if self.time_input is not None:
                    self.auto_select_thread = threading.Thread(target=self.auto_select_loop_with_time)
                    self.auto_select_thread.start()
                else:
                    self.stop_auto_select(None)
            else:
                messagebox.showerror("Error", "There are no names in the list")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def auto_select_loop_with_time(self):
        try:
            start_time = time.time()
            while self.auto_selecting and time.time() - start_time < self.time_input:
                names = self.name_list.get(0, "end")
                if names:
                    name = random.choice(names)
                    self.master.after(0, self.update_result_label, name)
                    if self.remove_on_pick_var.get():
                        self.master.after(0, self.remove_selected_name, name)
                    self.save_history(name)
                else:
                    messagebox.showerror("Error", "There are no names in the list")
                self.master.after(100, self.update_time_label, start_time)
                time.sleep(0.1)
            self.stop_auto_select(None)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def update_time_label(self, start_time):
        remaining_time = int(self.time_input - (time.time() - start_time))
        self.dim_label.config(text=f"Click anywhere to stop\n{remaining_time}", justify='center')

    def show_history(self):
        try:
            self.history_frame = ttk.Frame(self.main_frame)
            self.history_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
            self.right_frame.grid_remove()
            self.history_button.config(text="Back to Main Page", command=self.back_to_main_page)
            self.history_display = tk.Text(self.history_frame, state="disabled") 
            createToolTip(self.history_display, "This displays the history of names you have previously selected.")
            self.history_display.config(state="normal")
            self.history_display.insert('end', '\n'.join(self.history_list))
            self.history_display.config(state="disabled")
            self.history_display.grid(row=2, column=0, sticky="nsew")

            scrollbar = ttk.Scrollbar(self.history_frame, command=self.history_display.yview)
            createToolTip(scrollbar, "This is the scrollbar for the history display.")
            scrollbar.grid(row=2, column=1, sticky="ns")
            self.history_display['yscrollcommand'] = scrollbar.set

            self.clear_button = ttk.Button(self.history_frame, text="Clear History", command=self.clear_history)
            createToolTip(self.clear_button, "Click to clear the history.")
            self.clear_button.grid(row=3, column=0, pady=10, sticky="ew")

            self.copy_all_button = ttk.Button(self.history_frame, text="Copy All", command=self.copy_all_history)
            createToolTip(self.copy_all_button, "Click to copy all the history.")
            self.copy_all_button.grid(row=4, column=0, pady=10, sticky="ew")

            self.export_button = ttk.Button(self.history_frame, text="Export History", command=self.export_history)
            createToolTip(self.export_button, "Click to export history.")
            self.export_button.grid(row=5, column=0, pady=10, sticky="ew")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def back_to_main_page(self):
        try:
            self.right_frame.grid()

            if hasattr(self, 'history_frame'):
                self.history_frame.destroy()

            if hasattr(self, 'shortcuts_frame'):
                self.shortcuts_frame.destroy()

            self.history_button.config(text="History", command=self.show_history)
            self.shortcuts_button.config(text="Show Shortcuts", command=self.show_shortcuts)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def load_history(self):
        try:
            with open(self.history_file, 'r') as f:
                self.history_list = json.load(f)
        except FileNotFoundError:
            with open(self.history_file, 'w') as f:
                json.dump(self.history_list, f)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def save_history(self, name):
        try:
            self.history_list.append(name)
            with open(self.history_file, 'w') as f:
                json.dump(self.history_list, f)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def clear_history(self):
        try:
            if self.history_list:
                self.history_list = []
                if self.history_display is not None:
                    self.history_display.config(state="normal")
                    self.history_display.delete('1.0', 'end')
                    self.history_display.config(state="disabled")

                with open(self.history_file, 'w') as f:
                    json.dump(self.history_list, f)

                messagebox.showinfo("Clear History", "History has been cleared.")
            else:
                messagebox.showinfo("Info", "History is already empty.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def copy_all_history(self):
        try:
            if self.history_list:
                pyperclip.copy('\n'.join(self.history_list))
                messagebox.showinfo("Copy All", "History has been copied to the clipboard.")
            else:
                messagebox.showinfo("Info", "History is empty.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def export_history(self):
        try:
            if self.history_list:
                filename = filedialog.asksaveasfilename(defaultextension=".txt", initialfile="history.txt")
                if filename:
                    with open(filename, 'w') as f:
                        f.write('\n'.join(self.history_list))
            else:
                messagebox.showinfo("Info", "History is empty.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def save_options(self):
        try:
            names = self.name_list.get(0, "end")
            if names:
                file_path = filedialog.asksaveasfilename(initialfile="options", defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
                if file_path:
                    with open(file_path, 'w') as f:
                        f.write('\n'.join(names))
            else:
                messagebox.showwarning("No Options", "There are no options to save.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def load_options(self):
        try:
            file_path = filedialog.askopenfilename(title="Load Options", filetypes=[("Text files", "*.txt")])

            if file_path:
                with open(file_path, 'r') as f:
                    self.names = f.read().splitlines()

                self.update_options_list()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def update_options_list(self):
        self.name_list.delete(0, "end")
        for name in self.names:
            self.name_list.insert("end", name)

    def delete_selected_name(self):
        try:
            result_text = self.result_label.cget("text")
            if result_text.startswith("The name picked is"):
                selected_name = result_text[len("The name picked is "):]
                index = self.name_list.get(0, "end").index(selected_name)
                self.name_list.delete(index)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def delete_and_copy_selected_name(self):
        try:
            result_text = self.result_label.cget("text")
            if result_text.startswith("The name picked is"):
                selected_name = result_text[len("The name picked is "):]
                index = self.name_list.get(0, "end").index(selected_name)
                self.name_list.delete(index)
                pyperclip.copy(selected_name)
                messagebox.showinfo("Delete and Copy", f"The selected name '{selected_name}' has been copied to the clipboard.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def shuffle_names(self, event):
        try:
            names = self.name_list.get(0, "end")
            if names:
                names = list(names) 
                random.shuffle(names)
                self.name_list.delete(0, "end")
                for name in names:
                    self.name_list.insert("end", name)
            else:
                messagebox.showwarning("No Names", "There are no names to shuffle")
        except Exception as e: 
            messagebox.showerror("Error", f"An error occurred: {e}")

    def send_feedback(self):
        try:
            webbrowser.open("https://github.com/fatherxtreme123/RandomPicker/issues")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_shortcuts(self):
        try:
            shortcuts_info = (
                "Keyboard Shortcuts:\n"
                "Control-n: Add Name\n"
                "Control-r: Add Range\n"
                "Control-d: Delete Selected Name\n"
                "Control-c: Clear All Names\n"
                "Control-p: Pick Randomly\n"
                "Control-a: Automatic Selection\n"
                "Control-m: Stop Automatic Selection\n"
                "Control-BackSpace: Clear History\n"
                "Control-q: Copy All History\n"
                "Control-e: Export History\n"
                "Control-s: Save Options\n"
                "Control-l: Load Options\n"
                "Control-d: Delete and Copy Selected Name\n"
                "Control-f: Send Feedback\n"
            )

            self.shortcuts_frame = ttk.Frame(self.main_frame)
            self.shortcuts_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

            self.right_frame.grid_remove()

            self.shortcuts_button.config(text="Back to Main Page", command=self.back_to_main_page)

            self.shortcuts_label = ttk.Label(self.shortcuts_frame, text=shortcuts_info)
            self.shortcuts_label.grid(padx=10, pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        App().run()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
