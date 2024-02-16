import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from CTkListbox import *
import random
import threading
import time
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
            tooltip = ctk.CTkToplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = ctk.CTkLabel(tooltip, text=text, fg_color="black", text_color="white")
            label.grid()
            widget._tooltip = tooltip

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)
    except Exception as e:
        CTkMessagebox(title="Error", message=f"An error occurred: {e}")

class App(ctk.CTk):
    def __init__(self):
        try:
            super().__init__()

            self.title('RandomPicker')
            self.iconbitmap('RandomPicker.ico')
            self.resizable(False, False)

            self.main_frame = ctk.CTkFrame(self)
            self.main_frame.grid(row=0, column=0, sticky="nsew")

            self.left_frame = ctk.CTkFrame(self.main_frame, width=200, height=400)
            self.left_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ns")

            self.right_frame = ctk.CTkFrame(self.main_frame)
            self.right_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

            self.input_frame = ctk.CTkFrame(self.right_frame)
            self.input_frame.grid(row=0, column=0, sticky="ew")

            self.history_file = "history.json"
            self.history_list = []
            self.load_history()

            self.input_frame.columnconfigure(0, weight=1)
            self.input_frame.columnconfigure(1, weight=1)

            self.name_input = ctk.CTkEntry(self.input_frame, font=("Arial", 12))
            self.name_input.grid(row=0, column=0, sticky="ew", padx=5, pady=10)
            createToolTip(self.name_input, "Enter a name to add to the list")

            self.add_button = ctk.CTkButton(self.input_frame, text="Add Name", command=self.add_name)
            self.add_button.grid(row=0, column=1, sticky="ew", padx=5, pady=10)
            createToolTip(self.add_button, "Click to add the name entered in the entry box to the list")

            self.add_range_button = ctk.CTkButton(self.input_frame, text="Add Range", command=self.add_range)
            self.add_range_button.grid(row=2, column=1, sticky="ew", padx=5, pady=10)
            createToolTip(self.add_range_button, "Click to add the range of numbers entered in the entry boxes to the list")

            self.start_input = ctk.CTkEntry(self.input_frame, font=("Arial", 12))
            self.start_input.grid(row=2, column=0, sticky="w", padx=5, pady=10)
            createToolTip(self.start_input, "Enter the start value of the range")

            self.end_input = ctk.CTkEntry(self.input_frame, font=("Arial", 12))
            self.end_input.grid(row=2, column=0, sticky="e", padx=5, pady=10)
            createToolTip(self.end_input, "Enter the end value of the range")

            self.start_input.configure(width=139)
            self.end_input.configure(width=139)

            self.name_list = CTkListbox(self.right_frame, font=("Arial", 12), width=560, height=440)
            self.name_list.grid(row=2, column=0, sticky="nsew", pady=10)

            self.pick_button = ctk.CTkButton(self.right_frame, text="Pick Randomly", command=self.pick_randomly)
            self.pick_button.grid(row=3, column=0, sticky="ew", pady=10)
            createToolTip(self.pick_button, "Click to pick a name randomly from the list")

            self.auto_select_button = ctk.CTkButton(self.left_frame, text="Automatic Selection", command=self.auto_select)
            self.auto_select_button.grid(row=0, column=0, sticky="ew", pady=10, padx=5)
            createToolTip(self.auto_select_button, "Click to start automatic selection")

            self.auto_select_symbol = ctk.CTkButton(self.left_frame, text="⮞", command=self.auto_select_with_time, width=30)
            self.auto_select_symbol.grid(row=0, column=1, sticky="ew", pady=10, padx=5)
            createToolTip(self.auto_select_symbol, "Click to enter the number of seconds for automatic selection")

            self.add_multiple_button = ctk.CTkButton(self.left_frame, text="Add Multiple Names", command=self.add_multiple_names)
            self.add_multiple_button.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10, padx=5)
            createToolTip(self.add_multiple_button, "Click to add multiple names to the list")

            self.clear_all_button = ctk.CTkButton(self.left_frame, text="Clear All", command=self.clear_all_names)
            self.clear_all_button.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10, padx=5)
            createToolTip(self.clear_all_button, "Click to clear all names in the list")

            self.remove_duplicates_button = ctk.CTkButton(self.left_frame, text="Remove Duplicates", command=self.remove_duplicates)
            self.remove_duplicates_button.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10, padx=5)
            createToolTip(self.remove_duplicates_button, "Click to remove all duplicate names in the list, keeping only one instance")

            self.history_button = ctk.CTkButton(self.left_frame, text="History", command=self.show_history)
            self.history_button.grid(row=4, column=0, columnspan=2, sticky="ew", pady=10, padx=5)
            createToolTip(self.history_button, "Click to view the history of the names picked")

            self.delete_selected_button = ctk.CTkButton(self.left_frame, text="Delete Selected", command=self.delete_selected_name)
            self.delete_selected_button.grid(row=5, column=0, columnspan=2, sticky="ew", pady=10, padx=5)
            createToolTip(self.delete_selected_button, "Click to delete the selected name")

            self.shuffle_button = ctk.CTkButton(self.left_frame, text="Shuffle Names", command=self.shuffle_names)
            self.shuffle_button.grid(row=6, column=0, columnspan=2, sticky="ew", pady=10, padx=5)
            createToolTip(self.shuffle_button, "Click to shuffle all the names in the list")

            self.save_options_button = ctk.CTkButton(self.left_frame, text="Save Options", command=self.save_options)
            self.save_options_button.grid(row=7, column=0, columnspan=2, sticky="ew", pady=10, padx=5)
            createToolTip(self.save_options_button, "Click to save options to a file")

            self.load_options_button = ctk.CTkButton(self.left_frame, text="Load Options", command=self.load_options)
            self.load_options_button.grid(row=8, column=0, columnspan=2, sticky="ew", pady=10, padx=5)
            createToolTip(self.load_options_button, "Click to load options from a file")

            self.send_feedback_button = ctk.CTkButton(self.left_frame, text="Send Feedback", command=self.send_feedback)
            self.send_feedback_button.grid(row=9, column=0, columnspan=2, sticky="ew", pady=10, padx=5)  
            createToolTip(self.send_feedback_button, "Click to open the GitHub issues page and send feedback")

            self.shortcuts_button = ctk.CTkButton(self.left_frame, text="Show Shortcuts", command=self.show_shortcuts)
            self.shortcuts_button.grid(row=10, column=0, columnspan=2, sticky="ew", pady=10, padx=5)           
            createToolTip(self.shortcuts_button, "Click to view keyboard shortcuts")

            self.remove_on_pick_var = tk.BooleanVar()
            self.remove_on_pick_var.set(False)

            self.result_label = ctk.CTkLabel(self.right_frame, text="", font=("Arial", 30), anchor="center", width=30)
            self.result_label.grid(row=5, column=0, sticky="ew", pady=10)
            createToolTip(self.result_label, "This displays the randomly picked name")

            self.remove_on_pick_checkbox = ctk.CTkCheckBox(self.right_frame, text="Remove on Pick", variable=self.remove_on_pick_var)
            self.remove_on_pick_checkbox.grid(row=4, column=0, sticky="w", pady=10)
            createToolTip(self.remove_on_pick_checkbox, "Check to remove the picked name from the list")

            self.copy_selected_button = ctk.CTkButton(self.right_frame, text="Copy Selected", command=self.copy_selected_name)
            self.copy_selected_button.grid(row=4, column=0, sticky="e", pady=10, padx=(0, 10))
            createToolTip(self.copy_selected_button, "Click to copy the selected name")

            self.bind("<Control-n>", lambda event: self.add_name())
            self.bind("<Control-r>", lambda event: self.add_range())
            self.bind("<Control-c>", lambda event: self.clear_all_names())
            self.bind("<Control-p>", lambda event: self.pick_randomly())
            self.bind("<Control-a>", lambda event: self.auto_select())
            self.bind("<Control-m>", lambda event: self.stop_auto_select(None))
            self.bind("<Control-BackSpace>", lambda event: self.clear_history())
            self.bind("<Control-q>", lambda event: self.copy_all_history())
            self.bind("<Control-e>", lambda event: self.export_history())
            self.bind("<Control-s>", lambda event: self.save_options())
            self.bind("<Control-l>", lambda event: self.load_options())
            self.bind("<Control-f>", lambda event: self.send_feedback())
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def delete_selected_name(self):
        try:
            selected_index = self.name_list.curselection()
            if selected_index:
                self.name_list.delete(selected_index)
            else:
                CTkMessagebox(title="No Selection", message="Please select a name to delete.")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def shuffle_names(self):
        try:
            names = self.get_all_listbox_items(self.name_list)
            random.shuffle(names)
            self.name_list.delete(0, tk.END)
            for name in names:
                self.name_list.insert(tk.END, name)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred while shuffling names: {e}")

    def get_all_listbox_items(self, listbox):
        try:
            items_count = listbox.size()
            items = [listbox.get(i) for i in range(items_count)]
            return items
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def add_name(self):
        try:
            name = self.name_input.get()
            if name:
                self.name_list.insert(tk.END, name)
                self.name_input.delete(0, tk.END)
            else:
                CTkMessagebox(title="Warning", message="Please enter a name")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def add_range(self):
        try:
            start = int(self.start_input.get())
            end = int(self.end_input.get())
            if start <= end:
                for i in range(start, end + 1):
                    self.name_list.insert(tk.END, str(i))
                self.start_input.delete(0, tk.END)
                self.end_input.delete(0, tk.END)
            else:
                CTkMessagebox(title="Error", message="The start value must be less than or equal to the end value")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def add_multiple_names(self):
        try:
            name = ctk.CTkInputDialog(title="Add Multiple Names", text="Enter the name you want to add:")
            name_input = name.get_input()
            if name_input is not None:
                quantity = ctk.CTkInputDialog(title="Add Multiple Names", text="Enter the quantity to add:")
                quantity_input = quantity.get_input()
                if quantity_input is not None:
                    for _ in range(int(quantity_input)):
                        self.name_list.insert(tk.END, name_input)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def clear_all_names(self):
        try:
            self.name_list.delete(0, tk.END)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def remove_duplicates(self):
        try:
            names = self.get_all_listbox_items(self.name_list)
            if not names:
                CTkMessagebox(title="Info", message="The list is already empty.")
                return
            seen = set()
            unique_names = []
            for name in names:
                if name not in seen:
                    seen.add(name)
                    unique_names.append(name)
            if len(names) == len(unique_names):
                CTkMessagebox(title="Info", message="The list does not contain any duplicate names.")
                return
            self.name_list.delete(0, tk.END)
            for name in unique_names:
                self.name_list.insert(tk.END, name)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def copy_selected_name(self):
        try:
            result_text = self.result_label.cget("text")
            if result_text == "":
                CTkMessagebox(title="No Selected Name", message="There is no selected name to copy.")
                return
            selected_name = result_text[len(" "):]
            pyperclip.copy(selected_name)
            CTkMessagebox(title="Copy Selected", message=f"The selected name '{selected_name}' has been copied to the clipboard.")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def pick_randomly(self):
        try:
            names = self.get_all_listbox_items(self.name_list)
            if names:
                name = random.choice(names)
                self.result_label.configure(text=f" {name}")
                if self.remove_on_pick_var.get():
                    self.name_list.delete(self.get_all_listbox_items(self.name_list).index(name))
                self.save_history(name)
            else:
                CTkMessagebox(title="Error", message="There are no names in the list")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def auto_select(self):
        try:
            names = self.get_all_listbox_items(self.name_list)
            if names:
                self.auto_selecting = True
                self.dim_frame = ctk.CTkFrame(self, width=self.winfo_width(), height=self.winfo_height())
                self.dim_frame.place(x=0, y=0)
                self.dim_frame.bind("<Button-1>", self.stop_auto_select)
                self.dim_label = ctk.CTkLabel(self.dim_frame, text="Click anywhere to stop", font=("Arial", 20))
                self.dim_label.place(relx=0.5, rely=0.5, anchor="center")
                self.auto_select_thread = threading.Thread(target=self.auto_select_loop)
                self.auto_select_thread.start()
            else:
                CTkMessagebox(title="Error", message="There are no names in the list")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def auto_select_loop(self):
        try:
            while self.auto_selecting:
                names = self.get_all_listbox_items(self.name_list)
                if names:
                    name = random.choice(names)
                    self.after(0, self.update_result_label, name)
                    if self.remove_on_pick_var.get():
                        index_to_remove = names.index(name)
                        self.after(0, self.name_list.delete, index_to_remove)
                    self.save_history(name)
                else:
                    CTkMessagebox(title="Error", message="There are no names in the list")
                time.sleep(0.1)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def update_result_label(self, name):
        try:
            self.result_label.configure(text=f"{name}")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def remove_selected_name(self, name):
        try:
            self.name_list.delete(self.name_list.get(0, tk.END).index(name))
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def stop_auto_select(self, event):
        try:
            self.auto_selecting = False
            self.dim_frame.destroy()
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def auto_select_with_time(self):
        try:
            names = self.get_all_listbox_items(self.name_list)
            if names:
                self.auto_selecting = True
                self.dim_frame = ctk.CTkFrame(self, width=self.winfo_width(), height=self.winfo_height())
                self.dim_frame.place(x=0, y=0)
                self.dim_frame.bind("<Button-1>", self.stop_auto_select)
                self.dim_label = ctk.CTkLabel(self.dim_frame, text="", font=("Arial", 20))
                self.dim_label.place(relx=0.5, rely=0.5, anchor="center")
                time_input_dialog = ctk.CTkInputDialog(title="Enter Time", text="Enter the number of seconds for automatic selection:")
                time_input = time_input_dialog.get_input()
                if time_input is not None:
                    self.time_input = int(time_input)
                    self.auto_select_thread = threading.Thread(target=self.auto_select_loop_with_time)
                    self.auto_select_thread.start()
                else:
                    self.stop_auto_select(None)
            else:
                CTkMessagebox(title="Error", message="There are no names in the list")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def auto_select_loop_with_time(self):
        try:
            start_time = time.time()
            while self.auto_selecting and time.time() - start_time < self.time_input:
                names = self.get_all_listbox_items(self.name_list)
                if names:
                    name = random.choice(names)
                    self.after(0, self.update_result_label, name)
                    if self.remove_on_pick_var.get():
                        self.after(0, self.remove_selected_name, name)
                    self.save_history(name)
                else:
                    CTkMessagebox(title="Error", message="There are no names in the list")
                self.after(100, self.update_time_label, start_time)
                time.sleep(0.1)
            self.stop_auto_select(None)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def update_time_label(self, start_time):
        try:
            remaining_time = int(self.time_input - (time.time() - start_time))
            if hasattr(self, 'dim_label') and self.dim_label.winfo_exists():
                self.dim_label.configure(text=f"Click anywhere to stop\n{remaining_time}")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def show_history(self):
        try:
            self.history_frame = ctk.CTkFrame(self.main_frame)
            self.history_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
            self.right_frame.grid_remove()
            self.history_button.configure(text="Back to Main Page", command=self.back_to_main_page)
            
            self.history_display = CTkListbox(self.history_frame, font=("Arial", 12), width=550, height=420)
            
            self.history_display.grid(row=2, column=0, sticky="nsew")

            self.clear_button = ctk.CTkButton(self.history_frame, text="Clear History", command=self.clear_history)
            createToolTip(self.clear_button, "Click to clear the history.")
            self.clear_button.grid(row=3, column=0, pady=10, sticky="ew")

            self.copy_all_button = ctk.CTkButton(self.history_frame, text="Copy All", command=self.copy_all_history)
            createToolTip(self.copy_all_button, "Click to copy all the history.")
            self.copy_all_button.grid(row=4, column=0, pady=10, sticky="ew")

            self.export_button = ctk.CTkButton(self.history_frame, text="Export History", command=self.export_history)
            createToolTip(self.export_button, "Click to export history.")
            self.export_button.grid(row=5, column=0, pady=10, sticky="ew")

            threading.Thread(target=self.load_history_in_background, daemon=True).start()
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def load_history_in_background(self):
        try:
            with open(self.history_file, 'r') as f:
                history_list = json.load(f)
            
            self.after(0, self.update_history_display, history_list)
        except FileNotFoundError:
            with open(self.history_file, 'w') as f:
                json.dump([], f)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred while loading history: {e}")

    def update_history_display(self, history_list):
        try:
            self.history_display.delete(0, tk.END)
            for item in history_list:
                self.history_display.insert(tk.END, item)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred while updating history display: {e}")

    def back_to_main_page(self):
        try:
            self.right_frame.grid()

            if hasattr(self, 'history_frame'):
                self.history_frame.destroy()

            if hasattr(self, 'shortcuts_frame'):
                self.shortcuts_frame.destroy()

            self.history_button.configure(text="History", command=self.show_history)
            self.shortcuts_button.configure(text="Show Shortcuts", command=self.show_shortcuts)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def load_history(self):
        try:
            try:
                with open(self.history_file, 'r') as f:
                    self.history_list = json.load(f)
            except FileNotFoundError:
                with open(self.history_file, 'w') as f:
                    json.dump(self.history_list, f)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def save_history(self, name):
        try:
            self.history_list.append(name)
            
            if len(self.history_list) > 100:
                self.history_list.pop(0)
            
            if hasattr(self, 'history_display') and self.history_display.winfo_exists():
                self.history_display.insert(tk.END, name)
                if self.history_display.size() > 100:
                    self.history_display.delete(0)
            
            with open(self.history_file, 'w') as f:
                json.dump(self.history_list, f)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def clear_history(self):
        try:
            if self.history_list:
                self.history_list = []
                if hasattr(self, 'history_display') and self.history_display.winfo_exists():
                    self.history_display.delete(0, tk.END)

                with open(self.history_file, 'w') as f:
                    json.dump(self.history_list, f)

                CTkMessagebox(title="Clear History", message="History has been cleared.")
            else:
                CTkMessagebox(title="Info", message="History is already empty.")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def copy_all_history(self):
        try:
            if self.history_list:
                pyperclip.copy('\n'.join(self.history_list))
                CTkMessagebox(title="Copy All", message="History has been copied to the clipboard.")
            else:
                CTkMessagebox(title="Info", message="History is empty.")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def export_history(self):
        try:
            if self.history_list:
                filename = filedialog.asksaveasfilename(defaultextension=".txt", initialfile="history.txt")
                if filename:
                    with open(filename, 'w') as f:
                        f.write('\n'.join(self.history_list))
            else:
                CTkMessagebox(title="Info", message="History is empty.")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def save_options(self):
        try:
            names = self.get_all_listbox_items(self.name_list)
            if names:
                file_path = filedialog.asksaveasfilename(initialfile="options", defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
                if file_path:
                    with open(file_path, 'w') as f:
                        f.write('\n'.join(names))
            else:
                CTkMessagebox(title="No Options", message="There are no options to save.")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def load_options(self):
        try:
            file_path = filedialog.askopenfilename(title="Load Options", filetypes=[("Text files", "*.txt")])

            if file_path:
                with open(file_path, 'r') as f:
                    self.names = f.read().splitlines()

                self.update_options_list()
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def update_options_list(self):
        try:
            self.name_list.delete(0, tk.END)
            for name in self.names:
                self.name_list.insert(tk.END, name)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

    def send_feedback(self):
        try:
            webbrowser.open("https://github.com/fatherxtreme123/RandomPicker/issues")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

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

            self.shortcuts_frame = ctk.CTkFrame(self.main_frame)
            self.shortcuts_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

            self.right_frame.grid_remove()

            self.shortcuts_button.configure(text="Back to Main Page", command=self.back_to_main_page)

            self.shortcuts_label = ctk.CTkLabel(self.shortcuts_frame, text=shortcuts_info)
            self.shortcuts_label.grid(padx=10, pady=10)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        CTkMessagebox(title="Error", message=f"An error occurred: {e}")
