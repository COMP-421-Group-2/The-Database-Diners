import tkinter as tk
from tkinter import ttk

class MultiPageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multipage Interface")

        # Create a container for the pages
        self.container = ttk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        # Dictionary to hold the pages
        self.pages = {}

        # Initialize the pages
        for Page in (Page1, Page2, Page3):
            page = Page(self.container, self)
            self.pages[Page] = page
            page.grid(row=0, column=0, sticky="nsew")

        # Show the first page
        self.show_page(Page1)

    def show_page(self, page_class):
        """Bring a page to the front."""
        page = self.pages[page_class]
        page.tkraise()

class Page1(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = ttk.Label(self, text="This is Page 1")
        label.pack(pady=10)
        button = ttk.Button(self, text="Go to Page 2",
                            command=lambda: controller.show_page(Page2))
        button.pack()

class Page2(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = ttk.Label(self, text="This is Page 2")
        label.pack(pady=10)
        button1 = ttk.Button(self, text="Go to Page 1",
                             command=lambda: controller.show_page(Page1))
        button1.pack()
        button2 = ttk.Button(self, text="Go to Page 3",
                             command=lambda: controller.show_page(Page3))
        button2.pack()

class Page3(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = ttk.Label(self, text="This is Page 3")
        label.pack(pady=10)
        button = ttk.Button(self, text="Go to Page 1",
                            command=lambda: controller.show_page(Page1))
        button.pack()

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = MultiPageApp(root)
    root.mainloop()
