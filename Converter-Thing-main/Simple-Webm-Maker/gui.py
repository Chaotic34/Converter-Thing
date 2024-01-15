import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def convert_image(input_path, output_folder, quality, use_lossless, use_multi_threading, success_messages):
    try:
        # Get the path to cwebp.exe in the same folder as the script
        cwebp_path = os.path.join(os.path.dirname(__file__), "cwebp.exe")

        # Ensure output directory exists
        os.makedirs(output_folder, exist_ok=True)

        # Construct the output file path within the "output" folder
        _, input_filename = os.path.split(input_path)
        output_file_path = os.path.join(output_folder, os.path.splitext(input_filename)[0] + ".webp")

        # Construct the command list
        command = [cwebp_path, input_path, "-o", output_file_path, "-m", str(quality)]

        # Add -lossless option if lossless mode is enabled
        if use_lossless:
            command.append("-lossless")

        # Add -mt option if multi-threading is enabled
        if use_multi_threading:
            command.append("-mt")

        # Use cwebp.exe to convert the image
        subprocess.run(command)
        success_messages.append(f"Image converted: {input_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Error during conversion of {input_path}: {str(e)}")

def open_file_dialog(entry, allowed_types):
    file_path = filedialog.askopenfilenames(filetypes=allowed_types)
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, ";".join(file_path))

def open_directory_dialog(entry):
    dir_path = filedialog.askdirectory()
    if dir_path:
        entry.delete(0, tk.END)
        entry.insert(0, dir_path)

# Create the main window
root = tk.Tk()
root.title("Image Converter")

# Input Files
input_frame = tk.Frame(root)
input_label = tk.Label(input_frame, text="Input Files/Folder:")
input_label.pack(side=tk.LEFT, padx=5)
input_entry = tk.Entry(input_frame, width=40)
input_entry.pack(side=tk.LEFT, padx=5)
input_button = tk.Button(input_frame, text="Browse", command=lambda: open_file_dialog(input_entry, [("Image files", "*.png;*.jpg;*.jpeg;*.tiff;*.webp")]))
input_button.pack(side=tk.LEFT, padx=5)
input_frame.pack(pady=10)

# Output Directory
output_frame = tk.Frame(root)
output_label = tk.Label(output_frame, text="Output Location:")
output_label.pack(side=tk.LEFT, padx=5)
output_entry = tk.Entry(output_frame, width=40)
output_entry.pack(side=tk.LEFT, padx=5)
output_entry.insert(0, "output")  # Set initial value to "output"
output_button = tk.Button(output_frame, text="Browse", command=lambda: open_directory_dialog(output_entry))
output_button.pack(side=tk.LEFT, padx=5)
output_frame.pack(pady=10)

# Quality Slider
quality_frame = tk.Frame(root)
quality_label = tk.Label(quality_frame, text="Quality:")
quality_label.pack(side=tk.LEFT, padx=5)
quality_var = tk.IntVar()
quality_slider = tk.Scale(quality_frame, from_=1, to=6, orient=tk.HORIZONTAL, variable=quality_var, length=200)
quality_slider.set(4)  # Set a default value
quality_slider.pack(side=tk.LEFT, padx=5)
quality_frame.pack(pady=10)

# Lossless Checkbox
lossless_var = tk.BooleanVar()
lossless_checkbox = tk.Checkbutton(root, text="Use Lossless", variable=lossless_var)
lossless_checkbox.pack(pady=5)

# Multi-threading Checkbox
mt_var = tk.BooleanVar()
mt_checkbox = tk.Checkbutton(root, text="Use Multi-Threading", variable=mt_var)
mt_checkbox.pack(pady=5)

# Convert Button
def convert_button_click():
    input_paths = input_entry.get().split(";")
    output_folder = output_entry.get()
    quality = quality_var.get()
    use_lossless = lossless_var.get()
    use_multi_threading = mt_var.get()

    success_messages = []  # Accumulate success messages

    for input_path in input_paths:
        convert_image(input_path.strip(), output_folder, quality, use_lossless, use_multi_threading, success_messages)

    # Display a single message box with all success messages
    if success_messages:
        messagebox.showinfo("Batch Conversion Complete", "\n".join(success_messages))

convert_button = tk.Button(root, text="Convert Images", command=convert_button_click)
convert_button.pack(pady=20)

# Start the GUI event loop
root.mainloop()
