import os
import tkinter as tk
from tkinter import filedialog, messagebox

def create_from_ascii_tree(file_path, folder_name, save_location):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        root_path = os.path.join(save_location, folder_name)
        os.makedirs(root_path, exist_ok=True)

        stack = [root_path]
        prev_indent = 0

        for line in lines:
            line = line.rstrip()
            if not line.strip():
                continue

            stripped = line.lstrip('│├─└ ')
            indent = len(line) - len(stripped)

            while indent < prev_indent:
                stack.pop()
                prev_indent -= 4  # assumes 4 spaces per indent level

            current_path = os.path.join(stack[-1], stripped.strip())

            # Handle "or" in filenames
            if ' or ' in stripped:
                filenames = [name.strip() for name in stripped.split(' or ')]
                for fname in filenames:
                    open(os.path.join(stack[-1], fname), 'a').close()
            elif '.' in stripped:
                open(current_path, 'a').close()
            else:
                os.makedirs(current_path, exist_ok=True)
                stack.append(current_path)
                prev_indent = indent

        messagebox.showinfo("Success", f"Folder structure created in:\n{root_path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI Function
def run_gui():
    def browse_file():
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        input_file_var.set(path)

    def browse_save_folder():
        path = filedialog.askdirectory()
        save_location_var.set(path)

    def start_creation():
        create_from_ascii_tree(
            input_file_var.get(),
            folder_name_var.get(),
            save_location_var.get()
        )

    root = tk.Tk()
    root.title("Project Structure Creator")
    root.geometry("500x250")           # Set initial window size
    root.minsize(500, 250)             # Minimum window size
    root.maxsize(500, 250)             # Maximum window size


    input_file_var = tk.StringVar()
    folder_name_var = tk.StringVar()
    save_location_var = tk.StringVar()

    tk.Label(root, text="Select structure text file:").pack()
    tk.Entry(root, textvariable=input_file_var, width=50).pack()
    tk.Button(root, text="Browse File", command=browse_file).pack(pady=5)

    tk.Label(root, text="Enter parent folder name:").pack()
    tk.Entry(root, textvariable=folder_name_var, width=50).pack()

    tk.Label(root, text="Choose save location:").pack()
    tk.Entry(root, textvariable=save_location_var, width=50).pack()
    tk.Button(root, text="Browse Folder", command=browse_save_folder).pack(pady=5)

    tk.Button(root, text="Create Structure", bg="green", fg="white", command=start_creation).pack(pady=10)

    root.mainloop()

# Run the GUI
run_gui()
