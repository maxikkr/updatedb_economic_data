import tkinter as tk
#import api
#import updater

def on_enter(event=None):
    input_text = entry.get()
    print(input_text)
    entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()

    root.geometry("800x800")
    root.title("Stonkers")

    entry = tk.Entry(root, font=("Arial", 16))
    entry.pack()
    entry.bind("<Return>", on_enter)

    root.mainloop()