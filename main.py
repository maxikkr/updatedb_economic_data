import tkinter as tk
from tkinter import ttk


class CommandLineApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Command Line Search Tool")
        self.geometry("800x600")
        self.configure(bg="black")

        self.command_var = tk.StringVar()
        self.command_var.trace("w", self.update_suggestions)

        self.create_widgets()
        self.commands = {
            'EQ': 'Equity - Stocks and shares',
            'ETF': 'Exchange-Traded Fund',
            'IDX': 'Index - Market indices',
            'OPT': 'Option - Derivative contracts',
            'B': 'Bond - Debt securities'
        }
        self.action_types = {
            'N': 'News',
            'INFO': 'Information',
            'R': 'Realtime Data'
        }

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TLabel", background="black", foreground="white", font=('Consolas', 12))
        style.configure("TEntry", font=('Consolas', 12))
        style.configure("TListbox", font=('Consolas', 12))
        style.configure("TFrame", background="black")

        # Frame for entry and suggestions
        self.entry_frame = tk.Frame(self, bg="black")
        self.entry_frame.pack(fill=tk.X, padx=10, pady=10)

        # Command entry
        self.command_entry = tk.Entry(self.entry_frame, textvariable=self.command_var, font=('Consolas', 12), bg="#333",
                                      fg="white", insertbackground="white", relief=tk.FLAT)
        self.command_entry.pack(fill=tk.X, side=tk.TOP)
        self.command_entry.bind('<Return>', self.process_command)
        self.command_entry.bind('<Tab>', self.complete_command)
        self.command_entry.bind('<Down>', self.navigate_suggestions)
        self.command_entry.bind('<Up>', self.navigate_suggestions)

        # Suggestions listbox
        self.suggestion_listbox = tk.Listbox(self.entry_frame, font=('Consolas', 12), bg="#333", fg="white",
                                             selectbackground="gray", highlightbackground="white", activestyle="none",
                                             height=5, relief=tk.FLAT)
        self.suggestion_listbox.pack(fill=tk.X, side=tk.BOTTOM)
        self.suggestion_listbox.bind('<Return>', self.insert_suggestion)
        self.suggestion_listbox.bind('<Double-1>', self.insert_suggestion)

        # Frame to hold results
        self.results_frame = tk.Frame(self, bg="black")
        self.results_frame.pack(fill=tk.BOTH, expand=True)

        self.results_canvas = tk.Canvas(self.results_frame, bg="black")
        self.results_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.results_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.scrollable_frame = ttk.Frame(self.results_canvas, style="TFrame")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.results_canvas.configure(
                scrollregion=self.results_canvas.bbox("all")
            )
        )

        self.results_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.results_canvas.configure(yscrollcommand=self.scrollbar.set)

    def update_suggestions(self, *args):
        input_text = self.command_var.get().upper()
        self.suggestion_listbox.delete(0, tk.END)

        parts = input_text.split()
        if len(parts) == 1:
            # Show asset class suggestions
            for key in self.commands.keys():
                if key.startswith(parts[0]):
                    self.suggestion_listbox.insert(tk.END, key + " - " + self.commands[key])
        elif len(parts) == 2:
            # Show action type suggestions if asset class is valid
            if parts[0] in self.commands:
                for action in self.action_types.keys():
                    if action.startswith(parts[1]):
                        self.suggestion_listbox.insert(tk.END, f"{parts[0]} {action} - {self.action_types[action]}")
        elif len(parts) == 3:
            # Show completed suggestions if all parts are entered
            self.suggestion_listbox.insert(tk.END, input_text.upper())

    def complete_command(self, event):
        current_text = self.command_var.get().upper()
        if self.suggestion_listbox.size() > 0:
            suggestion = self.suggestion_listbox.get(0).split(" - ")[0]
            self.command_var.set(suggestion)
            self.command_entry.icursor(tk.END)
        return "break"

    def navigate_suggestions(self, event):
        if event.keysym == 'Down':
            if self.suggestion_listbox.size() > 0:
                current_selection = self.suggestion_listbox.curselection()
                if current_selection:
                    next_index = current_selection[0] + 1
                    if next_index < self.suggestion_listbox.size():
                        self.suggestion_listbox.select_clear(current_selection[0])
                        self.suggestion_listbox.select_set(next_index)
                        self.suggestion_listbox.activate(next_index)
                        self.suggestion_listbox.see(next_index)
                else:
                    self.suggestion_listbox.select_set(0)
                    self.suggestion_listbox.activate(0)
                    self.suggestion_listbox.see(0)
        elif event.keysym == 'Up':
            if self.suggestion_listbox.size() > 0:
                current_selection = self.suggestion_listbox.curselection()
                if current_selection:
                    next_index = current_selection[0] - 1
                    if next_index >= 0:
                        self.suggestion_listbox.select_clear(current_selection[0])
                        self.suggestion_listbox.select_set(next_index)
                        self.suggestion_listbox.activate(next_index)
                        self.suggestion_listbox.see(next_index)
        return "break"

    def insert_suggestion(self, event):
        suggestion = self.suggestion_listbox.get(tk.ACTIVE).split(" - ")[0]
        self.command_var.set(suggestion)
        self.command_entry.icursor(tk.END)

    def process_command(self, event):
        command = self.command_var.get().split()

        if len(command) == 3:
            asset_class, action_type, ticker = command

            # Dummy data for demonstration
            data = f"Showing results for {asset_class} {action_type} {ticker}"

            # Clear previous results
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()

            # Display results
            result_label = tk.Label(self.scrollable_frame, text=data, bg="black", fg="white", font=('Consolas', 12))
            result_label.pack()
        else:
            print("Invalid command format. Expected: <AssetClass> <ActionType> <Ticker>")


if __name__ == "__main__":
    app = CommandLineApp()
    app.mainloop()
