import tkinter as tk
from tkinter import filedialog, messagebox, ttk,Tk, PhotoImage
import os, sys
from image_tools import resize_images_in_directory, add_watermark_to_directory,resize_and_watermark_directory


class ImageToolApp:
    def __init__(self, master):
        self.master = master
        master.title("Image Resizer & Watermarker")
        master.geometry("540x360")
        master.resizable(False, False)

        # === Input/Output Selection ===
        tk.Label(master, text="Input Folder:").grid(row=0, column=0, sticky="w", padx=10, pady=8)
        self.input_entry = tk.Entry(master, width=50)
        self.input_entry.grid(row=0, column=1)
        tk.Button(master, text="Browse", command=self.select_input).grid(row=0, column=2)

        tk.Label(master, text="Output Folder:").grid(row=1, column=0, sticky="w", padx=10)
        self.output_entry = tk.Entry(master, width=50)
        self.output_entry.grid(row=1, column=1)
        tk.Button(master, text="Browse", command=self.select_output).grid(row=1, column=2)

        # === Resize Option ===
        self.resize_var = tk.BooleanVar(value=True)
        tk.Checkbutton(master, text="Resize Images", variable=self.resize_var).grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=10)

        # === Watermark Option ===
        self.watermark_var = tk.BooleanVar()
        self.wm_checkbox = tk.Checkbutton(master, text="Add Watermark", variable=self.watermark_var, command=self.toggle_watermark_options)
        self.wm_checkbox.grid(row=3, column=0, columnspan=2, sticky="w", padx=10)

        # === Watermark Type (Text vs Image) ===
        self.wm_type = tk.StringVar(value="text")
        self.radio_text = tk.Radiobutton(master, text="Text", variable=self.wm_type, value="text", state='disabled', command=self.toggle_watermark_inputs)
        self.radio_image = tk.Radiobutton(master, text="Image", variable=self.wm_type, value="image", state='disabled', command=self.toggle_watermark_inputs)
        self.radio_text.grid(row=4, column=0, sticky="w", padx=30)
        self.radio_image.grid(row=4, column=1, sticky="w")

        # === Watermark Text Input ===
        self.text_entry = tk.Entry(master, width=40, state='disabled')
        self.text_entry.insert(0, "© YourName")
        self.text_entry.grid(row=5, column=0, columnspan=2, sticky="w", padx=30)

        # === Watermark Logo Image Input ===
        # === Watermark Logo Input Row (Better aligned inside a frame) ===
        logo_frame = tk.Frame(master)
        logo_frame.grid(row=6, column=0, columnspan=3, sticky="w", padx=30)

        self.logo_entry = tk.Entry(logo_frame, width=36, state='disabled')
        self.logo_entry.pack(side="left", padx=(0, 8))

        self.logo_browse = tk.Button(logo_frame, text="Browse PNG", state='disabled', command=self.select_logo)
        self.logo_browse.pack(side="left")

        """
        self.logo_entry = tk.Entry(master, width=40, state='disabled')
        self.logo_entry.grid(row=6, column=0, columnspan=2, sticky="w", padx=30)
        self.logo_browse = tk.Button(master, text="Browse PNG", state='disabled', command=self.select_logo)
        self.logo_browse.grid(row=6, column=2, sticky="w")
        """

        # === Process Button ===
        tk.Button(master, text="Process Images", command=self.process).grid(row=7, column=1, pady=20)

    def toggle_watermark_options(self):
        enable = self.watermark_var.get()
        state = 'normal' if enable else 'disabled'
        self.radio_text.config(state=state)
        self.radio_image.config(state=state)
        self.toggle_watermark_inputs()

    def toggle_watermark_inputs(self):
        if self.wm_type.get() == "text" and self.watermark_var.get():
            self.text_entry.config(state='normal')
            self.logo_entry.config(state='disabled')
            self.logo_browse.config(state='disabled')
        elif self.wm_type.get() == "image" and self.watermark_var.get():
            self.text_entry.config(state='disabled')
            self.logo_entry.config(state='normal')
            self.logo_browse.config(state='normal')
        else:
            self.text_entry.config(state='disabled')
            self.logo_entry.config(state='disabled')
            self.logo_browse.config(state='disabled')

    def select_input(self):
        path = filedialog.askdirectory()
        if path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, path)

    def select_output(self):
        path = filedialog.askdirectory()
        if path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, path)

    def select_logo(self):
        path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png")])
        if path:
            self.logo_entry.delete(0, tk.END)
            self.logo_entry.insert(0, path)

    def process(self):
        input_dir = self.input_entry.get()
        output_dir = self.output_entry.get()

        if not os.path.isdir(input_dir) or not os.path.isdir(output_dir):
            messagebox.showerror("Error", "Invalid input/output folder.")
            return

        try:
            wm_text = self.text_entry.get() if (self.watermark_var.get() and self.wm_type.get() == "text") else None
            wm_logo = self.logo_entry.get() if (self.watermark_var.get() and self.wm_type.get() == "image") else None

            # Decide what function to call based on toggles
            if self.resize_var.get() and self.watermark_var.get():
                resize_and_watermark_directory(input_dir, output_dir, watermark_text=wm_text, watermark_logo_path=wm_logo)
            elif self.resize_var.get():
                resize_images_in_directory(input_dir, output_dir)
            elif self.watermark_var.get():
                add_watermark_to_directory(input_dir, output_dir, watermark_text=wm_text, watermark_logo_path=wm_logo)
            else:
                messagebox.showinfo("Notice", "Nothing selected.")
                return

            messagebox.showinfo("Done", "Images processed successfully.")

        except Exception as e:
            messagebox.showerror("Error", str(e))


# === Resource Path Helper for PyInstaller === 
def resource_path(relative_path):
    """Get absolute path to resource (for PyInstaller EXE)"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# === Start App ===
if __name__ == "__main__":
    root = tk.Tk()
    icon = PhotoImage(file=resource_path("assets/bird.gif"))
    root.iconphoto(False, icon)
    app = ImageToolApp(root)
    root.mainloop()
