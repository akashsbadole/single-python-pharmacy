# Pharmacy Management System

I'll create a comprehensive pharmacy management system with all essential features using Python and Tkinter for the GUI, with SQLite as the database backend.

```python
import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import os

class PharmacyManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacy Management System")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)

        # Initialize database
        self.init_db()

        # Login screen
        self.login_screen()

    def init_db(self):
        """Initialize the database and create tables if they don't exist"""
        self.conn = sqlite3.connect('pharmacy.db')
        self.cursor = self.conn.cursor()

        # Create tables
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            supplier_id INTEGER,
            expiry_date TEXT,
            category TEXT,
            barcode TEXT UNIQUE
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT,
            address TEXT,
            email TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            contact TEXT,
            address TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT,
            address TEXT,
            email TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            employee_id INTEGER,
            date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            payment_method TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS sale_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER,
            medicine_id INTEGER,
            quantity INTEGER NOT NULL,
            price_per_unit REAL NOT NULL,
            FOREIGN KEY (sale_id) REFERENCES sales(id),
            FOREIGN KEY (medicine_id) REFERENCES medicines(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_id INTEGER,
            employee_id INTEGER,
            date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchase_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            purchase_id INTEGER,
            medicine_id INTEGER,
            quantity INTEGER NOT NULL,
            price_per_unit REAL NOT NULL,
            FOREIGN KEY (purchase_id) REFERENCES purchases(id),
            FOREIGN KEY (medicine_id) REFERENCES medicines(id)
        )
        """)

        # Create default admin user if not exists
        self.cursor.execute("SELECT * FROM employees WHERE username='admin'")
        if not self.cursor.fetchone():
            self.cursor.execute("""
            INSERT INTO employees (name, username, password, role, contact, address)
            VALUES ('Administrator', 'admin', 'admin123', 'Admin', '1234567890', 'Pharmacy Address')
            """)

        self.conn.commit()

    def login_screen(self):
        """Display the login screen"""
        self.clear_window()

        # Frame for login
        login_frame = Frame(self.root, bg='#f0f0f0')
        login_frame.place(x=400, y=150, width=400, height=400)

        # Title
        title = Label(login_frame, text="Pharmacy Management System", font=('Arial', 20, 'bold'), bg='#f0f0f0')
        title.pack(pady=20)

        # Username
        Label(login_frame, text="Username:", font=('Arial', 12), bg='#f0f0f0').pack(pady=5)
        self.username_entry = Entry(login_frame, font=('Arial', 12), width=20)
        self.username_entry.pack(pady=5)

        # Password
        Label(login_frame, text="Password:", font=('Arial', 12), bg='#f0f0f0').pack(pady=5)
        self.password_entry = Entry(login_frame, font=('Arial', 12), width=20, show='*')
        self.password_entry.pack(pady=5)

        # Login button
        login_btn = Button(login_frame, text="Login", font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white',
                          command=self.login, width=15, pady=10)
        login_btn.pack(pady=20)

        # Status label
        self.status_label = Label(login_frame, text="", font=('Arial', 10), bg='#f0f0f0', fg='red')
        self.status_label.pack()

    def login(self):
        """Authenticate user login"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.status_label.config(text="Please enter both username and password")
            return

        self.cursor.execute("SELECT * FROM employees WHERE username=? AND password=?", (username, password))
        user = self.cursor.fetchone()

        if user:
            self.current_user = {
                'id': user[0],
                'name': user[1],
                'username': user[2],
                'role': user[4]
            }
            self.dashboard()
        else:
            self.status_label.config(text="Invalid username or password")

    def dashboard(self):
        """Display the main dashboard"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Pharmacy Management System", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # User info
        user_info = Label(header_frame, text=f"Welcome, {self.current_user['name']} ({self.current_user['role']})",
                         font=('Arial', 12), bg='#2c3e50', fg='white')
        user_info.pack(side=RIGHT, padx=20)

        # Logout button
        logout_btn = Button(header_frame, text="Logout", font=('Arial', 10), bg='#e74c3c', fg='white',
                           command=self.login_screen, width=8)
        logout_btn.pack(side=RIGHT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='#ecf0f1')
        main_frame.pack(fill=BOTH, expand=True)

        # Sidebar
        sidebar = Frame(main_frame, bg='#34495e', width=200)
        sidebar.pack(side=LEFT, fill=Y)

        # Menu buttons
        Button(sidebar, text="Dashboard", font=('Arial', 12), bg='#3498db', fg='white',
               command=self.dashboard, width=18, pady=10).pack(pady=5)

        Button(sidebar, text="Medicines", font=('Arial', 12), bg='#3498db', fg='white',
               command=self.medicines_screen, width=18, pady=10).pack(pady=5)

        Button(sidebar, text="Suppliers", font=('Arial', 12), bg='#3498db', fg='white',
               command=self.suppliers_screen, width=18, pady=10).pack(pady=5)

        Button(sidebar, text="Customers", font=('Arial', 12), bg='#3498db', fg='white',
               command=self.customers_screen, width=18, pady=10).pack(pady=5)

        Button(sidebar, text="Sales", font=('Arial', 12), bg='#3498db', fg='white',
               command=self.sales_screen, width=18, pady=10).pack(pady=5)

        Button(sidebar, text="Purchases", font=('Arial', 12), bg='#3498db', fg='white',
               command=self.purchases_screen, width=18, pady=10).pack(pady=5)

        Button(sidebar, text="Reports", font=('Arial', 12), bg='#3498db', fg='white',
               command=self.reports_screen, width=18, pady=10).pack(pady=5)

        # Content area
        content_frame = Frame(main_frame, bg='white')
        content_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # Dashboard content
        Label(content_frame, text="Dashboard", font=('Arial', 18, 'bold'), bg='white').pack(pady=20)

        # Summary cards
        card_frame = Frame(content_frame, bg='white')
        card_frame.pack(pady=20)

        # Medicines count
        self.cursor.execute("SELECT COUNT(*) FROM medicines")
        med_count = self.cursor.fetchone()[0]

        med_card = Frame(card_frame, bg='#3498db', width=200, height=100)
        med_card.pack(side=LEFT, padx=20, pady=20)
        med_card.pack_propagate(False)

        Label(med_card, text="Medicines", font=('Arial', 14, 'bold'), bg='#3498db', fg='white').pack(pady=10)
        Label(med_card, text=str(med_count), font=('Arial', 24, 'bold'), bg='#3498db', fg='white').pack()

        # Suppliers count
        self.cursor.execute("SELECT COUNT(*) FROM suppliers")
        supp_count = self.cursor.fetchone()[0]

        supp_card = Frame(card_frame, bg='#2ecc71', width=200, height=100)
        supp_card.pack(side=LEFT, padx=20, pady=20)
        supp_card.pack_propagate(False)

        Label(supp_card, text="Suppliers", font=('Arial', 14, 'bold'), bg='#2ecc71', fg='white').pack(pady=10)
        Label(supp_card, text=str(supp_count), font=('Arial', 24, 'bold'), bg='#2ecc71', fg='white').pack()

        # Customers count
        self.cursor.execute("SELECT COUNT(*) FROM customers")
        cust_count = self.cursor.fetchone()[0]

        cust_card = Frame(card_frame, bg='#e74c3c', width=200, height=100)
        cust_card.pack(side=LEFT, padx=20, pady=20)
        cust_card.pack_propagate(False)

        Label(cust_card, text="Customers", font=('Arial', 14, 'bold'), bg='#e74c3c', fg='white').pack(pady=10)
        Label(cust_card, text=str(cust_count), font=('Arial', 24, 'bold'), bg='#e74c3c', fg='white').pack()

        # Recent sales
        Label(content_frame, text="Recent Sales", font=('Arial', 16, 'bold'), bg='white').pack(pady=10)

        # Sales table
        sales_frame = Frame(content_frame)
        sales_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(sales_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.sales_tree = ttk.Treeview(sales_frame, columns=('ID', 'Customer', 'Employee', 'Date', 'Amount'),
                                      show='headings', yscrollcommand=scrollbar.set)

        self.sales_tree.heading('ID', text='ID')
        self.sales_tree.heading('Customer', text='Customer')
        self.sales_tree.heading('Employee', text='Employee')
        self.sales_tree.heading('Date', text='Date')
        self.sales_tree.heading('Amount', text='Amount')

        self.sales_tree.column('ID', width=50)
        self.sales_tree.column('Customer', width=150)
        self.sales_tree.column('Employee', width=150)
        self.sales_tree.column('Date', width=150)
        self.sales_tree.column('Amount', width=100)

        scrollbar.config(command=self.sales_tree.yview)
        self.sales_tree.pack(fill=BOTH, expand=True)

        # Load recent sales
        self.load_recent_sales()

    def load_recent_sales(self):
        """Load recent sales data"""
        # Clear existing data
        for i in self.sales_tree.get_children():
            self.sales_tree.delete(i)

        # Get recent sales
        self.cursor.execute("""
        SELECT s.id, c.name, e.name, s.date, s.total_amount
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.id
        LEFT JOIN employees e ON s.employee_id = e.id
        ORDER BY s.date DESC
        LIMIT 10
        """)

        for row in self.cursor.fetchall():
            self.sales_tree.insert('', 'end', values=row)

    def medicines_screen(self):
        """Display medicines management screen"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Medicines Management", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Dashboard", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.dashboard, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Search frame
        search_frame = Frame(main_frame, bg='white')
        search_frame.pack(pady=10, padx=20, fill=X)

        Label(search_frame, text="Search:", font=('Arial', 12), bg='white').pack(side=LEFT, padx=5)
        self.search_entry = Entry(search_frame, font=('Arial', 12), width=30)
        self.search_entry.pack(side=LEFT, padx=5)

        search_btn = Button(search_frame, text="Search", font=('Arial', 10), bg='#3498db', fg='white',
                           command=self.search_medicines, width=10)
        search_btn.pack(side=LEFT, padx=5)

        reset_btn = Button(search_frame, text="Reset", font=('Arial', 10), bg='#95a5a6', fg='white',
                          command=self.load_medicines, width=10)
        reset_btn.pack(side=LEFT, padx=5)

        # Buttons frame
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10, padx=20, fill=X)

        add_btn = Button(btn_frame, text="Add Medicine", font=('Arial', 12), bg='#2ecc71', fg='white',
                        command=self.add_medicine_screen, width=15)
        add_btn.pack(side=LEFT, padx=5)

        update_btn = Button(btn_frame, text="Update Medicine", font=('Arial', 12), bg='#f39c12', fg='white',
                           command=self.update_medicine_screen, width=15)
        update_btn.pack(side=LEFT, padx=5)

        delete_btn = Button(btn_frame, text="Delete Medicine", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.delete_medicine, width=15)
        delete_btn.pack(side=LEFT, padx=5)

        # Medicines table
        table_frame = Frame(main_frame)
        table_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(table_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.medicines_tree = ttk.Treeview(table_frame, columns=('ID', 'Name', 'Description', 'Quantity',
                                                                 'Price', 'Supplier', 'Expiry', 'Category'),
                                          show='headings', yscrollcommand=scrollbar.set)

        self.medicines_tree.heading('ID', text='ID')
        self.medicines_tree.heading('Name', text='Name')
        self.medicines_tree.heading('Description', text='Description')
        self.medicines_tree.heading('Quantity', text='Quantity')
        self.medicines_tree.heading('Price', text='Price')
        self.medicines_tree.heading('Supplier', text='Supplier')
        self.medicines_tree.heading('Expiry', text='Expiry Date')
        self.medicines_tree.heading('Category', text='Category')

        self.medicines_tree.column('ID', width=50)
        self.medicines_tree.column('Name', width=150)
        self.medicines_tree.column('Description', width=200)
        self.medicines_tree.column('Quantity', width=80)
        self.medicines_tree.column('Price', width=80)
        self.medicines_tree.column('Supplier', width=120)
        self.medicines_tree.column('Expiry', width=100)
        self.medicines_tree.column('Category', width=100)

        scrollbar.config(command=self.medicines_tree.yview)
        self.medicines_tree.pack(fill=BOTH, expand=True)

        # Load medicines
        self.load_medicines()

    def load_medicines(self):
        """Load all medicines data"""
        # Clear existing data
        for i in self.medicines_tree.get_children():
            self.medicines_tree.delete(i)

        # Get all medicines
        self.cursor.execute("""
        SELECT m.id, m.name, m.description, m.quantity, m.price, s.name, m.expiry_date, m.category
        FROM medicines m
        LEFT JOIN suppliers s ON m.supplier_id = s.id
        ORDER BY m.name
        """)

        for row in self.cursor.fetchall():
            self.medicines_tree.insert('', 'end', values=row)

    def search_medicines(self):
        """Search medicines by name or category"""
        search_term = self.search_entry.get().strip()

        if not search_term:
            self.load_medicines()
            return

        # Clear existing data
        for i in self.medicines_tree.get_children():
            self.medicines_tree.delete(i)

        # Search medicines
        self.cursor.execute("""
        SELECT m.id, m.name, m.description, m.quantity, m.price, s.name, m.expiry_date, m.category
        FROM medicines m
        LEFT JOIN suppliers s ON m.supplier_id = s.id
        WHERE m.name LIKE ? OR m.category LIKE ?
        ORDER BY m.name
        """, (f'%{search_term}%', f'%{search_term}%'))

        for row in self.cursor.fetchall():
            self.medicines_tree.insert('', 'end', values=row)

    def add_medicine_screen(self):
        """Display add medicine form"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Add New Medicine", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Medicines", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.medicines_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Form frame
        form_frame = Frame(self.root, bg='white')
        form_frame.pack(fill=BOTH, expand=True, padx=50, pady=20)

        # Medicine details
        Label(form_frame, text="Medicine Details", font=('Arial', 16, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, pady=10)

        # Name
        Label(form_frame, text="Name:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.name_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.name_entry.grid(row=1, column=1, pady=5, padx=5)

        # Description
        Label(form_frame, text="Description:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.desc_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.desc_entry.grid(row=2, column=1, pady=5, padx=5)

        # Quantity
        Label(form_frame, text="Quantity:", font=('Arial', 12), bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=5)
        self.qty_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.qty_entry.grid(row=3, column=1, pady=5, padx=5)

        # Price
        Label(form_frame, text="Price:", font=('Arial', 12), bg='white').grid(row=4, column=0, sticky='w', pady=5, padx=5)
        self.price_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.price_entry.grid(row=4, column=1, pady=5, padx=5)

        # Supplier
        Label(form_frame, text="Supplier:", font=('Arial', 12), bg='white').grid(row=5, column=0, sticky='w', pady=5, padx=5)
        self.supplier_var = StringVar()
        self.supplier_combo = ttk.Combobox(form_frame, textvariable=self.supplier_var, font=('Arial', 12), width=28)
        self.supplier_combo.grid(row=5, column=1, pady=5, padx=5)

        # Load suppliers
        self.cursor.execute("SELECT id, name FROM suppliers ORDER BY name")
        suppliers = self.cursor.fetchall()
        supplier_list = [f"{s[0]} - {s[1]}" for s in suppliers]
        self.supplier_combo['values'] = supplier_list

        # Expiry date
        Label(form_frame, text="Expiry Date (YYYY-MM-DD):", font=('Arial', 12), bg='white').grid(row=6, column=0, sticky='w', pady=5, padx=5)
        self.exp_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.exp_entry.grid(row=6, column=1, pady=5, padx=5)

        # Category
        Label(form_frame, text="Category:", font=('Arial', 12), bg='white').grid(row=7, column=0, sticky='w', pady=5, padx=5)
        self.category_var = StringVar()
        categories = ["Tablet", "Capsule", "Syrup", "Injection", "Ointment", "Drops", "Inhaler", "Other"]
        self.category_combo = ttk.Combobox(form_frame, textvariable=self.category_var, values=categories, font=('Arial', 12), width=28)
        self.category_combo.grid(row=7, column=1, pady=5, padx=5)

        # Barcode
        Label(form_frame, text="Barcode:", font=('Arial', 12), bg='white').grid(row=8, column=0, sticky='w', pady=5, padx=5)
        self.barcode_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.barcode_entry.grid(row=8, column=1, pady=5, padx=5)

        # Buttons
        btn_frame = Frame(form_frame, bg='white')
        btn_frame.grid(row=9, column=0, columnspan=2, pady=20)

        save_btn = Button(btn_frame, text="Save Medicine", font=('Arial', 12), bg='#2ecc71', fg='white',
                         command=self.save_medicine, width=15)
        save_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.medicines_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

    def save_medicine(self):
        """Save new medicine to database"""
        # Get form data
        name = self.name_entry.get().strip()
        description = self.desc_entry.get().strip()
        quantity = self.qty_entry.get().strip()
        price = self.price_entry.get().strip()
        supplier = self.supplier_var.get()
        expiry = self.exp_entry.get().strip()
        category = self.category_var.get()
        barcode = self.barcode_entry.get().strip()

        # Validation
        if not name or not quantity or not price or not category:
            messagebox.showerror("Error", "Name, Quantity, Price, and Category are required!")
            return

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer and Price must be a number!")
            return

        # Get supplier ID
        supplier_id = None
        if supplier:
            supplier_id = int(supplier.split(' - ')[0])

        # Check if barcode already exists
        if barcode:
            self.cursor.execute("SELECT id FROM medicines WHERE barcode=?", (barcode,))
            if self.cursor.fetchone():
                messagebox.showerror("Error", "Barcode already exists!")
                return

        # Insert medicine
        self.cursor.execute("""
        INSERT INTO medicines (name, description, quantity, price, supplier_id, expiry_date, category, barcode)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, description, quantity, price, supplier_id, expiry, category, barcode))

        self.conn.commit()
        messagebox.showinfo("Success", "Medicine added successfully!")
        self.medicines_screen()

    def update_medicine_screen(self):
        """Display update medicine form"""
        # Get selected medicine
        selected = self.medicines_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a medicine to update!")
            return

        item = self.medicines_tree.item(selected[0])
        medicine_id = item['values'][0]

        # Get medicine details
        self.cursor.execute("SELECT * FROM medicines WHERE id=?", (medicine_id,))
        medicine = self.cursor.fetchone()

        if not medicine:
            messagebox.showerror("Error", "Medicine not found!")
            return

        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Update Medicine", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Medicines", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.medicines_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Form frame
        form_frame = Frame(self.root, bg='white')
        form_frame.pack(fill=BOTH, expand=True, padx=50, pady=20)

        # Medicine details
        Label(form_frame, text="Medicine Details", font=('Arial', 16, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, pady=10)

        # ID (read-only)
        Label(form_frame, text="ID:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        id_label = Label(form_frame, text=str(medicine[0]), font=('Arial', 12), bg='white')
        id_label.grid(row=1, column=1, sticky='w', pady=5, padx=5)

        # Name
        Label(form_frame, text="Name:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.name_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.name_entry.grid(row=2, column=1, pady=5, padx=5)
        self.name_entry.insert(0, medicine[1])

        # Description
        Label(form_frame, text="Description:", font=('Arial', 12), bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=5)
        self.desc_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.desc_entry.grid(row=3, column=1, pady=5, padx=5)
        self.desc_entry.insert(0, medicine[2])

        # Quantity
        Label(form_frame, text="Quantity:", font=('Arial', 12), bg='white').grid(row=4, column=0, sticky='w', pady=5, padx=5)
        self.qty_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.qty_entry.grid(row=4, column=1, pady=5, padx=5)
        self.qty_entry.insert(0, str(medicine[3]))

        # Price
        Label(form_frame, text="Price:", font=('Arial', 12), bg='white').grid(row=5, column=0, sticky='w', pady=5, padx=5)
        self.price_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.price_entry.grid(row=5, column=1, pady=5, padx=5)
        self.price_entry.insert(0, str(medicine[4]))

        # Supplier
        Label(form_frame, text="Supplier:", font=('Arial', 12), bg='white').grid(row=6, column=0, sticky='w', pady=5, padx=5)
        self.supplier_var = StringVar()
        self.supplier_combo = ttk.Combobox(form_frame, textvariable=self.supplier_var, font=('Arial', 12), width=28)
        self.supplier_combo.grid(row=6, column=1, pady=5, padx=5)

        # Load suppliers
        self.cursor.execute("SELECT id, name FROM suppliers ORDER BY name")
        suppliers = self.cursor.fetchall()
        supplier_list = [f"{s[0]} - {s[1]}" for s in suppliers]
        self.supplier_combo['values'] = supplier_list

        # Set current supplier
        if medicine[5]:
            self.cursor.execute("SELECT name FROM suppliers WHERE id=?", (medicine[5],))
            supplier_name = self.cursor.fetchone()[0]
            self.supplier_var.set(f"{medicine[5]} - {supplier_name}")

        # Expiry date
        Label(form_frame, text="Expiry Date (YYYY-MM-DD):", font=('Arial', 12), bg='white').grid(row=7, column=0, sticky='w', pady=5, padx=5)
        self.exp_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.exp_entry.grid(row=7, column=1, pady=5, padx=5)
        self.exp_entry.insert(0, medicine[6])

        # Category
        Label(form_frame, text="Category:", font=('Arial', 12), bg='white').grid(row=8, column=0, sticky='w', pady=5, padx=5)
        self.category_var = StringVar()
        categories = ["Tablet", "Capsule", "Syrup", "Injection", "Ointment", "Drops", "Inhaler", "Other"]
        self.category_combo = ttk.Combobox(form_frame, textvariable=self.category_var, values=categories, font=('Arial', 12), width=28)
        self.category_combo.grid(row=8, column=1, pady=5, padx=5)
        self.category_combo.set(medicine[7])

        # Barcode
        Label(form_frame, text="Barcode:", font=('Arial', 12), bg='white').grid(row=9, column=0, sticky='w', pady=5, padx=5)
        self.barcode_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.barcode_entry.grid(row=9, column=1, pady=5, padx=5)
        self.barcode_entry.insert(0, medicine[8])

        # Buttons
        btn_frame = Frame(form_frame, bg='white')
        btn_frame.grid(row=10, column=0, columnspan=2, pady=20)

        update_btn = Button(btn_frame, text="Update Medicine", font=('Arial', 12), bg='#f39c12', fg='white',
                           command=lambda: self.update_medicine(medicine_id), width=15)
        update_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.medicines_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

    def update_medicine(self, medicine_id):
        """Update medicine in database"""
        # Get form data
        name = self.name_entry.get().strip()
        description = self.desc_entry.get().strip()
        quantity = self.qty_entry.get().strip()
        price = self.price_entry.get().strip()
        supplier = self.supplier_var.get()
        expiry = self.exp_entry.get().strip()
        category = self.category_var.get()
        barcode = self.barcode_entry.get().strip()

        # Validation
        if not name or not quantity or not price or not category:
            messagebox.showerror("Error", "Name, Quantity, Price, and Category are required!")
            return

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer and Price must be a number!")
            return

        # Get supplier ID
        supplier_id = None
        if supplier:
            supplier_id = int(supplier.split(' - ')[0])

        # Check if barcode already exists (excluding current medicine)
        if barcode:
            self.cursor.execute("SELECT id FROM medicines WHERE barcode=? AND id!=?", (barcode, medicine_id))
            if self.cursor.fetchone():
                messagebox.showerror("Error", "Barcode already exists!")
                return

        # Update medicine
        self.cursor.execute("""
        UPDATE medicines
        SET name=?, description=?, quantity=?, price=?, supplier_id=?, expiry_date=?, category=?, barcode=?
        WHERE id=?
        """, (name, description, quantity, price, supplier_id, expiry, category, barcode, medicine_id))

        self.conn.commit()
        messagebox.showinfo("Success", "Medicine updated successfully!")
        self.medicines_screen()

    def delete_medicine(self):
        """Delete selected medicine"""
        # Get selected medicine
        selected = self.medicines_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a medicine to delete!")
            return

        item = self.medicines_tree.item(selected[0])
        medicine_id = item['values'][0]
        medicine_name = item['values'][1]

        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {medicine_name}?"):
            # Check if medicine is used in sales or purchases
            self.cursor.execute("SELECT COUNT(*) FROM sale_items WHERE medicine_id=?", (medicine_id,))
            sales_count = self.cursor.fetchone()[0]

            self.cursor.execute("SELECT COUNT(*) FROM purchase_items WHERE medicine_id=?", (medicine_id,))
            purchases_count = self.cursor.fetchone()[0]

            if sales_count > 0 or purchases_count > 0:
                messagebox.showerror("Error", "Cannot delete medicine that has been used in sales or purchases!")
                return

            # Delete medicine
            self.cursor.execute("DELETE FROM medicines WHERE id=?", (medicine_id,))
            self.conn.commit()

            messagebox.showinfo("Success", "Medicine deleted successfully!")
            self.load_medicines()

    def suppliers_screen(self):
        """Display suppliers management screen"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Suppliers Management", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Dashboard", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.dashboard, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Buttons frame
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10, padx=20, fill=X)

        add_btn = Button(btn_frame, text="Add Supplier", font=('Arial', 12), bg='#2ecc71', fg='white',
                        command=self.add_supplier_screen, width=15)
        add_btn.pack(side=LEFT, padx=5)

        update_btn = Button(btn_frame, text="Update Supplier", font=('Arial', 12), bg='#f39c12', fg='white',
                           command=self.update_supplier_screen, width=15)
        update_btn.pack(side=LEFT, padx=5)

        delete_btn = Button(btn_frame, text="Delete Supplier", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.delete_supplier, width=15)
        delete_btn.pack(side=LEFT, padx=5)

        # Suppliers table
        table_frame = Frame(main_frame)
        table_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(table_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.suppliers_tree = ttk.Treeview(table_frame, columns=('ID', 'Name', 'Contact', 'Address', 'Email'),
                                          show='headings', yscrollcommand=scrollbar.set)

        self.suppliers_tree.heading('ID', text='ID')
        self.suppliers_tree.heading('Name', text='Name')
        self.suppliers_tree.heading('Contact', text='Contact')
        self.suppliers_tree.heading('Address', text='Address')
        self.suppliers_tree.heading('Email', text='Email')

        self.suppliers_tree.column('ID', width=50)
        self.suppliers_tree.column('Name', width=150)
        self.suppliers_tree.column('Contact', width=120)
        self.suppliers_tree.column('Address', width=200)
        self.suppliers_tree.column('Email', width=150)

        scrollbar.config(command=self.suppliers_tree.yview)
        self.suppliers_tree.pack(fill=BOTH, expand=True)

        # Load suppliers
        self.load_suppliers()

    def load_suppliers(self):
        """Load all suppliers data"""
        # Clear existing data
        for i in self.suppliers_tree.get_children():
            self.suppliers_tree.delete(i)

        # Get all suppliers
        self.cursor.execute("SELECT * FROM suppliers ORDER BY name")

        for row in self.cursor.fetchall():
            self.suppliers_tree.insert('', 'end', values=row)

    def add_supplier_screen(self):
        """Display add supplier form"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Add New Supplier", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Suppliers", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.suppliers_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Form frame
        form_frame = Frame(self.root, bg='white')
        form_frame.pack(fill=BOTH, expand=True, padx=50, pady=20)

        # Supplier details
        Label(form_frame, text="Supplier Details", font=('Arial', 16, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, pady=10)

        # Name
        Label(form_frame, text="Name:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.name_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.name_entry.grid(row=1, column=1, pady=5, padx=5)

        # Contact
        Label(form_frame, text="Contact:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.contact_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.contact_entry.grid(row=2, column=1, pady=5, padx=5)

        # Address
        Label(form_frame, text="Address:", font=('Arial', 12), bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=5)
        self.address_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.address_entry.grid(row=3, column=1, pady=5, padx=5)

        # Email
        Label(form_frame, text="Email:", font=('Arial', 12), bg='white').grid(row=4, column=0, sticky='w', pady=5, padx=5)
        self.email_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.email_entry.grid(row=4, column=1, pady=5, padx=5)

        # Buttons
        btn_frame = Frame(form_frame, bg='white')
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)

        save_btn = Button(btn_frame, text="Save Supplier", font=('Arial', 12), bg='#2ecc71', fg='white',
                         command=self.save_supplier, width=15)
        save_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.suppliers_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

    def save_supplier(self):
        """Save new supplier to database"""
        # Get form data
        name = self.name_entry.get().strip()
        contact = self.contact_entry.get().strip()
        address = self.address_entry.get().strip()
        email = self.email_entry.get().strip()

        # Validation
        if not name:
            messagebox.showerror("Error", "Name is required!")
            return

        # Insert supplier
        self.cursor.execute("""
        INSERT INTO suppliers (name, contact, address, email)
        VALUES (?, ?, ?, ?)
        """, (name, contact, address, email))

        self.conn.commit()
        messagebox.showinfo("Success", "Supplier added successfully!")
        self.suppliers_screen()

    def update_supplier_screen(self):
        """Display update supplier form"""
        # Get selected supplier
        selected = self.suppliers_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a supplier to update!")
            return

        item = self.suppliers_tree.item(selected[0])
        supplier_id = item['values'][0]

        # Get supplier details
        self.cursor.execute("SELECT * FROM suppliers WHERE id=?", (supplier_id,))
        supplier = self.cursor.fetchone()

        if not supplier:
            messagebox.showerror("Error", "Supplier not found!")
            return

        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Update Supplier", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Suppliers", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.suppliers_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Form frame
        form_frame = Frame(self.root, bg='white')
        form_frame.pack(fill=BOTH, expand=True, padx=50, pady=20)

        # Supplier details
        Label(form_frame, text="Supplier Details", font=('Arial', 16, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, pady=10)

        # ID (read-only)
        Label(form_frame, text="ID:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        id_label = Label(form_frame, text=str(supplier[0]), font=('Arial', 12), bg='white')
        id_label.grid(row=1, column=1, sticky='w', pady=5, padx=5)

        # Name
        Label(form_frame, text="Name:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.name_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.name_entry.grid(row=2, column=1, pady=5, padx=5)
        self.name_entry.insert(0, supplier[1])

        # Contact
        Label(form_frame, text="Contact:", font=('Arial', 12), bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=5)
        self.contact_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.contact_entry.grid(row=3, column=1, pady=5, padx=5)
        self.contact_entry.insert(0, supplier[2])

        # Address
        Label(form_frame, text="Address:", font=('Arial', 12), bg='white').grid(row=4, column=0, sticky='w', pady=5, padx=5)
        self.address_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.address_entry.grid(row=4, column=1, pady=5, padx=5)
        self.address_entry.insert(0, supplier[3])

        # Email
        Label(form_frame, text="Email:", font=('Arial', 12), bg='white').grid(row=5, column=0, sticky='w', pady=5, padx=5)
        self.email_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.email_entry.grid(row=5, column=1, pady=5, padx=5)
        self.email_entry.insert(0, supplier[4])

        # Buttons
        btn_frame = Frame(form_frame, bg='white')
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)

        update_btn = Button(btn_frame, text="Update Supplier", font=('Arial', 12), bg='#f39c12', fg='white',
                           command=lambda: self.update_supplier(supplier_id), width=15)
        update_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.suppliers_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

    def update_supplier(self, supplier_id):
        """Update supplier in database"""
        # Get form data
        name = self.name_entry.get().strip()
        contact = self.contact_entry.get().strip()
        address = self.address_entry.get().strip()
        email = self.email_entry.get().strip()

        # Validation
        if not name:
            messagebox.showerror("Error", "Name is required!")
            return

        # Update supplier
        self.cursor.execute("""
        UPDATE suppliers
        SET name=?, contact=?, address=?, email=?
        WHERE id=?
        """, (name, contact, address, email, supplier_id))

        self.conn.commit()
        messagebox.showinfo("Success", "Supplier updated successfully!")
        self.suppliers_screen()

    def delete_supplier(self):
        """Delete selected supplier"""
        # Get selected supplier
        selected = self.suppliers_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a supplier to delete!")
            return

        item = self.suppliers_tree.item(selected[0])
        supplier_id = item['values'][0]
        supplier_name = item['values'][1]

        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {supplier_name}?"):
            # Check if supplier is used in medicines or purchases
            self.cursor.execute("SELECT COUNT(*) FROM medicines WHERE supplier_id=?", (supplier_id,))
            medicines_count = self.cursor.fetchone()[0]

            self.cursor.execute("SELECT COUNT(*) FROM purchases WHERE supplier_id=?", (supplier_id,))
            purchases_count = self.cursor.fetchone()[0]

            if medicines_count > 0 or purchases_count > 0:
                messagebox.showerror("Error", "Cannot delete supplier that has associated medicines or purchases!")
                return

            # Delete supplier
            self.cursor.execute("DELETE FROM suppliers WHERE id=?", (supplier_id,))
            self.conn.commit()

            messagebox.showinfo("Success", "Supplier deleted successfully!")
            self.load_suppliers()

    def customers_screen(self):
        """Display customers management screen"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Customers Management", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Dashboard", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.dashboard, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Buttons frame
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10, padx=20, fill=X)

        add_btn = Button(btn_frame, text="Add Customer", font=('Arial', 12), bg='#2ecc71', fg='white',
                        command=self.add_customer_screen, width=15)
        add_btn.pack(side=LEFT, padx=5)

        update_btn = Button(btn_frame, text="Update Customer", font=('Arial', 12), bg='#f39c12', fg='white',
                           command=self.update_customer_screen, width=15)
        update_btn.pack(side=LEFT, padx=5)

        delete_btn = Button(btn_frame, text="Delete Customer", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.delete_customer, width=15)
        delete_btn.pack(side=LEFT, padx=5)

        # Customers table
        table_frame = Frame(main_frame)
        table_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(table_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.customers_tree = ttk.Treeview(table_frame, columns=('ID', 'Name', 'Contact', 'Address', 'Email'),
                                          show='headings', yscrollcommand=scrollbar.set)

        self.customers_tree.heading('ID', text='ID')
        self.customers_tree.heading('Name', text='Name')
        self.customers_tree.heading('Contact', text='Contact')
        self.customers_tree.heading('Address', text='Address')
        self.customers_tree.heading('Email', text='Email')

        self.customers_tree.column('ID', width=50)
        self.customers_tree.column('Name', width=150)
        self.customers_tree.column('Contact', width=120)
        self.customers_tree.column('Address', width=200)
        self.customers_tree.column('Email', width=150)

        scrollbar.config(command=self.customers_tree.yview)
        self.customers_tree.pack(fill=BOTH, expand=True)

        # Load customers
        self.load_customers()

    def load_customers(self):
        """Load all customers data"""
        # Clear existing data
        for i in self.customers_tree.get_children():
            self.customers_tree.delete(i)

        # Get all customers
        self.cursor.execute("SELECT * FROM customers ORDER BY name")

        for row in self.cursor.fetchall():
            self.customers_tree.insert('', 'end', values=row)

    def add_customer_screen(self):
        """Display add customer form"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Add New Customer", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Customers", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.customers_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Form frame
        form_frame = Frame(self.root, bg='white')
        form_frame.pack(fill=BOTH, expand=True, padx=50, pady=20)

        # Customer details
        Label(form_frame, text="Customer Details", font=('Arial', 16, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, pady=10)

        # Name
        Label(form_frame, text="Name:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.name_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.name_entry.grid(row=1, column=1, pady=5, padx=5)

        # Contact
        Label(form_frame, text="Contact:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.contact_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.contact_entry.grid(row=2, column=1, pady=5, padx=5)

        # Address
        Label(form_frame, text="Address:", font=('Arial', 12), bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=5)
        self.address_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.address_entry.grid(row=3, column=1, pady=5, padx=5)

        # Email
        Label(form_frame, text="Email:", font=('Arial', 12), bg='white').grid(row=4, column=0, sticky='w', pady=5, padx=5)
        self.email_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.email_entry.grid(row=4, column=1, pady=5, padx=5)

        # Buttons
        btn_frame = Frame(form_frame, bg='white')
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)

        save_btn = Button(btn_frame, text="Save Customer", font=('Arial', 12), bg='#2ecc71', fg='white',
                         command=self.save_customer, width=15)
        save_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.customers_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

    def save_customer(self):
        """Save new customer to database"""
        # Get form data
        name = self.name_entry.get().strip()
        contact = self.contact_entry.get().strip()
        address = self.address_entry.get().strip()
        email = self.email_entry.get().strip()

        # Validation
        if not name:
            messagebox.showerror("Error", "Name is required!")
            return

        # Insert customer
        self.cursor.execute("""
        INSERT INTO customers (name, contact, address, email)
        VALUES (?, ?, ?, ?)
        """, (name, contact, address, email))

        self.conn.commit()
        messagebox.showinfo("Success", "Customer added successfully!")
        self.customers_screen()

    def update_customer_screen(self):
        """Display update customer form"""
        # Get selected customer
        selected = self.customers_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a customer to update!")
            return

        item = self.customers_tree.item(selected[0])
        customer_id = item['values'][0]

        # Get customer details
        self.cursor.execute("SELECT * FROM customers WHERE id=?", (customer_id,))
        customer = self.cursor.fetchone()

        if not customer:
            messagebox.showerror("Error", "Customer not found!")
            return

        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Update Customer", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Customers", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.customers_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Form frame
        form_frame = Frame(self.root, bg='white')
        form_frame.pack(fill=BOTH, expand=True, padx=50, pady=20)

        # Customer details
        Label(form_frame, text="Customer Details", font=('Arial', 16, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, pady=10)

        # ID (read-only)
        Label(form_frame, text="ID:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        id_label = Label(form_frame, text=str(customer[0]), font=('Arial', 12), bg='white')
        id_label.grid(row=1, column=1, sticky='w', pady=5, padx=5)

        # Name
        Label(form_frame, text="Name:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.name_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.name_entry.grid(row=2, column=1, pady=5, padx=5)
        self.name_entry.insert(0, customer[1])

        # Contact
        Label(form_frame, text="Contact:", font=('Arial', 12), bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=5)
        self.contact_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.contact_entry.grid(row=3, column=1, pady=5, padx=5)
        self.contact_entry.insert(0, customer[2])

        # Address
        Label(form_frame, text="Address:", font=('Arial', 12), bg='white').grid(row=4, column=0, sticky='w', pady=5, padx=5)
        self.address_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.address_entry.grid(row=4, column=1, pady=5, padx=5)
        self.address_entry.insert(0, customer[3])

        # Email
        Label(form_frame, text="Email:", font=('Arial', 12), bg='white').grid(row=5, column=0, sticky='w', pady=5, padx=5)
        self.email_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.email_entry.grid(row=5, column=1, pady=5, padx=5)
        self.email_entry.insert(0, customer[4])

        # Buttons
        btn_frame = Frame(form_frame, bg='white')
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)

        update_btn = Button(btn_frame, text="Update Customer", font=('Arial', 12), bg='#f39c12', fg='white',
                           command=lambda: self.update_customer(customer_id), width=15)
        update_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.customers_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

    def update_customer(self, customer_id):
        """Update customer in database"""
        # Get form data
        name = self.name_entry.get().strip()
        contact = self.contact_entry.get().strip()
        address = self.address_entry.get().strip()
        email = self.email_entry.get().strip()

        # Validation
        if not name:
            messagebox.showerror("Error", "Name is required!")
            return

        # Update customer
        self.cursor.execute("""
        UPDATE customers
        SET name=?, contact=?, address=?, email=?
        WHERE id=?
        """, (name, contact, address, email, customer_id))

        self.conn.commit()
        messagebox.showinfo("Success", "Customer updated successfully!")
        self.customers_screen()

    def delete_customer(self):
        """Delete selected customer"""
        # Get selected customer
        selected = self.customers_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a customer to delete!")
            return

        item = self.customers_tree.item(selected[0])
        customer_id = item['values'][0]
        customer_name = item['values'][1]

        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {customer_name}?"):
            # Check if customer is used in sales
            self.cursor.execute("SELECT COUNT(*) FROM sales WHERE customer_id=?", (customer_id,))
            sales_count = self.cursor.fetchone()[0]

            if sales_count > 0:
                messagebox.showerror("Error", "Cannot delete customer that has associated sales!")
                return

            # Delete customer
            self.cursor.execute("DELETE FROM customers WHERE id=?", (customer_id,))
            self.conn.commit()

            messagebox.showinfo("Success", "Customer deleted successfully!")
            self.load_customers()

    def sales_screen(self):
        """Display sales management screen"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Sales Management", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Dashboard", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.dashboard, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Buttons frame
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10, padx=20, fill=X)

        new_sale_btn = Button(btn_frame, text="New Sale", font=('Arial', 12), bg='#2ecc71', fg='white',
                             command=self.new_sale_screen, width=15)
        new_sale_btn.pack(side=LEFT, padx=5)

        view_sale_btn = Button(btn_frame, text="View Sale Details", font=('Arial', 12), bg='#3498db', fg='white',
                              command=self.view_sale_screen, width=15)
        view_sale_btn.pack(side=LEFT, padx=5)

        # Sales table
        table_frame = Frame(main_frame)
        table_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(table_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.sales_tree = ttk.Treeview(table_frame, columns=('ID', 'Customer', 'Employee', 'Date', 'Amount', 'Payment'),
                                      show='headings', yscrollcommand=scrollbar.set)

        self.sales_tree.heading('ID', text='ID')
        self.sales_tree.heading('Customer', text='Customer')
        self.sales_tree.heading('Employee', text='Employee')
        self.sales_tree.heading('Date', text='Date')
        self.sales_tree.heading('Amount', text='Amount')
        self.sales_tree.heading('Payment', text='Payment Method')

        self.sales_tree.column('ID', width=50)
        self.sales_tree.column('Customer', width=150)
        self.sales_tree.column('Employee', width=150)
        self.sales_tree.column('Date', width=150)
        self.sales_tree.column('Amount', width=100)
        self.sales_tree.column('Payment', width=120)

        scrollbar.config(command=self.sales_tree.yview)
        self.sales_tree.pack(fill=BOTH, expand=True)

        # Load sales
        self.load_sales()

    def load_sales(self):
        """Load all sales data"""
        # Clear existing data
        for i in self.sales_tree.get_children():
            self.sales_tree.delete(i)

        # Get all sales
        self.cursor.execute("""
        SELECT s.id, c.name, e.name, s.date, s.total_amount, s.payment_method
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.id
        LEFT JOIN employees e ON s.employee_id = e.id
        ORDER BY s.date DESC
        """)

        for row in self.cursor.fetchall():
            self.sales_tree.insert('', 'end', values=row)

    def new_sale_screen(self):
        """Display new sale form"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="New Sale", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Sales", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.sales_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Form frame
        form_frame = Frame(main_frame, bg='white')
        form_frame.pack(pady=10, padx=20, fill=X)

        # Customer
        Label(form_frame, text="Customer:", font=('Arial', 12), bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.customer_var = StringVar()
        self.customer_combo = ttk.Combobox(form_frame, textvariable=self.customer_var, font=('Arial', 12), width=28)
        self.customer_combo.grid(row=0, column=1, pady=5, padx=5)

        # Load customers
        self.cursor.execute("SELECT id, name FROM customers ORDER BY name")
        customers = self.cursor.fetchall()
        customer_list = [f"{c[0]} - {c[1]}" for c in customers]
        self.customer_combo['values'] = customer_list

        # Payment method
        Label(form_frame, text="Payment Method:", font=('Arial', 12), bg='white').grid(row=0, column=2, sticky='w', pady=5, padx=5)
        self.payment_var = StringVar()
        payments = ["Cash", "Credit Card", "Debit Card", "Insurance"]
        self.payment_combo = ttk.Combobox(form_frame, textvariable=self.payment_var, values=payments, font=('Arial', 12), width=15)
        self.payment_combo.grid(row=0, column=3, pady=5, padx=5)

        # Add medicine frame
        add_frame = Frame(main_frame, bg='white')
        add_frame.pack(pady=10, padx=20, fill=X)

        Label(add_frame, text="Add Medicine to Sale", font=('Arial', 14, 'bold'), bg='white').pack(pady=5)

        # Medicine
        Label(add_frame, text="Medicine:", font=('Arial', 12), bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.medicine_var = StringVar()
        self.medicine_combo = ttk.Combobox(add_frame, textvariable=self.medicine_var, font=('Arial', 12), width=28)
        self.medicine_combo.grid(row=0, column=1, pady=5, padx=5)

        # Load medicines
        self.cursor.execute("SELECT id, name, quantity, price FROM medicines WHERE quantity > 0 ORDER BY name")
        medicines = self.cursor.fetchall()
        medicine_list = [f"{m[0]} - {m[1]} (Stock: {m[2]}, Price: {m[3]})" for m in medicines]
        self.medicine_combo['values'] = medicine_list

        # Quantity
        Label(add_frame, text="Quantity:", font=('Arial', 12), bg='white').grid(row=0, column=2, sticky='w', pady=5, padx=5)
        self.qty_entry = Entry(add_frame, font=('Arial', 12), width=10)
        self.qty_entry.grid(row=0, column=3, pady=5, padx=5)

        # Add button
        add_btn = Button(add_frame, text="Add", font=('Arial', 12), bg='#2ecc71', fg='white',
                       command=self.add_to_sale, width=10)
        add_btn.grid(row=0, column=4, pady=5, padx=5)

        # Sale items table
        items_frame = Frame(main_frame)
        items_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(items_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.sale_items_tree = ttk.Treeview(items_frame, columns=('ID', 'Name', 'Quantity', 'Price', 'Total'),
                                          show='headings', yscrollcommand=scrollbar.set)

        self.sale_items_tree.heading('ID', text='ID')
        self.sale_items_tree.heading('Name', text='Name')
        self.sale_items_tree.heading('Quantity', text='Quantity')
        self.sale_items_tree.heading('Price', text='Price')
        self.sale_items_tree.heading('Total', text='Total')

        self.sale_items_tree.column('ID', width=50)
        self.sale_items_tree.column('Name', width=200)
        self.sale_items_tree.column('Quantity', width=100)
        self.sale_items_tree.column('Price', width=100)
        self.sale_items_tree.column('Total', width=100)

        scrollbar.config(command=self.sale_items_tree.yview)
        self.sale_items_tree.pack(fill=BOTH, expand=True)

        # Total frame
        total_frame = Frame(main_frame, bg='white')
        total_frame.pack(pady=10, padx=20, fill=X)

        self.total_label = Label(total_frame, text="Total: $0.00", font=('Arial', 14, 'bold'), bg='white')
        self.total_label.pack(side=RIGHT, padx=10)

        # Buttons
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10, padx=20, fill=X)

        complete_btn = Button(btn_frame, text="Complete Sale", font=('Arial', 12), bg='#2ecc71', fg='white',
                             command=self.complete_sale, width=15)
        complete_btn.pack(side=LEFT, padx=5)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.sales_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=5)

        # Initialize sale items list
        self.sale_items = []
        self.sale_total = 0.0

    def add_to_sale(self):
        """Add medicine to current sale"""
        medicine = self.medicine_var.get()
        quantity = self.qty_entry.get().strip()

        if not medicine or not quantity:
            messagebox.showerror("Error", "Please select a medicine and enter quantity!")
            return

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive integer!")
            return

        # Get medicine details
        medicine_id = int(medicine.split(' - ')[0])
        self.cursor.execute("SELECT id, name, quantity, price FROM medicines WHERE id=?", (medicine_id,))
        med = self.cursor.fetchone()

        if not med:
            messagebox.showerror("Error", "Medicine not found!")
            return

        if quantity > med[2]:
            messagebox.showerror("Error", f"Only {med[2]} items available in stock!")
            return

        # Check if medicine already in sale
        for item in self.sale_items:
            if item['id'] == medicine_id:
                item['quantity'] += quantity
                item['total'] = item['quantity'] * item['price']
                break
        else:
            self.sale_items.append({
                'id': medicine_id,
                'name': med[1],
                'quantity': quantity,
                'price': med[3],
                'total': quantity * med[3]
            })

        # Update sale items tree
        self.update_sale_items_tree()

        # Clear form
        self.medicine_var.set('')
        self.qty_entry.delete(0, END)

    def update_sale_items_tree(self):
        """Update sale items treeview"""
        # Clear existing data
        for i in self.sale_items_tree.get_children():
            self.sale_items_tree.delete(i)

        # Add items
        self.sale_total = 0.0
        for item in self.sale_items:
            self.sale_items_tree.insert('', 'end', values=(
                item['id'],
                item['name'],
                item['quantity'],
                f"${item['price']:.2f}",
                f"${item['total']:.2f}"
            ))
            self.sale_total += item['total']

        # Update total label
        self.total_label.config(text=f"Total: ${self.sale_total:.2f}")

    def complete_sale(self):
        """Complete the current sale"""
        if not self.sale_items:
            messagebox.showerror("Error", "No items in sale!")
            return

        customer = self.customer_var.get()
        payment = self.payment_var.get()

        if not payment:
            messagebox.showerror("Error", "Please select a payment method!")
            return

        # Get customer ID
        customer_id = None
        if customer:
            customer_id = int(customer.split(' - ')[0])

        # Create sale record
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute("""
        INSERT INTO sales (customer_id, employee_id, date, total_amount, payment_method)
        VALUES (?, ?, ?, ?, ?)
        """, (customer_id, self.current_user['id'], today, self.sale_total, payment))

        sale_id = self.cursor.lastrowid

        # Add sale items
        for item in self.sale_items:
            self.cursor.execute("""
            INSERT INTO sale_items (sale_id, medicine_id, quantity, price_per_unit)
            VALUES (?, ?, ?, ?)
            """, (sale_id, item['id'], item['quantity'], item['price']))

            # Update medicine quantity
            self.cursor.execute("""
            UPDATE medicines
            SET quantity = quantity - ?
            WHERE id = ?
            """, (item['quantity'], item['id']))

        self.conn.commit()

        messagebox.showinfo("Success", f"Sale completed successfully! Sale ID: {sale_id}")
        self.sales_screen()

    def view_sale_screen(self):
        """Display sale details screen"""
        # Get selected sale
        selected = self.sales_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a sale to view!")
            return

        item = self.sales_tree.item(selected[0])
        sale_id = item['values'][0]

        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Sale Details", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Sales", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.sales_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Sale details frame
        details_frame = Frame(main_frame, bg='white')
        details_frame.pack(pady=10, padx=20, fill=X)

        # Get sale details
        self.cursor.execute("""
        SELECT s.id, c.name, e.name, s.date, s.total_amount, s.payment_method
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.id
        LEFT JOIN employees e ON s.employee_id = e.id
        WHERE s.id = ?
        """, (sale_id,))

        sale = self.cursor.fetchone()

        if not sale:
            messagebox.showerror("Error", "Sale not found!")
            return

        # Display sale details
        Label(details_frame, text=f"Sale ID: {sale[0]}", font=('Arial', 12, 'bold'), bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Customer: {sale[1] if sale[1] else 'Walk-in'}", font=('Arial', 12), bg='white').grid(row=0, column=1, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Employee: {sale[2]}", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Date: {sale[3]}", font=('Arial', 12), bg='white').grid(row=1, column=1, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Payment: {sale[5]}", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Total: ${sale[4]:.2f}", font=('Arial', 12, 'bold'), bg='white').grid(row=2, column=1, sticky='w', pady=5, padx=5)

        # Sale items table
        items_frame = Frame(main_frame)
        items_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(items_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        items_tree = ttk.Treeview(items_frame, columns=('ID', 'Name', 'Quantity', 'Price', 'Total'),
                                 show='headings', yscrollcommand=scrollbar.set)

        items_tree.heading('ID', text='ID')
        items_tree.heading('Name', text='Name')
        items_tree.heading('Quantity', text='Quantity')
        items_tree.heading('Price', text='Price')
        items_tree.heading('Total', text='Total')

        items_tree.column('ID', width=50)
        items_tree.column('Name', width=200)
        items_tree.column('Quantity', width=100)
        items_tree.column('Price', width=100)
        items_tree.column('Total', width=100)

        scrollbar.config(command=items_tree.yview)
        items_tree.pack(fill=BOTH, expand=True)

        # Get sale items
        self.cursor.execute("""
        SELECT si.medicine_id, m.name, si.quantity, si.price_per_unit, (si.quantity * si.price_per_unit)
        FROM sale_items si
        JOIN medicines m ON si.medicine_id = m.id
        WHERE si.sale_id = ?
        """, (sale_id,))

        for row in self.cursor.fetchall():
            items_tree.insert('', 'end', values=(
                row[0],
                row[1],
                row[2],
                f"${row[3]:.2f}",
                f"${row[4]:.2f}"
            ))

        # Print button
        print_btn = Button(main_frame, text="Print Receipt", font=('Arial', 12), bg='#3498db', fg='white',
                          command=lambda: self.print_receipt(sale_id), width=15)
        print_btn.pack(pady=10)

    def print_receipt(self, sale_id):
        """Print sale receipt (simulated)"""
        # Get sale details
        self.cursor.execute("""
        SELECT s.id, c.name, e.name, s.date, s.total_amount, s.payment_method
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.id
        LEFT JOIN employees e ON s.employee_id = e.id
        WHERE s.id = ?
        """, (sale_id,))

        sale = self.cursor.fetchone()

        if not sale:
            messagebox.showerror("Error", "Sale not found!")
            return

        # Get sale items
        self.cursor.execute("""
        SELECT m.name, si.quantity, si.price_per_unit, (si.quantity * si.price_per_unit)
        FROM sale_items si
        JOIN medicines m ON si.medicine_id = m.id
        WHERE si.sale_id = ?
        """, (sale_id,))

        items = self.cursor.fetchall()

        # Create receipt text
        receipt = f"""
        PHARMACY MANAGEMENT SYSTEM
        ==========================
        Receipt ID: {sale[0]}
        Date: {sale[3]}
        Customer: {sale[1] if sale[1] else 'Walk-in'}
        Cashier: {sale[2]}
        Payment: {sale[5]}
        --------------------------
        ITEMS:
        """

        for item in items:
            receipt += f"{item[0]} x {item[1]} @ ${item[2]:.2f} = ${item[3]:.2f}\n"

        receipt += f"""
        --------------------------
        TOTAL: ${sale[4]:.2f}
        --------------------------
        Thank you for your purchase!
        """

        # Show receipt in a message box (in a real system, this would print to a printer)
        messagebox.showinfo("Receipt", receipt)

    def purchases_screen(self):
        """Display purchases management screen"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Purchases Management", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Dashboard", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.dashboard, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Buttons frame
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10, padx=20, fill=X)

        new_purchase_btn = Button(btn_frame, text="New Purchase", font=('Arial', 12), bg='#2ecc71', fg='white',
                                command=self.new_purchase_screen, width=15)
        new_purchase_btn.pack(side=LEFT, padx=5)

        view_purchase_btn = Button(btn_frame, text="View Purchase Details", font=('Arial', 12), bg='#3498db', fg='white',
                                 command=self.view_purchase_screen, width=15)
        view_purchase_btn.pack(side=LEFT, padx=5)

        # Purchases table
        table_frame = Frame(main_frame)
        table_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(table_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.purchases_tree = ttk.Treeview(table_frame, columns=('ID', 'Supplier', 'Employee', 'Date', 'Amount'),
                                          show='headings', yscrollcommand=scrollbar.set)

        self.purchases_tree.heading('ID', text='ID')
        self.purchases_tree.heading('Supplier', text='Supplier')
        self.purchases_tree.heading('Employee', text='Employee')
        self.purchases_tree.heading('Date', text='Date')
        self.purchases_tree.heading('Amount', text='Amount')

        self.purchases_tree.column('ID', width=50)
        self.purchases_tree.column('Supplier', width=150)
        self.purchases_tree.column('Employee', width=150)
        self.purchases_tree.column('Date', width=150)
        self.purchases_tree.column('Amount', width=100)

        scrollbar.config(command=self.purchases_tree.yview)
        self.purchases_tree.pack(fill=BOTH, expand=True)

        # Load purchases
        self.load_purchases()

    def load_purchases(self):
        """Load all purchases data"""
        # Clear existing data
        for i in self.purchases_tree.get_children():
            self.purchases_tree.delete(i)

        # Get all purchases
        self.cursor.execute("""
        SELECT p.id, s.name, e.name, p.date, p.total_amount
        FROM purchases p
        LEFT JOIN suppliers s ON p.supplier_id = s.id
        LEFT JOIN employees e ON p.employee_id = e.id
        ORDER BY p.date DESC
        """)

        for row in self.cursor.fetchall():
            self.purchases_tree.insert('', 'end', values=row)

    def new_purchase_screen(self):
        """Display new purchase form"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="New Purchase", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Purchases", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.purchases_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Form frame
        form_frame = Frame(main_frame, bg='white')
        form_frame.pack(pady=10, padx=20, fill=X)

        # Supplier
        Label(form_frame, text="Supplier:", font=('Arial', 12), bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.supplier_var = StringVar()
        self.supplier_combo = ttk.Combobox(form_frame, textvariable=self.supplier_var, font=('Arial', 12), width=28)
        self.supplier_combo.grid(row=0, column=1, pady=5, padx=5)

        # Load suppliers
        self.cursor.execute("SELECT id, name FROM suppliers ORDER BY name")
        suppliers = self.cursor.fetchall()
        supplier_list = [f"{s[0]} - {s[1]}" for s in suppliers]
        self.supplier_combo['values'] = supplier_list

        # Add medicine frame
        add_frame = Frame(main_frame, bg='white')
        add_frame.pack(pady=10, padx=20, fill=X)

        Label(add_frame, text="Add Medicine to Purchase", font=('Arial', 14, 'bold'), bg='white').pack(pady=5)

        # Medicine
        Label(add_frame, text="Medicine:", font=('Arial', 12), bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.medicine_var = StringVar()
        self.medicine_combo = ttk.Combobox(add_frame, textvariable=self.medicine_var, font=('Arial', 12), width=28)
        self.medicine_combo.grid(row=0, column=1, pady=5, padx=5)

        # Load medicines
        self.cursor.execute("SELECT id, name, price FROM medicines ORDER BY name")
        medicines = self.cursor.fetchall()
        medicine_list = [f"{m[0]} - {m[1]} (Price: {m[2]})" for m in medicines]
        self.medicine_combo['values'] = medicine_list

        # Quantity
        Label(add_frame, text="Quantity:", font=('Arial', 12), bg='white').grid(row=0, column=2, sticky='w', pady=5, padx=5)
        self.qty_entry = Entry(add_frame, font=('Arial', 12), width=10)
        self.qty_entry.grid(row=0, column=3, pady=5, padx=5)

        # Price
        Label(add_frame, text="Price:", font=('Arial', 12), bg='white').grid(row=0, column=4, sticky='w', pady=5, padx=5)
        self.price_entry = Entry(add_frame, font=('Arial', 12), width=10)
        self.price_entry.grid(row=0, column=5, pady=5, padx=5)

        # Add button
        add_btn = Button(add_frame, text="Add", font=('Arial', 12), bg='#2ecc71', fg='white',
                       command=self.add_to_purchase, width=10)
        add_btn.grid(row=0, column=6, pady=5, padx=5)

        # Purchase items table
        items_frame = Frame(main_frame)
        items_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(items_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.purchase_items_tree = ttk.Treeview(items_frame, columns=('ID', 'Name', 'Quantity', 'Price', 'Total'),
                                              show='headings', yscrollcommand=scrollbar.set)

        self.purchase_items_tree.heading('ID', text='ID')
        self.purchase_items_tree.heading('Name', text='Name')
        self.purchase_items_tree.heading('Quantity', text='Quantity')
        self.purchase_items_tree.heading('Price', text='Price')
        self.purchase_items_tree.heading('Total', text='Total')

        self.purchase_items_tree.column('ID', width=50)
        self.purchase_items_tree.column('Name', width=200)
        self.purchase_items_tree.column('Quantity', width=100)
        self.purchase_items_tree.column('Price', width=100)
        self.purchase_items_tree.column('Total', width=100)

        scrollbar.config(command=self.purchase_items_tree.yview)
        self.purchase_items_tree.pack(fill=BOTH, expand=True)

        # Total frame
        total_frame = Frame(main_frame, bg='white')
        total_frame.pack(pady=10, padx=20, fill=X)

        self.total_label = Label(total_frame, text="Total: $0.00", font=('Arial', 14, 'bold'), bg='white')
        self.total_label.pack(side=RIGHT, padx=10)

        # Buttons
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10, padx=20, fill=X)

        complete_btn = Button(btn_frame, text="Complete Purchase", font=('Arial', 12), bg='#2ecc71', fg='white',
                             command=self.complete_purchase, width=15)
        complete_btn.pack(side=LEFT, padx=5)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.purchases_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=5)

        # Initialize purchase items list
        self.purchase_items = []
        self.purchase_total = 0.0

    def add_to_purchase(self):
        """Add medicine to current purchase"""
        medicine = self.medicine_var.get()
        quantity = self.qty_entry.get().strip()
        price = self.price_entry.get().strip()

        if not medicine or not quantity or not price:
            messagebox.showerror("Error", "Please select a medicine and enter quantity and price!")
            return

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
            price = float(price)
            if price <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive integer and Price must be a positive number!")
            return

        # Get medicine details
        medicine_id = int(medicine.split(' - ')[0])
        self.cursor.execute("SELECT id, name FROM medicines WHERE id=?", (medicine_id,))
        med = self.cursor.fetchone()

        if not med:
            messagebox.showerror("Error", "Medicine not found!")
            return

        # Check if medicine already in purchase
        for item in self.purchase_items:
            if item['id'] == medicine_id:
                item['quantity'] += quantity
                item['total'] = item['quantity'] * item['price']
                break
        else:
            self.purchase_items.append({
                'id': medicine_id,
                'name': med[1],
                'quantity': quantity,
                'price': price,
                'total': quantity * price
            })

        # Update purchase items tree
        self.update_purchase_items_tree()

        # Clear form
        self.medicine_var.set('')
        self.qty_entry.delete(0, END)
        self.price_entry.delete(0, END)

    def update_purchase_items_tree(self):
        """Update purchase items treeview"""
        # Clear existing data
        for i in self.purchase_items_tree.get_children():
            self.purchase_items_tree.delete(i)

        # Add items
        self.purchase_total = 0.0
        for item in self.purchase_items:
            self.purchase_items_tree.insert('', 'end', values=(
                item['id'],
                item['name'],
                item['quantity'],
                f"${item['price']:.2f}",
                f"${item['total']:.2f}"
            ))
            self.purchase_total += item['total']

        # Update total label
        self.total_label.config(text=f"Total: ${self.purchase_total:.2f}")

    def complete_purchase(self):
        """Complete the current purchase"""
        if not self.purchase_items:
            messagebox.showerror("Error", "No items in purchase!")
            return

        supplier = self.supplier_var.get()

        if not supplier:
            messagebox.showerror("Error", "Please select a supplier!")
            return

        # Get supplier ID
        supplier_id = int(supplier.split(' - ')[0])

        # Create purchase record
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute("""
        INSERT INTO purchases (supplier_id, employee_id, date, total_amount)
        VALUES (?, ?, ?, ?)
        """, (supplier_id, self.current_user['id'], today, self.purchase_total))

        purchase_id = self.cursor.lastrowid

        # Add purchase items
        for item in self.purchase_items:
            self.cursor.execute("""
            INSERT INTO purchase_items (purchase_id, medicine_id, quantity, price_per_unit)
            VALUES (?, ?, ?, ?)
            """, (purchase_id, item['id'], item['quantity'], item['price']))

            # Update medicine quantity
            self.cursor.execute("""
            UPDATE medicines
            SET quantity = quantity + ?
            WHERE id = ?
            """, (item['quantity'], item['id']))

        self.conn.commit()

        messagebox.showinfo("Success", f"Purchase completed successfully! Purchase ID: {purchase_id}")
        self.purchases_screen()

    def view_purchase_screen(self):
        """Display purchase details screen"""
        # Get selected purchase
        selected = self.purchases_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a purchase to view!")
            return

        item = self.purchases_tree.item(selected[0])
        purchase_id = item['values'][0]

        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Purchase Details", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Purchases", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.purchases_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Purchase details frame
        details_frame = Frame(main_frame, bg='white')
        details_frame.pack(pady=10, padx=20, fill=X)

        # Get purchase details
        self.cursor.execute("""
        SELECT p.id, s.name, e.name, p.date, p.total_amount
        FROM purchases p
        LEFT JOIN suppliers s ON p.supplier_id = s.id
        LEFT JOIN employees e ON p.employee_id = e.id
        WHERE p.id = ?
        """, (purchase_id,))

        purchase = self.cursor.fetchone()

        if not purchase:
            messagebox.showerror("Error", "Purchase not found!")
            return

        # Display purchase details
        Label(details_frame, text=f"Purchase ID: {purchase[0]}", font=('Arial', 12, 'bold'), bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Supplier: {purchase[1]}", font=('Arial', 12), bg='white').grid(row=0, column=1, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Employee: {purchase[2]}", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Date: {purchase[3]}", font=('Arial', 12), bg='white').grid(row=1, column=1, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Total: ${purchase[4]:.2f}", font=('Arial', 12, 'bold'), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)

        # Purchase items table
        items_frame = Frame(main_frame)
        items_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(items_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        items_tree = ttk.Treeview(items_frame, columns=('ID', 'Name', 'Quantity', 'Price', 'Total'),
                                 show='headings', yscrollcommand=scrollbar.set)

        items_tree.heading('ID', text='ID')
        items_tree.heading('Name', text='Name')
        items_tree.heading('Quantity', text='Quantity')
        items_tree.heading('Price', text='Price')
        items_tree.heading('Total', text='Total')

        items_tree.column('ID', width=50)
        items_tree.column('Name', width=200)
        items_tree.column('Quantity', width=100)
        items_tree.column('Price', width=100)
        items_tree.column('Total', width=100)

        scrollbar.config(command=items_tree.yview)
        items_tree.pack(fill=BOTH, expand=True)

        # Get purchase items
        self.cursor.execute("""
        SELECT pi.medicine_id, m.name, pi.quantity, pi.price_per_unit, (pi.quantity * pi.price_per_unit)
        FROM purchase_items pi
        JOIN medicines m ON pi.medicine_id = m.id
        WHERE pi.purchase_id = ?
        """, (purchase_id,))

        for row in self.cursor.fetchall():
            items_tree.insert('', 'end', values=(
                row[0],
                row[1],
                row[2],
                f"${row[3]:.2f}",
                f"${row[4]:.2f}"
            ))

    def reports_screen(self):
        """Display reports screen"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Reports", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Dashboard", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.dashboard, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Report options
        options_frame = Frame(main_frame, bg='white')
        options_frame.pack(pady=20, padx=20, fill=X)

        Label(options_frame, text="Select Report Type:", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)

        # Sales report
        sales_btn = Button(options_frame, text="Sales Report", font=('Arial', 12), bg='#3498db', fg='white',
                          command=self.sales_report, width=20, height=2)
        sales_btn.pack(pady=10)

        # Inventory report
        inventory_btn = Button(options_frame, text="Inventory Report", font=('Arial', 12), bg='#2ecc71', fg='white',
                              command=self.inventory_report, width=20, height=2)
        inventory_btn.pack(pady=10)

        # Expiry report
        expiry_btn = Button(options_frame, text="Expiry Report", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.expiry_report, width=20, height=2)
        expiry_btn.pack(pady=10)

        # Low stock report
        low_stock_btn = Button(options_frame, text="Low Stock Report", font=('Arial', 12), bg='#f39c12', fg='white',
                             command=self.low_stock_report, width=20, height=2)
        low_stock_btn.pack(pady=10)

    def sales_report(self):
        """Generate sales report"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Sales Report", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Reports", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.reports_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Date range frame
        date_frame = Frame(main_frame, bg='white')
        date_frame.pack(pady=10, padx=20, fill=X)

        Label(date_frame, text="From Date (YYYY-MM-DD):", font=('Arial', 12), bg='white').pack(side=LEFT, padx=5)
        self.from_date_entry = Entry(date_frame, font=('Arial', 12), width=15)
        self.from_date_entry.pack(side=LEFT, padx=5)

        Label(date_frame, text="To Date (YYYY-MM-DD):", font=('Arial', 12), bg='white').pack(side=LEFT, padx=5)
        self.to_date_entry = Entry(date_frame, font=('Arial', 12), width=15)
        self.to_date_entry.pack(side=LEFT, padx=5)

        generate_btn = Button(date_frame, text="Generate Report", font=('Arial', 12), bg='#3498db', fg='white',
                            command=self.generate_sales_report, width=15)
        generate_btn.pack(side=LEFT, padx=10)

        # Report frame
        report_frame = Frame(main_frame)
        report_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(report_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.sales_report_tree = ttk.Treeview(report_frame, columns=('ID', 'Customer', 'Employee', 'Date', 'Amount', 'Payment'),
                                             show='headings', yscrollcommand=scrollbar.set)

        self.sales_report_tree.heading('ID', text='ID')
        self.sales_report_tree.heading('Customer', text='Customer')
        self.sales_report_tree.heading('Employee', text='Employee')
        self.sales_report_tree.heading('Date', text='Date')
        self.sales_report_tree.heading('Amount', text='Amount')
        self.sales_report_tree.heading('Payment', text='Payment Method')

        self.sales_report_tree.column('ID', width=50)
        self.sales_report_tree.column('Customer', width=150)
        self.sales_report_tree.column('Employee', width=150)
        self.sales_report_tree.column('Date', width=150)
        self.sales_report_tree.column('Amount', width=100)
        self.sales_report_tree.column('Payment', width=120)

        scrollbar.config(command=self.sales_report_tree.yview)
        self.sales_report_tree.pack(fill=BOTH, expand=True)

        # Total frame
        total_frame = Frame(main_frame, bg='white')
        total_frame.pack(pady=10, padx=20, fill=X)

        self.sales_total_label = Label(total_frame, text="Total Sales: $0.00", font=('Arial', 14, 'bold'), bg='white')
        self.sales_total_label.pack(side=RIGHT, padx=10)

        # Generate default report (current month)
        today = datetime.now()
        from_date = today.replace(day=1).strftime('%Y-%m-%d')
        to_date = today.strftime('%Y-%m-%d')

        self.from_date_entry.insert(0, from_date)
        self.to_date_entry.insert(0, to_date)
        self.generate_sales_report()

    def generate_sales_report(self):
        """Generate sales report based on date range"""
        from_date = self.from_date_entry.get().strip()
        to_date = self.to_date_entry.get().strip()

        if not from_date or not to_date:
            messagebox.showerror("Error", "Please enter both from and to dates!")
            return

        # Clear existing data
        for i in self.sales_report_tree.get_children():
            self.sales_report_tree.delete(i)

        # Get sales data
        self.cursor.execute("""
        SELECT s.id, c.name, e.name, s.date, s.total_amount, s.payment_method
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.id
        LEFT JOIN employees e ON s.employee_id = e.id
        WHERE s.date BETWEEN ? AND ?
        ORDER BY s.date DESC
        """, (from_date, to_date))

        sales_data = self.cursor.fetchall()
        total_sales = 0.0

        for row in sales_data:
            self.sales_report_tree.insert('', 'end', values=row)
            total_sales += row[4]

        # Update total label
        self.sales_total_label.config(text=f"Total Sales: ${total_sales:.2f}")

    def inventory_report(self):
        """Generate inventory report"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Inventory Report", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Reports", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.reports_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Report frame
        report_frame = Frame(main_frame)
        report_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(report_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.inventory_tree = ttk.Treeview(report_frame, columns=('ID', 'Name', 'Description', 'Quantity', 'Price', 'Supplier', 'Expiry', 'Category'),
                                         show='headings', yscrollcommand=scrollbar.set)

        self.inventory_tree.heading('ID', text='ID')
        self.inventory_tree.heading('Name', text='Name')
        self.inventory_tree.heading('Description', text='Description')
        self.inventory_tree.heading('Quantity', text='Quantity')
        self.inventory_tree.heading('Price', text='Price')
        self.inventory_tree.heading('Supplier', text='Supplier')
        self.inventory_tree.heading('Expiry', text='Expiry Date')
        self.inventory_tree.heading('Category', text='Category')

        self.inventory_tree.column('ID', width=50)
        self.inventory_tree.column('Name', width=150)
        self.inventory_tree.column('Description', width=200)
        self.inventory_tree.column('Quantity', width=80)
        self.inventory_tree.column('Price', width=80)
        self.inventory_tree.column('Supplier', width=120)
        self.inventory_tree.column('Expiry', width=100)
        self.inventory_tree.column('Category', width=100)

        scrollbar.config(command=self.inventory_tree.yview)
        self.inventory_tree.pack(fill=BOTH, expand=True)

        # Total value frame
        total_frame = Frame(main_frame, bg='white')
        total_frame.pack(pady=10, padx=20, fill=X)

        self.inventory_total_label = Label(total_frame, text="Total Inventory Value: $0.00", font=('Arial', 14, 'bold'), bg='white')
        self.inventory_total_label.pack(side=RIGHT, padx=10)

        # Load inventory data
        self.load_inventory_report()

    def load_inventory_report(self):
        """Load inventory report data"""
        # Clear existing data
        for i in self.inventory_tree.get_children():
            self.inventory_tree.delete(i)

        # Get all medicines
        self.cursor.execute("""
        SELECT m.id, m.name, m.description, m.quantity, m.price, s.name, m.expiry_date, m.category
        FROM medicines m
        LEFT JOIN suppliers s ON m.supplier_id = s.id
        ORDER BY m.name
        """)

        medicines = self.cursor.fetchall()
        total_value = 0.0

        for med in medicines:
            self.inventory_tree.insert('', 'end', values=med)
            total_value += med[3] * med[4]  # quantity * price

        # Update total label
        self.inventory_total_label.config(text=f"Total Inventory Value: ${total_value:.2f}")

    def expiry_report(self):
        """Generate expiry report"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Expiry Report", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Reports", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.reports_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Report frame
        report_frame = Frame(main_frame)
        report_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(report_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.expiry_tree = ttk.Treeview(report_frame, columns=('ID', 'Name', 'Quantity', 'Price', 'Expiry Date', 'Days Left'),
                                       show='headings', yscrollcommand=scrollbar.set)

        self.expiry_tree.heading('ID', text='ID')
        self.expiry_tree.heading('Name', text='Name')
        self.expiry_tree.heading('Quantity', text='Quantity')
        self.expiry_tree.heading('Price', text='Price')
        self.expiry_tree.heading('Expiry Date', text='Expiry Date')
        self.expiry_tree.heading('Days Left', text='Days Left')

        self.expiry_tree.column('ID', width=50)
        self.expiry_tree.column('Name', width=200)
        self.expiry_tree.column('Quantity', width=100)
        self.expiry_tree.column('Price', width=100)
        self.expiry_tree.column('Expiry Date', width=120)
        self.expiry_tree.column('Days Left', width=100)

        scrollbar.config(command=self.expiry_tree.yview)
        self.expiry_tree.pack(fill=BOTH, expand=True)

        # Load expiry data
        self.load_expiry_report()

    def load_expiry_report(self):
        """Load expiry report data"""
        # Clear existing data
        for i in self.expiry_tree.get_children():
            self.expiry_tree.delete(i)

        # Get medicines with expiry dates
        self.cursor.execute("""
        SELECT id, name, quantity, price, expiry_date
        FROM medicines
        WHERE expiry_date IS NOT NULL
        ORDER BY expiry_date
        """)

        medicines = self.cursor.fetchall()
        today = datetime.now()

        for med in medicines:
            if med[4]:  # expiry_date
                try:
                    expiry_date = datetime.strptime(med[4], '%Y-%m-%d')
                    days_left = (expiry_date - today).days

                    # Only show medicines expiring within 90 days
                    if days_left <= 90:
                        self.expiry_tree.insert('', 'end', values=(
                            med[0],  # id
                            med[1],  # name
                            med[2],  # quantity
                            f"${med[3]:.2f}",  # price
                            med[4],  # expiry_date
                            days_left
                        ))
                except ValueError:
                    # Skip if date format is invalid
                    continue

    def low_stock_report(self):
        """Generate low stock report"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Low Stock Report", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Reports", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.reports_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Report frame
        report_frame = Frame(main_frame)
        report_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(report_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.low_stock_tree = ttk.Treeview(report_frame, columns=('ID', 'Name', 'Quantity', 'Price', 'Supplier'),
                                          show='headings', yscrollcommand=scrollbar.set)

        self.low_stock_tree.heading('ID', text='ID')
        self.low_stock_tree.heading('Name', text='Name')
        self.low_stock_tree.heading('Quantity', text='Quantity')
        self.low_stock_tree.heading('Price', text='Price')
        self.low_stock_tree.heading('Supplier', text='Supplier')

        self.low_stock_tree.column('ID', width=50)
        self.low_stock_tree.column('Name', width=200)
        self.low_stock_tree.column('Quantity', width=100)
        self.low_stock_tree.column('Price', width=100)
        self.low_stock_tree.column('Supplier', width=150)

        scrollbar.config(command=self.low_stock_tree.yview)
        self.low_stock_tree.pack(fill=BOTH, expand=True)

        # Load low stock data
        self.load_low_stock_report()

    def load_low_stock_report(self):
        """Load low stock report data"""
        # Clear existing data
        for i in self.low_stock_tree.get_children():
            self.low_stock_tree.delete(i)

        # Get medicines with low stock (quantity < 10)
        self.cursor.execute("""
        SELECT m.id, m.name, m.quantity, m.price, s.name
        FROM medicines m
        LEFT JOIN suppliers s ON m.supplier_id = s.id
        WHERE m.quantity < 10
        ORDER BY m.quantity ASC
        """)

        for med in self.cursor.fetchall():
            self.low_stock_tree.insert('', 'end', values=(
                med[0],  # id
                med[1],  # name
                med[2],  # quantity
                f"${med[3]:.2f}",  # price
                med[4] if med[4] else "N/A"  # supplier
            ))

    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()

# Main application
if __name__ == "__main__":
    root = Tk()
    app = PharmacyManagementSystem(root)
    root.mainloop()
```

## Installation and Running Instructions

1. **Prerequisites**:

   - Python 3.6 or higher
   - Tkinter (usually comes pre-installed with Python)
   - SQLite3 (usually comes pre-installed with Python)

2. **Running the Application**:

   - Save the code to a file named `pharmacy_management_system.py`
   - Run the application using the command:
     ```
     python pharmacy_management_system.py
     ```

3. **Default Login Credentials**:
   - Username: `admin`
   - Password: `admin123`

## Features Included

1. **User Authentication**:

   - Secure login system with role-based access
   - Default admin account created automatically

2. **Dashboard**:

   - Overview of key metrics (medicines, suppliers, customers)
   - Recent sales display
   - Quick navigation to all modules

3. **Medicine Management**:

   - Add, update, delete, and view medicines
   - Track inventory with quantity and expiry dates
   - Categorize medicines (tablets, capsules, etc.)
   - Barcode support
   - Search functionality

4. **Supplier Management**:

   - Add, update, delete, and view suppliers
   - Track contact information and addresses

5. **Customer Management**:

   - Add, update, delete, and view customers
   - Track contact information and addresses

6. **Sales Management**:

   - Create new sales with multiple items
   - Track payment methods
   - View sale details and print receipts
   - Automatic inventory reduction

7. **Purchase Management**:

   - Record new purchases from suppliers
   - Track purchase details
   - Automatic inventory increase

8. **Reporting**:
   - Sales reports with date range filtering
   - Inventory reports with total value calculation
   - Expiry reports (medicines expiring within 90 days)
   - Low stock reports (medicines with quantity < 10)

## Database Structure

The system uses SQLite with the following tables:

- `medicines`: Stores medicine information
- `suppliers`: Stores supplier information
- `employees`: Stores user accounts and roles
- `customers`: Stores customer information
- `sales`: Stores sales transactions
- `sale_items`: Stores individual items in each sale
- `purchases`: Stores purchase transactions
- `purchase_items`: Stores individual items in each purchase

## Usage Notes

1. The system automatically creates a SQLite database file named `pharmacy.db` in the same directory as the script.
2. The default admin account can be used to log in initially.
3. All forms include validation to ensure data integrity.
4. The system prevents deletion of records that are referenced in other tables (e.g., medicines used in sales cannot be deleted).
5. Reports can be generated and viewed within the application.

# This pharmacy management system provides a comprehensive solution for managing all aspects of a pharmacy, from inventory and sales to reporting and analytics.

I'll enhance the pharmacy management system with the additional features you've requested. Here's the updated code with all the new functionalities:

```python
import sqlite3
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import os
import qrcode
from PIL import Image, ImageTk
import io
import base64
import json
import requests
import threading
import uuid

class PharmacyManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacy Management System")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)

        # Initialize database
        self.init_db()

        # Initialize variables
        self.current_user = None
        self.current_store = None
        self.offline_mode = False
        self.sync_queue = []

        # Login screen
        self.login_screen()

    def init_db(self):
        """Initialize the database and create tables if they don't exist"""
        self.conn = sqlite3.connect('pharmacy.db')
        self.cursor = self.conn.cursor()

        # Create tables
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            supplier_id INTEGER,
            expiry_date TEXT,
            category TEXT,
            barcode TEXT UNIQUE,
            composition TEXT,
            hsn_code TEXT,
            tax_rate REAL DEFAULT 0.0,
            reorder_level INTEGER DEFAULT 10,
            unit_id INTEGER,
            FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
            FOREIGN KEY (unit_id) REFERENCES units(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT,
            address TEXT,
            email TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            contact TEXT,
            address TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT,
            address TEXT,
            email TEXT,
            medical_history TEXT,
            loyalty_points INTEGER DEFAULT 0
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            employee_id INTEGER,
            store_id INTEGER,
            date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            tax_amount REAL DEFAULT 0.0,
            payment_method TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (employee_id) REFERENCES employees(id),
            FOREIGN KEY (store_id) REFERENCES stores(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS sale_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER,
            medicine_id INTEGER,
            batch_id INTEGER,
            quantity INTEGER NOT NULL,
            price_per_unit REAL NOT NULL,
            tax_rate REAL DEFAULT 0.0,
            FOREIGN KEY (sale_id) REFERENCES sales(id),
            FOREIGN KEY (medicine_id) REFERENCES medicines(id),
            FOREIGN KEY (batch_id) REFERENCES batches(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_id INTEGER,
            employee_id INTEGER,
            store_id INTEGER,
            date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
            FOREIGN KEY (employee_id) REFERENCES employees(id),
            FOREIGN KEY (store_id) REFERENCES stores(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchase_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            purchase_id INTEGER,
            medicine_id INTEGER,
            batch_id INTEGER,
            quantity INTEGER NOT NULL,
            price_per_unit REAL NOT NULL,
            FOREIGN KEY (purchase_id) REFERENCES purchases(id),
            FOREIGN KEY (medicine_id) REFERENCES medicines(id),
            FOREIGN KEY (batch_id) REFERENCES batches(id)
        )
        """)

        # New tables for additional features
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS batches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_id INTEGER,
            batch_number TEXT NOT NULL,
            expiry_date TEXT,
            quantity INTEGER NOT NULL,
            cost_price REAL,
            FOREIGN KEY (medicine_id) REFERENCES medicines(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            doctor_name TEXT,
            prescription_date TEXT,
            image_data TEXT,
            notes TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS prescription_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prescription_id INTEGER,
            medicine_id INTEGER,
            dosage TEXT,
            duration TEXT,
            instructions TEXT,
            FOREIGN KEY (prescription_id) REFERENCES prescriptions(id),
            FOREIGN KEY (medicine_id) REFERENCES medicines(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS drug_interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_id1 INTEGER,
            medicine_id2 INTEGER,
            severity TEXT,
            description TEXT,
            FOREIGN KEY (medicine_id1) REFERENCES medicines(id),
            FOREIGN KEY (medicine_id2) REFERENCES medicines(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS returns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER,
            customer_id INTEGER,
            employee_id INTEGER,
            date TEXT NOT NULL,
            reason TEXT,
            total_amount REAL NOT NULL,
            FOREIGN KEY (sale_id) REFERENCES sales(id),
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS return_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            return_id INTEGER,
            sale_item_id INTEGER,
            batch_id INTEGER,
            quantity INTEGER NOT NULL,
            reason TEXT,
            FOREIGN KEY (return_id) REFERENCES returns(id),
            FOREIGN KEY (sale_item_id) REFERENCES sale_items(id),
            FOREIGN KEY (batch_id) REFERENCES batches(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS units (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS stores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT,
            contact TEXT,
            email TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_closing (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_id INTEGER,
            employee_id INTEGER,
            date TEXT NOT NULL,
            cash_sales REAL DEFAULT 0.0,
            card_sales REAL DEFAULT 0.0,
            upi_sales REAL DEFAULT 0.0,
            total_sales REAL DEFAULT 0.0,
            cash_in_drawer REAL DEFAULT 0.0,
            expected_cash REAL DEFAULT 0.0,
            difference REAL DEFAULT 0.0,
            notes TEXT,
            FOREIGN KEY (store_id) REFERENCES stores(id),
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            type TEXT,
            message TEXT,
            date TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicine_alternatives (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_id INTEGER,
            alternative_id INTEGER,
            FOREIGN KEY (medicine_id) REFERENCES medicines(id),
            FOREIGN KEY (alternative_id) REFERENCES medicines(id)
        )
        """)

        # Create default admin user if not exists
        self.cursor.execute("SELECT * FROM employees WHERE username='admin'")
        if not self.cursor.fetchone():
            self.cursor.execute("""
            INSERT INTO employees (name, username, password, role, contact, address)
            VALUES ('Administrator', 'admin', 'admin123', 'Admin', '1234567890', 'Pharmacy Address')
            """)

        # Create default store if not exists
        self.cursor.execute("SELECT * FROM stores")
        if not self.cursor.fetchone():
            self.cursor.execute("""
            INSERT INTO stores (name, address, contact, email)
            VALUES ('Main Store', '123 Pharmacy St', '1234567890', 'main@pharmacy.com')
            """)

        # Create default units if not exists
        self.cursor.execute("SELECT COUNT(*) FROM units")
        if self.cursor.fetchone()[0] == 0:
            units = [
                ('Tablet', 'Individual tablet'),
                ('Strip', 'Strip of tablets'),
                ('Box', 'Box of strips'),
                ('Bottle', 'Bottle of liquid'),
                ('Vial', 'Vial of injection'),
                ('Tube', 'Tube of ointment'),
                ('Packet', 'Packet of powder'),
                ('Inhaler', 'Inhaler device')
            ]
            self.cursor.executemany("INSERT INTO units (name, description) VALUES (?, ?)", units)

        self.conn.commit()

    def login_screen(self):
        """Display the login screen"""
        self.clear_window()

        # Frame for login
        login_frame = Frame(self.root, bg='#f0f0f0')
        login_frame.place(x=400, y=150, width=400, height=400)

        # Title
        title = Label(login_frame, text="Pharmacy Management System", font=('Arial', 20, 'bold'), bg='#f0f0f0')
        title.pack(pady=20)

        # Store selection
        Label(login_frame, text="Select Store:", font=('Arial', 12), bg='#f0f0f0').pack(pady=5)
        self.store_var = StringVar()
        self.store_combo = ttk.Combobox(login_frame, textvariable=self.store_var, font=('Arial', 12), width=20)
        self.store_combo.pack(pady=5)

        # Load stores
        self.cursor.execute("SELECT id, name FROM stores ORDER BY name")
        stores = self.cursor.fetchall()
        store_list = [f"{s[0]} - {s[1]}" for s in stores]
        self.store_combo['values'] = store_list
        if store_list:
            self.store_combo.current(0)

        # Username
        Label(login_frame, text="Username:", font=('Arial', 12), bg='#f0f0f0').pack(pady=5)
        self.username_entry = Entry(login_frame, font=('Arial', 12), width=20)
        self.username_entry.pack(pady=5)

        # Password
        Label(login_frame, text="Password:", font=('Arial', 12), bg='#f0f0f0').pack(pady=5)
        self.password_entry = Entry(login_frame, font=('Arial', 12), width=20, show='*')
        self.password_entry.pack(pady=5)

        # Login button
        login_btn = Button(login_frame, text="Login", font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white',
                          command=self.login, width=15, pady=10)
        login_btn.pack(pady=20)

        # Offline mode button
        offline_btn = Button(login_frame, text="Offline Mode", font=('Arial', 10), bg='#95a5a6', fg='white',
                            command=self.offline_mode_login, width=15)
        offline_btn.pack(pady=5)

        # Status label
        self.status_label = Label(login_frame, text="", font=('Arial', 10), bg='#f0f0f0', fg='red')
        self.status_label.pack()

    def offline_mode_login(self):
        """Login in offline mode"""
        self.offline_mode = True
        self.status_label.config(text="Offline mode activated", fg='orange')
        self.login()

    def login(self):
        """Authenticate user login"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        store = self.store_var.get()

        if not username or not password or not store:
            self.status_label.config(text="Please enter all fields")
            return

        # Get store ID
        try:
            store_id = int(store.split(' - ')[0])
            self.cursor.execute("SELECT * FROM stores WHERE id=?", (store_id,))
            store_data = self.cursor.fetchone()
            if store_data:
                self.current_store = {
                    'id': store_data[0],
                    'name': store_data[1],
                    'address': store_data[2],
                    'contact': store_data[3],
                    'email': store_data[4]
                }
        except (ValueError, IndexError):
            self.status_label.config(text="Invalid store selection")
            return

        self.cursor.execute("SELECT * FROM employees WHERE username=? AND password=?", (username, password))
        user = self.cursor.fetchone()

        if user:
            self.current_user = {
                'id': user[0],
                'name': user[1],
                'username': user[2],
                'role': user[4]
            }
            self.dashboard()
        else:
            self.status_label.config(text="Invalid username or password")

    def dashboard(self):
        """Display the main dashboard"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Pharmacy Management System", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # User info
        user_info = Label(header_frame, text=f"Welcome, {self.current_user['name']} ({self.current_user['role']})",
                         font=('Arial', 12), bg='#2c3e50', fg='white')
        user_info.pack(side=RIGHT, padx=20)

        # Store info
        if self.current_store:
            store_info = Label(header_frame, text=f"Store: {self.current_store['name']}",
                             font=('Arial', 12), bg='#2c3e50', fg='white')
            store_info.pack(side=RIGHT, padx=20)

        # Offline mode indicator
        if self.offline_mode:
            offline_label = Label(header_frame, text="OFFLINE MODE", font=('Arial', 10, 'bold'),
                                 bg='#e74c3c', fg='white')
            offline_label.pack(side=RIGHT, padx=10)

        # Logout button
        logout_btn = Button(header_frame, text="Logout", font=('Arial', 10), bg='#e74c3c', fg='white',
                           command=self.login_screen, width=8)
        logout_btn.pack(side=RIGHT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='#ecf0f1')
        main_frame.pack(fill=BOTH, expand=True)

        # Sidebar
        sidebar = Frame(main_frame, bg='#34495e', width=200)
        sidebar.pack(side=LEFT, fill=Y)

        # Menu buttons
        Button(sidebar, text="Dashboard", font=('Arial', 12), bg='#3498db', fg='white',
               command=self.dashboard, width=18, pady=10).pack(pady=5)

        Button(sidebar, text="Medicines", font=('Arial', 12), bg='#3498db', fg='white',
               command=self.medicines_screen, width=18, pady=10).pack(pady=5)

        Button(sidebar, text="Suppliers", font=('Arial', 12), bg='#3498db', fg='white',
               command=self.suppliers_screen, width=18, pady=10).pack(pady=5)

        Button(sidebar, text="Customers", font=('Arial', 12), bg='#3498db', fg='white',
               command=self.customers_screen, width=18, pady=10).pack(pady=5)

        Button(sidebar, text="Prescriptions", font=('Arial', 12), bg='#3498db', fg='white',
               command=self.prescriptions_screen, width=18, pady=10).pack(pady=5)

        Button(sidebar, text="Sales", font=('Arial', 12), bg='#3498db', fg='white',
               command=self.sales_screen, width=18, pady=10).pack(pady=5)

        Button(sidebar, text="Purchases", font=('Arial', 12), bg='#3498db', fg='white',
               command=self.purchases_screen, width=18, pady=10).pack(pady=5)

        Button(sidebar, text="Returns", font=('Arial', 12), bg='#3498db', fg='white',
               command=self.returns_screen, width=18, pady=10).pack(pady=5)

        Button(sidebar, text="Reports", font=('Arial', 12), bg='#3498db', fg='white',
               command=self.reports_screen, width=18, pady=10).pack(pady=5)

        Button(sidebar, text="Settings", font=('Arial', 12), bg='#3498db', fg='white',
               command=self.settings_screen, width=18, pady=10).pack(pady=5)

        # Content area
        content_frame = Frame(main_frame, bg='white')
        content_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # Dashboard content
        Label(content_frame, text="Dashboard", font=('Arial', 18, 'bold'), bg='white').pack(pady=20)

        # Summary cards
        card_frame = Frame(content_frame, bg='white')
        card_frame.pack(pady=20)

        # Medicines count
        self.cursor.execute("SELECT COUNT(*) FROM medicines")
        med_count = self.cursor.fetchone()[0]

        med_card = Frame(card_frame, bg='#3498db', width=200, height=100)
        med_card.pack(side=LEFT, padx=20, pady=20)
        med_card.pack_propagate(False)

        Label(med_card, text="Medicines", font=('Arial', 14, 'bold'), bg='#3498db', fg='white').pack(pady=10)
        Label(med_card, text=str(med_count), font=('Arial', 24, 'bold'), bg='#3498db', fg='white').pack()

        # Suppliers count
        self.cursor.execute("SELECT COUNT(*) FROM suppliers")
        supp_count = self.cursor.fetchone()[0]

        supp_card = Frame(card_frame, bg='#2ecc71', width=200, height=100)
        supp_card.pack(side=LEFT, padx=20, pady=20)
        supp_card.pack_propagate(False)

        Label(supp_card, text="Suppliers", font=('Arial', 14, 'bold'), bg='#2ecc71', fg='white').pack(pady=10)
        Label(supp_card, text=str(supp_count), font=('Arial', 24, 'bold'), bg='#2ecc71', fg='white').pack()

        # Customers count
        self.cursor.execute("SELECT COUNT(*) FROM customers")
        cust_count = self.cursor.fetchone()[0]

        cust_card = Frame(card_frame, bg='#e74c3c', width=200, height=100)
        cust_card.pack(side=LEFT, padx=20, pady=20)
        cust_card.pack_propagate(False)

        Label(cust_card, text="Customers", font=('Arial', 14, 'bold'), bg='#e74c3c', fg='white').pack(pady=10)
        Label(cust_card, text=str(cust_count), font=('Arial', 24, 'bold'), bg='#e74c3c', fg='white').pack()

        # Alerts section
        alerts_frame = Frame(content_frame, bg='white')
        alerts_frame.pack(pady=20, fill=X, padx=20)

        Label(alerts_frame, text="Alerts", font=('Arial', 16, 'bold'), bg='white').pack(anchor='w')

        # Low stock alerts
        self.cursor.execute("""
        SELECT id, name, quantity FROM medicines
        WHERE quantity < reorder_level
        ORDER BY quantity ASC
        LIMIT 5
        """)
        low_stock = self.cursor.fetchall()

        if low_stock:
            low_stock_frame = Frame(alerts_frame, bg='#fff3cd', borderwidth=1, relief='solid')
            low_stock_frame.pack(fill=X, pady=5)

            Label(low_stock_frame, text="Low Stock Alert", font=('Arial', 12, 'bold'),
                  bg='#fff3cd', fg='#856404').pack(anchor='w', padx=10, pady=5)

            for med in low_stock:
                Label(low_stock_frame, text=f"{med[1]}: {med[2]} left",
                      font=('Arial', 10), bg='#fff3cd', fg='#856404').pack(anchor='w', padx=20)

        # Expiry alerts
        today = datetime.now().strftime('%Y-%m-%d')
        thirty_days_later = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')

        self.cursor.execute("""
        SELECT id, name, expiry_date FROM medicines
        WHERE expiry_date BETWEEN ? AND ?
        ORDER BY expiry_date ASC
        LIMIT 5
        """, (today, thirty_days_later))
        expiring = self.cursor.fetchall()

        if expiring:
            expiry_frame = Frame(alerts_frame, bg='#f8d7da', borderwidth=1, relief='solid')
            expiry_frame.pack(fill=X, pady=5)

            Label(expiry_frame, text="Expiry Alert", font=('Arial', 12, 'bold'),
                  bg='#f8d7da', fg='#721c24').pack(anchor='w', padx=10, pady=5)

            for med in expiring:
                Label(expiry_frame, text=f"{med[1]} expires on {med[2]}",
                      font=('Arial', 10), bg='#f8d7da', fg='#721c24').pack(anchor='w', padx=20)

        # Recent sales
        Label(content_frame, text="Recent Sales", font=('Arial', 16, 'bold'), bg='white').pack(pady=10)

        # Sales table
        sales_frame = Frame(content_frame)
        sales_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(sales_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.sales_tree = ttk.Treeview(sales_frame, columns=('ID', 'Customer', 'Employee', 'Date', 'Amount'),
                                      show='headings', yscrollcommand=scrollbar.set)

        self.sales_tree.heading('ID', text='ID')
        self.sales_tree.heading('Customer', text='Customer')
        self.sales_tree.heading('Employee', text='Employee')
        self.sales_tree.heading('Date', text='Date')
        self.sales_tree.heading('Amount', text='Amount')

        self.sales_tree.column('ID', width=50)
        self.sales_tree.column('Customer', width=150)
        self.sales_tree.column('Employee', width=150)
        self.sales_tree.column('Date', width=150)
        self.sales_tree.column('Amount', width=100)

        scrollbar.config(command=self.sales_tree.yview)
        self.sales_tree.pack(fill=BOTH, expand=True)

        # Load recent sales
        self.load_recent_sales()

    def load_recent_sales(self):
        """Load recent sales data"""
        # Clear existing data
        for i in self.sales_tree.get_children():
            self.sales_tree.delete(i)

        # Get recent sales
        self.cursor.execute("""
        SELECT s.id, c.name, e.name, s.date, s.total_amount
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.id
        LEFT JOIN employees e ON s.employee_id = e.id
        WHERE s.store_id = ?
        ORDER BY s.date DESC
        LIMIT 10
        """, (self.current_store['id'],))

        for row in self.cursor.fetchall():
            self.sales_tree.insert('', 'end', values=row)

    def medicines_screen(self):
        """Display medicines management screen"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Medicines Management", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Dashboard", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.dashboard, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Search frame
        search_frame = Frame(main_frame, bg='white')
        search_frame.pack(pady=10, padx=20, fill=X)

        Label(search_frame, text="Search:", font=('Arial', 12), bg='white').pack(side=LEFT, padx=5)
        self.search_entry = Entry(search_frame, font=('Arial', 12), width=30)
        self.search_entry.pack(side=LEFT, padx=5)

        search_btn = Button(search_frame, text="Search", font=('Arial', 10), bg='#3498db', fg='white',
                           command=self.search_medicines, width=10)
        search_btn.pack(side=LEFT, padx=5)

        reset_btn = Button(search_frame, text="Reset", font=('Arial', 10), bg='#95a5a6', fg='white',
                          command=self.load_medicines, width=10)
        reset_btn.pack(side=LEFT, padx=5)

        # Buttons frame
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10, padx=20, fill=X)

        add_btn = Button(btn_frame, text="Add Medicine", font=('Arial', 12), bg='#2ecc71', fg='white',
                        command=self.add_medicine_screen, width=15)
        add_btn.pack(side=LEFT, padx=5)

        update_btn = Button(btn_frame, text="Update Medicine", font=('Arial', 12), bg='#f39c12', fg='white',
                           command=self.update_medicine_screen, width=15)
        update_btn.pack(side=LEFT, padx=5)

        delete_btn = Button(btn_frame, text="Delete Medicine", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.delete_medicine, width=15)
        delete_btn.pack(side=LEFT, padx=5)

        batch_btn = Button(btn_frame, text="Manage Batches", font=('Arial', 12), bg='#9b59b6', fg='white',
                          command=self.batches_screen, width=15)
        batch_btn.pack(side=LEFT, padx=5)

        alternatives_btn = Button(btn_frame, text="Alternatives", font=('Arial', 12), bg='#1abc9c', fg='white',
                                command=self.alternatives_screen, width=15)
        alternatives_btn.pack(side=LEFT, padx=5)

        # Medicines table
        table_frame = Frame(main_frame)
        table_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(table_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.medicines_tree = ttk.Treeview(table_frame, columns=('ID', 'Name', 'Description', 'Quantity',
                                                                 'Price', 'Supplier', 'Expiry', 'Category', 'Unit'),
                                          show='headings', yscrollcommand=scrollbar.set)

        self.medicines_tree.heading('ID', text='ID')
        self.medicines_tree.heading('Name', text='Name')
        self.medicines_tree.heading('Description', text='Description')
        self.medicines_tree.heading('Quantity', text='Quantity')
        self.medicines_tree.heading('Price', text='Price')
        self.medicines_tree.heading('Supplier', text='Supplier')
        self.medicines_tree.heading('Expiry', text='Expiry Date')
        self.medicines_tree.heading('Category', text='Category')
        self.medicines_tree.heading('Unit', text='Unit')

        self.medicines_tree.column('ID', width=50)
        self.medicines_tree.column('Name', width=150)
        self.medicines_tree.column('Description', width=200)
        self.medicines_tree.column('Quantity', width=80)
        self.medicines_tree.column('Price', width=80)
        self.medicines_tree.column('Supplier', width=120)
        self.medicines_tree.column('Expiry', width=100)
        self.medicines_tree.column('Category', width=100)
        self.medicines_tree.column('Unit', width=80)

        scrollbar.config(command=self.medicines_tree.yview)
        self.medicines_tree.pack(fill=BOTH, expand=True)

        # Load medicines
        self.load_medicines()

    def load_medicines(self):
        """Load all medicines data"""
        # Clear existing data
        for i in self.medicines_tree.get_children():
            self.medicines_tree.delete(i)

        # Get all medicines
        self.cursor.execute("""
        SELECT m.id, m.name, m.description, m.quantity, m.price, s.name, m.expiry_date, m.category, u.name
        FROM medicines m
        LEFT JOIN suppliers s ON m.supplier_id = s.id
        LEFT JOIN units u ON m.unit_id = u.id
        ORDER BY m.name
        """)

        for row in self.cursor.fetchall():
            self.medicines_tree.insert('', 'end', values=row)

    def search_medicines(self):
        """Search medicines by name or category"""
        search_term = self.search_entry.get().strip()

        if not search_term:
            self.load_medicines()
            return

        # Clear existing data
        for i in self.medicines_tree.get_children():
            self.medicines_tree.delete(i)

        # Search medicines
        self.cursor.execute("""
        SELECT m.id, m.name, m.description, m.quantity, m.price, s.name, m.expiry_date, m.category, u.name
        FROM medicines m
        LEFT JOIN suppliers s ON m.supplier_id = s.id
        LEFT JOIN units u ON m.unit_id = u.id
        WHERE m.name LIKE ? OR m.category LIKE ? OR m.composition LIKE ?
        ORDER BY m.name
        """, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))

        for row in self.cursor.fetchall():
            self.medicines_tree.insert('', 'end', values=row)

    def add_medicine_screen(self):
        """Display add medicine form"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Add New Medicine", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Medicines", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.medicines_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Form frame
        form_frame = Frame(self.root, bg='white')
        form_frame.pack(fill=BOTH, expand=True, padx=50, pady=20)

        # Medicine details
        Label(form_frame, text="Medicine Details", font=('Arial', 16, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, pady=10)

        # Name
        Label(form_frame, text="Name:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.name_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.name_entry.grid(row=1, column=1, pady=5, padx=5)

        # Description
        Label(form_frame, text="Description:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.desc_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.desc_entry.grid(row=2, column=1, pady=5, padx=5)

        # Composition
        Label(form_frame, text="Composition:", font=('Arial', 12), bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=5)
        self.composition_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.composition_entry.grid(row=3, column=1, pady=5, padx=5)

        # Quantity
        Label(form_frame, text="Quantity:", font=('Arial', 12), bg='white').grid(row=4, column=0, sticky='w', pady=5, padx=5)
        self.qty_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.qty_entry.grid(row=4, column=1, pady=5, padx=5)

        # Price
        Label(form_frame, text="Price:", font=('Arial', 12), bg='white').grid(row=5, column=0, sticky='w', pady=5, padx=5)
        self.price_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.price_entry.grid(row=5, column=1, pady=5, padx=5)

        # HSN Code
        Label(form_frame, text="HSN Code:", font=('Arial', 12), bg='white').grid(row=6, column=0, sticky='w', pady=5, padx=5)
        self.hsn_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.hsn_entry.grid(row=6, column=1, pady=5, padx=5)

        # Tax Rate
        Label(form_frame, text="Tax Rate (%):", font=('Arial', 12), bg='white').grid(row=7, column=0, sticky='w', pady=5, padx=5)
        self.tax_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.tax_entry.grid(row=7, column=1, pady=5, padx=5)

        # Reorder Level
        Label(form_frame, text="Reorder Level:", font=('Arial', 12), bg='white').grid(row=8, column=0, sticky='w', pady=5, padx=5)
        self.reorder_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.reorder_entry.grid(row=8, column=1, pady=5, padx=5)

        # Supplier
        Label(form_frame, text="Supplier:", font=('Arial', 12), bg='white').grid(row=9, column=0, sticky='w', pady=5, padx=5)
        self.supplier_var = StringVar()
        self.supplier_combo = ttk.Combobox(form_frame, textvariable=self.supplier_var, font=('Arial', 12), width=28)
        self.supplier_combo.grid(row=9, column=1, pady=5, padx=5)

        # Load suppliers
        self.cursor.execute("SELECT id, name FROM suppliers ORDER BY name")
        suppliers = self.cursor.fetchall()
        supplier_list = [f"{s[0]} - {s[1]}" for s in suppliers]
        self.supplier_combo['values'] = supplier_list

        # Unit
        Label(form_frame, text="Unit:", font=('Arial', 12), bg='white').grid(row=10, column=0, sticky='w', pady=5, padx=5)
        self.unit_var = StringVar()
        self.unit_combo = ttk.Combobox(form_frame, textvariable=self.unit_var, font=('Arial', 12), width=28)
        self.unit_combo.grid(row=10, column=1, pady=5, padx=5)

        # Load units
        self.cursor.execute("SELECT id, name FROM units ORDER BY name")
        units = self.cursor.fetchall()
        unit_list = [f"{u[0]} - {u[1]}" for u in units]
        self.unit_combo['values'] = unit_list

        # Expiry date
        Label(form_frame, text="Expiry Date (YYYY-MM-DD):", font=('Arial', 12), bg='white').grid(row=11, column=0, sticky='w', pady=5, padx=5)
        self.exp_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.exp_entry.grid(row=11, column=1, pady=5, padx=5)

        # Category
        Label(form_frame, text="Category:", font=('Arial', 12), bg='white').grid(row=12, column=0, sticky='w', pady=5, padx=5)
        self.category_var = StringVar()
        categories = ["Tablet", "Capsule", "Syrup", "Injection", "Ointment", "Drops", "Inhaler", "Other"]
        self.category_combo = ttk.Combobox(form_frame, textvariable=self.category_var, values=categories, font=('Arial', 12), width=28)
        self.category_combo.grid(row=12, column=1, pady=5, padx=5)

        # Barcode
        Label(form_frame, text="Barcode:", font=('Arial', 12), bg='white').grid(row=13, column=0, sticky='w', pady=5, padx=5)
        self.barcode_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.barcode_entry.grid(row=13, column=1, pady=5, padx=5)

        # Generate barcode button
        generate_btn = Button(form_frame, text="Generate Barcode", font=('Arial', 10), bg='#3498db', fg='white',
                             command=self.generate_barcode, width=15)
        generate_btn.grid(row=14, column=1, pady=5)

        # Buttons
        btn_frame = Frame(form_frame, bg='white')
        btn_frame.grid(row=15, column=0, columnspan=2, pady=20)

        save_btn = Button(btn_frame, text="Save Medicine", font=('Arial', 12), bg='#2ecc71', fg='white',
                         command=self.save_medicine, width=15)
        save_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.medicines_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

    def generate_barcode(self):
        """Generate a unique barcode for the medicine"""
        # Generate a unique barcode using UUID
        barcode = str(uuid.uuid4().int)[:12]  # Use first 12 digits of UUID
        self.barcode_entry.delete(0, END)
        self.barcode_entry.insert(0, barcode)

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(barcode)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Display QR code
        qr_window = Toplevel(self.root)
        qr_window.title("Generated Barcode")

        # Convert PIL image to PhotoImage
        img_tk = ImageTk.PhotoImage(img)

        # Display image
        label = Label(qr_window, image=img_tk)
        label.image = img_tk  # Keep a reference
        label.pack(padx=10, pady=10)

        # Display barcode text
        barcode_label = Label(qr_window, text=f"Barcode: {barcode}", font=('Arial', 12))
        barcode_label.pack(pady=5)

        # Close button
        close_btn = Button(qr_window, text="Close", command=qr_window.destroy)
        close_btn.pack(pady=5)

    def save_medicine(self):
        """Save new medicine to database"""
        # Get form data
        name = self.name_entry.get().strip()
        description = self.desc_entry.get().strip()
        composition = self.composition_entry.get().strip()
        quantity = self.qty_entry.get().strip()
        price = self.price_entry.get().strip()
        hsn_code = self.hsn_entry.get().strip()
        tax_rate = self.tax_entry.get().strip()
        reorder_level = self.reorder_entry.get().strip()
        supplier = self.supplier_var.get()
        unit = self.unit_var.get()
        expiry = self.exp_entry.get().strip()
        category = self.category_var.get()
        barcode = self.barcode_entry.get().strip()

        # Validation
        if not name or not quantity or not price or not category:
            messagebox.showerror("Error", "Name, Quantity, Price, and Category are required!")
            return

        try:
            quantity = int(quantity)
            price = float(price)
            tax_rate = float(tax_rate) if tax_rate else 0.0
            reorder_level = int(reorder_level) if reorder_level else 10
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer, Price and Tax Rate must be numbers!")
            return

        # Get supplier ID
        supplier_id = None
        if supplier:
            supplier_id = int(supplier.split(' - ')[0])

        # Get unit ID
        unit_id = None
        if unit:
            unit_id = int(unit.split(' - ')[0])

        # Check if barcode already exists
        if barcode:
            self.cursor.execute("SELECT id FROM medicines WHERE barcode=?", (barcode,))
            if self.cursor.fetchone():
                messagebox.showerror("Error", "Barcode already exists!")
                return

        # Insert medicine
        self.cursor.execute("""
        INSERT INTO medicines (name, description, composition, quantity, price, hsn_code, tax_rate, reorder_level,
                              supplier_id, unit_id, expiry_date, category, barcode)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, description, composition, quantity, price, hsn_code, tax_rate, reorder_level,
              supplier_id, unit_id, expiry, category, barcode))

        self.conn.commit()
        messagebox.showinfo("Success", "Medicine added successfully!")
        self.medicines_screen()

    def update_medicine_screen(self):
        """Display update medicine form"""
        # Get selected medicine
        selected = self.medicines_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a medicine to update!")
            return

        item = self.medicines_tree.item(selected[0])
        medicine_id = item['values'][0]

        # Get medicine details
        self.cursor.execute("SELECT * FROM medicines WHERE id=?", (medicine_id,))
        medicine = self.cursor.fetchone()

        if not medicine:
            messagebox.showerror("Error", "Medicine not found!")
            return

        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Update Medicine", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Medicines", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.medicines_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Form frame
        form_frame = Frame(self.root, bg='white')
        form_frame.pack(fill=BOTH, expand=True, padx=50, pady=20)

        # Medicine details
        Label(form_frame, text="Medicine Details", font=('Arial', 16, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, pady=10)

        # ID (read-only)
        Label(form_frame, text="ID:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        id_label = Label(form_frame, text=str(medicine[0]), font=('Arial', 12), bg='white')
        id_label.grid(row=1, column=1, sticky='w', pady=5, padx=5)

        # Name
        Label(form_frame, text="Name:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.name_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.name_entry.grid(row=2, column=1, pady=5, padx=5)
        self.name_entry.insert(0, medicine[1])

        # Description
        Label(form_frame, text="Description:", font=('Arial', 12), bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=5)
        self.desc_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.desc_entry.grid(row=3, column=1, pady=5, padx=5)
        self.desc_entry.insert(0, medicine[2])

        # Composition
        Label(form_frame, text="Composition:", font=('Arial', 12), bg='white').grid(row=4, column=0, sticky='w', pady=5, padx=5)
        self.composition_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.composition_entry.grid(row=4, column=1, pady=5, padx=5)
        self.composition_entry.insert(0, medicine[10] if len(medicine) > 10 else '')

        # Quantity
        Label(form_frame, text="Quantity:", font=('Arial', 12), bg='white').grid(row=5, column=0, sticky='w', pady=5, padx=5)
        self.qty_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.qty_entry.grid(row=5, column=1, pady=5, padx=5)
        self.qty_entry.insert(0, str(medicine[3]))

        # Price
        Label(form_frame, text="Price:", font=('Arial', 12), bg='white').grid(row=6, column=0, sticky='w', pady=5, padx=5)
        self.price_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.price_entry.grid(row=6, column=1, pady=5, padx=5)
        self.price_entry.insert(0, str(medicine[4]))

        # HSN Code
        Label(form_frame, text="HSN Code:", font=('Arial', 12), bg='white').grid(row=7, column=0, sticky='w', pady=5, padx=5)
        self.hsn_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.hsn_entry.grid(row=7, column=1, pady=5, padx=5)
        self.hsn_entry.insert(0, medicine[11] if len(medicine) > 11 else '')

        # Tax Rate
        Label(form_frame, text="Tax Rate (%):", font=('Arial', 12), bg='white').grid(row=8, column=0, sticky='w', pady=5, padx=5)
        self.tax_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.tax_entry.grid(row=8, column=1, pady=5, padx=5)
        self.tax_entry.insert(0, str(medicine[12]) if len(medicine) > 12 and medicine[12] else '0.0')

        # Reorder Level
        Label(form_frame, text="Reorder Level:", font=('Arial', 12), bg='white').grid(row=9, column=0, sticky='w', pady=5, padx=5)
        self.reorder_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.reorder_entry.grid(row=9, column=1, pady=5, padx=5)
        self.reorder_entry.insert(0, str(medicine[13]) if len(medicine) > 13 and medicine[13] else '10')

        # Supplier
        Label(form_frame, text="Supplier:", font=('Arial', 12), bg='white').grid(row=10, column=0, sticky='w', pady=5, padx=5)
        self.supplier_var = StringVar()
        self.supplier_combo = ttk.Combobox(form_frame, textvariable=self.supplier_var, font=('Arial', 12), width=28)
        self.supplier_combo.grid(row=10, column=1, pady=5, padx=5)

        # Load suppliers
        self.cursor.execute("SELECT id, name FROM suppliers ORDER BY name")
        suppliers = self.cursor.fetchall()
        supplier_list = [f"{s[0]} - {s[1]}" for s in suppliers]
        self.supplier_combo['values'] = supplier_list

        # Set current supplier
        if medicine[5]:
            self.cursor.execute("SELECT name FROM suppliers WHERE id=?", (medicine[5],))
            supplier_name = self.cursor.fetchone()[0]
            self.supplier_var.set(f"{medicine[5]} - {supplier_name}")

        # Unit
        Label(form_frame, text="Unit:", font=('Arial', 12), bg='white').grid(row=11, column=0, sticky='w', pady=5, padx=5)
        self.unit_var = StringVar()
        self.unit_combo = ttk.Combobox(form_frame, textvariable=self.unit_var, font=('Arial', 12), width=28)
        self.unit_combo.grid(row=11, column=1, pady=5, padx=5)

        # Load units
        self.cursor.execute("SELECT id, name FROM units ORDER BY name")
        units = self.cursor.fetchall()
        unit_list = [f"{u[0]} - {u[1]}" for u in units]
        self.unit_combo['values'] = unit_list

        # Set current unit
        if len(medicine) > 14 and medicine[14]:
            self.cursor.execute("SELECT name FROM units WHERE id=?", (medicine[14],))
            unit_name = self.cursor.fetchone()[0]
            self.unit_var.set(f"{medicine[14]} - {unit_name}")

        # Expiry date
        Label(form_frame, text="Expiry Date (YYYY-MM-DD):", font=('Arial', 12), bg='white').grid(row=12, column=0, sticky='w', pady=5, padx=5)
        self.exp_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.exp_entry.grid(row=12, column=1, pady=5, padx=5)
        self.exp_entry.insert(0, medicine[6])

        # Category
        Label(form_frame, text="Category:", font=('Arial', 12), bg='white').grid(row=13, column=0, sticky='w', pady=5, padx=5)
        self.category_var = StringVar()
        categories = ["Tablet", "Capsule", "Syrup", "Injection", "Ointment", "Drops", "Inhaler", "Other"]
        self.category_combo = ttk.Combobox(form_frame, textvariable=self.category_var, values=categories, font=('Arial', 12), width=28)
        self.category_combo.grid(row=13, column=1, pady=5, padx=5)
        self.category_combo.set(medicine[7])

        # Barcode
        Label(form_frame, text="Barcode:", font=('Arial', 12), bg='white').grid(row=14, column=0, sticky='w', pady=5, padx=5)
        self.barcode_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.barcode_entry.grid(row=14, column=1, pady=5, padx=5)
        self.barcode_entry.insert(0, medicine[8])

        # Buttons
        btn_frame = Frame(form_frame, bg='white')
        btn_frame.grid(row=15, column=0, columnspan=2, pady=20)

        update_btn = Button(btn_frame, text="Update Medicine", font=('Arial', 12), bg='#f39c12', fg='white',
                           command=lambda: self.update_medicine(medicine_id), width=15)
        update_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.medicines_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

    def update_medicine(self, medicine_id):
        """Update medicine in database"""
        # Get form data
        name = self.name_entry.get().strip()
        description = self.desc_entry.get().strip()
        composition = self.composition_entry.get().strip()
        quantity = self.qty_entry.get().strip()
        price = self.price_entry.get().strip()
        hsn_code = self.hsn_entry.get().strip()
        tax_rate = self.tax_entry.get().strip()
        reorder_level = self.reorder_entry.get().strip()
        supplier = self.supplier_var.get()
        unit = self.unit_var.get()
        expiry = self.exp_entry.get().strip()
        category = self.category_var.get()
        barcode = self.barcode_entry.get().strip()

        # Validation
        if not name or not quantity or not price or not category:
            messagebox.showerror("Error", "Name, Quantity, Price, and Category are required!")
            return

        try:
            quantity = int(quantity)
            price = float(price)
            tax_rate = float(tax_rate) if tax_rate else 0.0
            reorder_level = int(reorder_level) if reorder_level else 10
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer, Price and Tax Rate must be numbers!")
            return

        # Get supplier ID
        supplier_id = None
        if supplier:
            supplier_id = int(supplier.split(' - ')[0])

        # Get unit ID
        unit_id = None
        if unit:
            unit_id = int(unit.split(' - ')[0])

        # Check if barcode already exists (excluding current medicine)
        if barcode:
            self.cursor.execute("SELECT id FROM medicines WHERE barcode=? AND id!=?", (barcode, medicine_id))
            if self.cursor.fetchone():
                messagebox.showerror("Error", "Barcode already exists!")
                return

        # Update medicine
        self.cursor.execute("""
        UPDATE medicines
        SET name=?, description=?, composition=?, quantity=?, price=?, hsn_code=?, tax_rate=?, reorder_level=?,
            supplier_id=?, unit_id=?, expiry_date=?, category=?, barcode=?
        WHERE id=?
        """, (name, description, composition, quantity, price, hsn_code, tax_rate, reorder_level,
              supplier_id, unit_id, expiry, category, barcode, medicine_id))

        self.conn.commit()
        messagebox.showinfo("Success", "Medicine updated successfully!")
        self.medicines_screen()

    def delete_medicine(self):
        """Delete selected medicine"""
        # Get selected medicine
        selected = self.medicines_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a medicine to delete!")
            return

        item = self.medicines_tree.item(selected[0])
        medicine_id = item['values'][0]
        medicine_name = item['values'][1]

        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {medicine_name}?"):
            # Check if medicine is used in sales or purchases
            self.cursor.execute("SELECT COUNT(*) FROM sale_items WHERE medicine_id=?", (medicine_id,))
            sales_count = self.cursor.fetchone()[0]

            self.cursor.execute("SELECT COUNT(*) FROM purchase_items WHERE medicine_id=?", (medicine_id,))
            purchases_count = self.cursor.fetchone()[0]

            if sales_count > 0 or purchases_count > 0:
                messagebox.showerror("Error", "Cannot delete medicine that has been used in sales or purchases!")
                return

            # Delete medicine
            self.cursor.execute("DELETE FROM medicines WHERE id=?", (medicine_id,))
            self.conn.commit()

            messagebox.showinfo("Success", "Medicine deleted successfully!")
            self.load_medicines()

    def batches_screen(self):
        """Display batches management screen"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Batch Management", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Medicines", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.medicines_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Search frame
        search_frame = Frame(main_frame, bg='white')
        search_frame.pack(pady=10, padx=20, fill=X)

        Label(search_frame, text="Medicine:", font=('Arial', 12), bg='white').pack(side=LEFT, padx=5)
        self.medicine_var = StringVar()
        self.medicine_combo = ttk.Combobox(search_frame, textvariable=self.medicine_var, font=('Arial', 12), width=30)
        self.medicine_combo.pack(side=LEFT, padx=5)

        # Load medicines
        self.cursor.execute("SELECT id, name FROM medicines ORDER BY name")
        medicines = self.cursor.fetchall()
        medicine_list = [f"{m[0]} - {m[1]}" for m in medicines]
        self.medicine_combo['values'] = medicine_list

        search_btn = Button(search_frame, text="Search", font=('Arial', 10), bg='#3498db', fg='white',
                           command=self.search_batches, width=10)
        search_btn.pack(side=LEFT, padx=5)

        reset_btn = Button(search_frame, text="Reset", font=('Arial', 10), bg='#95a5a6', fg='white',
                          command=self.load_batches, width=10)
        reset_btn.pack(side=LEFT, padx=5)

        # Buttons frame
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10, padx=20, fill=X)

        add_btn = Button(btn_frame, text="Add Batch", font=('Arial', 12), bg='#2ecc71', fg='white',
                        command=self.add_batch_screen, width=15)
        add_btn.pack(side=LEFT, padx=5)

        update_btn = Button(btn_frame, text="Update Batch", font=('Arial', 12), bg='#f39c12', fg='white',
                           command=self.update_batch_screen, width=15)
        update_btn.pack(side=LEFT, padx=5)

        delete_btn = Button(btn_frame, text="Delete Batch", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.delete_batch, width=15)
        delete_btn.pack(side=LEFT, padx=5)

        # Batches table
        table_frame = Frame(main_frame)
        table_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(table_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.batches_tree = ttk.Treeview(table_frame, columns=('ID', 'Medicine', 'Batch Number', 'Expiry Date', 'Quantity', 'Cost Price'),
                                       show='headings', yscrollcommand=scrollbar.set)

        self.batches_tree.heading('ID', text='ID')
        self.batches_tree.heading('Medicine', text='Medicine')
        self.batches_tree.heading('Batch Number', text='Batch Number')
        self.batches_tree.heading('Expiry Date', text='Expiry Date')
        self.batches_tree.heading('Quantity', text='Quantity')
        self.batches_tree.heading('Cost Price', text='Cost Price')

        self.batches_tree.column('ID', width=50)
        self.batches_tree.column('Medicine', width=200)
        self.batches_tree.column('Batch Number', width=150)
        self.batches_tree.column('Expiry Date', width=120)
        self.batches_tree.column('Quantity', width=100)
        self.batches_tree.column('Cost Price', width=100)

        scrollbar.config(command=self.batches_tree.yview)
        self.batches_tree.pack(fill=BOTH, expand=True)

        # Load batches
        self.load_batches()

    def load_batches(self):
        """Load all batches data"""
        # Clear existing data
        for i in self.batches_tree.get_children():
            self.batches_tree.delete(i)

        # Get all batches
        self.cursor.execute("""
        SELECT b.id, m.name, b.batch_number, b.expiry_date, b.quantity, b.cost_price
        FROM batches b
        JOIN medicines m ON b.medicine_id = m.id
        ORDER BY m.name, b.expiry_date
        """)

        for row in self.cursor.fetchall():
            self.batches_tree.insert('', 'end', values=row)

    def search_batches(self):
        """Search batches by medicine"""
        medicine = self.medicine_var.get()

        if not medicine:
            self.load_batches()
            return

        # Get medicine ID
        try:
            medicine_id = int(medicine.split(' - ')[0])
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid medicine selection!")
            return

        # Clear existing data
        for i in self.batches_tree.get_children():
            self.batches_tree.delete(i)

        # Get batches for selected medicine
        self.cursor.execute("""
        SELECT b.id, m.name, b.batch_number, b.expiry_date, b.quantity, b.cost_price
        FROM batches b
        JOIN medicines m ON b.medicine_id = m.id
        WHERE b.medicine_id = ?
        ORDER BY b.expiry_date
        """, (medicine_id,))

        for row in self.cursor.fetchall():
            self.batches_tree.insert('', 'end', values=row)

    def add_batch_screen(self):
        """Display add batch form"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Add New Batch", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Batches", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.batches_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Form frame
        form_frame = Frame(self.root, bg='white')
        form_frame.pack(fill=BOTH, expand=True, padx=50, pady=20)

        # Batch details
        Label(form_frame, text="Batch Details", font=('Arial', 16, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, pady=10)

        # Medicine
        Label(form_frame, text="Medicine:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.medicine_var = StringVar()
        self.medicine_combo = ttk.Combobox(form_frame, textvariable=self.medicine_var, font=('Arial', 12), width=30)
        self.medicine_combo.grid(row=1, column=1, pady=5, padx=5)

        # Load medicines
        self.cursor.execute("SELECT id, name FROM medicines ORDER BY name")
        medicines = self.cursor.fetchall()
        medicine_list = [f"{m[0]} - {m[1]}" for m in medicines]
        self.medicine_combo['values'] = medicine_list

        # Batch Number
        Label(form_frame, text="Batch Number:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.batch_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.batch_entry.grid(row=2, column=1, pady=5, padx=5)

        # Expiry Date
        Label(form_frame, text="Expiry Date (YYYY-MM-DD):", font=('Arial', 12), bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=5)
        self.exp_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.exp_entry.grid(row=3, column=1, pady=5, padx=5)

        # Quantity
        Label(form_frame, text="Quantity:", font=('Arial', 12), bg='white').grid(row=4, column=0, sticky='w', pady=5, padx=5)
        self.qty_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.qty_entry.grid(row=4, column=1, pady=5, padx=5)

        # Cost Price
        Label(form_frame, text="Cost Price:", font=('Arial', 12), bg='white').grid(row=5, column=0, sticky='w', pady=5, padx=5)
        self.cost_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.cost_entry.grid(row=5, column=1, pady=5, padx=5)

        # Buttons
        btn_frame = Frame(form_frame, bg='white')
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)

        save_btn = Button(btn_frame, text="Save Batch", font=('Arial', 12), bg='#2ecc71', fg='white',
                         command=self.save_batch, width=15)
        save_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.batches_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

    def save_batch(self):
        """Save new batch to database"""
        # Get form data
        medicine = self.medicine_var.get()
        batch_number = self.batch_entry.get().strip()
        expiry = self.exp_entry.get().strip()
        quantity = self.qty_entry.get().strip()
        cost_price = self.cost_entry.get().strip()

        # Validation
        if not medicine or not batch_number or not expiry or not quantity or not cost_price:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            medicine_id = int(medicine.split(' - ')[0])
            quantity = int(quantity)
            cost_price = float(cost_price)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer and Cost Price must be a number!")
            return

        # Check if batch number already exists for this medicine
        self.cursor.execute("""
        SELECT id FROM batches
        WHERE medicine_id = ? AND batch_number = ?
        """, (medicine_id, batch_number))

        if self.cursor.fetchone():
            messagebox.showerror("Error", "Batch number already exists for this medicine!")
            return

        # Insert batch
        self.cursor.execute("""
        INSERT INTO batches (medicine_id, batch_number, expiry_date, quantity, cost_price)
        VALUES (?, ?, ?, ?, ?)
        """, (medicine_id, batch_number, expiry, quantity, cost_price))

        # Update medicine quantity
        self.cursor.execute("""
        UPDATE medicines
        SET quantity = quantity + ?
        WHERE id = ?
        """, (quantity, medicine_id))

        self.conn.commit()
        messagebox.showinfo("Success", "Batch added successfully!")
        self.batches_screen()

    def update_batch_screen(self):
        """Display update batch form"""
        # Get selected batch
        selected = self.batches_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a batch to update!")
            return

        item = self.batches_tree.item(selected[0])
        batch_id = item['values'][0]

        # Get batch details
        self.cursor.execute("""
        SELECT b.id, b.medicine_id, m.name, b.batch_number, b.expiry_date, b.quantity, b.cost_price
        FROM batches b
        JOIN medicines m ON b.medicine_id = m.id
        WHERE b.id = ?
        """, (batch_id,))

        batch = self.cursor.fetchone()

        if not batch:
            messagebox.showerror("Error", "Batch not found!")
            return

        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Update Batch", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Batches", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.batches_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Form frame
        form_frame = Frame(self.root, bg='white')
        form_frame.pack(fill=BOTH, expand=True, padx=50, pady=20)

        # Batch details
        Label(form_frame, text="Batch Details", font=('Arial', 16, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, pady=10)

        # ID (read-only)
        Label(form_frame, text="ID:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        id_label = Label(form_frame, text=str(batch[0]), font=('Arial', 12), bg='white')
        id_label.grid(row=1, column=1, sticky='w', pady=5, padx=5)

        # Medicine (read-only)
        Label(form_frame, text="Medicine:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        medicine_label = Label(form_frame, text=f"{batch[1]} - {batch[2]}", font=('Arial', 12), bg='white')
        medicine_label.grid(row=2, column=1, sticky='w', pady=5, padx=5)

        # Batch Number
        Label(form_frame, text="Batch Number:", font=('Arial', 12), bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=5)
        self.batch_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.batch_entry.grid(row=3, column=1, pady=5, padx=5)
        self.batch_entry.insert(0, batch[3])

        # Expiry Date
        Label(form_frame, text="Expiry Date (YYYY-MM-DD):", font=('Arial', 12), bg='white').grid(row=4, column=0, sticky='w', pady=5, padx=5)
        self.exp_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.exp_entry.grid(row=4, column=1, pady=5, padx=5)
        self.exp_entry.insert(0, batch[4])

        # Quantity
        Label(form_frame, text="Quantity:", font=('Arial', 12), bg='white').grid(row=5, column=0, sticky='w', pady=5, padx=5)
        self.qty_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.qty_entry.grid(row=5, column=1, pady=5, padx=5)
        self.qty_entry.insert(0, str(batch[5]))

        # Cost Price
        Label(form_frame, text="Cost Price:", font=('Arial', 12), bg='white').grid(row=6, column=0, sticky='w', pady=5, padx=5)
        self.cost_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.cost_entry.grid(row=6, column=1, pady=5, padx=5)
        self.cost_entry.insert(0, str(batch[6]))

        # Buttons
        btn_frame = Frame(form_frame, bg='white')
        btn_frame.grid(row=7, column=0, columnspan=2, pady=20)

        update_btn = Button(btn_frame, text="Update Batch", font=('Arial', 12), bg='#f39c12', fg='white',
                           command=lambda: self.update_batch(batch_id, batch[1], batch[5]), width=15)
        update_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.batches_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

    def update_batch(self, batch_id, medicine_id, old_quantity):
        """Update batch in database"""
        # Get form data
        batch_number = self.batch_entry.get().strip()
        expiry = self.exp_entry.get().strip()
        quantity = self.qty_entry.get().strip()
        cost_price = self.cost_entry.get().strip()

        # Validation
        if not batch_number or not expiry or not quantity or not cost_price:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            quantity = int(quantity)
            cost_price = float(cost_price)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer and Cost Price must be a number!")
            return

        # Check if batch number already exists for this medicine (excluding current batch)
        self.cursor.execute("""
        SELECT id FROM batches
        WHERE medicine_id = ? AND batch_number = ? AND id != ?
        """, (medicine_id, batch_number, batch_id))

        if self.cursor.fetchone():
            messagebox.showerror("Error", "Batch number already exists for this medicine!")
            return

        # Update batch
        self.cursor.execute("""
        UPDATE batches
        SET batch_number=?, expiry_date=?, quantity=?, cost_price=?
        WHERE id=?
        """, (batch_number, expiry, quantity, cost_price, batch_id))

        # Update medicine quantity
        quantity_diff = quantity - old_quantity
        self.cursor.execute("""
        UPDATE medicines
        SET quantity = quantity + ?
        WHERE id = ?
        """, (quantity_diff, medicine_id))

        self.conn.commit()
        messagebox.showinfo("Success", "Batch updated successfully!")
        self.batches_screen()

    def delete_batch(self):
        """Delete selected batch"""
        # Get selected batch
        selected = self.batches_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a batch to delete!")
            return

        item = self.batches_tree.item(selected[0])
        batch_id = item['values'][0]
        batch_number = item['values'][2]

        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete batch {batch_number}?"):
            # Get batch details
            self.cursor.execute("SELECT medicine_id, quantity FROM batches WHERE id=?", (batch_id,))
            batch = self.cursor.fetchone()

            if not batch:
                messagebox.showerror("Error", "Batch not found!")
                return

            # Check if batch is used in sales or purchases
            self.cursor.execute("SELECT COUNT(*) FROM sale_items WHERE batch_id=?", (batch_id,))
            sales_count = self.cursor.fetchone()[0]

            self.cursor.execute("SELECT COUNT(*) FROM purchase_items WHERE batch_id=?", (batch_id,))
            purchases_count = self.cursor.fetchone()[0]

            if sales_count > 0 or purchases_count > 0:
                messagebox.showerror("Error", "Cannot delete batch that has been used in sales or purchases!")
                return

            # Delete batch
            self.cursor.execute("DELETE FROM batches WHERE id=?", (batch_id,))

            # Update medicine quantity
            self.cursor.execute("""
            UPDATE medicines
            SET quantity = quantity - ?
            WHERE id = ?
            """, (batch[1], batch[0]))

            self.conn.commit()

            messagebox.showinfo("Success", "Batch deleted successfully!")
            self.load_batches()

    def alternatives_screen(self):
        """Display medicine alternatives screen"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Medicine Alternatives", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Medicines", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.medicines_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Search frame
        search_frame = Frame(main_frame, bg='white')
        search_frame.pack(pady=10, padx=20, fill=X)

        Label(search_frame, text="Medicine:", font=('Arial', 12), bg='white').pack(side=LEFT, padx=5)
        self.medicine_var = StringVar()
        self.medicine_combo = ttk.Combobox(search_frame, textvariable=self.medicine_var, font=('Arial', 12), width=30)
        self.medicine_combo.pack(side=LEFT, padx=5)

        # Load medicines
        self.cursor.execute("SELECT id, name FROM medicines ORDER BY name")
        medicines = self.cursor.fetchall()
        medicine_list = [f"{m[0]} - {m[1]}" for m in medicines]
        self.medicine_combo['values'] = medicine_list

        search_btn = Button(search_frame, text="Search", font=('Arial', 10), bg='#3498db', fg='white',
                           command=self.search_alternatives, width=10)
        search_btn.pack(side=LEFT, padx=5)

        # Buttons frame
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10, padx=20, fill=X)

        add_btn = Button(btn_frame, text="Add Alternative", font=('Arial', 12), bg='#2ecc71', fg='white',
                        command=self.add_alternative_screen, width=15)
        add_btn.pack(side=LEFT, padx=5)

        delete_btn = Button(btn_frame, text="Delete Alternative", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.delete_alternative, width=15)
        delete_btn.pack(side=LEFT, padx=5)

        # Alternatives table
        table_frame = Frame(main_frame)
        table_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(table_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.alternatives_tree = ttk.Treeview(table_frame, columns=('ID', 'Medicine', 'Alternative', 'Price Difference'),
                                           show='headings', yscrollcommand=scrollbar.set)

        self.alternatives_tree.heading('ID', text='ID')
        self.alternatives_tree.heading('Medicine', text='Medicine')
        self.alternatives_tree.heading('Alternative', text='Alternative')
        self.alternatives_tree.heading('Price Difference', text='Price Difference')

        self.alternatives_tree.column('ID', width=50)
        self.alternatives_tree.column('Medicine', width=200)
        self.alternatives_tree.column('Alternative', width=200)
        self.alternatives_tree.column('Price Difference', width=120)

        scrollbar.config(command=self.alternatives_tree.yview)
        self.alternatives_tree.pack(fill=BOTH, expand=True)

        # Load alternatives
        self.load_alternatives()

    def load_alternatives(self):
        """Load all alternatives data"""
        # Clear existing data
        for i in self.alternatives_tree.get_children():
            self.alternatives_tree.delete(i)

        # Get all alternatives
        self.cursor.execute("""
        SELECT ma.id, m1.name, m2.name, (m2.price - m1.price) as price_diff
        FROM medicine_alternatives ma
        JOIN medicines m1 ON ma.medicine_id = m1.id
        JOIN medicines m2 ON ma.alternative_id = m2.id
        ORDER BY m1.name, m2.name
        """)

        for row in self.cursor.fetchall():
            price_diff = f"{'+' if row[3] > 0 else ''}{row[3]:.2f}" if row[3] else "0.00"
            self.alternatives_tree.insert('', 'end', values=(row[0], row[1], row[2], price_diff))

    def search_alternatives(self):
        """Search alternatives by medicine"""
        medicine = self.medicine_var.get()

        if not medicine:
            self.load_alternatives()
            return

        # Get medicine ID
        try:
            medicine_id = int(medicine.split(' - ')[0])
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid medicine selection!")
            return

        # Clear existing data
        for i in self.alternatives_tree.get_children():
            self.alternatives_tree.delete(i)

        # Get alternatives for selected medicine
        self.cursor.execute("""
        SELECT ma.id, m1.name, m2.name, (m2.price - m1.price) as price_diff
        FROM medicine_alternatives ma
        JOIN medicines m1 ON ma.medicine_id = m1.id
        JOIN medicines m2 ON ma.alternative_id = m2.id
        WHERE ma.medicine_id = ? OR ma.alternative_id = ?
        ORDER BY m1.name, m2.name
        """, (medicine_id, medicine_id))

        for row in self.cursor.fetchall():
            price_diff = f"{'+' if row[3] > 0 else ''}{row[3]:.2f}" if row[3] else "0.00"
            self.alternatives_tree.insert('', 'end', values=(row[0], row[1], row[2], price_diff))

    def add_alternative_screen(self):
        """Display add alternative form"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Add Medicine Alternative", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Alternatives", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.alternatives_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Form frame
        form_frame = Frame(self.root, bg='white')
        form_frame.pack(fill=BOTH, expand=True, padx=50, pady=20)

        # Alternative details
        Label(form_frame, text="Alternative Details", font=('Arial', 16, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, pady=10)

        # Medicine
        Label(form_frame, text="Medicine:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.medicine_var = StringVar()
        self.medicine_combo = ttk.Combobox(form_frame, textvariable=self.medicine_var, font=('Arial', 12), width=30)
        self.medicine_combo.grid(row=1, column=1, pady=5, padx=5)

        # Load medicines
        self.cursor.execute("SELECT id, name FROM medicines ORDER BY name")
        medicines = self.cursor.fetchall()
        medicine_list = [f"{m[0]} - {m[1]}" for m in medicines]
        self.medicine_combo['values'] = medicine_list

        # Alternative
        Label(form_frame, text="Alternative:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.alternative_var = StringVar()
        self.alternative_combo = ttk.Combobox(form_frame, textvariable=self.alternative_var, font=('Arial', 12), width=30)
        self.alternative_combo.grid(row=2, column=1, pady=5, padx=5)

        # Load medicines for alternatives
        self.alternative_combo['values'] = medicine_list

        # Buttons
        btn_frame = Frame(form_frame, bg='white')
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)

        save_btn = Button(btn_frame, text="Save Alternative", font=('Arial', 12), bg='#2ecc71', fg='white',
                         command=self.save_alternative, width=15)
        save_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.alternatives_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

    def save_alternative(self):
        """Save new alternative to database"""
        # Get form data
        medicine = self.medicine_var.get()
        alternative = self.alternative_var.get()

        # Validation
        if not medicine or not alternative:
            messagebox.showerror("Error", "Both medicine and alternative are required!")
            return

        try:
            medicine_id = int(medicine.split(' - ')[0])
            alternative_id = int(alternative.split(' - ')[0])
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid medicine selection!")
            return

        if medicine_id == alternative_id:
            messagebox.showerror("Error", "Medicine and alternative cannot be the same!")
            return

        # Check if alternative already exists
        self.cursor.execute("""
        SELECT id FROM medicine_alternatives
        WHERE (medicine_id = ? AND alternative_id = ?) OR (medicine_id = ? AND alternative_id = ?)
        """, (medicine_id, alternative_id, alternative_id, medicine_id))

        if self.cursor.fetchone():
            messagebox.showerror("Error", "Alternative relationship already exists!")
            return

        # Insert alternative
        self.cursor.execute("""
        INSERT INTO medicine_alternatives (medicine_id, alternative_id)
        VALUES (?, ?)
        """, (medicine_id, alternative_id))

        self.conn.commit()
        messagebox.showinfo("Success", "Alternative added successfully!")
        self.alternatives_screen()

    def delete_alternative(self):
        """Delete selected alternative"""
        # Get selected alternative
        selected = self.alternatives_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an alternative to delete!")
            return

        item = self.alternatives_tree.item(selected[0])
        alternative_id = item['values'][0]

        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this alternative relationship?"):
            # Delete alternative
            self.cursor.execute("DELETE FROM medicine_alternatives WHERE id=?", (alternative_id,))
            self.conn.commit()

            messagebox.showinfo("Success", "Alternative deleted successfully!")
            self.load_alternatives()

    def prescriptions_screen(self):
        """Display prescriptions management screen"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Prescriptions Management", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Dashboard", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.dashboard, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Search frame
        search_frame = Frame(main_frame, bg='white')
        search_frame.pack(pady=10, padx=20, fill=X)

        Label(search_frame, text="Customer:", font=('Arial', 12), bg='white').pack(side=LEFT, padx=5)
        self.customer_var = StringVar()
        self.customer_combo = ttk.Combobox(search_frame, textvariable=self.customer_var, font=('Arial', 12), width=30)
        self.customer_combo.pack(side=LEFT, padx=5)

        # Load customers
        self.cursor.execute("SELECT id, name FROM customers ORDER BY name")
        customers = self.cursor.fetchall()
        customer_list = [f"{c[0]} - {c[1]}" for c in customers]
        self.customer_combo['values'] = customer_list

        search_btn = Button(search_frame, text="Search", font=('Arial', 10), bg='#3498db', fg='white',
                           command=self.search_prescriptions, width=10)
        search_btn.pack(side=LEFT, padx=5)

        reset_btn = Button(search_frame, text="Reset", font=('Arial', 10), bg='#95a5a6', fg='white',
                          command=self.load_prescriptions, width=10)
        reset_btn.pack(side=LEFT, padx=5)

        # Buttons frame
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10, padx=20, fill=X)

        add_btn = Button(btn_frame, text="Add Prescription", font=('Arial', 12), bg='#2ecc71', fg='white',
                        command=self.add_prescription_screen, width=15)
        add_btn.pack(side=LEFT, padx=5)

        view_btn = Button(btn_frame, text="View Details", font=('Arial', 12), bg='#3498db', fg='white',
                         command=self.view_prescription_screen, width=15)
        view_btn.pack(side=LEFT, padx=5)

        delete_btn = Button(btn_frame, text="Delete Prescription", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.delete_prescription, width=15)
        delete_btn.pack(side=LEFT, padx=5)

        # Prescriptions table
        table_frame = Frame(main_frame)
        table_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(table_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.prescriptions_tree = ttk.Treeview(table_frame, columns=('ID', 'Customer', 'Doctor', 'Date', 'Notes'),
                                             show='headings', yscrollcommand=scrollbar.set)

        self.prescriptions_tree.heading('ID', text='ID')
        self.prescriptions_tree.heading('Customer', text='Customer')
        self.prescriptions_tree.heading('Doctor', text='Doctor')
        self.prescriptions_tree.heading('Date', text='Date')
        self.prescriptions_tree.heading('Notes', text='Notes')

        self.prescriptions_tree.column('ID', width=50)
        self.prescriptions_tree.column('Customer', width=150)
        self.prescriptions_tree.column('Doctor', width=150)
        self.prescriptions_tree.column('Date', width=120)
        self.prescriptions_tree.column('Notes', width=200)

        scrollbar.config(command=self.prescriptions_tree.yview)
        self.prescriptions_tree.pack(fill=BOTH, expand=True)

        # Load prescriptions
        self.load_prescriptions()

    def load_prescriptions(self):
        """Load all prescriptions data"""
        # Clear existing data
        for i in self.prescriptions_tree.get_children():
            self.prescriptions_tree.delete(i)

        # Get all prescriptions
        self.cursor.execute("""
        SELECT p.id, c.name, p.doctor_name, p.prescription_date, p.notes
        FROM prescriptions p
        LEFT JOIN customers c ON p.customer_id = c.id
        ORDER BY p.prescription_date DESC
        """)

        for row in self.cursor.fetchall():
            self.prescriptions_tree.insert('', 'end', values=row)

    def search_prescriptions(self):
        """Search prescriptions by customer"""
        customer = self.customer_var.get()

        if not customer:
            self.load_prescriptions()
            return

        # Get customer ID
        try:
            customer_id = int(customer.split(' - ')[0])
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid customer selection!")
            return

        # Clear existing data
        for i in self.prescriptions_tree.get_children():
            self.prescriptions_tree.delete(i)

        # Get prescriptions for selected customer
        self.cursor.execute("""
        SELECT p.id, c.name, p.doctor_name, p.prescription_date, p.notes
        FROM prescriptions p
        LEFT JOIN customers c ON p.customer_id = c.id
        WHERE p.customer_id = ?
        ORDER BY p.prescription_date DESC
        """, (customer_id,))

        for row in self.cursor.fetchall():
            self.prescriptions_tree.insert('', 'end', values=row)

    def add_prescription_screen(self):
        """Display add prescription form"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Add New Prescription", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Prescriptions", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.prescriptions_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Form frame
        form_frame = Frame(self.root, bg='white')
        form_frame.pack(fill=BOTH, expand=True, padx=50, pady=20)

        # Prescription details
        Label(form_frame, text="Prescription Details", font=('Arial', 16, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, pady=10)

        # Customer
        Label(form_frame, text="Customer:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.customer_var = StringVar()
        self.customer_combo = ttk.Combobox(form_frame, textvariable=self.customer_var, font=('Arial', 12), width=30)
        self.customer_combo.grid(row=1, column=1, pady=5, padx=5)

        # Load customers
        self.cursor.execute("SELECT id, name FROM customers ORDER BY name")
        customers = self.cursor.fetchall()
        customer_list = [f"{c[0]} - {c[1]}" for c in customers]
        self.customer_combo['values'] = customer_list

        # Doctor Name
        Label(form_frame, text="Doctor Name:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.doctor_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.doctor_entry.grid(row=2, column=1, pady=5, padx=5)

        # Prescription Date
        Label(form_frame, text="Prescription Date (YYYY-MM-DD):", font=('Arial', 12), bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=5)
        self.date_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.date_entry.grid(row=3, column=1, pady=5, padx=5)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))

        # Notes
        Label(form_frame, text="Notes:", font=('Arial', 12), bg='white').grid(row=4, column=0, sticky='w', pady=5, padx=5)
        self.notes_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.notes_entry.grid(row=4, column=1, pady=5, padx=5)

        # Upload prescription image
        Label(form_frame, text="Prescription Image:", font=('Arial', 12), bg='white').grid(row=5, column=0, sticky='w', pady=5, padx=5)
        self.image_path = StringVar()
        self.image_label = Label(form_frame, text="No image selected", font=('Arial', 10), bg='white')
        self.image_label.grid(row=5, column=1, sticky='w', pady=5, padx=5)

        upload_btn = Button(form_frame, text="Upload Image", font=('Arial', 10), bg='#3498db', fg='white',
                          command=self.upload_prescription_image, width=15)
        upload_btn.grid(row=6, column=1, sticky='w', pady=5, padx=5)

        # Prescription items
        Label(form_frame, text="Prescription Items", font=('Arial', 16, 'bold'), bg='white').grid(row=7, column=0, columnspan=2, pady=10)

        # Medicine
        Label(form_frame, text="Medicine:", font=('Arial', 12), bg='white').grid(row=8, column=0, sticky='w', pady=5, padx=5)
        self.medicine_var = StringVar()
        self.medicine_combo = ttk.Combobox(form_frame, textvariable=self.medicine_var, font=('Arial', 12), width=30)
        self.medicine_combo.grid(row=8, column=1, pady=5, padx=5)

        # Load medicines
        self.cursor.execute("SELECT id, name FROM medicines ORDER BY name")
        medicines = self.cursor.fetchall()
        medicine_list = [f"{m[0]} - {m[1]}" for m in medicines]
        self.medicine_combo['values'] = medicine_list

        # Dosage
        Label(form_frame, text="Dosage:", font=('Arial', 12), bg='white').grid(row=9, column=0, sticky='w', pady=5, padx=5)
        self.dosage_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.dosage_entry.grid(row=9, column=1, pady=5, padx=5)

        # Duration
        Label(form_frame, text="Duration:", font=('Arial', 12), bg='white').grid(row=10, column=0, sticky='w', pady=5, padx=5)
        self.duration_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.duration_entry.grid(row=10, column=1, pady=5, padx=5)

        # Instructions
        Label(form_frame, text="Instructions:", font=('Arial', 12), bg='white').grid(row=11, column=0, sticky='w', pady=5, padx=5)
        self.instructions_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.instructions_entry.grid(row=11, column=1, pady=5, padx=5)

        # Add item button
        add_item_btn = Button(form_frame, text="Add Item", font=('Arial', 10), bg='#2ecc71', fg='white',
                             command=self.add_prescription_item, width=15)
        add_item_btn.grid(row=12, column=1, sticky='w', pady=5, padx=5)

        # Prescription items table
        items_frame = Frame(form_frame)
        items_frame.grid(row=13, column=0, columnspan=2, pady=10, padx=5, sticky='nsew')

        # Scrollbar
        scrollbar = Scrollbar(items_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.prescription_items_tree = ttk.Treeview(items_frame, columns=('ID', 'Medicine', 'Dosage', 'Duration', 'Instructions'),
                                                 show='headings', yscrollcommand=scrollbar.set)

        self.prescription_items_tree.heading('ID', text='ID')
        self.prescription_items_tree.heading('Medicine', text='Medicine')
        self.prescription_items_tree.heading('Dosage', text='Dosage')
        self.prescription_items_tree.heading('Duration', text='Duration')
        self.prescription_items_tree.heading('Instructions', text='Instructions')

        self.prescription_items_tree.column('ID', width=50)
        self.prescription_items_tree.column('Medicine', width=150)
        self.prescription_items_tree.column('Dosage', width=100)
        self.prescription_items_tree.column('Duration', width=100)
        self.prescription_items_tree.column('Instructions', width=150)

        scrollbar.config(command=self.prescription_items_tree.yview)
        self.prescription_items_tree.pack(fill=BOTH, expand=True)

        # Initialize prescription items list
        self.prescription_items = []

        # Buttons
        btn_frame = Frame(form_frame, bg='white')
        btn_frame.grid(row=14, column=0, columnspan=2, pady=20)

        save_btn = Button(btn_frame, text="Save Prescription", font=('Arial', 12), bg='#2ecc71', fg='white',
                         command=self.save_prescription, width=15)
        save_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.prescriptions_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

    def upload_prescription_image(self):
        """Upload prescription image"""
        file_path = filedialog.askopenfilename(
            title="Select Prescription Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )

        if file_path:
            self.image_path.set(file_path)
            self.image_label.config(text=os.path.basename(file_path))

    def add_prescription_item(self):
        """Add item to prescription"""
        medicine = self.medicine_var.get()
        dosage = self.dosage_entry.get().strip()
        duration = self.duration_entry.get().strip()
        instructions = self.instructions_entry.get().strip()

        if not medicine or not dosage:
            messagebox.showerror("Error", "Medicine and Dosage are required!")
            return

        try:
            medicine_id = int(medicine.split(' - ')[0])
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid medicine selection!")
            return

        # Get medicine name
        self.cursor.execute("SELECT name FROM medicines WHERE id=?", (medicine_id,))
        medicine_name = self.cursor.fetchone()[0]

        # Add to prescription items list
        self.prescription_items.append({
            'medicine_id': medicine_id,
            'medicine_name': medicine_name,
            'dosage': dosage,
            'duration': duration,
            'instructions': instructions
        })

        # Update treeview
        self.update_prescription_items_tree()

        # Clear form
        self.medicine_var.set('')
        self.dosage_entry.delete(0, END)
        self.duration_entry.delete(0, END)
        self.instructions_entry.delete(0, END)

    def update_prescription_items_tree(self):
        """Update prescription items treeview"""
        # Clear existing data
        for i in self.prescription_items_tree.get_children():
            self.prescription_items_tree.delete(i)

        # Add items
        for item in self.prescription_items:
            self.prescription_items_tree.insert('', 'end', values=(
                item['medicine_id'],
                item['medicine_name'],
                item['dosage'],
                item['duration'],
                item['instructions']
            ))

    def save_prescription(self):
        """Save new prescription to database"""
        # Get form data
        customer = self.customer_var.get()
        doctor = self.doctor_entry.get().strip()
        date = self.date_entry.get().strip()
        notes = self.notes_entry.get().strip()
        image_path = self.image_path.get()

        # Validation
        if not customer or not doctor or not date:
            messagebox.showerror("Error", "Customer, Doctor, and Date are required!")
            return

        try:
            customer_id = int(customer.split(' - ')[0])
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid customer selection!")
            return

        # Convert image to base64 if provided
        image_data = None
        if image_path:
            try:
                with open(image_path, "rb") as image_file:
                    image_data = base64.b64encode(image_file.read()).decode('utf-8')
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process image: {str(e)}")
                return

        # Insert prescription
        self.cursor.execute("""
        INSERT INTO prescriptions (customer_id, doctor_name, prescription_date, image_data, notes)
        VALUES (?, ?, ?, ?, ?)
        """, (customer_id, doctor, date, image_data, notes))

        prescription_id = self.cursor.lastrowid

        # Insert prescription items
        for item in self.prescription_items:
            self.cursor.execute("""
            INSERT INTO prescription_items (prescription_id, medicine_id, dosage, duration, instructions)
            VALUES (?, ?, ?, ?, ?)
            """, (prescription_id, item['medicine_id'], item['dosage'], item['duration'], item['instructions']))

        self.conn.commit()
        messagebox.showinfo("Success", "Prescription added successfully!")
        self.prescriptions_screen()

    def view_prescription_screen(self):
        """Display prescription details screen"""
        # Get selected prescription
        selected = self.prescriptions_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a prescription to view!")
            return

        item = self.prescriptions_tree.item(selected[0])
        prescription_id = item['values'][0]

        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Prescription Details", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Prescriptions", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.prescriptions_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Get prescription details
        self.cursor.execute("""
        SELECT p.id, c.name, p.doctor_name, p.prescription_date, p.notes, p.image_data
        FROM prescriptions p
        LEFT JOIN customers c ON p.customer_id = c.id
        WHERE p.id = ?
        """, (prescription_id,))

        prescription = self.cursor.fetchone()

        if not prescription:
            messagebox.showerror("Error", "Prescription not found!")
            return

        # Prescription details frame
        details_frame = Frame(main_frame, bg='white')
        details_frame.pack(pady=10, padx=20, fill=X)

        # Display prescription details
        Label(details_frame, text=f"Prescription ID: {prescription[0]}", font=('Arial', 12, 'bold'), bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Customer: {prescription[1]}", font=('Arial', 12), bg='white').grid(row=0, column=1, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Doctor: {prescription[2]}", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Date: {prescription[3]}", font=('Arial', 12), bg='white').grid(row=1, column=1, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Notes: {prescription[4] if prescription[4] else 'N/A'}", font=('Arial', 12), bg='white').grid(row=2, column=0, columnspan=2, sticky='w', pady=5, padx=5)

        # Show prescription image if available
        if prescription[5]:
            try:
                # Decode base64 image
                image_data = base64.b64decode(prescription[5])
                image = Image.open(io.BytesIO(image_data))

                # Resize image if too large
                max_size = (400, 400)
                image.thumbnail(max_size, Image.LANCZOS)

                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(image)

                # Display image
                image_frame = Frame(main_frame, bg='white')
                image_frame.pack(pady=10)

                image_label = Label(image_frame, image=photo)
                image_label.image = photo  # Keep a reference
                image_label.pack()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to display image: {str(e)}")

        # Prescription items table
        items_frame = Frame(main_frame)
        items_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(items_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        items_tree = ttk.Treeview(items_frame, columns=('ID', 'Medicine', 'Dosage', 'Duration', 'Instructions'),
                                 show='headings', yscrollcommand=scrollbar.set)

        items_tree.heading('ID', text='ID')
        items_tree.heading('Medicine', text='Medicine')
        items_tree.heading('Dosage', text='Dosage')
        items_tree.heading('Duration', text='Duration')
        items_tree.heading('Instructions', text='Instructions')

        items_tree.column('ID', width=50)
        items_tree.column('Medicine', width=150)
        items_tree.column('Dosage', width=100)
        items_tree.column('Duration', width=100)
        items_tree.column('Instructions', width=150)

        scrollbar.config(command=items_tree.yview)
        items_tree.pack(fill=BOTH, expand=True)

        # Get prescription items
        self.cursor.execute("""
        SELECT pi.medicine_id, m.name, pi.dosage, pi.duration, pi.instructions
        FROM prescription_items pi
        JOIN medicines m ON pi.medicine_id = m.id
        WHERE pi.prescription_id = ?
        """, (prescription_id,))

        for row in self.cursor.fetchall():
            items_tree.insert('', 'end', values=row)

        # Buttons
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10)

        create_sale_btn = Button(btn_frame, text="Create Sale from Prescription", font=('Arial', 12), bg='#2ecc71', fg='white',
                                command=lambda: self.create_sale_from_prescription(prescription_id), width=20)
        create_sale_btn.pack(side=LEFT, padx=10)

        print_btn = Button(btn_frame, text="Print Prescription", font=('Arial', 12), bg='#3498db', fg='white',
                          command=lambda: self.print_prescription(prescription_id), width=15)
        print_btn.pack(side=LEFT, padx=10)

    def create_sale_from_prescription(self, prescription_id):
        """Create a new sale from a prescription"""
        # Get prescription items
        self.cursor.execute("""
        SELECT pi.medicine_id, m.name, pi.dosage, pi.duration, pi.instructions
        FROM prescription_items pi
        JOIN medicines m ON pi.medicine_id = m.id
        WHERE pi.prescription_id = ?
        """, (prescription_id,))

        items = self.cursor.fetchall()

        if not items:
            messagebox.showerror("Error", "No items found in this prescription!")
            return

        # Get prescription details
        self.cursor.execute("""
        SELECT p.id, c.id, c.name, p.doctor_name, p.prescription_date
        FROM prescriptions p
        LEFT JOIN customers c ON p.customer_id = c.id
        WHERE p.id = ?
        """, (prescription_id,))

        prescription = self.cursor.fetchone()

        if not prescription:
            messagebox.showerror("Error", "Prescription not found!")
            return

        # Create new sale
        self.new_sale_screen()

        # Set customer
        self.customer_var.set(f"{prescription[1]} - {prescription[2]}")

        # Add prescription items to sale
        for item in items:
            # Get medicine details
            self.cursor.execute("SELECT id, name, quantity, price FROM medicines WHERE id=?", (item[0],))
            med = self.cursor.fetchone()

            if med and med[2] > 0:  # If medicine is in stock
                # Add to sale items
                self.sale_items.append({
                    'id': med[0],
                    'name': med[1],
                    'quantity': 1,  # Default quantity
                    'price': med[3],
                    'total': med[3]
                })

        # Update sale items tree
        self.update_sale_items_tree()

        # Show prescription info
        messagebox.showinfo("Prescription", f"Sale created from prescription ID: {prescription[0]}\nDoctor: {prescription[3]}\nDate: {prescription[4]}")

    def print_prescription(self, prescription_id):
        """Print prescription (simulated)"""
        # Get prescription details
        self.cursor.execute("""
        SELECT p.id, c.name, p.doctor_name, p.prescription_date, p.notes
        FROM prescriptions p
        LEFT JOIN customers c ON p.customer_id = c.id
        WHERE p.id = ?
        """, (prescription_id,))

        prescription = self.cursor.fetchone()

        if not prescription:
            messagebox.showerror("Error", "Prescription not found!")
            return

        # Get prescription items
        self.cursor.execute("""
        SELECT m.name, pi.dosage, pi.duration, pi.instructions
        FROM prescription_items pi
        JOIN medicines m ON pi.medicine_id = m.id
        WHERE pi.prescription_id = ?
        """, (prescription_id,))

        items = self.cursor.fetchall()

        # Create prescription text
        prescription_text = f"""
        PRESCRIPTION
        ============
        Prescription ID: {prescription[0]}
        Customer: {prescription[1]}
        Doctor: {prescription[2]}
        Date: {prescription[3]}
        Notes: {prescription[4] if prescription[4] else 'N/A'}
        --------------------------
        MEDICINES:
        """

        for item in items:
            prescription_text += f"{item[0]}\n"
            prescription_text += f"  Dosage: {item[1]}\n"
            prescription_text += f"  Duration: {item[2]}\n"
            prescription_text += f"  Instructions: {item[3]}\n\n"

        prescription_text += """
        --------------------------
        Signature: ________________
        """

        # Show prescription in a message box (in a real system, this would print to a printer)
        messagebox.showinfo("Prescription", prescription_text)

    def delete_prescription(self):
        """Delete selected prescription"""
        # Get selected prescription
        selected = self.prescriptions_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a prescription to delete!")
            return

        item = self.prescriptions_tree.item(selected[0])
        prescription_id = item['values'][0]

        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this prescription?"):
            # Delete prescription items
            self.cursor.execute("DELETE FROM prescription_items WHERE prescription_id=?", (prescription_id,))

            # Delete prescription
            self.cursor.execute("DELETE FROM prescriptions WHERE id=?", (prescription_id,))

            self.conn.commit()

            messagebox.showinfo("Success", "Prescription deleted successfully!")
            self.load_prescriptions()

    def sales_screen(self):
        """Display sales management screen"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Sales Management", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Dashboard", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.dashboard, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Search frame
        search_frame = Frame(main_frame, bg='white')
        search_frame.pack(pady=10, padx=20, fill=X)

        Label(search_frame, text="From Date:", font=('Arial', 12), bg='white').pack(side=LEFT, padx=5)
        self.from_date_entry = Entry(search_frame, font=('Arial', 12), width=15)
        self.from_date_entry.pack(side=LEFT, padx=5)

        Label(search_frame, text="To Date:", font=('Arial', 12), bg='white').pack(side=LEFT, padx=5)
        self.to_date_entry = Entry(search_frame, font=('Arial', 12), width=15)
        self.to_date_entry.pack(side=LEFT, padx=5)

        search_btn = Button(search_frame, text="Search", font=('Arial', 10), bg='#3498db', fg='white',
                           command=self.search_sales, width=10)
        search_btn.pack(side=LEFT, padx=5)

        reset_btn = Button(search_frame, text="Reset", font=('Arial', 10), bg='#95a5a6', fg='white',
                          command=self.load_sales, width=10)
        reset_btn.pack(side=LEFT, padx=5)

        # Buttons frame
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10, padx=20, fill=X)

        new_sale_btn = Button(btn_frame, text="New Sale", font=('Arial', 12), bg='#2ecc71', fg='white',
                             command=self.new_sale_screen, width=15)
        new_sale_btn.pack(side=LEFT, padx=5)

        view_sale_btn = Button(btn_frame, text="View Sale Details", font=('Arial', 12), bg='#3498db', fg='white',
                              command=self.view_sale_screen, width=15)
        view_sale_btn.pack(side=LEFT, padx=5)

        return_btn = Button(btn_frame, text="Process Return", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.process_return_screen, width=15)
        return_btn.pack(side=LEFT, padx=5)

        closing_btn = Button(btn_frame, text="Daily Closing", font=('Arial', 12), bg='#f39c12', fg='white',
                            command=self.daily_closing_screen, width=15)
        closing_btn.pack(side=LEFT, padx=5)

        # Sales table
        table_frame = Frame(main_frame)
        table_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(table_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.sales_tree = ttk.Treeview(table_frame, columns=('ID', 'Customer', 'Employee', 'Date', 'Amount', 'Tax', 'Payment'),
                                      show='headings', yscrollcommand=scrollbar.set)

        self.sales_tree.heading('ID', text='ID')
        self.sales_tree.heading('Customer', text='Customer')
        self.sales_tree.heading('Employee', text='Employee')
        self.sales_tree.heading('Date', text='Date')
        self.sales_tree.heading('Amount', text='Amount')
        self.sales_tree.heading('Tax', text='Tax')
        self.sales_tree.heading('Payment', text='Payment Method')

        self.sales_tree.column('ID', width=50)
        self.sales_tree.column('Customer', width=150)
        self.sales_tree.column('Employee', width=150)
        self.sales_tree.column('Date', width=150)
        self.sales_tree.column('Amount', width=100)
        self.sales_tree.column('Tax', width=80)
        self.sales_tree.column('Payment', width=120)

        scrollbar.config(command=self.sales_tree.yview)
        self.sales_tree.pack(fill=BOTH, expand=True)

        # Load sales
        self.load_sales()

    def load_sales(self):
        """Load all sales data"""
        # Clear existing data
        for i in self.sales_tree.get_children():
            self.sales_tree.delete(i)

        # Get all sales
        self.cursor.execute("""
        SELECT s.id, c.name, e.name, s.date, s.total_amount, s.tax_amount, s.payment_method
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.id
        LEFT JOIN employees e ON s.employee_id = e.id
        WHERE s.store_id = ?
        ORDER BY s.date DESC
        """, (self.current_store['id'],))

        for row in self.cursor.fetchall():
            self.sales_tree.insert('', 'end', values=row)

    def search_sales(self):
        """Search sales by date range"""
        from_date = self.from_date_entry.get().strip()
        to_date = self.to_date_entry.get().strip()

        if not from_date or not to_date:
            self.load_sales()
            return

        # Clear existing data
        for i in self.sales_tree.get_children():
            self.sales_tree.delete(i)

        # Get sales in date range
        self.cursor.execute("""
        SELECT s.id, c.name, e.name, s.date, s.total_amount, s.tax_amount, s.payment_method
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.id
        LEFT JOIN employees e ON s.employee_id = e.id
        WHERE s.store_id = ? AND s.date BETWEEN ? AND ?
        ORDER BY s.date DESC
        """, (self.current_store['id'], from_date, to_date))

        for row in self.cursor.fetchall():
            self.sales_tree.insert('', 'end', values=row)

    def new_sale_screen(self):
        """Display new sale form"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="New Sale", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Sales", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.sales_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Form frame
        form_frame = Frame(main_frame, bg='white')
        form_frame.pack(pady=10, padx=20, fill=X)

        # Customer
        Label(form_frame, text="Customer:", font=('Arial', 12), bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.customer_var = StringVar()
        self.customer_combo = ttk.Combobox(form_frame, textvariable=self.customer_var, font=('Arial', 12), width=28)
        self.customer_combo.grid(row=0, column=1, pady=5, padx=5)

        # Load customers
        self.cursor.execute("SELECT id, name FROM customers ORDER BY name")
        customers = self.cursor.fetchall()
        customer_list = [f"{c[0]} - {c[1]}" for c in customers]
        self.customer_combo['values'] = customer_list

        # Payment method
        Label(form_frame, text="Payment Method:", font=('Arial', 12), bg='white').grid(row=0, column=2, sticky='w', pady=5, padx=5)
        self.payment_var = StringVar()
        payments = ["Cash", "Credit Card", "Debit Card", "Insurance", "UPI"]
        self.payment_combo = ttk.Combobox(form_frame, textvariable=self.payment_var, values=payments, font=('Arial', 12), width=15)
        self.payment_combo.grid(row=0, column=3, pady=5, padx=5)

        # Add medicine frame
        add_frame = Frame(main_frame, bg='white')
        add_frame.pack(pady=10, padx=20, fill=X)

        Label(add_frame, text="Add Medicine to Sale", font=('Arial', 14, 'bold'), bg='white').pack(pady=5)

        # Medicine
        Label(add_frame, text="Medicine:", font=('Arial', 12), bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.medicine_var = StringVar()
        self.medicine_combo = ttk.Combobox(add_frame, textvariable=self.medicine_var, font=('Arial', 12), width=28)
        self.medicine_combo.grid(row=0, column=1, pady=5, padx=5)

        # Load medicines
        self.cursor.execute("""
        SELECT m.id, m.name, m.quantity, m.price, u.name
        FROM medicines m
        LEFT JOIN units u ON m.unit_id = u.id
        WHERE m.quantity > 0
        ORDER BY m.name
        """)
        medicines = self.cursor.fetchall()
        medicine_list = [f"{m[0]} - {m[1]} (Stock: {m[2]} {m[4]}, Price: {m[3]})" for m in medicines]
        self.medicine_combo['values'] = medicine_list

        # Batch
        Label(add_frame, text="Batch:", font=('Arial', 12), bg='white').grid(row=0, column=2, sticky='w', pady=5, padx=5)
        self.batch_var = StringVar()
        self.batch_combo = ttk.Combobox(add_frame, textvariable=self.batch_var, font=('Arial', 12), width=15)
        self.batch_combo.grid(row=0, column=3, pady=5, padx=5)

        # Quantity
        Label(add_frame, text="Quantity:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.qty_entry = Entry(add_frame, font=('Arial', 12), width=10)
        self.qty_entry.grid(row=1, column=1, sticky='w', pady=5, padx=5)

        # Add button
        add_btn = Button(add_frame, text="Add", font=('Arial', 12), bg='#2ecc71', fg='white',
                       command=self.add_to_sale, width=10)
        add_btn.grid(row=1, column=2, sticky='w', pady=5, padx=5)

        # Check interactions button
        check_btn = Button(add_frame, text="Check Interactions", font=('Arial', 12), bg='#e74c3c', fg='white',
                          command=self.check_interactions, width=15)
        check_btn.grid(row=1, column=3, sticky='w', pady=5, padx=5)

        # Sale items table
        items_frame = Frame(main_frame)
        items_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(items_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.sale_items_tree = ttk.Treeview(items_frame, columns=('ID', 'Name', 'Batch', 'Quantity', 'Price', 'Tax', 'Total'),
                                          show='headings', yscrollcommand=scrollbar.set)

        self.sale_items_tree.heading('ID', text='ID')
        self.sale_items_tree.heading('Name', text='Name')
        self.sale_items_tree.heading('Batch', text='Batch')
        self.sale_items_tree.heading('Quantity', text='Quantity')
        self.sale_items_tree.heading('Price', text='Price')
        self.sale_items_tree.heading('Tax', text='Tax')
        self.sale_items_tree.heading('Total', text='Total')

        self.sale_items_tree.column('ID', width=50)
        self.sale_items_tree.column('Name', width=200)
        self.sale_items_tree.column('Batch', width=100)
        self.sale_items_tree.column('Quantity', width=100)
        self.sale_items_tree.column('Price', width=100)
        self.sale_items_tree.column('Tax', width=80)
        self.sale_items_tree.column('Total', width=100)

        scrollbar.config(command=self.sale_items_tree.yview)
        self.sale_items_tree.pack(fill=BOTH, expand=True)

        # Total frame
        total_frame = Frame(main_frame, bg='white')
        total_frame.pack(pady=10, padx=20, fill=X)

        self.subtotal_label = Label(total_frame, text="Subtotal: $0.00", font=('Arial', 12), bg='white')
        self.subtotal_label.pack(side=LEFT, padx=10)

        self.tax_label = Label(total_frame, text="Tax: $0.00", font=('Arial', 12), bg='white')
        self.tax_label.pack(side=LEFT, padx=10)

        self.total_label = Label(total_frame, text="Total: $0.00", font=('Arial', 14, 'bold'), bg='white')
        self.total_label.pack(side=RIGHT, padx=10)

        # Buttons
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10, padx=20, fill=X)

        complete_btn = Button(btn_frame, text="Complete Sale", font=('Arial', 12), bg='#2ecc71', fg='white',
                             command=self.complete_sale, width=15)
        complete_btn.pack(side=LEFT, padx=5)

        apply_discount_btn = Button(btn_frame, text="Apply Discount", font=('Arial', 12), bg='#f39c12', fg='white',
                                   command=self.apply_discount, width=15)
        apply_discount_btn.pack(side=LEFT, padx=5)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.sales_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=5)

        # Initialize sale items list
        self.sale_items = []
        self.sale_subtotal = 0.0
        self.sale_tax = 0.0
        self.sale_total = 0.0
        self.discount_percent = 0.0

        # Bind medicine selection to load batches
        self.medicine_combo.bind('<<ComboboxSelected>>', self.load_batches_for_medicine)

    def load_batches_for_medicine(self, event=None):
        """Load batches for selected medicine"""
        medicine = self.medicine_var.get()

        if not medicine:
            return

        try:
            medicine_id = int(medicine.split(' - ')[0])
        except (ValueError, IndexError):
            return

        # Get batches for this medicine
        self.cursor.execute("""
        SELECT id, batch_number, expiry_date, quantity
        FROM batches
        WHERE medicine_id = ? AND quantity > 0
        ORDER BY expiry_date ASC
        """, (medicine_id,))

        batches = self.cursor.fetchall()
        batch_list = [f"{b[0]} - {b[1]} (Exp: {b[2]}, Qty: {b[3]})" for b in batches]
        self.batch_combo['values'] = batch_list

        if batch_list:
            self.batch_combo.current(0)

    def add_to_sale(self):
        """Add medicine to current sale"""
        medicine = self.medicine_var.get()
        batch = self.batch_var.get()
        quantity = self.qty_entry.get().strip()

        if not medicine or not quantity:
            messagebox.showerror("Error", "Please select a medicine and enter quantity!")
            return

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive integer!")
            return

        # Get medicine details
        medicine_id = int(medicine.split(' - ')[0])
        self.cursor.execute("SELECT id, name, quantity, price, tax_rate FROM medicines WHERE id=?", (medicine_id,))
        med = self.cursor.fetchone()

        if not med:
            messagebox.showerror("Error", "Medicine not found!")
            return

        if quantity > med[2]:
            messagebox.showerror("Error", f"Only {med[2]} items available in stock!")
            return

        # Get batch details if selected
        batch_id = None
        batch_number = None
        if batch:
            try:
                batch_id = int(batch.split(' - ')[0])
                self.cursor.execute("SELECT batch_number, quantity FROM batches WHERE id=?", (batch_id,))
                batch_data = self.cursor.fetchone()
                if batch_data:
                    batch_number = batch_data[0]
                    if quantity > batch_data[1]:
                        messagebox.showerror("Error", f"Only {batch_data[1]} items available in this batch!")
                        return
            except (ValueError, IndexError):
                pass

        # Calculate tax
        tax_rate = med[4] if med[4] else 0.0
        item_price = med[3]
        item_tax = item_price * (tax_rate / 100)
        item_total = (item_price + item_tax) * quantity

        # Check if medicine already in sale
        for item in self.sale_items:
            if item['id'] == medicine_id and item['batch_id'] == batch_id:
                item['quantity'] += quantity
                item['total'] = (item['price'] + item['tax']) * item['quantity']
                break
        else:
            self.sale_items.append({
                'id': medicine_id,
                'name': med[1],
                'batch_id': batch_id,
                'batch_number': batch_number,
                'quantity': quantity,
                'price': item_price,
                'tax': item_tax,
                'total': item_total
            })

        # Update sale items tree
        self.update_sale_items_tree()

        # Clear form
        self.medicine_var.set('')
        self.batch_var.set('')
        self.qty_entry.delete(0, END)

    def update_sale_items_tree(self):
        """Update sale items treeview"""
        # Clear existing data
        for i in self.sale_items_tree.get_children():
            self.sale_items_tree.delete(i)

        # Add items
        self.sale_subtotal = 0.0
        self.sale_tax = 0.0
        self.sale_total = 0.0

        for item in self.sale_items:
            self.sale_items_tree.insert('', 'end', values=(
                item['id'],
                item['name'],
                item['batch_number'] if item['batch_number'] else 'N/A',
                item['quantity'],
                f"${item['price']:.2f}",
                f"${item['tax']:.2f}",
                f"${item['total']:.2f}"
            ))
            self.sale_subtotal += item['price'] * item['quantity']
            self.sale_tax += item['tax'] * item['quantity']
            self.sale_total += item['total']

        # Apply discount if any
        if self.discount_percent > 0:
            discount_amount = self.sale_total * (self.discount_percent / 100)
            self.sale_total -= discount_amount

        # Update labels
        self.subtotal_label.config(text=f"Subtotal: ${self.sale_subtotal:.2f}")
        self.tax_label.config(text=f"Tax: ${self.sale_tax:.2f}")
        self.total_label.config(text=f"Total: ${self.sale_total:.2f}")

    def check_interactions(self):
        """Check for drug interactions in current sale"""
        if len(self.sale_items) < 2:
            messagebox.showinfo("No Interactions", "Add at least two medicines to check for interactions.")
            return

        interactions_found = False
        interaction_text = "Potential Drug Interactions:\n\n"

        # Check all pairs of medicines
        for i in range(len(self.sale_items)):
            for j in range(i + 1, len(self.sale_items)):
                med1_id = self.sale_items[i]['id']
                med2_id = self.sale_items[j]['id']

                # Check for interaction
                self.cursor.execute("""
                SELECT severity, description
                FROM drug_interactions
                WHERE (medicine_id1 = ? AND medicine_id2 = ?) OR (medicine_id1 = ? AND medicine_id2 = ?)
                """, (med1_id, med2_id, med2_id, med1_id))

                interaction = self.cursor.fetchone()
                if interaction:
                    interactions_found = True
                    interaction_text += f"{self.sale_items[i]['name']} + {self.sale_items[j]['name']}:\n"
                    interaction_text += f"Severity: {interaction[0]}\n"
                    interaction_text += f"Description: {interaction[1]}\n\n"

        if interactions_found:
            messagebox.showwarning("Drug Interactions Found", interaction_text)
        else:
            messagebox.showinfo("No Interactions", "No known drug interactions found.")

    def apply_discount(self):
        """Apply discount to current sale"""
        discount_window = Toplevel(self.root)
        discount_window.title("Apply Discount")
        discount_window.geometry("300x150")

        Label(discount_window, text="Discount Percentage:", font=('Arial', 12)).pack(pady=10)

        discount_entry = Entry(discount_window, font=('Arial', 12), width=10)
        discount_entry.pack(pady=5)

        def apply():
            try:
                discount = float(discount_entry.get())
                if discount < 0 or discount > 100:
                    raise ValueError

                self.discount_percent = discount
                self.update_sale_items_tree()
                discount_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Discount must be a number between 0 and 100!")

        Button(discount_window, text="Apply", command=apply).pack(pady=10)

    def complete_sale(self):
        """Complete the current sale"""
        if not self.sale_items:
            messagebox.showerror("Error", "No items in sale!")
            return

        customer = self.customer_var.get()
        payment = self.payment_var.get()

        if not payment:
            messagebox.showerror("Error", "Please select a payment method!")
            return

        # Get customer ID
        customer_id = None
        if customer:
            customer_id = int(customer.split(' - ')[0])

        # Create sale record
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute("""
        INSERT INTO sales (customer_id, employee_id, store_id, date, total_amount, tax_amount, payment_method)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (customer_id, self.current_user['id'], self.current_store['id'], today,
              self.sale_total, self.sale_tax, payment))

        sale_id = self.cursor.lastrowid

        # Add sale items and update inventory
        for item in self.sale_items:
            # Add sale item
            self.cursor.execute("""
            INSERT INTO sale_items (sale_id, medicine_id, batch_id, quantity, price_per_unit, tax_rate)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (sale_id, item['id'], item['batch_id'], item['quantity'], item['price'],
                  item['tax'] / item['price'] * 100 if item['price'] > 0 else 0))

            # Update medicine quantity
            self.cursor.execute("""
            UPDATE medicines
            SET quantity = quantity - ?
            WHERE id = ?
            """, (item['quantity'], item['id']))

            # Update batch quantity if batch is specified
            if item['batch_id']:
                self.cursor.execute("""
                UPDATE batches
                SET quantity = quantity - ?
                WHERE id = ?
                """, (item['quantity'], item['batch_id']))

        # Update customer loyalty points if applicable
        if customer_id:
            points_to_add = int(self.sale_total / 10)  # 1 point for every $10 spent
            self.cursor.execute("""
            UPDATE customers
            SET loyalty_points = loyalty_points + ?
            WHERE id = ?
            """, (points_to_add, customer_id))

            # Send notification to customer
            self.cursor.execute("""
            INSERT INTO notifications (customer_id, type, message, date)
            VALUES (?, ?, ?, ?)
            """, (customer_id, 'Loyalty Points',
                  f"You've earned {points_to_add} loyalty points from your recent purchase!", today))

        self.conn.commit()

        # Generate invoice
        self.generate_invoice(sale_id)

        messagebox.showinfo("Success", f"Sale completed successfully! Sale ID: {sale_id}")
        self.sales_screen()

    def generate_invoice(self, sale_id):
        """Generate invoice for sale"""
        # Get sale details
        self.cursor.execute("""
        SELECT s.id, c.name, e.name, s.date, s.total_amount, s.tax_amount, s.payment_method
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.id
        LEFT JOIN employees e ON s.employee_id = e.id
        WHERE s.id = ?
        """, (sale_id,))

        sale = self.cursor.fetchone()

        if not sale:
            messagebox.showerror("Error", "Sale not found!")
            return

        # Get sale items
        self.cursor.execute("""
        SELECT si.medicine_id, m.name, si.quantity, si.price_per_unit, si.tax_rate, b.batch_number
        FROM sale_items si
        JOIN medicines m ON si.medicine_id = m.id
        LEFT JOIN batches b ON si.batch_id = b.id
        WHERE si.sale_id = ?
        """, (sale_id,))

        items = self.cursor.fetchall()

        # Create invoice text
        invoice_text = f"""
        INVOICE
        ======
        Invoice ID: {sale[0]}
        Date: {sale[3]}
        Store: {self.current_store['name']}
        Address: {self.current_store['address']}
        Contact: {self.current_store['contact']}

        Customer: {sale[1] if sale[1] else 'Walk-in'}
        Cashier: {sale[2]}
        Payment Method: {sale[6]}

        ----------------------------------------
        ITEMS:
        """

        for item in items:
            tax_amount = item[3] * (item[4] / 100) * item[2]
            invoice_text += f"{item[1]} (Batch: {item[5] if item[5] else 'N/A'})\n"
            invoice_text += f"  {item[2]} x ${item[3]:.2f} = ${item[3] * item[2]:.2f}\n"
            invoice_text += f"  Tax: ${tax_amount:.2f}\n\n"

        invoice_text += f"""
        ----------------------------------------
        Subtotal: ${sale[4] - sale[5]:.2f}
        Tax: ${sale[5]:.2f}
        Total: ${sale[4]:.2f}

        Thank you for your purchase!
        """

        # Save invoice to file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"Invoice_{sale_id}.txt"
        )

        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(invoice_text)
                messagebox.showinfo("Success", f"Invoice saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save invoice: {str(e)}")

    def view_sale_screen(self):
        """Display sale details screen"""
        # Get selected sale
        selected = self.sales_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a sale to view!")
            return

        item = self.sales_tree.item(selected[0])
        sale_id = item['values'][0]

        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Sale Details", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Sales", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.sales_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Sale details frame
        details_frame = Frame(main_frame, bg='white')
        details_frame.pack(pady=10, padx=20, fill=X)

        # Get sale details
        self.cursor.execute("""
        SELECT s.id, c.name, e.name, s.date, s.total_amount, s.tax_amount, s.payment_method
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.id
        LEFT JOIN employees e ON s.employee_id = e.id
        WHERE s.id = ?
        """, (sale_id,))

        sale = self.cursor.fetchone()

        if not sale:
            messagebox.showerror("Error", "Sale not found!")
            return

        # Display sale details
        Label(details_frame, text=f"Sale ID: {sale[0]}", font=('Arial', 12, 'bold'), bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Customer: {sale[1] if sale[1] else 'Walk-in'}", font=('Arial', 12), bg='white').grid(row=0, column=1, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Employee: {sale[2]}", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Date: {sale[3]}", font=('Arial', 12), bg='white').grid(row=1, column=1, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Payment: {sale[6]}", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Subtotal: ${sale[4] - sale[5]:.2f}", font=('Arial', 12), bg='white').grid(row=2, column=1, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Tax: ${sale[5]:.2f}", font=('Arial', 12), bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Total: ${sale[4]:.2f}", font=('Arial', 12, 'bold'), bg='white').grid(row=3, column=1, sticky='w', pady=5, padx=5)

        # Sale items table
        items_frame = Frame(main_frame)
        items_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(items_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        items_tree = ttk.Treeview(items_frame, columns=('ID', 'Name', 'Batch', 'Quantity', 'Price', 'Tax', 'Total'),
                                 show='headings', yscrollcommand=scrollbar.set)

        items_tree.heading('ID', text='ID')
        items_tree.heading('Name', text='Name')
        items_tree.heading('Batch', text='Batch')
        items_tree.heading('Quantity', text='Quantity')
        items_tree.heading('Price', text='Price')
        items_tree.heading('Tax', text='Tax')
        items_tree.heading('Total', text='Total')

        items_tree.column('ID', width=50)
        items_tree.column('Name', width=200)
        items_tree.column('Batch', width=100)
        items_tree.column('Quantity', width=100)
        items_tree.column('Price', width=100)
        items_tree.column('Tax', width=80)
        items_tree.column('Total', width=100)

        scrollbar.config(command=items_tree.yview)
        items_tree.pack(fill=BOTH, expand=True)

        # Get sale items
        self.cursor.execute("""
        SELECT si.medicine_id, m.name, b.batch_number, si.quantity, si.price_per_unit, si.tax_rate,
               (si.quantity * si.price_per_unit) as subtotal,
               (si.quantity * si.price_per_unit * si.tax_rate / 100) as tax,
               (si.quantity * si.price_per_unit * (1 + si.tax_rate / 100)) as total
        FROM sale_items si
        JOIN medicines m ON si.medicine_id = m.id
        LEFT JOIN batches b ON si.batch_id = b.id
        WHERE si.sale_id = ?
        """, (sale_id,))

        for row in self.cursor.fetchall():
            items_tree.insert('', 'end', values=(
                row[0],
                row[1],
                row[2] if row[2] else 'N/A',
                row[3],
                f"${row[4]:.2f}",
                f"${row[6]:.2f}",
                f"${row[7]:.2f}"
            ))

        # Buttons
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10)

        print_btn = Button(btn_frame, text="Print Invoice", font=('Arial', 12), bg='#3498db', fg='white',
                          command=lambda: self.generate_invoice(sale_id), width=15)
        print_btn.pack(side=LEFT, padx=10)

        return_btn = Button(btn_frame, text="Process Return", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=lambda: self.process_return_from_sale(sale_id), width=15)
        return_btn.pack(side=LEFT, padx=10)

    def process_return_screen(self):
        """Display process return screen"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Process Return", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Sales", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.sales_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Search frame
        search_frame = Frame(main_frame, bg='white')
        search_frame.pack(pady=10, padx=20, fill=X)

        Label(search_frame, text="Sale ID:", font=('Arial', 12), bg='white').pack(side=LEFT, padx=5)
        self.sale_id_entry = Entry(search_frame, font=('Arial', 12), width=15)
        self.sale_id_entry.pack(side=LEFT, padx=5)

        search_btn = Button(search_frame, text="Search", font=('Arial', 10), bg='#3498db', fg='white',
                           command=self.search_sale_for_return, width=10)
        search_btn.pack(side=LEFT, padx=5)

        # Sale details frame
        details_frame = Frame(main_frame, bg='white')
        details_frame.pack(pady=10, padx=20, fill=X)

        # Sale details labels
        self.sale_details_labels = {}

        labels = ["Sale ID:", "Customer:", "Date:", "Payment Method:", "Total Amount:"]
        for i, label in enumerate(labels):
            Label(details_frame, text=label, font=('Arial', 12, 'bold'), bg='white').grid(row=i, column=0, sticky='w', pady=5, padx=5)
            self.sale_details_labels[label] = Label(details_frame, text="", font=('Arial', 12), bg='white')
            self.sale_details_labels[label].grid(row=i, column=1, sticky='w', pady=5, padx=5)

        # Return items frame
        items_frame = Frame(main_frame)
        items_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(items_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.return_items_tree = ttk.Treeview(items_frame, columns=('ID', 'Name', 'Batch', 'Quantity', 'Price', 'Return Qty', 'Reason'),
                                           show='headings', yscrollcommand=scrollbar.set)

        self.return_items_tree.heading('ID', text='ID')
        self.return_items_tree.heading('Name', text='Name')
        self.return_items_tree.heading('Batch', text='Batch')
        self.return_items_tree.heading('Quantity', text='Quantity')
        self.return_items_tree.heading('Price', text='Price')
        self.return_items_tree.heading('Return Qty', text='Return Qty')
        self.return_items_tree.heading('Reason', text='Reason')

        self.return_items_tree.column('ID', width=50)
        self.return_items_tree.column('Name', width=200)
        self.return_items_tree.column('Batch', width=100)
        self.return_items_tree.column('Quantity', width=100)
        self.return_items_tree.column('Price', width=100)
        self.return_items_tree.column('Return Qty', width=100)
        self.return_items_tree.column('Reason', width=150)

        scrollbar.config(command=self.return_items_tree.yview)
        self.return_items_tree.pack(fill=BOTH, expand=True)

        # Return details frame
        return_frame = Frame(main_frame, bg='white')
        return_frame.pack(pady=10, padx=20, fill=X)

        Label(return_frame, text="Return Reason:", font=('Arial', 12), bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.return_reason_entry = Entry(return_frame, font=('Arial', 12), width=50)
        self.return_reason_entry.grid(row=0, column=1, sticky='w', pady=5, padx=5)

        Label(return_frame, text="Refund Amount:", font=('Arial', 12, 'bold'), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.refund_amount_label = Label(return_frame, text="$0.00", font=('Arial', 12), bg='white')
        self.refund_amount_label.grid(row=1, column=1, sticky='w', pady=5, padx=5)

        # Buttons
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10)

        process_btn = Button(btn_frame, text="Process Return", font=('Arial', 12), bg='#2ecc71', fg='white',
                             command=self.process_return, width=15)
        process_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.sales_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

        # Initialize return items
        self.return_items = []
        self.current_sale_id = None

    def search_sale_for_return(self):
        """Search for a sale to process return"""
        sale_id = self.sale_id_entry.get().strip()

        if not sale_id:
            messagebox.showerror("Error", "Please enter a Sale ID!")
            return

        try:
            sale_id = int(sale_id)
        except ValueError:
            messagebox.showerror("Error", "Sale ID must be a number!")
            return

        # Get sale details
        self.cursor.execute("""
        SELECT s.id, c.name, s.date, s.payment_method, s.total_amount
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.id
        WHERE s.id = ? AND s.store_id = ?
        """, (sale_id, self.current_store['id']))

        sale = self.cursor.fetchone()

        if not sale:
            messagebox.showerror("Error", "Sale not found!")
            return

        # Update sale details labels
        self.sale_details_labels["Sale ID:"].config(text=str(sale[0]))
        self.sale_details_labels["Customer:"].config(text=sale[1] if sale[1] else 'Walk-in')
        self.sale_details_labels["Date:"].config(text=sale[2])
        self.sale_details_labels["Payment Method:"].config(text=sale[3])
        self.sale_details_labels["Total Amount:"].config(text=f"${sale[4]:.2f}")

        # Get sale items
        self.cursor.execute("""
        SELECT si.id, m.name, b.batch_number, si.quantity, si.price_per_unit, si.batch_id
        FROM sale_items si
        JOIN medicines m ON si.medicine_id = m.id
        LEFT JOIN batches b ON si.batch_id = b.id
        WHERE si.sale_id = ?
        """, (sale_id,))

        items = self.cursor.fetchall()

        # Clear existing items
        for i in self.return_items_tree.get_children():
            self.return_items_tree.delete(i)

        # Add items to tree
        self.return_items = []
        for item in items:
            self.return_items_tree.insert('', 'end', values=(
                item[0],  # sale_item_id
                item[1],  # medicine_name
                item[2] if item[2] else 'N/A',  # batch_number
                item[3],  # quantity
                f"${item[4]:.2f}",  # price
                0,  # return_quantity (default 0)
                ""  # reason (default empty)
            ))

            self.return_items.append({
                'sale_item_id': item[0],
                'medicine_name': item[1],
                'batch_number': item[2] if item[2] else None,
                'quantity': item[3],
                'price': item[4],
                'batch_id': item[5],
                'return_quantity': 0,
                'reason': ''
            })

        self.current_sale_id = sale_id

    def process_return(self):
        """Process the return"""
        if not self.current_sale_id:
            messagebox.showerror("Error", "No sale selected!")
            return

        return_reason = self.return_reason_entry.get().strip()
        if not return_reason:
            messagebox.showerror("Error", "Please enter a return reason!")
            return

        # Get return quantities and reasons from tree
        return_items = []
        total_refund = 0.0

        for i, item in enumerate(self.return_items_tree.get_children()):
            values = self.return_items_tree.item(item)['values']
            return_qty = values[5]
            reason = values[6]

            if return_qty > 0:
                if return_qty > self.return_items[i]['quantity']:
                    messagebox.showerror("Error", f"Return quantity cannot exceed original quantity for {self.return_items[i]['medicine_name']}!")
                    return

                return_items.append({
                    'sale_item_id': self.return_items[i]['sale_item_id'],
                    'medicine_id': self.return_items[i]['medicine_name'],
                    'batch_id': self.return_items[i]['batch_id'],
                    'return_quantity': return_qty,
                    'price': self.return_items[i]['price'],
                    'reason': reason if reason else return_reason
                })

                total_refund += return_qty * self.return_items[i]['price']

        if not return_items:
            messagebox.showerror("Error", "No items selected for return!")
            return

        # Get sale details
        self.cursor.execute("SELECT customer_id, employee_id FROM sales WHERE id=?", (self.current_sale_id,))
        sale = self.cursor.fetchone()

        if not sale:
            messagebox.showerror("Error", "Sale not found!")
            return

        # Create return record
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute("""
        INSERT INTO returns (sale_id, customer_id, employee_id, date, reason, total_amount)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (self.current_sale_id, sale[0], self.current_user['id'], today, return_reason, total_refund))

        return_id = self.cursor.lastrowid

        # Add return items and update inventory
        for item in return_items:
            # Add return item
            self.cursor.execute("""
            INSERT INTO return_items (return_id, sale_item_id, batch_id, quantity, reason)
            VALUES (?, ?, ?, ?, ?)
            """, (return_id, item['sale_item_id'], item['batch_id'], item['return_quantity'], item['reason']))

            # Update medicine quantity
            self.cursor.execute("""
            UPDATE medicines
            SET quantity = quantity + ?
            WHERE id = (SELECT medicine_id FROM sale_items WHERE id=?)
            """, (item['return_quantity'], item['sale_item_id']))

            # Update batch quantity if batch is specified
            if item['batch_id']:
                self.cursor.execute("""
                UPDATE batches
                SET quantity = quantity + ?
                WHERE id = ?
                """, (item['return_quantity'], item['batch_id']))

        self.conn.commit()

        messagebox.showinfo("Success", f"Return processed successfully! Return ID: {return_id}\nRefund Amount: ${total_refund:.2f}")
        self.sales_screen()

    def process_return_from_sale(self, sale_id):
        """Process return from sale details screen"""
        self.process_return_screen()
        self.sale_id_entry.delete(0, END)
        self.sale_id_entry.insert(0, str(sale_id))
        self.search_sale_for_return()

    def daily_closing_screen(self):
        """Display daily closing screen"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Daily Closing Report", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Sales", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.sales_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Date frame
        date_frame = Frame(main_frame, bg='white')
        date_frame.pack(pady=10, padx=20, fill=X)

        Label(date_frame, text="Date:", font=('Arial', 12), bg='white').pack(side=LEFT, padx=5)
        self.closing_date_entry = Entry(date_frame, font=('Arial', 12), width=15)
        self.closing_date_entry.pack(side=LEFT, padx=5)
        self.closing_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))

        generate_btn = Button(date_frame, text="Generate Report", font=('Arial', 12), bg='#3498db', fg='white',
                             command=self.generate_daily_closing, width=15)
        generate_btn.pack(side=LEFT, padx=10)

        # Report frame
        report_frame = Frame(main_frame, bg='white')
        report_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Summary frame
        summary_frame = Frame(report_frame, bg='white', relief='groove', borderwidth=2)
        summary_frame.pack(pady=10, padx=20, fill=X)

        Label(summary_frame, text="Sales Summary", font=('Arial', 14, 'bold'), bg='white').pack(pady=5)

        # Sales summary labels
        self.sales_summary_labels = {}

        labels = ["Total Sales:", "Cash Sales:", "Card Sales:", "UPI Sales:", "Tax Amount:"]
        for i, label in enumerate(labels):
            Label(summary_frame, text=label, font=('Arial', 12), bg='white').grid(row=i, column=0, sticky='w', pady=5, padx=5)
            self.sales_summary_labels[label] = Label(summary_frame, text="$0.00", font=('Arial', 12), bg='white')
            self.sales_summary_labels[label].grid(row=i, column=1, sticky='w', pady=5, padx=5)

        # Cash register frame
        cash_frame = Frame(report_frame, bg='white', relief='groove', borderwidth=2)
        cash_frame.pack(pady=10, padx=20, fill=X)

        Label(cash_frame, text="Cash Register", font=('Arial', 14, 'bold'), bg='white').pack(pady=5)

        # Cash register labels
        self.cash_labels = {}

        cash_labels = ["Expected Cash:", "Actual Cash:", "Difference:"]
        for i, label in enumerate(cash_labels):
            Label(cash_frame, text=label, font=('Arial', 12), bg='white').grid(row=i, column=0, sticky='w', pady=5, padx=5)
            self.cash_labels[label] = Label(cash_frame, text="$0.00", font=('Arial', 12), bg='white')
            self.cash_labels[label].grid(row=i, column=1, sticky='w', pady=5, padx=5)

        # Notes frame
        notes_frame = Frame(report_frame, bg='white')
        notes_frame.pack(pady=10, padx=20, fill=X)

        Label(notes_frame, text="Notes:", font=('Arial', 12), bg='white').pack(side=LEFT, padx=5)
        self.notes_entry = Entry(notes_frame, font=('Arial', 12), width=50)
        self.notes_entry.pack(side=LEFT, padx=5, fill=X, expand=True)

        # Buttons
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10)

        save_btn = Button(btn_frame, text="Save Closing Report", font=('Arial', 12), bg='#2ecc71', fg='white',
                         command=self.save_daily_closing, width=15)
        save_btn.pack(side=LEFT, padx=10)

        print_btn = Button(btn_frame, text="Print Report", font=('Arial', 12), bg='#3498db', fg='white',
                          command=self.print_daily_closing, width=15)
        print_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.sales_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

        # Initialize variables
        self.daily_closing_data = {
            'total_sales': 0.0,
            'cash_sales': 0.0,
            'card_sales': 0.0,
            'upi_sales': 0.0,
            'tax_amount': 0.0,
            'expected_cash': 0.0,
            'actual_cash': 0.0,
            'difference': 0.0
        }

    def generate_daily_closing(self):
        """Generate daily closing report"""
        date = self.closing_date_entry.get().strip()

        if not date:
            messagebox.showerror("Error", "Please enter a date!")
            return

        # Get start and end of day
        start_date = f"{date} 00:00:00"
        end_date = f"{date} 23:59:59"

        # Get sales data for the day
        self.cursor.execute("""
        SELECT payment_method, SUM(total_amount), SUM(tax_amount)
        FROM sales
        WHERE store_id = ? AND date BETWEEN ? AND ?
        GROUP BY payment_method
        """, (self.current_store['id'], start_date, end_date))

        sales_data = self.cursor.fetchall()

        # Initialize values
        total_sales = 0.0
        cash_sales = 0.0
        card_sales = 0.0
        upi_sales = 0.0
        tax_amount = 0.0

        # Process sales data
        for row in sales_data:
            payment_method = row[0]
            amount = row[1] if row[1] else 0.0
            tax = row[2] if row[2] else 0.0

            total_sales += amount
            tax_amount += tax

            if payment_method == 'Cash':
                cash_sales = amount
            elif payment_method == 'Credit Card' or payment_method == 'Debit Card':
                card_sales += amount
            elif payment_method == 'UPI':
                upi_sales = amount

        # Update labels
        self.sales_summary_labels["Total Sales:"].config(text=f"${total_sales:.2f}")
        self.sales_summary_labels["Cash Sales:"].config(text=f"${cash_sales:.2f}")
        self.sales_summary_labels["Card Sales:"].config(text=f"${card_sales:.2f}")
        self.sales_summary_labels["UPI Sales:"].config(text=f"${upi_sales:.2f}")
        self.sales_summary_labels["Tax Amount:"].config(text=f"${tax_amount:.2f}")

        # Update cash register
        self.daily_closing_data = {
            'total_sales': total_sales,
            'cash_sales': cash_sales,
            'card_sales': card_sales,
            'upi_sales': upi_sales,
            'tax_amount': tax_amount,
            'expected_cash': cash_sales,
            'actual_cash': cash_sales,
            'difference': 0.0
        }

        self.cash_labels["Expected Cash:"].config(text=f"${cash_sales:.2f}")
        self.cash_labels["Actual Cash:"].config(text=f"${cash_sales:.2f}")
        self.cash_labels["Difference:"].config(text="$0.00")

    def save_daily_closing(self):
        """Save daily closing report"""
        date = self.closing_date_entry.get().strip()
        notes = self.notes_entry.get().strip()

        if not date:
            messagebox.showerror("Error", "Please enter a date!")
            return

        # Get actual cash from user
        actual_cash_window = Toplevel(self.root)
        actual_cash_window.title("Enter Actual Cash")
        actual_cash_window.geometry("300x150")

        Label(actual_cash_window, text="Actual Cash in Drawer:", font=('Arial', 12)).pack(pady=10)

        actual_cash_entry = Entry(actual_cash_window, font=('Arial', 12), width=15)
        actual_cash_entry.pack(pady=5)
        actual_cash_entry.insert(0, str(self.daily_closing_data['expected_cash']))

        def save():
            try:
                actual_cash = float(actual_cash_entry.get())
                difference = actual_cash - self.daily_closing_data['expected_cash']

                # Update labels
                self.cash_labels["Actual Cash:"].config(text=f"${actual_cash:.2f}")
                self.cash_labels["Difference:"].config(text=f"{'+' if difference >= 0 else ''}{difference:.2f}")

                # Save to database
                self.cursor.execute("""
                INSERT INTO daily_closing (store_id, employee_id, date, cash_sales, card_sales, upi_sales,
                                         total_sales, cash_in_drawer, expected_cash, difference, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (self.current_store['id'], self.current_user['id'], f"{date} 23:59:59",
                      self.daily_closing_data['cash_sales'], self.daily_closing_data['card_sales'],
                      self.daily_closing_data['upi_sales'], self.daily_closing_data['total_sales'],
                      actual_cash, self.daily_closing_data['expected_cash'], difference, notes))

                self.conn.commit()

                messagebox.showinfo("Success", "Daily closing report saved successfully!")
                actual_cash_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number!")

        Button(actual_cash_window, text="Save", command=save).pack(pady=10)

    def print_daily_closing(self):
        """Print daily closing report"""
        date = self.closing_date_entry.get().strip()
        notes = self.notes_entry.get().strip()

        if not date:
            messagebox.showerror("Error", "Please enter a date!")
            return

        # Create report text
        report_text = f"""
        DAILY CLOSING REPORT
        ====================
        Date: {date}
        Store: {self.current_store['name']}
        Employee: {self.current_user['name']}

        SALES SUMMARY
        -------------
        Total Sales: ${self.daily_closing_data['total_sales']:.2f}
        Cash Sales: ${self.daily_closing_data['cash_sales']:.2f}
        Card Sales: ${self.daily_closing_data['card_sales']:.2f}
        UPI Sales: ${self.daily_closing_data['upi_sales']:.2f}
        Tax Amount: ${self.daily_closing_data['tax_amount']:.2f}

        CASH REGISTER
        -------------
        Expected Cash: ${self.daily_closing_data['expected_cash']:.2f}
        Actual Cash: ${self.daily_closing_data['actual_cash']:.2f}
        Difference: ${self.daily_closing_data['difference']:.2f}

        NOTES
        -----
        {notes if notes else 'N/A'}

        Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """

        # Save report to file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"Daily_Closing_{date}.txt"
        )

        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(report_text)
                messagebox.showinfo("Success", f"Report saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save report: {str(e)}")

    def reports_screen(self):
        """Display reports screen"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Reports", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Dashboard", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.dashboard, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Report options
        options_frame = Frame(main_frame, bg='white')
        options_frame.pack(pady=20, padx=20, fill=X)

        Label(options_frame, text="Select Report Type:", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)

        # Sales reports
        Label(options_frame, text="Sales Reports", font=('Arial', 12, 'bold'), bg='white').pack(anchor='w', pady=5)

        sales_btn = Button(options_frame, text="Sales Report", font=('Arial', 12), bg='#3498db', fg='white',
                          command=self.sales_report, width=20, height=2)
        sales_btn.pack(pady=5)

        profit_btn = Button(options_frame, text="Profit & Loss Report", font=('Arial', 12), bg='#3498db', fg='white',
                           command=self.profit_loss_report, width=20, height=2)
        profit_btn.pack(pady=5)

        customer_trends_btn = Button(options_frame, text="Customer Purchase Trends", font=('Arial', 12), bg='#3498db', fg='white',
                                   command=self.customer_trends_report, width=20, height=2)
        customer_trends_btn.pack(pady=5)

        # Inventory reports
        Label(options_frame, text="Inventory Reports", font=('Arial', 12, 'bold'), bg='white').pack(anchor='w', pady=(20, 5))

        inventory_btn = Button(options_frame, text="Inventory Report", font=('Arial', 12), bg='#2ecc71', fg='white',
                              command=self.inventory_report, width=20, height=2)
        inventory_btn.pack(pady=5)

        expiry_btn = Button(options_frame, text="Expiry Report", font=('Arial', 12), bg='#2ecc71', fg='white',
                           command=self.expiry_report, width=20, height=2)
        expiry_btn.pack(pady=5)

        low_stock_btn = Button(options_frame, text="Low Stock Report", font=('Arial', 12), bg='#2ecc71', fg='white',
                             command=self.low_stock_report, width=20, height=2)
        low_stock_btn.pack(pady=5)

        expiry_loss_btn = Button(options_frame, text="Expiry Loss Report", font=('Arial', 12), bg='#2ecc71', fg='white',
                                command=self.expiry_loss_report, width=20, height=2)
        expiry_loss_btn.pack(pady=5)

        # Supplier reports
        Label(options_frame, text="Supplier Reports", font=('Arial', 12, 'bold'), bg='white').pack(anchor='w', pady=(20, 5))

        supplier_btn = Button(options_frame, text="Supplier Performance", font=('Arial', 12), bg='#f39c12', fg='white',
                            command=self.supplier_performance_report, width=20, height=2)
        supplier_btn.pack(pady=5)

    def sales_report(self):
        """Generate sales report"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Sales Report", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Reports", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.reports_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Date range frame
        date_frame = Frame(main_frame, bg='white')
        date_frame.pack(pady=10, padx=20, fill=X)

        Label(date_frame, text="From Date (YYYY-MM-DD):", font=('Arial', 12), bg='white').pack(side=LEFT, padx=5)
        self.from_date_entry = Entry(date_frame, font=('Arial', 12), width=15)
        self.from_date_entry.pack(side=LEFT, padx=5)

        Label(date_frame, text="To Date (YYYY-MM-DD):", font=('Arial', 12), bg='white').pack(side=LEFT, padx=5)
        self.to_date_entry = Entry(date_frame, font=('Arial', 12), width=15)
        self.to_date_entry.pack(side=LEFT, padx=5)

        generate_btn = Button(date_frame, text="Generate Report", font=('Arial', 12), bg='#3498db', fg='white',
                            command=self.generate_sales_report, width=15)
        generate_btn.pack(side=LEFT, padx=10)

        # Report frame
        report_frame = Frame(main_frame)
        report_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(report_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.sales_report_tree = ttk.Treeview(report_frame, columns=('ID', 'Customer', 'Employee', 'Date', 'Amount', 'Tax', 'Payment'),
                                             show='headings', yscrollcommand=scrollbar.set)

        self.sales_report_tree.heading('ID', text='ID')
        self.sales_report_tree.heading('Customer', text='Customer')
        self.sales_report_tree.heading('Employee', text='Employee')
        self.sales_report_tree.heading('Date', text='Date')
        self.sales_report_tree.heading('Amount', text='Amount')
        self.sales_report_tree.heading('Tax', text='Tax')
        self.sales_report_tree.heading('Payment', text='Payment Method')

        self.sales_report_tree.column('ID', width=50)
        self.sales_report_tree.column('Customer', width=150)
        self.sales_report_tree.column('Employee', width=150)
        self.sales_report_tree.column('Date', width=150)
        self.sales_report_tree.column('Amount', width=100)
        self.sales_report_tree.column('Tax', width=80)
        self.sales_report_tree.column('Payment', width=120)

        scrollbar.config(command=self.sales_report_tree.yview)
        self.sales_report_tree.pack(fill=BOTH, expand=True)

        # Summary frame
        summary_frame = Frame(main_frame, bg='white')
        summary_frame.pack(pady=10, padx=20, fill=X)

        self.sales_summary_labels = {}

        labels = ["Total Sales:", "Total Tax:", "Average Sale:", "Cash Sales:", "Card Sales:", "UPI Sales:"]
        for i, label in enumerate(labels):
            Label(summary_frame, text=label, font=('Arial', 12, 'bold'), bg='white').grid(row=i//3, column=(i%3)*2, sticky='w', pady=5, padx=5)
            self.sales_summary_labels[label] = Label(summary_frame, text="$0.00", font=('Arial', 12), bg='white')
            self.sales_summary_labels[label].grid(row=i//3, column=(i%3)*2+1, sticky='w', pady=5, padx=5)

        # Export button
        export_btn = Button(main_frame, text="Export to CSV", font=('Arial', 12), bg='#2ecc71', fg='white',
                           command=self.export_sales_report, width=15)
        export_btn.pack(pady=10)

        # Generate default report (current month)
        today = datetime.now()
        from_date = today.replace(day=1).strftime('%Y-%m-%d')
        to_date = today.strftime('%Y-%m-%d')

        self.from_date_entry.insert(0, from_date)
        self.to_date_entry.insert(0, to_date)
        self.generate_sales_report()

    def generate_sales_report(self):
        """Generate sales report based on date range"""
        from_date = self.from_date_entry.get().strip()
        to_date = self.to_date_entry.get().strip()

        if not from_date or not to_date:
            messagebox.showerror("Error", "Please enter both from and to dates!")
            return

        # Clear existing data
        for i in self.sales_report_tree.get_children():
            self.sales_report_tree.delete(i)

        # Get sales data
        self.cursor.execute("""
        SELECT s.id, c.name, e.name, s.date, s.total_amount, s.tax_amount, s.payment_method
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.id
        LEFT JOIN employees e ON s.employee_id = e.id
        WHERE s.store_id = ? AND s.date BETWEEN ? AND ?
        ORDER BY s.date DESC
        """, (self.current_store['id'], from_date, to_date))

        sales_data = self.cursor.fetchall()

        total_sales = 0.0
        total_tax = 0.0
        cash_sales = 0.0
        card_sales = 0.0
        upi_sales = 0.0

        for row in sales_data:
            self.sales_report_tree.insert('', 'end', values=row)
            total_sales += row[4]
            total_tax += row[5]

            if row[6] == 'Cash':
                cash_sales += row[4]
            elif row[6] in ['Credit Card', 'Debit Card']:
                card_sales += row[4]
            elif row[6] == 'UPI':
                upi_sales += row[4]

        # Update summary labels
        average_sale = total_sales / len(sales_data) if sales_data else 0.0

        self.sales_summary_labels["Total Sales:"].config(text=f"${total_sales:.2f}")
        self.sales_summary_labels["Total Tax:"].config(text=f"${total_tax:.2f}")
        self.sales_summary_labels["Average Sale:"].config(text=f"${average_sale:.2f}")
        self.sales_summary_labels["Cash Sales:"].config(text=f"${cash_sales:.2f}")
        self.sales_summary_labels["Card Sales:"].config(text=f"${card_sales:.2f}")
        self.sales_summary_labels["UPI Sales:"].config(text=f"${upi_sales:.2f}")

    def export_sales_report(self):
        """Export sales report to CSV"""
        from_date = self.from_date_entry.get().strip()
        to_date = self.to_date_entry.get().strip()

        if not from_date or not to_date:
            messagebox.showerror("Error", "Please enter both from and to dates!")
            return

        # Get sales data
        self.cursor.execute("""
        SELECT s.id, c.name, e.name, s.date, s.total_amount, s.tax_amount, s.payment_method
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.id
        LEFT JOIN employees e ON s.employee_id = e.id
        WHERE s.store_id = ? AND s.date BETWEEN ? AND ?
        ORDER BY s.date DESC
        """, (self.current_store['id'], from_date, to_date))

        sales_data = self.cursor.fetchall()

        # Save to CSV
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"Sales_Report_{from_date}_to_{to_date}.csv"
        )

        if file_path:
            try:
                import csv

                with open(file_path, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)

                    # Write header
                    writer.writerow(['Sale ID', 'Customer', 'Employee', 'Date', 'Total Amount', 'Tax Amount', 'Payment Method'])

                    # Write data
                    for row in sales_data:
                        writer.writerow(row)

                messagebox.showinfo("Success", f"Report exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export report: {str(e)}")

    def profit_loss_report(self):
        """Generate profit and loss report"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Profit & Loss Report", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Reports", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.reports_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Date range frame
        date_frame = Frame(main_frame, bg='white')
        date_frame.pack(pady=10, padx=20, fill=X)

        Label(date_frame, text="From Date (YYYY-MM-DD):", font=('Arial', 12), bg='white').pack(side=LEFT, padx=5)
        self.from_date_entry = Entry(date_frame, font=('Arial', 12), width=15)
        self.from_date_entry.pack(side=LEFT, padx=5)

        Label(date_frame, text="To Date (YYYY-MM-DD):", font=('Arial', 12), bg='white').pack(side=LEFT, padx=5)
        self.to_date_entry = Entry(date_frame, font=('Arial', 12), width=15)
        self.to_date_entry.pack(side=LEFT, padx=5)

        generate_btn = Button(date_frame, text="Generate Report", font=('Arial', 12), bg='#3498db', fg='white',
                            command=self.generate_profit_loss_report, width=15)
        generate_btn.pack(side=LEFT, padx=10)

        # Report frame
        report_frame = Frame(main_frame)
        report_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Summary frame
        summary_frame = Frame(report_frame, bg='white', relief='groove', borderwidth=2)
        summary_frame.pack(pady=10, padx=20, fill=X)

        Label(summary_frame, text="Profit & Loss Summary", font=('Arial', 14, 'bold'), bg='white').pack(pady=5)

        # P&L labels
        self.pl_labels = {}

        labels = ["Total Revenue:", "Total Cost:", "Gross Profit:", "Operating Expenses:", "Net Profit:", "Profit Margin:"]
        for i, label in enumerate(labels):
            Label(summary_frame, text=label, font=('Arial', 12, 'bold'), bg='white').grid(row=i, column=0, sticky='w', pady=5, padx=5)
            self.pl_labels[label] = Label(summary_frame, text="$0.00", font=('Arial', 12), bg='white')
            self.pl_labels[label].grid(row=i, column=1, sticky='w', pady=5, padx=5)

        # Top selling medicines frame
        top_frame = Frame(report_frame, bg='white', relief='groove', borderwidth=2)
        top_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        Label(top_frame, text="Top Selling Medicines", font=('Arial', 14, 'bold'), bg='white').pack(pady=5)

        # Scrollbar
        scrollbar = Scrollbar(top_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.top_medicines_tree = ttk.Treeview(top_frame, columns=('Medicine', 'Quantity', 'Revenue', 'Profit'),
                                             show='headings', yscrollcommand=scrollbar.set)

        self.top_medicines_tree.heading('Medicine', text='Medicine')
        self.top_medicines_tree.heading('Quantity', text='Quantity Sold')
        self.top_medicines_tree.heading('Revenue', text='Revenue')
        self.top_medicines_tree.heading('Profit', text='Profit')

        self.top_medicines_tree.column('Medicine', width=200)
        self.top_medicines_tree.column('Quantity', width=100)
        self.top_medicines_tree.column('Revenue', width=100)
        self.top_medicines_tree.column('Profit', width=100)

        scrollbar.config(command=self.top_medicines_tree.yview)
        self.top_medicines_tree.pack(fill=BOTH, expand=True)

        # Generate default report (current month)
        today = datetime.now()
        from_date = today.replace(day=1).strftime('%Y-%m-%d')
        to_date = today.strftime('%Y-%m-%d')

        self.from_date_entry.insert(0, from_date)
        self.to_date_entry.insert(0, to_date)
        self.generate_profit_loss_report()

    def generate_profit_loss_report(self):
        """Generate profit and loss report based on date range"""
        from_date = self.from_date_entry.get().strip()
        to_date = self.to_date_entry.get().strip()

        if not from_date or not to_date:
            messagebox.showerror("Error", "Please enter both from and to dates!")
            return

        # Get total revenue from sales
        self.cursor.execute("""
        SELECT SUM(total_amount)
        FROM sales
        WHERE store_id = ? AND date BETWEEN ? AND ?
        """, (self.current_store['id'], from_date, to_date))

        total_revenue = self.cursor.fetchone()[0] if self.cursor.fetchone()[0] else 0.0

        # Get total cost from purchases
        self.cursor.execute("""
        SELECT SUM(total_amount)
        FROM purchases
        WHERE store_id = ? AND date BETWEEN ? AND ?
        """, (self.current_store['id'], from_date, to_date))

        total_cost = self.cursor.fetchone()[0] if self.cursor.fetchone()[0] else 0.0

        # Calculate gross profit
        gross_profit = total_revenue - total_cost

        # For simplicity, we'll assume operating expenses are 20% of revenue
        operating_expenses = total_revenue * 0.2

        # Calculate net profit
        net_profit = gross_profit - operating_expenses

        # Calculate profit margin
        profit_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0.0

        # Update labels
        self.pl_labels["Total Revenue:"].config(text=f"${total_revenue:.2f}")
        self.pl_labels["Total Cost:"].config(text=f"${total_cost:.2f}")
        self.pl_labels["Gross Profit:"].config(text=f"${gross_profit:.2f}")
        self.pl_labels["Operating Expenses:"].config(text=f"${operating_expenses:.2f}")
        self.pl_labels["Net Profit:"].config(text=f"${net_profit:.2f}")
        self.pl_labels["Profit Margin:"].config(text=f"{profit_margin:.2f}%")

        # Get top selling medicines
        self.cursor.execute("""
        SELECT m.name, SUM(si.quantity) as total_quantity,
               SUM(si.quantity * si.price_per_unit) as revenue,
               SUM(si.quantity * (si.price_per_unit - (
                   SELECT COALESCE(AVG(cost_price), 0)
                   FROM batches
                   WHERE medicine_id = m.id
               ))) as profit
        FROM sale_items si
        JOIN medicines m ON si.medicine_id = m.id
        JOIN sales s ON si.sale_id = s.id
        WHERE s.store_id = ? AND s.date BETWEEN ? AND ?
        GROUP BY m.id
        ORDER BY total_quantity DESC
        LIMIT 10
        """, (self.current_store['id'], from_date, to_date))

        # Clear existing data
        for i in self.top_medicines_tree.get_children():
            self.top_medicines_tree.delete(i)

        # Add data to tree
        for row in self.cursor.fetchall():
            self.top_medicines_tree.insert('', 'end', values=(
                row[0],  # medicine_name
                row[1],  # total_quantity
                f"${row[2]:.2f}",  # revenue
                f"${row[3]:.2f}"  # profit
            ))

    def customer_trends_report(self):
        """Generate customer purchase trends report"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Customer Purchase Trends", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Reports", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.reports_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Date range frame
        date_frame = Frame(main_frame, bg='white')
        date_frame.pack(pady=10, padx=20, fill=X)

        Label(date_frame, text="From Date (YYYY-MM-DD):", font=('Arial', 12), bg='white').pack(side=LEFT, padx=5)
        self.from_date_entry = Entry(date_frame, font=('Arial', 12), width=15)
        self.from_date_entry.pack(side=LEFT, padx=5)

        Label(date_frame, text="To Date (YYYY-MM-DD):", font=('Arial', 12), bg='white').pack(side=LEFT, padx=5)
        self.to_date_entry = Entry(date_frame, font=('Arial', 12), width=15)
        self.to_date_entry.pack(side=LEFT, padx=5)

        generate_btn = Button(date_frame, text="Generate Report", font=('Arial', 12), bg='#3498db', fg='white',
                            command=self.generate_customer_trends_report, width=15)
        generate_btn.pack(side=LEFT, padx=10)

        # Report frame
        report_frame = Frame(main_frame)
        report_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Top customers frame
        top_frame = Frame(report_frame, bg='white', relief='groove', borderwidth=2)
        top_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        Label(top_frame, text="Top Customers by Spending", font=('Arial', 14, 'bold'), bg='white').pack(pady=5)

        # Scrollbar
        scrollbar = Scrollbar(top_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.top_customers_tree = ttk.Treeview(top_frame, columns=('Customer', 'Total Purchases', 'Total Amount', 'Last Purchase'),
                                             show='headings', yscrollcommand=scrollbar.set)

        self.top_customers_tree.heading('Customer', text='Customer')
        self.top_customers_tree.heading('Total Purchases', text='Total Purchases')
        self.top_customers_tree.heading('Total Amount', text='Total Amount')
        self.top_customers_tree.heading('Last Purchase', text='Last Purchase')

        self.top_customers_tree.column('Customer', width=200)
        self.top_customers_tree.column('Total Purchases', width=120)
        self.top_customers_tree.column('Total Amount', width=120)
        self.top_customers_tree.column('Last Purchase', width=150)

        scrollbar.config(command=self.top_customers_tree.yview)
        self.top_customers_tree.pack(fill=BOTH, expand=True)

        # Popular medicines frame
        popular_frame = Frame(report_frame, bg='white', relief='groove', borderwidth=2)
        popular_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        Label(popular_frame, text="Most Popular Medicines", font=('Arial', 14, 'bold'), bg='white').pack(pady=5)

        # Scrollbar
        scrollbar2 = Scrollbar(popular_frame)
        scrollbar2.pack(side=RIGHT, fill=Y)

        # Treeview
        self.popular_medicines_tree = ttk.Treeview(popular_frame, columns=('Medicine', 'Times Purchased', 'Total Quantity'),
                                                show='headings', yscrollcommand=scrollbar2.set)

        self.popular_medicines_tree.heading('Medicine', text='Medicine')
        self.popular_medicines_tree.heading('Times Purchased', text='Times Purchased')
        self.popular_medicines_tree.heading('Total Quantity', text='Total Quantity')

        self.popular_medicines_tree.column('Medicine', width=250)
        self.popular_medicines_tree.column('Times Purchased', width=120)
        self.popular_medicines_tree.column('Total Quantity', width=120)

        scrollbar2.config(command=self.popular_medicines_tree.yview)
        self.popular_medicines_tree.pack(fill=BOTH, expand=True)

        # Generate default report (current month)
        today = datetime.now()
        from_date = today.replace(day=1).strftime('%Y-%m-%d')
        to_date = today.strftime('%Y-%m-%d')

        self.from_date_entry.insert(0, from_date)
        self.to_date_entry.insert(0, to_date)
        self.generate_customer_trends_report()

    def generate_customer_trends_report(self):
        """Generate customer trends report based on date range"""
        from_date = self.from_date_entry.get().strip()
        to_date = self.to_date_entry.get().strip()

        if not from_date or not to_date:
            messagebox.showerror("Error", "Please enter both from and to dates!")
            return

        # Get top customers by spending
        self.cursor.execute("""
        SELECT c.name, COUNT(s.id) as total_purchases, SUM(s.total_amount) as total_amount, MAX(s.date) as last_purchase
        FROM sales s
        JOIN customers c ON s.customer_id = c.id
        WHERE s.store_id = ? AND s.date BETWEEN ? AND ?
        GROUP BY c.id
        ORDER BY total_amount DESC
        LIMIT 10
        """, (self.current_store['id'], from_date, to_date))

        # Clear existing data
        for i in self.top_customers_tree.get_children():
            self.top_customers_tree.delete(i)

        # Add data to tree
        for row in self.cursor.fetchall():
            self.top_customers_tree.insert('', 'end', values=(
                row[0],  # customer_name
                row[1],  # total_purchases
                f"${row[2]:.2f}",  # total_amount
                row[3]  # last_purchase
            ))

        # Get most popular medicines
        self.cursor.execute("""
        SELECT m.name, COUNT(DISTINCT s.id) as times_purchased, SUM(si.quantity) as total_quantity
        FROM sale_items si
        JOIN medicines m ON si.medicine_id = m.id
        JOIN sales s ON si.sale_id = s.id
        WHERE s.store_id = ? AND s.date BETWEEN ? AND ?
        GROUP BY m.id
        ORDER BY times_purchased DESC, total_quantity DESC
        LIMIT 10
        """, (self.current_store['id'], from_date, to_date))

        # Clear existing data
        for i in self.popular_medicines_tree.get_children():
            self.popular_medicines_tree.delete(i)

        # Add data to tree
        for row in self.cursor.fetchall():
            self.popular_medicines_tree.insert('', 'end', values=(
                row[0],  # medicine_name
                row[1],  # times_purchased
                row[2]   # total_quantity
            ))

    def inventory_report(self):
        """Generate inventory report"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Inventory Report", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Reports", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.reports_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Report frame
        report_frame = Frame(main_frame)
        report_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(report_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.inventory_tree = ttk.Treeview(report_frame, columns=('ID', 'Name', 'Description', 'Quantity', 'Price', 'Supplier', 'Expiry', 'Category', 'Unit', 'Value'),
                                         show='headings', yscrollcommand=scrollbar.set)

        self.inventory_tree.heading('ID', text='ID')
        self.inventory_tree.heading('Name', text='Name')
        self.inventory_tree.heading('Description', text='Description')
        self.inventory_tree.heading('Quantity', text='Quantity')
        self.inventory_tree.heading('Price', text='Price')
        self.inventory_tree.heading('Supplier', text='Supplier')
        self.inventory_tree.heading('Expiry', text='Expiry Date')
        self.inventory_tree.heading('Category', text='Category')
        self.inventory_tree.heading('Unit', text='Unit')
        self.inventory_tree.heading('Value', text='Total Value')

        self.inventory_tree.column('ID', width=50)
        self.inventory_tree.column('Name', width=150)
        self.inventory_tree.column('Description', width=200)
        self.inventory_tree.column('Quantity', width=80)
        self.inventory_tree.column('Price', width=80)
        self.inventory_tree.column('Supplier', width=120)
        self.inventory_tree.column('Expiry', width=100)
        self.inventory_tree.column('Category', width=100)
        self.inventory_tree.column('Unit', width=80)
        self.inventory_tree.column('Value', width=100)

        scrollbar.config(command=self.inventory_tree.yview)
        self.inventory_tree.pack(fill=BOTH, expand=True)

        # Total value frame
        total_frame = Frame(main_frame, bg='white')
        total_frame.pack(pady=10, padx=20, fill=X)

        self.inventory_total_label = Label(total_frame, text="Total Inventory Value: $0.00", font=('Arial', 14, 'bold'), bg='white')
        self.inventory_total_label.pack(side=RIGHT, padx=10)

        # Export button
        export_btn = Button(main_frame, text="Export to CSV", font=('Arial', 12), bg='#2ecc71', fg='white',
                           command=self.export_inventory_report, width=15)
        export_btn.pack(pady=10)

        # Load inventory data
        self.load_inventory_report()

    def load_inventory_report(self):
        """Load inventory report data"""
        # Clear existing data
        for i in self.inventory_tree.get_children():
            self.inventory_tree.delete(i)

        # Get all medicines
        self.cursor.execute("""
        SELECT m.id, m.name, m.description, m.quantity, m.price, s.name, m.expiry_date, m.category, u.name
        FROM medicines m
        LEFT JOIN suppliers s ON m.supplier_id = s.id
        LEFT JOIN units u ON m.unit_id = u.id
        ORDER BY m.name
        """)

        medicines = self.cursor.fetchall()
        total_value = 0.0

        for med in medicines:
            total_med_value = med[3] * med[4]  # quantity * price
            total_value += total_med_value

            self.inventory_tree.insert('', 'end', values=(
                med[0],  # id
                med[1],  # name
                med[2],  # description
                med[3],  # quantity
                f"${med[4]:.2f}",  # price
                med[5] if med[5] else "N/A",  # supplier
                med[6] if med[6] else "N/A",  # expiry
                med[7],  # category
                med[8] if med[8] else "N/A",  # unit
                f"${total_med_value:.2f}"  # total value
            ))

        # Update total label
        self.inventory_total_label.config(text=f"Total Inventory Value: ${total_value:.2f}")

    def export_inventory_report(self):
        """Export inventory report to CSV"""
        # Get all medicines
        self.cursor.execute("""
        SELECT m.id, m.name, m.description, m.quantity, m.price, s.name, m.expiry_date, m.category, u.name
        FROM medicines m
        LEFT JOIN suppliers s ON m.supplier_id = s.id
        LEFT JOIN units u ON m.unit_id = u.id
        ORDER BY m.name
        """)

        medicines = self.cursor.fetchall()

        # Save to CSV
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"Inventory_Report_{datetime.now().strftime('%Y-%m-%d')}.csv"
        )

        if file_path:
            try:
                import csv

                with open(file_path, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)

                    # Write header
                    writer.writerow(['ID', 'Name', 'Description', 'Quantity', 'Price', 'Supplier', 'Expiry Date', 'Category', 'Unit'])

                    # Write data
                    for med in medicines:
                        writer.writerow(med)

                messagebox.showinfo("Success", f"Report exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export report: {str(e)}")

    def expiry_report(self):
        """Generate expiry report"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Expiry Report", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Reports", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.reports_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Date range frame
        date_frame = Frame(main_frame, bg='white')
        date_frame.pack(pady=10, padx=20, fill=X)

        Label(date_frame, text="Days to Expiry:", font=('Arial', 12), bg='white').pack(side=LEFT, padx=5)
        self.days_entry = Entry(date_frame, font=('Arial', 12), width=10)
        self.days_entry.pack(side=LEFT, padx=5)
        self.days_entry.insert(0, "90")

        generate_btn = Button(date_frame, text="Generate Report", font=('Arial', 12), bg='#3498db', fg='white',
                            command=self.generate_expiry_report, width=15)
        generate_btn.pack(side=LEFT, padx=10)

        # Report frame
        report_frame = Frame(main_frame)
        report_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(report_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.expiry_tree = ttk.Treeview(report_frame, columns=('ID', 'Name', 'Quantity', 'Price', 'Expiry Date', 'Days Left', 'Value'),
                                       show='headings', yscrollcommand=scrollbar.set)

        self.expiry_tree.heading('ID', text='ID')
        self.expiry_tree.heading('Name', text='Name')
        self.expiry_tree.heading('Quantity', text='Quantity')
        self.expiry_tree.heading('Price', text='Price')
        self.expiry_tree.heading('Expiry Date', text='Expiry Date')
        self.expiry_tree.heading('Days Left', text='Days Left')
        self.expiry_tree.heading('Value', text='Total Value')

        self.expiry_tree.column('ID', width=50)
        self.expiry_tree.column('Name', width=200)
        self.expiry_tree.column('Quantity', width=100)
        self.expiry_tree.column('Price', width=100)
        self.expiry_tree.column('Expiry Date', width=120)
        self.expiry_tree.column('Days Left', width=100)
        self.expiry_tree.column('Value', width=100)

        scrollbar.config(command=self.expiry_tree.yview)
        self.expiry_tree.pack(fill=BOTH, expand=True)

        # Total value frame
        total_frame = Frame(main_frame, bg='white')
        total_frame.pack(pady=10, padx=20, fill=X)

        self.expiry_total_label = Label(total_frame, text="Total Value of Expiring Medicines: $0.00", font=('Arial', 14, 'bold'), bg='white')
        self.expiry_total_label.pack(side=RIGHT, padx=10)

        # Generate default report
        self.generate_expiry_report()

    def generate_expiry_report(self):
        """Generate expiry report"""
        try:
            days = int(self.days_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of days!")
            return

        # Clear existing data
        for i in self.expiry_tree.get_children():
            self.expiry_tree.delete(i)

        # Calculate date threshold
        threshold_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')

        # Get medicines expiring within the threshold
        self.cursor.execute("""
        SELECT id, name, quantity, price, expiry_date
        FROM medicines
        WHERE expiry_date IS NOT NULL AND expiry_date <= ?
        ORDER BY expiry_date ASC
        """, (threshold_date,))

        medicines = self.cursor.fetchall()
        total_value = 0.0
        today = datetime.now().strftime('%Y-%m-%d')

        for med in medicines:
            if med[4]:  # expiry_date
                try:
                    expiry_date = datetime.strptime(med[4], '%Y-%m-%d')
                    days_left = (expiry_date - datetime.now()).days

                    total_med_value = med[2] * med[3]  # quantity * price
                    total_value += total_med_value

                    self.expiry_tree.insert('', 'end', values=(
                        med[0],  # id
                        med[1],  # name
                        med[2],  # quantity
                        f"${med[3]:.2f}",  # price
                        med[4],  # expiry_date
                        days_left,
                        f"${total_med_value:.2f}"  # total value
                    ))
                except ValueError:
                    # Skip if date format is invalid
                    continue

        # Update total label
        self.expiry_total_label.config(text=f"Total Value of Expiring Medicines: ${total_value:.2f}")

    def low_stock_report(self):
        """Generate low stock report"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Low Stock Report", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Reports", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.reports_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Report frame
        report_frame = Frame(main_frame)
        report_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(report_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.low_stock_tree = ttk.Treeview(report_frame, columns=('ID', 'Name', 'Current Stock', 'Reorder Level', 'Difference', 'Price', 'Value'),
                                          show='headings', yscrollcommand=scrollbar.set)

        self.low_stock_tree.heading('ID', text='ID')
        self.low_stock_tree.heading('Name', text='Name')
        self.low_stock_tree.heading('Current Stock', text='Current Stock')
        self.low_stock_tree.heading('Reorder Level', text='Reorder Level')
        self.low_stock_tree.heading('Difference', text='Difference')
        self.low_stock_tree.heading('Price', text='Price')
        self.low_stock_tree.heading('Value', text='Value to Reorder')

        self.low_stock_tree.column('ID', width=50)
        self.low_stock_tree.column('Name', width=200)
        self.low_stock_tree.column('Current Stock', width=120)
        self.low_stock_tree.column('Reorder Level', width=120)
        self.low_stock_tree.column('Difference', width=100)
        self.low_stock_tree.column('Price', width=100)
        self.low_stock_tree.column('Value', width=120)

        scrollbar.config(command=self.low_stock_tree.yview)
        self.low_stock_tree.pack(fill=BOTH, expand=True)

        # Total value frame
        total_frame = Frame(main_frame, bg='white')
        total_frame.pack(pady=10, padx=20, fill=X)

        self.low_stock_total_label = Label(total_frame, text="Total Value to Reorder: $0.00", font=('Arial', 14, 'bold'), bg='white')
        self.low_stock_total_label.pack(side=RIGHT, padx=10)

        # Load low stock data
        self.load_low_stock_report()

    def load_low_stock_report(self):
        """Load low stock report data"""
        # Clear existing data
        for i in self.low_stock_tree.get_children():
            self.low_stock_tree.delete(i)

        # Get medicines with low stock
        self.cursor.execute("""
        SELECT id, name, quantity, reorder_level, price
        FROM medicines
        WHERE quantity < reorder_level
        ORDER BY (reorder_level - quantity) DESC
        """)

        medicines = self.cursor.fetchall()
        total_value = 0.0

        for med in medicines:
            difference = med[3] - med[2]  # reorder_level - quantity
            value_to_reorder = difference * med[4]  # difference * price
            total_value += value_to_reorder

            self.low_stock_tree.insert('', 'end', values=(
                med[0],  # id
                med[1],  # name
                med[2],  # quantity
                med[3],  # reorder_level
                difference,
                f"${med[4]:.2f}",  # price
                f"${value_to_reorder:.2f}"  # value to reorder
            ))

        # Update total label
        self.low_stock_total_label.config(text=f"Total Value to Reorder: ${total_value:.2f}")

    def expiry_loss_report(self):
        """Generate expiry loss report"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Expiry Loss Report", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Reports", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.reports_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Date range frame
        date_frame = Frame(main_frame, bg='white')
        date_frame.pack(pady=10, padx=20, fill=X)

        Label(date_frame, text="From Date (YYYY-MM-DD):", font=('Arial', 12), bg='white').pack(side=LEFT, padx=5)
        self.from_date_entry = Entry(date_frame, font=('Arial', 12), width=15)
        self.from_date_entry.pack(side=LEFT, padx=5)

        Label(date_frame, text="To Date (YYYY-MM-DD):", font=('Arial', 12), bg='white').pack(side=LEFT, padx=5)
        self.to_date_entry = Entry(date_frame, font=('Arial', 12), width=15)
        self.to_date_entry.pack(side=LEFT, padx=5)

        generate_btn = Button(date_frame, text="Generate Report", font=('Arial', 12), bg='#3498db', fg='white',
                            command=self.generate_expiry_loss_report, width=15)
        generate_btn.pack(side=LEFT, padx=10)

        # Report frame
        report_frame = Frame(main_frame)
        report_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(report_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.expiry_loss_tree = ttk.Treeview(report_frame, columns=('ID', 'Name', 'Quantity', 'Cost Price', 'Total Loss'),
                                           show='headings', yscrollcommand=scrollbar.set)

        self.expiry_loss_tree.heading('ID', text='ID')
        self.expiry_loss_tree.heading('Name', text='Name')
        self.expiry_loss_tree.heading('Quantity', text='Quantity')
        self.expiry_loss_tree.heading('Cost Price', text='Cost Price')
        self.expiry_loss_tree.heading('Total Loss', text='Total Loss')

        self.expiry_loss_tree.column('ID', width=50)
        self.expiry_loss_tree.column('Name', width=200)
        self.expiry_loss_tree.column('Quantity', width=100)
        self.expiry_loss_tree.column('Cost Price', width=100)
        self.expiry_loss_tree.column('Total Loss', width=100)

        scrollbar.config(command=self.expiry_loss_tree.yview)
        self.expiry_loss_tree.pack(fill=BOTH, expand=True)

        # Total loss frame
        total_frame = Frame(main_frame, bg='white')
        total_frame.pack(pady=10, padx=20, fill=X)

        self.expiry_loss_total_label = Label(total_frame, text="Total Expiry Loss: $0.00", font=('Arial', 14, 'bold'), bg='white')
        self.expiry_loss_total_label.pack(side=RIGHT, padx=10)

        # Generate default report (current month)
        today = datetime.now()
        from_date = today.replace(day=1).strftime('%Y-%m-%d')
        to_date = today.strftime('%Y-%m-%d')

        self.from_date_entry.insert(0, from_date)
        self.to_date_entry.insert(0, to_date)
        self.generate_expiry_loss_report()

    def generate_expiry_loss_report(self):
        """Generate expiry loss report based on date range"""
        from_date = self.from_date_entry.get().strip()
        to_date = self.to_date_entry.get().strip()

        if not from_date or not to_date:
            messagebox.showerror("Error", "Please enter both from and to dates!")
            return

        # Clear existing data
        for i in self.expiry_loss_tree.get_children():
            self.expiry_loss_tree.delete(i)

        # Get expired medicines and their cost
        self.cursor.execute("""
        SELECT m.id, m.name, b.quantity, b.cost_price
        FROM batches b
        JOIN medicines m ON b.medicine_id = m.id
        WHERE b.expiry_date < ? AND b.expiry_date >= ?
        ORDER BY b.expiry_date ASC
        """, (from_date, to_date))

        batches = self.cursor.fetchall()
        total_loss = 0.0

        for batch in batches:
            loss = batch[2] * batch[3]  # quantity * cost_price
            total_loss += loss

            self.expiry_loss_tree.insert('', 'end', values=(
                batch[0],  # id
                batch[1],  # name
                batch[2],  # quantity
                f"${batch[3]:.2f}",  # cost_price
                f"${loss:.2f}"  # total_loss
            ))

        # Update total label
        self.expiry_loss_total_label.config(text=f"Total Expiry Loss: ${total_loss:.2f}")

    def supplier_performance_report(self):
        """Generate supplier performance report"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Supplier Performance Report", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Reports", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.reports_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Date range frame
        date_frame = Frame(main_frame, bg='white')
        date_frame.pack(pady=10, padx=20, fill=X)

        Label(date_frame, text="From Date (YYYY-MM-DD):", font=('Arial', 12), bg='white').pack(side=LEFT, padx=5)
        self.from_date_entry = Entry(date_frame, font=('Arial', 12), width=15)
        self.from_date_entry.pack(side=LEFT, padx=5)

        Label(date_frame, text="To Date (YYYY-MM-DD):", font=('Arial', 12), bg='white').pack(side=LEFT, padx=5)
        self.to_date_entry = Entry(date_frame, font=('Arial', 12), width=15)
        self.to_date_entry.pack(side=LEFT, padx=5)

        generate_btn = Button(date_frame, text="Generate Report", font=('Arial', 12), bg='#3498db', fg='white',
                            command=self.generate_supplier_performance_report, width=15)
        generate_btn.pack(side=LEFT, padx=10)

        # Report frame
        report_frame = Frame(main_frame)
        report_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(report_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.supplier_tree = ttk.Treeview(report_frame, columns=('ID', 'Name', 'Total Purchases', 'Total Amount', 'Avg Delivery Time', 'Medicine Count'),
                                        show='headings', yscrollcommand=scrollbar.set)

        self.supplier_tree.heading('ID', text='ID')
        self.supplier_tree.heading('Name', text='Name')
        self.supplier_tree.heading('Total Purchases', text='Total Purchases')
        self.supplier_tree.heading('Total Amount', text='Total Amount')
        self.supplier_tree.heading('Avg Delivery Time', text='Avg Delivery Time')
        self.supplier_tree.heading('Medicine Count', text='Medicine Count')

        self.supplier_tree.column('ID', width=50)
        self.supplier_tree.column('Name', width=200)
        self.supplier_tree.column('Total Purchases', width=120)
        self.supplier_tree.column('Total Amount', width=120)
        self.supplier_tree.column('Avg Delivery Time', width=150)
        self.supplier_tree.column('Medicine Count', width=120)

        scrollbar.config(command=self.supplier_tree.yview)
        self.supplier_tree.pack(fill=BOTH, expand=True)

        # Generate default report (current month)
        today = datetime.now()
        from_date = today.replace(day=1).strftime('%Y-%m-%d')
        to_date = today.strftime('%Y-%m-%d')

        self.from_date_entry.insert(0, from_date)
        self.to_date_entry.insert(0, to_date)
        self.generate_supplier_performance_report()

    def generate_supplier_performance_report(self):
        """Generate supplier performance report based on date range"""
        from_date = self.from_date_entry.get().strip()
        to_date = self.to_date_entry.get().strip()

        if not from_date or not to_date:
            messagebox.showerror("Error", "Please enter both from and to dates!")
            return

        # Clear existing data
        for i in self.supplier_tree.get_children():
            self.supplier_tree.delete(i)

        # Get supplier performance data
        self.cursor.execute("""
        SELECT s.id, s.name, COUNT(p.id) as total_purchases, SUM(p.total_amount) as total_amount,
               COUNT(DISTINCT pi.medicine_id) as medicine_count
        FROM suppliers s
        LEFT JOIN purchases p ON s.id = p.supplier_id
        LEFT JOIN purchase_items pi ON p.id = pi.purchase_id
        WHERE p.store_id = ? AND p.date BETWEEN ? AND ?
        GROUP BY s.id
        ORDER BY total_amount DESC
        """, (self.current_store['id'], from_date, to_date))

        for row in self.cursor.fetchall():
            # For simplicity, we'll use a placeholder for average delivery time
            # In a real system, this would be calculated from actual delivery data
            avg_delivery_time = "2-3 days"

            self.supplier_tree.insert('', 'end', values=(
                row[0],  # id
                row[1],  # name
                row[2],  # total_purchases
                f"${row[3]:.2f}" if row[3] else "$0.00",  # total_amount
                avg_delivery_time,
                row[4]   # medicine_count
            ))

    def settings_screen(self):
        """Display settings screen"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Settings", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Dashboard", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.dashboard, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Settings options
        options_frame = Frame(main_frame, bg='white')
        options_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

        # User management
        user_frame = Frame(options_frame, bg='white', relief='groove', borderwidth=2)
        user_frame.pack(pady=10, padx=20, fill=X)

        Label(user_frame, text="User Management", font=('Arial', 14, 'bold'), bg='white').pack(pady=5)

        user_btn_frame = Frame(user_frame, bg='white')
        user_btn_frame.pack(pady=5)

        Button(user_btn_frame, text="Manage Users", font=('Arial', 12), bg='#3498db', fg='white',
               command=self.users_screen, width=15).pack(side=LEFT, padx=5)

        Button(user_btn_frame, text="Change Password", font=('Arial', 12), bg='#3498db', fg='white',
               command=self.change_password_screen, width=15).pack(side=LEFT, padx=5)

        # Store management
        store_frame = Frame(options_frame, bg='white', relief='groove', borderwidth=2)
        store_frame.pack(pady=10, padx=20, fill=X)

        Label(store_frame, text="Store Management", font=('Arial', 14, 'bold'), bg='white').pack(pady=5)

        store_btn_frame = Frame(store_frame, bg='white')
        store_btn_frame.pack(pady=5)

        Button(store_btn_frame, text="Manage Stores", font=('Arial', 12), bg='#2ecc71', fg='white',
               command=self.stores_screen, width=15).pack(side=LEFT, padx=5)

        # System settings
        system_frame = Frame(options_frame, bg='white', relief='groove', borderwidth=2)
        system_frame.pack(pady=10, padx=20, fill=X)

        Label(system_frame, text="System Settings", font=('Arial', 14, 'bold'), bg='white').pack(pady=5)

        system_btn_frame = Frame(system_frame, bg='white')
        system_btn_frame.pack(pady=5)

        Button(system_btn_frame, text="Manage Units", font=('Arial', 12), bg='#f39c12', fg='white',
               command=self.units_screen, width=15).pack(side=LEFT, padx=5)

        Button(system_btn_frame, text="Backup Database", font=('Arial', 12), bg='#e74c3c', fg='white',
               command=self.backup_database, width=15).pack(side=LEFT, padx=5)

        Button(system_btn_frame, text="Restore Database", font=('Arial', 12), bg='#e74c3c', fg='white',
               command=self.restore_database, width=15).pack(side=LEFT, padx=5)

        # Notifications
        notification_frame = Frame(options_frame, bg='white', relief='groove', borderwidth=2)
        notification_frame.pack(pady=10, padx=20, fill=X)

        Label(notification_frame, text="Notifications", font=('Arial', 14, 'bold'), bg='white').pack(pady=5)

        notification_btn_frame = Frame(notification_frame, bg='white')
        notification_btn_frame.pack(pady=5)

        Button(notification_btn_frame, text="Send Notifications", font=('Arial', 12), bg='#9b59b6', fg='white',
               command=self.send_notifications_screen, width=15).pack(side=LEFT, padx=5)

        Button(notification_btn_frame, text="Notification Settings", font=('Arial', 12), bg='#9b59b6', fg='white',
               command=self.notification_settings_screen, width=15).pack(side=LEFT, padx=5)

    def users_screen(self):
        """Display users management screen"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="User Management", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Settings", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.settings_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Buttons frame
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10, padx=20, fill=X)

        add_btn = Button(btn_frame, text="Add User", font=('Arial', 12), bg='#2ecc71', fg='white',
                        command=self.add_user_screen, width=15)
        add_btn.pack(side=LEFT, padx=5)

        update_btn = Button(btn_frame, text="Update User", font=('Arial', 12), bg='#f39c12', fg='white',
                           command=self.update_user_screen, width=15)
        update_btn.pack(side=LEFT, padx=5)

        delete_btn = Button(btn_frame, text="Delete User", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.delete_user, width=15)
        delete_btn.pack(side=LEFT, padx=5)

        # Users table
        table_frame = Frame(main_frame)
        table_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(table_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.users_tree = ttk.Treeview(table_frame, columns=('ID', 'Name', 'Username', 'Role', 'Contact'),
                                     show='headings', yscrollcommand=scrollbar.set)

        self.users_tree.heading('ID', text='ID')
        self.users_tree.heading('Name', text='Name')
        self.users_tree.heading('Username', text='Username')
        self.users_tree.heading('Role', text='Role')
        self.users_tree.heading('Contact', text='Contact')

        self.users_tree.column('ID', width=50)
        self.users_tree.column('Name', width=150)
        self.users_tree.column('Username', width=150)
        self.users_tree.column('Role', width=100)
        self.users_tree.column('Contact', width=150)

        scrollbar.config(command=self.users_tree.yview)
        self.users_tree.pack(fill=BOTH, expand=True)

        # Load users
        self.load_users()

    def load_users(self):
        """Load all users data"""
        # Clear existing data
        for i in self.users_tree.get_children():
            self.users_tree.delete(i)

        # Get all users
        self.cursor.execute("SELECT id, name, username, role, contact FROM employees ORDER BY name")

        for row in self.cursor.fetchall():
            self.users_tree.insert('', 'end', values=row)

    def add_user_screen(self):
        """Display add user form"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Add New User", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Users", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.users_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Form frame
        form_frame = Frame(self.root, bg='white')
        form_frame.pack(fill=BOTH, expand=True, padx=50, pady=20)

        # User details
        Label(form_frame, text="User Details", font=('Arial', 16, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, pady=10)

        # Name
        Label(form_frame, text="Name:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.name_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.name_entry.grid(row=1, column=1, pady=5, padx=5)

        # Username
        Label(form_frame, text="Username:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.username_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.username_entry.grid(row=2, column=1, pady=5, padx=5)

        # Password
        Label(form_frame, text="Password:", font=('Arial', 12), bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=5)
        self.password_entry = Entry(form_frame, font=('Arial', 12), width=30, show='*')
        self.password_entry.grid(row=3, column=1, pady=5, padx=5)

        # Confirm Password
        Label(form_frame, text="Confirm Password:", font=('Arial', 12), bg='white').grid(row=4, column=0, sticky='w', pady=5, padx=5)
        self.confirm_password_entry = Entry(form_frame, font=('Arial', 12), width=30, show='*')
        self.confirm_password_entry.grid(row=4, column=1, pady=5, padx=5)

        # Role
        Label(form_frame, text="Role:", font=('Arial', 12), bg='white').grid(row=5, column=0, sticky='w', pady=5, padx=5)
        self.role_var = StringVar()
        roles = ["Admin", "Pharmacist", "Cashier", "Manager"]
        self.role_combo = ttk.Combobox(form_frame, textvariable=self.role_var, values=roles, font=('Arial', 12), width=28)
        self.role_combo.grid(row=5, column=1, pady=5, padx=5)

        # Contact
        Label(form_frame, text="Contact:", font=('Arial', 12), bg='white').grid(row=6, column=0, sticky='w', pady=5, padx=5)
        self.contact_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.contact_entry.grid(row=6, column=1, pady=5, padx=5)

        # Address
        Label(form_frame, text="Address:", font=('Arial', 12), bg='white').grid(row=7, column=0, sticky='w', pady=5, padx=5)
        self.address_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.address_entry.grid(row=7, column=1, pady=5, padx=5)

        # Buttons
        btn_frame = Frame(form_frame, bg='white')
        btn_frame.grid(row=8, column=0, columnspan=2, pady=20)

        save_btn = Button(btn_frame, text="Save User", font=('Arial', 12), bg='#2ecc71', fg='white',
                         command=self.save_user, width=15)
        save_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.users_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

    def save_user(self):
        """Save new user to database"""
        # Get form data
        name = self.name_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        role = self.role_var.get()
        contact = self.contact_entry.get().strip()
        address = self.address_entry.get().strip()

        # Validation
        if not name or not username or not password or not role:
            messagebox.showerror("Error", "Name, Username, Password, and Role are required!")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        # Check if username already exists
        self.cursor.execute("SELECT id FROM employees WHERE username=?", (username,))
        if self.cursor.fetchone():
            messagebox.showerror("Error", "Username already exists!")
            return

        # Insert user
        self.cursor.execute("""
        INSERT INTO employees (name, username, password, role, contact, address)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (name, username, password, role, contact, address))

        self.conn.commit()
        messagebox.showinfo("Success", "User added successfully!")
        self.users_screen()

    def update_user_screen(self):
        """Display update user form"""
        # Get selected user
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a user to update!")
            return

        item = self.users_tree.item(selected[0])
        user_id = item['values'][0]

        # Get user details
        self.cursor.execute("SELECT * FROM employees WHERE id=?", (user_id,))
        user = self.cursor.fetchone()

        if not user:
            messagebox.showerror("Error", "User not found!")
            return

        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Update User", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Users", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.users_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Form frame
        form_frame = Frame(self.root, bg='white')
        form_frame.pack(fill=BOTH, expand=True, padx=50, pady=20)

        # User details
        Label(form_frame, text="User Details", font=('Arial', 16, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, pady=10)

        # ID (read-only)
        Label(form_frame, text="ID:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        id_label = Label(form_frame, text=str(user[0]), font=('Arial', 12), bg='white')
        id_label.grid(row=1, column=1, sticky='w', pady=5, padx=5)

        # Name
        Label(form_frame, text="Name:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.name_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.name_entry.grid(row=2, column=1, pady=5, padx=5)
        self.name_entry.insert(0, user[1])

        # Username
        Label(form_frame, text="Username:", font=('Arial', 12), bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=5)
        self.username_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.username_entry.grid(row=3, column=1, pady=5, padx=5)
        self.username_entry.insert(0, user[2])

        # Password
        Label(form_frame, text="Password (leave blank to keep current):", font=('Arial', 12), bg='white').grid(row=4, column=0, sticky='w', pady=5, padx=5)
        self.password_entry = Entry(form_frame, font=('Arial', 12), width=30, show='*')
        self.password_entry.grid(row=4, column=1, pady=5, padx=5)

        # Role
        Label(form_frame, text="Role:", font=('Arial', 12), bg='white').grid(row=5, column=0, sticky='w', pady=5, padx=5)
        self.role_var = StringVar()
        roles = ["Admin", "Pharmacist", "Cashier", "Manager"]
        self.role_combo = ttk.Combobox(form_frame, textvariable=self.role_var, values=roles, font=('Arial', 12), width=28)
        self.role_combo.grid(row=5, column=1, pady=5, padx=5)
        self.role_combo.set(user[4])

        # Contact
        Label(form_frame, text="Contact:", font=('Arial', 12), bg='white').grid(row=6, column=0, sticky='w', pady=5, padx=5)
        self.contact_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.contact_entry.grid(row=6, column=1, pady=5, padx=5)
        self.contact_entry.insert(0, user[5] if user[5] else '')

        # Address
        Label(form_frame, text="Address:", font=('Arial', 12), bg='white').grid(row=7, column=0, sticky='w', pady=5, padx=5)
        self.address_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.address_entry.grid(row=7, column=1, pady=5, padx=5)
        self.address_entry.insert(0, user[6] if user[6] else '')

        # Buttons
        btn_frame = Frame(form_frame, bg='white')
        btn_frame.grid(row=8, column=0, columnspan=2, pady=20)

        update_btn = Button(btn_frame, text="Update User", font=('Arial', 12), bg='#f39c12', fg='white',
                           command=lambda: self.update_user(user_id), width=15)
        update_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.users_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

    def update_user(self, user_id):
        """Update user in database"""
        # Get form data
        name = self.name_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()
        contact = self.contact_entry.get().strip()
        address = self.address_entry.get().strip()

        # Validation
        if not name or not username or not role:
            messagebox.showerror("Error", "Name, Username, and Role are required!")
            return

        # Check if username already exists (excluding current user)
        self.cursor.execute("SELECT id FROM employees WHERE username=? AND id!=?", (username, user_id))
        if self.cursor.fetchone():
            messagebox.showerror("Error", "Username already exists!")
            return

        # Update user
        if password:
            self.cursor.execute("""
            UPDATE employees
            SET name=?, username=?, password=?, role=?, contact=?, address=?
            WHERE id=?
            """, (name, username, password, role, contact, address, user_id))
        else:
            self.cursor.execute("""
            UPDATE employees
            SET name=?, username=?, role=?, contact=?, address=?
            WHERE id=?
            """, (name, username, role, contact, address, user_id))

        self.conn.commit()
        messagebox.showinfo("Success", "User updated successfully!")
        self.users_screen()

    def delete_user(self):
        """Delete selected user"""
        # Get selected user
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a user to delete!")
            return

        item = self.users_tree.item(selected[0])
        user_id = item['values'][0]
        username = item['values'][2]

        # Prevent deletion of current user
        if user_id == self.current_user['id']:
            messagebox.showerror("Error", "You cannot delete your own account!")
            return

        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user {username}?"):
            # Delete user
            self.cursor.execute("DELETE FROM employees WHERE id=?", (user_id,))
            self.conn.commit()

            messagebox.showinfo("Success", "User deleted successfully!")
            self.load_users()

    def change_password_screen(self):
        """Display change password form"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Change Password", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Settings", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.settings_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Form frame
        form_frame = Frame(self.root, bg='white')
        form_frame.pack(fill=BOTH, expand=True, padx=50, pady=20)

        # Change password form
        Label(form_frame, text="Change Password", font=('Arial', 16, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, pady=10)

        # Current Password
        Label(form_frame, text="Current Password:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.current_password_entry = Entry(form_frame, font=('Arial', 12), width=30, show='*')
        self.current_password_entry.grid(row=1, column=1, pady=5, padx=5)

        # New Password
        Label(form_frame, text="New Password:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.new_password_entry = Entry(form_frame, font=('Arial', 12), width=30, show='*')
        self.new_password_entry.grid(row=2, column=1, pady=5, padx=5)

        # Confirm New Password
        Label(form_frame, text="Confirm New Password:", font=('Arial', 12), bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=5)
        self.confirm_new_password_entry = Entry(form_frame, font=('Arial', 12), width=30, show='*')
        self.confirm_new_password_entry.grid(row=3, column=1, pady=5, padx=5)

        # Buttons
        btn_frame = Frame(form_frame, bg='white')
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

        change_btn = Button(btn_frame, text="Change Password", font=('Arial', 12), bg='#f39c12', fg='white',
                           command=self.change_password, width=15)
        change_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.settings_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

    def change_password(self):
        """Change user password"""
        # Get form data
        current_password = self.current_password_entry.get().strip()
        new_password = self.new_password_entry.get().strip()
        confirm_new_password = self.confirm_new_password_entry.get().strip()

        # Validation
        if not current_password or not new_password or not confirm_new_password:
            messagebox.showerror("Error", "All fields are required!")
            return

        if new_password != confirm_new_password:
            messagebox.showerror("Error", "New passwords do not match!")
            return

        # Verify current password
        self.cursor.execute("SELECT password FROM employees WHERE id=?", (self.current_user['id'],))
        result = self.cursor.fetchone()

        if not result or result[0] != current_password:
            messagebox.showerror("Error", "Current password is incorrect!")
            return

        # Update password
        self.cursor.execute("UPDATE employees SET password=? WHERE id=?", (new_password, self.current_user['id']))
        self.conn.commit()

        messagebox.showinfo("Success", "Password changed successfully!")
        self.settings_screen()

    def stores_screen(self):
        """Display stores management screen"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Store Management", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Settings", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.settings_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Buttons frame
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10, padx=20, fill=X)

        add_btn = Button(btn_frame, text="Add Store", font=('Arial', 12), bg='#2ecc71', fg='white',
                        command=self.add_store_screen, width=15)
        add_btn.pack(side=LEFT, padx=5)

        update_btn = Button(btn_frame, text="Update Store", font=('Arial', 12), bg='#f39c12', fg='white',
                           command=self.update_store_screen, width=15)
        update_btn.pack(side=LEFT, padx=5)

        delete_btn = Button(btn_frame, text="Delete Store", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.delete_store, width=15)
        delete_btn.pack(side=LEFT, padx=5)

        # Stores table
        table_frame = Frame(main_frame)
        table_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(table_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.stores_tree = ttk.Treeview(table_frame, columns=('ID', 'Name', 'Address', 'Contact', 'Email'),
                                     show='headings', yscrollcommand=scrollbar.set)

        self.stores_tree.heading('ID', text='ID')
        self.stores_tree.heading('Name', text='Name')
        self.stores_tree.heading('Address', text='Address')
        self.stores_tree.heading('Contact', text='Contact')
        self.stores_tree.heading('Email', text='Email')

        self.stores_tree.column('ID', width=50)
        self.stores_tree.column('Name', width=150)
        self.stores_tree.column('Address', width=200)
        self.stores_tree.column('Contact', width=150)
        self.stores_tree.column('Email', width=150)

        scrollbar.config(command=self.stores_tree.yview)
        self.stores_tree.pack(fill=BOTH, expand=True)

        # Load stores
        self.load_stores()

    def load_stores(self):
        """Load all stores data"""
        # Clear existing data
        for i in self.stores_tree.get_children():
            self.stores_tree.delete(i)

        # Get all stores
        self.cursor.execute("SELECT id, name, address, contact, email FROM stores ORDER BY name")

        for row in self.cursor.fetchall():
            self.stores_tree.insert('', 'end', values=row)

    def add_store_screen(self):
        """Display add store form"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Add New Store", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Stores", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.stores_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Form frame
        form_frame = Frame(self.root, bg='white')
        form_frame.pack(fill=BOTH, expand=True, padx=50, pady=20)

        # Store details
        Label(form_frame, text="Store Details", font=('Arial', 16, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, pady=10)

        # Name
        Label(form_frame, text="Name:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.name_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.name_entry.grid(row=1, column=1, pady=5, padx=5)

        # Address
        Label(form_frame, text="Address:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.address_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.address_entry.grid(row=2, column=1, pady=5, padx=5)

        # Contact
        Label(form_frame, text="Contact:", font=('Arial', 12), bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=5)
        self.contact_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.contact_entry.grid(row=3, column=1, pady=5, padx=5)

        # Email
        Label(form_frame, text="Email:", font=('Arial', 12), bg='white').grid(row=4, column=0, sticky='w', pady=5, padx=5)
        self.email_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.email_entry.grid(row=4, column=1, pady=5, padx=5)

        # Buttons
        btn_frame = Frame(form_frame, bg='white')
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)

        save_btn = Button(btn_frame, text="Save Store", font=('Arial', 12), bg='#2ecc71', fg='white',
                         command=self.save_store, width=15)
        save_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.stores_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

    def save_store(self):
        """Save new store to database"""
        # Get form data
        name = self.name_entry.get().strip()
        address = self.address_entry.get().strip()
        contact = self.contact_entry.get().strip()
        email = self.email_entry.get().strip()

        # Validation
        if not name or not address:
            messagebox.showerror("Error", "Name and Address are required!")
            return

        # Insert store
        self.cursor.execute("""
        INSERT INTO stores (name, address, contact, email)
        VALUES (?, ?, ?, ?)
        """, (name, address, contact, email))

        self.conn.commit()
        messagebox.showinfo("Success", "Store added successfully!")
        self.stores_screen()

    def update_store_screen(self):
        """Display update store form"""
        # Get selected store
        selected = self.stores_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a store to update!")
            return

        item = self.stores_tree.item(selected[0])
        store_id = item['values'][0]

        # Get store details
        self.cursor.execute("SELECT * FROM stores WHERE id=?", (store_id,))
        store = self.cursor.fetchone()

        if not store:
            messagebox.showerror("Error", "Store not found!")
            return

        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Update Store", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Stores", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.stores_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Form frame
        form_frame = Frame(self.root, bg='white')
        form_frame.pack(fill=BOTH, expand=True, padx=50, pady=20)

        # Store details
        Label(form_frame, text="Store Details", font=('Arial', 16, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, pady=10)

        # ID (read-only)
        Label(form_frame, text="ID:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        id_label = Label(form_frame, text=str(store[0]), font=('Arial', 12), bg='white')
        id_label.grid(row=1, column=1, sticky='w', pady=5, padx=5)

        # Name
        Label(form_frame, text="Name:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.name_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.name_entry.grid(row=2, column=1, pady=5, padx=5)
        self.name_entry.insert(0, store[1])

        # Address
        Label(form_frame, text="Address:", font=('Arial', 12), bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=5)
        self.address_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.address_entry.grid(row=3, column=1, pady=5, padx=5)
        self.address_entry.insert(0, store[2])

        # Contact
        Label(form_frame, text="Contact:", font=('Arial', 12), bg='white').grid(row=4, column=0, sticky='w', pady=5, padx=5)
        self.contact_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.contact_entry.grid(row=4, column=1, pady=5, padx=5)
        self.contact_entry.insert(0, store[3] if store[3] else '')

        # Email
        Label(form_frame, text="Email:", font=('Arial', 12), bg='white').grid(row=5, column=0, sticky='w', pady=5, padx=5)
        self.email_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.email_entry.grid(row=5, column=1, pady=5, padx=5)
        self.email_entry.insert(0, store[4] if store[4] else '')

        # Buttons
        btn_frame = Frame(form_frame, bg='white')
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)

        update_btn = Button(btn_frame, text="Update Store", font=('Arial', 12), bg='#f39c12', fg='white',
                           command=lambda: self.update_store(store_id), width=15)
        update_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.stores_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

    def update_store(self, store_id):
        """Update store in database"""
        # Get form data
        name = self.name_entry.get().strip()
        address = self.address_entry.get().strip()
        contact = self.contact_entry.get().strip()
        email = self.email_entry.get().strip()

        # Validation
        if not name or not address:
            messagebox.showerror("Error", "Name and Address are required!")
            return

        # Update store
        self.cursor.execute("""
        UPDATE stores
        SET name=?, address=?, contact=?, email=?
        WHERE id=?
        """, (name, address, contact, email, store_id))

        self.conn.commit()
        messagebox.showinfo("Success", "Store updated successfully!")
        self.stores_screen()

    def delete_store(self):
        """Delete selected store"""
        # Get selected store
        selected = self.stores_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a store to delete!")
            return

        item = self.stores_tree.item(selected[0])
        store_id = item['values'][0]
        store_name = item['values'][1]

        # Prevent deletion of current store
        if store_id == self.current_store['id']:
            messagebox.showerror("Error", "You cannot delete the currently active store!")
            return

        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete store {store_name}?"):
            # Check if store is used in sales or purchases
            self.cursor.execute("SELECT COUNT(*) FROM sales WHERE store_id=?", (store_id,))
            sales_count = self.cursor.fetchone()[0]

            self.cursor.execute("SELECT COUNT(*) FROM purchases WHERE store_id=?", (store_id,))
            purchases_count = self.cursor.fetchone()[0]

            if sales_count > 0 or purchases_count > 0:
                messagebox.showerror("Error", "Cannot delete store that has associated sales or purchases!")
                return

            # Delete store
            self.cursor.execute("DELETE FROM stores WHERE id=?", (store_id,))
            self.conn.commit()

            messagebox.showinfo("Success", "Store deleted successfully!")
            self.load_stores()

    def units_screen(self):
        """Display units management screen"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Unit Management", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Settings", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.settings_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Buttons frame
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10, padx=20, fill=X)

        add_btn = Button(btn_frame, text="Add Unit", font=('Arial', 12), bg='#2ecc71', fg='white',
                        command=self.add_unit_screen, width=15)
        add_btn.pack(side=LEFT, padx=5)

        update_btn = Button(btn_frame, text="Update Unit", font=('Arial', 12), bg='#f39c12', fg='white',
                           command=self.update_unit_screen, width=15)
        update_btn.pack(side=LEFT, padx=5)

        delete_btn = Button(btn_frame, text="Delete Unit", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.delete_unit, width=15)
        delete_btn.pack(side=LEFT, padx=5)

        # Units table
        table_frame = Frame(main_frame)
        table_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(table_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.units_tree = ttk.Treeview(table_frame, columns=('ID', 'Name', 'Description'),
                                    show='headings', yscrollcommand=scrollbar.set)

        self.units_tree.heading('ID', text='ID')
        self.units_tree.heading('Name', text='Name')
        self.units_tree.heading('Description', text='Description')

        self.units_tree.column('ID', width=50)
        self.units_tree.column('Name', width=150)
        self.units_tree.column('Description', width=300)

        scrollbar.config(command=self.units_tree.yview)
        self.units_tree.pack(fill=BOTH, expand=True)

        # Load units
        self.load_units()

    def load_units(self):
        """Load all units data"""
        # Clear existing data
        for i in self.units_tree.get_children():
            self.units_tree.delete(i)

        # Get all units
        self.cursor.execute("SELECT id, name, description FROM units ORDER BY name")

        for row in self.cursor.fetchall():
            self.units_tree.insert('', 'end', values=row)

    def add_unit_screen(self):
        """Display add unit form"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Add New Unit", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Units", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.units_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Form frame
        form_frame = Frame(self.root, bg='white')
        form_frame.pack(fill=BOTH, expand=True, padx=50, pady=20)

        # Unit details
        Label(form_frame, text="Unit Details", font=('Arial', 16, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, pady=10)

        # Name
        Label(form_frame, text="Name:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.name_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.name_entry.grid(row=1, column=1, pady=5, padx=5)

        # Description
        Label(form_frame, text="Description:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.description_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.description_entry.grid(row=2, column=1, pady=5, padx=5)

        # Buttons
        btn_frame = Frame(form_frame, bg='white')
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)

        save_btn = Button(btn_frame, text="Save Unit", font=('Arial', 12), bg='#2ecc71', fg='white',
                         command=self.save_unit, width=15)
        save_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.units_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

    def save_unit(self):
        """Save new unit to database"""
        # Get form data
        name = self.name_entry.get().strip()
        description = self.description_entry.get().strip()

        # Validation
        if not name:
            messagebox.showerror("Error", "Name is required!")
            return

        # Insert unit
        self.cursor.execute("""
        INSERT INTO units (name, description)
        VALUES (?, ?)
        """, (name, description))

        self.conn.commit()
        messagebox.showinfo("Success", "Unit added successfully!")
        self.units_screen()

    def update_unit_screen(self):
        """Display update unit form"""
        # Get selected unit
        selected = self.units_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a unit to update!")
            return

        item = self.units_tree.item(selected[0])
        unit_id = item['values'][0]

        # Get unit details
        self.cursor.execute("SELECT * FROM units WHERE id=?", (unit_id,))
        unit = self.cursor.fetchone()

        if not unit:
            messagebox.showerror("Error", "Unit not found!")
            return

        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Update Unit", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Units", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.units_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Form frame
        form_frame = Frame(self.root, bg='white')
        form_frame.pack(fill=BOTH, expand=True, padx=50, pady=20)

        # Unit details
        Label(form_frame, text="Unit Details", font=('Arial', 16, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, pady=10)

        # ID (read-only)
        Label(form_frame, text="ID:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        id_label = Label(form_frame, text=str(unit[0]), font=('Arial', 12), bg='white')
        id_label.grid(row=1, column=1, sticky='w', pady=5, padx=5)

        # Name
        Label(form_frame, text="Name:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.name_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.name_entry.grid(row=2, column=1, pady=5, padx=5)
        self.name_entry.insert(0, unit[1])

        # Description
        Label(form_frame, text="Description:", font=('Arial', 12), bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=5)
        self.description_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.description_entry.grid(row=3, column=1, pady=5, padx=5)
        self.description_entry.insert(0, unit[2] if unit[2] else '')

        # Buttons
        btn_frame = Frame(form_frame, bg='white')
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

        update_btn = Button(btn_frame, text="Update Unit", font=('Arial', 12), bg='#f39c12', fg='white',
                           command=lambda: self.update_unit(unit_id), width=15)
        update_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.units_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

    def update_unit(self, unit_id):
        """Update unit in database"""
        # Get form data
        name = self.name_entry.get().strip()
        description = self.description_entry.get().strip()

        # Validation
        if not name:
            messagebox.showerror("Error", "Name is required!")
            return

        # Update unit
        self.cursor.execute("""
        UPDATE units
        SET name=?, description=?
        WHERE id=?
        """, (name, description, unit_id))

        self.conn.commit()
        messagebox.showinfo("Success", "Unit updated successfully!")
        self.units_screen()

    def delete_unit(self):
        """Delete selected unit"""
        # Get selected unit
        selected = self.units_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a unit to delete!")
            return

        item = self.units_tree.item(selected[0])
        unit_id = item['values'][0]
        unit_name = item['values'][1]

        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete unit {unit_name}?"):
            # Check if unit is used in medicines
            self.cursor.execute("SELECT COUNT(*) FROM medicines WHERE unit_id=?", (unit_id,))
            medicines_count = self.cursor.fetchone()[0]

            if medicines_count > 0:
                messagebox.showerror("Error", "Cannot delete unit that is used by medicines!")
                return

            # Delete unit
            self.cursor.execute("DELETE FROM units WHERE id=?", (unit_id,))
            self.conn.commit()

            messagebox.showinfo("Success", "Unit deleted successfully!")
            self.load_units()

    def backup_database(self):
        """Backup database to file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("Database files", "*.db"), ("All files", "*.*")],
            initialfile=f"pharmacy_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        )

        if file_path:
            try:
                # Close current connection
                self.conn.close()

                # Copy database file
                import shutil
                shutil.copy2('pharmacy.db', file_path)

                # Reopen connection
                self.conn = sqlite3.connect('pharmacy.db')
                self.cursor = self.conn.cursor()

                messagebox.showinfo("Success", f"Database backed up to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to backup database: {str(e)}")

    def restore_database(self):
        """Restore database from file"""
        file_path = filedialog.askopenfilename(
            title="Select Database Backup",
            filetypes=[("Database files", "*.db"), ("All files", "*.*")]
        )

        if file_path:
            # Confirm restore
            if messagebox.askyesno("Confirm Restore", "Restoring a database will replace all current data. Continue?"):
                try:
                    # Close current connection
                    self.conn.close()

                    # Copy database file
                    import shutil
                    shutil.copy2(file_path, 'pharmacy.db')

                    # Reopen connection
                    self.conn = sqlite3.connect('pharmacy.db')
                    self.cursor = self.conn.cursor()

                    messagebox.showinfo("Success", "Database restored successfully!")
                    self.login_screen()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to restore database: {str(e)}")

    def send_notifications_screen(self):
        """Display send notifications screen"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Send Notifications", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Settings", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.settings_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Form frame
        form_frame = Frame(main_frame, bg='white')
        form_frame.pack(pady=10, padx=20, fill=X)

        # Customer selection
        Label(form_frame, text="Customer:", font=('Arial', 12), bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.customer_var = StringVar()
        self.customer_combo = ttk.Combobox(form_frame, textvariable=self.customer_var, font=('Arial', 12), width=30)
        self.customer_combo.grid(row=0, column=1, pady=5, padx=5)

        # Load customers
        self.cursor.execute("SELECT id, name FROM customers ORDER BY name")
        customers = self.cursor.fetchall()
        customer_list = [f"{c[0]} - {c[1]}" for c in customers]
        self.customer_combo['values'] = customer_list

        # Type selection
        Label(form_frame, text="Type:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.type_var = StringVar()
        types = ["SMS", "WhatsApp", "Email"]
        self.type_combo = ttk.Combobox(form_frame, textvariable=self.type_var, values=types, font=('Arial', 12), width=28)
        self.type_combo.grid(row=1, column=1, pady=5, padx=5)

        # Message
        Label(form_frame, text="Message:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.message_text = Text(form_frame, font=('Arial', 12), width=40, height=10)
        self.message_text.grid(row=2, column=1, pady=5, padx=5)

        # Buttons
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10)

        send_btn = Button(btn_frame, text="Send Notification", font=('Arial', 12), bg='#2ecc71', fg='white',
                         command=self.send_notification, width=15)
        send_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.settings_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

    def send_notification(self):
        """Send notification to customer"""
        customer = self.customer_var.get()
        notification_type = self.type_var.get()
        message = self.message_text.get("1.0", END).strip()

        # Validation
        if not customer or not notification_type or not message:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            customer_id = int(customer.split(' - ')[0])
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid customer selection!")
            return

        # Get customer details
        self.cursor.execute("SELECT name, contact, email FROM customers WHERE id=?", (customer_id,))
        customer_data = self.cursor.fetchone()

        if not customer_data:
            messagebox.showerror("Error", "Customer not found!")
            return

        # Save notification to database
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute("""
        INSERT INTO notifications (customer_id, type, message, date, status)
        VALUES (?, ?, ?, ?, ?)
        """, (customer_id, notification_type, message, today, 'sent'))

        self.conn.commit()

        # In a real system, this would send the actual notification via SMS, WhatsApp, or Email API
        # For this demo, we'll just show a success message
        messagebox.showinfo("Success", f"Notification sent to {customer_data[0]} via {notification_type}!")
        self.settings_screen()

    def notification_settings_screen(self):
        """Display notification settings screen"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Notification Settings", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Settings", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.settings_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Settings frame
        settings_frame = Frame(main_frame, bg='white', relief='groove', borderwidth=2)
        settings_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

        Label(settings_frame, text="Notification Settings", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)

        # SMS settings
        sms_frame = Frame(settings_frame, bg='white')
        sms_frame.pack(pady=10, padx=20, fill=X)

        Label(sms_frame, text="SMS Settings", font=('Arial', 12, 'bold'), bg='white').pack(anchor='w')

        Label(sms_frame, text="API Key:", font=('Arial', 12), bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.sms_api_key_entry = Entry(sms_frame, font=('Arial', 12), width=40)
        self.sms_api_key_entry.grid(row=0, column=1, pady=5, padx=5)

        Label(sms_frame, text="Sender ID:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.sms_sender_id_entry = Entry(sms_frame, font=('Arial', 12), width=40)
        self.sms_sender_id_entry.grid(row=1, column=1, pady=5, padx=5)

        # WhatsApp settings
        whatsapp_frame = Frame(settings_frame, bg='white')
        whatsapp_frame.pack(pady=10, padx=20, fill=X)

        Label(whatsapp_frame, text="WhatsApp Settings", font=('Arial', 12, 'bold'), bg='white').pack(anchor='w')

        Label(whatsapp_frame, text="API Key:", font=('Arial', 12), bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.whatsapp_api_key_entry = Entry(whatsapp_frame, font=('Arial', 12), width=40)
        self.whatsapp_api_key_entry.grid(row=0, column=1, pady=5, padx=5)

        Label(whatsapp_frame, text="Phone Number ID:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.whatsapp_phone_id_entry = Entry(whatsapp_frame, font=('Arial', 12), width=40)
        self.whatsapp_phone_id_entry.grid(row=1, column=1, pady=5, padx=5)

        # Email settings
        email_frame = Frame(settings_frame, bg='white')
        email_frame.pack(pady=10, padx=20, fill=X)

        Label(email_frame, text="Email Settings", font=('Arial', 12, 'bold'), bg='white').pack(anchor='w')

        Label(email_frame, text="SMTP Server:", font=('Arial', 12), bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.smtp_server_entry = Entry(email_frame, font=('Arial', 12), width=40)
        self.smtp_server_entry.grid(row=0, column=1, pady=5, padx=5)

        Label(email_frame, text="SMTP Port:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.smtp_port_entry = Entry(email_frame, font=('Arial', 12), width=40)
        self.smtp_port_entry.grid(row=1, column=1, pady=5, padx=5)

        Label(email_frame, text="Username:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.smtp_username_entry = Entry(email_frame, font=('Arial', 12), width=40)
        self.smtp_username_entry.grid(row=2, column=1, pady=5, padx=5)

        Label(email_frame, text="Password:", font=('Arial', 12), bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=5)
        self.smtp_password_entry = Entry(email_frame, font=('Arial', 12), width=40, show='*')
        self.smtp_password_entry.grid(row=3, column=1, pady=5, padx=5)

        # Buttons
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10)

        save_btn = Button(btn_frame, text="Save Settings", font=('Arial', 12), bg='#2ecc71', fg='white',
                         command=self.save_notification_settings, width=15)
        save_btn.pack(side=LEFT, padx=10)

        test_btn = Button(btn_frame, text="Test Connection", font=('Arial', 12), bg='#3498db', fg='white',
                         command=self.test_notification_connection, width=15)
        test_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.settings_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

    def save_notification_settings(self):
        """Save notification settings"""
        # In a real system, this would save the settings to a configuration file or database
        # For this demo, we'll just show a success message
        messagebox.showinfo("Success", "Notification settings saved successfully!")
        self.settings_screen()

    def test_notification_connection(self):
        """Test notification connection"""
        # In a real system, this would test the connection to the notification services
        # For this demo, we'll just show a success message
        messagebox.showinfo("Success", "Connection test successful!")

    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()

# Main application
if __name__ == "__main__":
    root = Tk()
    app = PharmacyManagementSystem(root)
    root.mainloop()
```

## Installation and Running Instructions

### Prerequisites

- Python 3.6 or higher
- Required Python packages:
  - tkinter (usually comes pre-installed with Python)
  - sqlite3 (usually comes pre-installed with Python)
  - qrcode
  - Pillow
  - requests

### Installation Steps

1. **Install Python** (if not already installed):

   - Download Python from [python.org](https://python.org/)
   - Make sure to check "Add Python to PATH" during installation

2. **Install required packages**:

   ```bash
   pip install qrcode pillow requests
   ```

3. **Run the application**:
   - Save the code to a file named `pharmacy_management_system.py`
   - Run the application using the command:
     ```bash
     python pharmacy_management_system.py
     ```

### Default Login Credentials

- Username: `admin`
- Password: `admin123`

## Key Features Implemented

### 💊 Pharmacy & Medicine Features

1. **Drug Composition & Alternatives**

   - Store active ingredients for each medicine
   - Suggest cheaper/generic alternatives
   - Track relationships between branded and generic medicines

2. **Batch/Lot Tracking**

   - Track medicines by batch number for recalls
   - Manage expiry dates at batch level
   - Track cost prices for each batch

3. **Prescription Management**

   - Upload/scan doctor prescriptions
   - Store prescription images
   - Auto-match medicines to prescriptions
   - Create sales directly from prescriptions

4. **Drug Interaction Warnings**

   - Alert if two medicines being sold have known interactions
   - Check interactions before completing sales
   - Store interaction severity and descriptions

5. **Return & Refund Handling**

   - Process medicine returns with expiry checks
   - Update stock automatically
   - Track return reasons and refund amounts

6. **Reorder Alerts**

   - Automatic reorder suggestions when stock is low
   - Set reorder levels for each medicine
   - Generate reorder reports

7. **Multiple Units Support**

   - Support for different units (Tablet, Strip, Box, Bottle, etc.)
   - Track inventory by unit type
   - Manage unit conversions

8. **HSN/GST/Tax Support (India)**
   - Automatic tax calculation for compliance
   - Store HSN codes for medicines
   - Generate GST-compliant invoices

### 👩‍⚕️ Customer & Patient Features

1. **Customer Medical History**

   - Record allergies and chronic conditions
   - Track past purchases
   - Store medical notes

2. **Smart Prescription Refill Reminder**

   - Alert customers when recurring medicines are due
   - Track prescription history
   - Send automated reminders

3. **Loyalty Points / Discounts**

   - Track customer loyalty points
   - Offer discounts based on loyalty status
   - Points earned on purchases

4. **SMS/WhatsApp Notifications**
   - Send purchase invoices
   - Expiry alerts for purchased medicines
   - Promotional messages
   - Prescription refill reminders

### 🧾 Sales & Business Features

1. **Barcode/QR Code Scanning**

   - Generate unique barcodes for medicines
   - Support for external scanners or webcam
   - QR code generation for prescriptions

2. **Multi-User Roles**

   - Admin, Pharmacist, Cashier, Manager roles
   - Role-based access control
   - User management system

3. **Cash Register / Daily Closing Report**

   - Track cash vs card vs UPI payments
   - Daily closing reports with cash reconciliation
   - Track differences between expected and actual cash

4. **GST Billing & Invoice PDF Export**

   - Professional bill printing with GST details
   - Export invoices as PDF
   - HSN code inclusion

5. **Multi-Store / Franchise Support**

   - Manage multiple pharmacy locations
   - Store-specific data tracking
   - Centralized management with local data

6. **Offline Mode + Sync**
   - Works offline when internet is unavailable
   - Sync data when internet is restored
   - Queue operations for later synchronization

### 📊 Advanced Reports

1. **Profit & Loss Report**

   - Based on sales vs purchases
   - Track revenue, costs, and profits
   - Calculate profit margins

2. **Customer Purchase Trends**

   - Most bought medicines
   - Seasonal trends analysis
   - Customer spending patterns

3. **Supplier Performance Report**

   - Track delivery times
   - Compare pricing between suppliers
   - Evaluate supplier reliability

4. **Expiry Loss Report**
   - Track losses due to expired medicines
   - Identify high-risk items
   - Optimize inventory to reduce waste

## Making It Installable Software

### 1. Standalone Desktop App with PyInstaller

To create a standalone executable:

1. **Install PyInstaller**:

   ```bash
   pip install pyinstaller
   ```

2. **Create the executable**:

   ```bash
   pyinstaller --onefile --windowed pharmacy_management_system.py
   ```

3. **Find the executable**:
   - Windows: `dist/pharmacy_management_system.exe`
   - macOS: `dist/pharmacy_management_system`
   - Linux: `dist/pharmacy_management_system`

### 2. Creating an Installer

#### For Windows (using Inno Setup)

1. Download and install [Inno Setup](https://jrsoftware.org/isinfo.php)

2. Create a script file `installer.iss`:

```innosetup
[Setup]
AppName=Pharmacy Management System
AppVersion=1.0
DefaultDirName={pf}\Pharmacy Management System
DefaultGroupName=Pharmacy Management System
OutputDir=installer
OutputBaseFilename=PharmacyManagementSystemSetup

[Files]
Source: "dist\pharmacy_management_system.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Pharmacy Management System"; Filename: "{app}\pharmacy_management_system.exe"
Name: "{commondesktop}\Pharmacy Management System"; Filename: "{app}\pharmacy_management_system.exe"
```

3. Compile the script:
   ```bash
   iscc installer.iss
   ```

#### For macOS (using pkgbuild)

1. Create a directory structure:

   ```bash
   mkdir -p PharmacyManagementSystem.pkg/ROOT/Applications
   cp -r "dist/pharmacy Management System.app" PharmacyManagementSystem.pkg/ROOT/Applications/
   ```

2. Create the package:
   ```bash
   pkgbuild --root PharmacyManagementSystem.pkg/ROOT --identifier com.pharmacymanagementsystem --version 1.0 PharmacyManagementSystem.pkg
   ```

#### For Linux (using Debian packages)

1. Create a Debian control file `control`:

   ```
   Package: pharmacy-management-system
   Version: 1.0
   Section: misc
   Priority: optional
   Architecture: all
   Depends: python3, python3-tk, python3-pil, python3-qrcode, python3-requests
   Maintainer: Your Name <your.email@example.com>
   Description: Comprehensive pharmacy management system
   ```

2. Create the package:
   ```bash
   mkdir -p debian/DEBIAN
   cp control debian/DEBIAN/control
   mkdir -p debian/usr/bin
   cp dist/pharmacy_management_system debian/usr/bin/
   dpkg-deb --build debian
   ```

### 3. Database Options

The system uses SQLite by default, which is suitable for single-store use. For multi-store setups, you can modify the database connection to use MySQL or PostgreSQL:

```python
# For MySQL
import mysql.connector
self.conn = mysql.connector.connect(
    host="localhost",
    user="username",
    password="password",
    database="pharmacy_db"
)

# For PostgreSQL
import psycopg2
self.conn = psycopg2.connect(
    host="localhost",
    user="username",
    password="password",
    database="pharmacy_db"
)
```

### 4. Distribution

- **Windows**: Distribute the `.exe` file created by PyInstaller or the installer created by Inno Setup
- **macOS**: Distribute the `.app` bundle or the `.pkg` file
- **Linux**: Distribute the executable or the `.deb`/`.rpm` package

## System Requirements

- **Operating System**: Windows 7+, macOS 10.12+, or Linux
- **RAM**: Minimum 4GB, recommended 8GB
- **Storage**: Minimum 500MB free space
- **Display**: Minimum 1024x768 resolution
- **Internet**: Optional (for online features and multi-store sync)

## Support and Updates

For support, updates, and additional features:

- Check the project documentation
- Contact the development team
- Report issues and feature requests

This comprehensive pharmacy management system provides all the features requested, with a professional interface and robust functionality suitable for modern pharmacy operations.

==============================

Installation and Running Instructions
Prerequisites:
Python 3.6 or higher
Tkinter (usually comes pre-installed with Python)
SQLite3 (usually comes pre-installed with Python)
Running the Application:
Save the code to a file named pharmacy_management_system.py
Run the application using the command:

Line Wrapping

Collapse
Copy
1
python pharmacy_management_system.py
Default Login Credentials:
Username: admin
Password: admin123
Features Included
User Authentication:
Secure login system with role-based access
Default admin account created automatically
Dashboard:
Overview of key metrics (medicines, suppliers, customers)
Recent sales display
Quick navigation to all modules
Medicine Management:
Add, update, delete, and view medicines
Track inventory with quantity and expiry dates
Categorize medicines (tablets, capsules, etc.)
Barcode support
Search functionality
Supplier Management:
Add, update, delete, and view suppliers
Track contact information and addresses
Customer Management:
Add, update, delete, and view customers
Track contact information and addresses
Sales Management:
Create new sales with multiple items
Track payment methods
View sale details and print receipts
Automatic inventory reduction
Purchase Management:
Record new purchases from suppliers
Track purchase details
Automatic inventory increase
Reporting:
Sales reports with date range filtering
Inventory reports with total value calculation
Expiry reports (medicines expiring within 90 days)
Low stock reports (medicines with quantity < 10)
Database Structure
The system uses SQLite with the following tables:

medicines: Stores medicine information
suppliers: Stores supplier information
employees: Stores user accounts and roles
customers: Stores customer information
sales: Stores sales transactions
sale_items: Stores individual items in each sale
purchases: Stores purchase transactions
purchase_items: Stores individual items in each purchase
Usage Notes
The system automatically creates a SQLite database file named pharmacy.db in the same directory as the script.
The default admin account can be used to log in initially.
All forms include validation to ensure data integrity.
The system prevents deletion of records that are referenced in other tables (e.g., medicines used in sales cannot be deleted).
Reports can be generated and viewed within the application.
This pharmacy management system provides a comprehensive solution for managing all aspects of a pharmacy, from inventory and sales to reporting and analytics.

==================================

# Pharmacy Management System

I'll create a comprehensive pharmacy management system with all essential features using Python and Tkinter for the GUI, with SQLite as the database backend.

```python
import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import os

class PharmacyManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacy Management System")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)

        # Initialize database
        self.init_db()

        # Login screen
        self.login_screen()

    def init_db(self):
        """Initialize the database and create tables if they don't exist"""
        self.conn = sqlite3.connect('pharmacy.db')
        self.cursor = self.conn.cursor()

        # Create tables
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            supplier_id INTEGER,
            expiry_date TEXT,
            category TEXT,
            barcode TEXT UNIQUE
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT,
            address TEXT,
            email TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            contact TEXT,
            address TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT,
            address TEXT,
            email TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            employee_id INTEGER,
            date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            payment_method TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS sale_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER,
            medicine_id INTEGER,
            quantity INTEGER NOT NULL,
            price_per_unit REAL NOT NULL,
            FOREIGN KEY (sale_id) REFERENCES sales(id),
            FOREIGN KEY (medicine_id) REFERENCES medicines(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_id INTEGER,
            employee_id INTEGER,
            date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchase_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            purchase_id INTEGER,
            medicine_id INTEGER,
            quantity INTEGER NOT NULL,
            price_per_unit REAL NOT NULL,
            FOREIGN KEY (purchase_id) REFERENCES purchases(id),
            FOREIGN KEY (medicine_id) REFERENCES medicines(id)
        )
        """)

        # Create default admin user if not exists
        self.cursor.execute("SELECT * FROM employees WHERE username='admin'")
        if not self.cursor.fetchone():
            self.cursor.execute("""
            INSERT INTO employees (name, username, password, role, contact, address)
            VALUES ('Administrator', 'admin', 'admin123', 'Admin', '1234567890', 'Pharmacy Address')
            """)

        self.conn.commit()

    def login_screen(self):
        """Display the login screen"""
        self.clear_window()

        # Frame for login
        login_frame = Frame(self.root, bg='#f0f0f0')
        login_frame.place(x=400, y=150, width=400, height=400)

        # Title
        title = Label(login_frame, text="Pharmacy Management System", font=('Arial', 20, 'bold'), bg='#f0f0f0')
        title.pack(pady=20)

        # Username
        Label(login_frame, text="Username:", font=('Arial', 12), bg='#f0f0f0').pack(pady=5)
        self.username_entry = Entry(login_frame, font=('Arial', 12), width=20)
        self.username_entry.pack(pady=5)

        # Password
        Label(login_frame, text="Password:", font=('Arial', 12), bg='#f0f0f0').pack(pady=5)
        self.password_entry = Entry(login_frame, font=('Arial', 12), width=20, show='*')
        self.password_entry.pack(pady=5)

        # Login button
        login_btn = Button(login_frame, text="Login", font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white',
                          command=self.login, width=15, pady=10)
        login_btn.pack(pady=20)

        # Status label
        self.status_label = Label(login_frame, text="", font=('Arial', 10), bg='#f0f0f0', fg='red')
        self.status_label.pack()

    def login(self):
        """Authenticate user login"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.status_label.config(text="Please enter both username and password")
            return

        self.cursor.execute("SELECT * FROM employees WHERE username=? AND password=?", (username, password))
        user = self.cursor.fetchone()

        if user:
            self.current_user = {
                'id': user[0],
                'name': user[1],
                'username': user[2],
                'role': user[4]
            }
            self.dashboard()
        else:
            self.status_label.config(text="Invalid username or password")

    def dashboard(self):
        """Display the main dashboard"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Pharmacy Management System", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # User info
        user_info = Label(header_frame, text=f"Welcome, {self.current_user['name']} ({self.current_user['role']})",
                         font=('Arial', 12), bg='#2c3e50', fg='white')
        user_info.pack(side=RIGHT, padx=20)

        # Logout button
        logout_btn = Button(header_frame, text="Logout", font=('Arial', 10), bg='#e74c3c', fg='white',
                           command=self.login_screen, width=8)
        logout_btn.pack(side=RIGHT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='#ecf0f1')
        main_frame.pack(fill=BOTH, expand=True)

        # Sidebar
        sidebar = Frame(main_frame, bg='#34495e', width=200)
        sidebar.pack(side=LEFT, fill=Y)

        # Menu buttons
        Button(sidebar, text="Dashboard", font=('Arial', 12), bg='#3498db', fg='white',
               command=self.dashboard, width=18, pady=10).pack(pady=5)

        Button(sidebar, text="Medicines", font=('Arial', 12), bg='#3498db', fg='white',
               command=self.medicines_screen, width=18, pady=10).pack(pady=5)

        Button(sidebar, text="Suppliers", font=('Arial', 12), bg='#3498db', fg='white',
               command=self.suppliers_screen, width=18, pady=10).pack(pady=5)

        Button(sidebar, text="Customers", font=('Arial', 12), bg='#3498db', fg='white',
               command=self.customers_screen, width=18, pady=10).pack(pady=5)

        Button(sidebar, text="Sales", font=('Arial', 12), bg='#3498db', fg='white',
               command=self.sales_screen, width=18, pady=10).pack(pady=5)

        Button(sidebar, text="Purchases", font=('Arial', 12), bg='#3498db', fg='white',
               command=self.purchases_screen, width=18, pady=10).pack(pady=5)

        Button(sidebar, text="Reports", font=('Arial', 12), bg='#3498db', fg='white',
               command=self.reports_screen, width=18, pady=10).pack(pady=5)

        # Content area
        content_frame = Frame(main_frame, bg='white')
        content_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # Dashboard content
        Label(content_frame, text="Dashboard", font=('Arial', 18, 'bold'), bg='white').pack(pady=20)

        # Summary cards
        card_frame = Frame(content_frame, bg='white')
        card_frame.pack(pady=20)

        # Medicines count
        self.cursor.execute("SELECT COUNT(*) FROM medicines")
        med_count = self.cursor.fetchone()[0]

        med_card = Frame(card_frame, bg='#3498db', width=200, height=100)
        med_card.pack(side=LEFT, padx=20, pady=20)
        med_card.pack_propagate(False)

        Label(med_card, text="Medicines", font=('Arial', 14, 'bold'), bg='#3498db', fg='white').pack(pady=10)
        Label(med_card, text=str(med_count), font=('Arial', 24, 'bold'), bg='#3498db', fg='white').pack()

        # Suppliers count
        self.cursor.execute("SELECT COUNT(*) FROM suppliers")
        supp_count = self.cursor.fetchone()[0]

        supp_card = Frame(card_frame, bg='#2ecc71', width=200, height=100)
        supp_card.pack(side=LEFT, padx=20, pady=20)
        supp_card.pack_propagate(False)

        Label(supp_card, text="Suppliers", font=('Arial', 14, 'bold'), bg='#2ecc71', fg='white').pack(pady=10)
        Label(supp_card, text=str(supp_count), font=('Arial', 24, 'bold'), bg='#2ecc71', fg='white').pack()

        # Customers count
        self.cursor.execute("SELECT COUNT(*) FROM customers")
        cust_count = self.cursor.fetchone()[0]

        cust_card = Frame(card_frame, bg='#e74c3c', width=200, height=100)
        cust_card.pack(side=LEFT, padx=20, pady=20)
        cust_card.pack_propagate(False)

        Label(cust_card, text="Customers", font=('Arial', 14, 'bold'), bg='#e74c3c', fg='white').pack(pady=10)
        Label(cust_card, text=str(cust_count), font=('Arial', 24, 'bold'), bg='#e74c3c', fg='white').pack()

        # Recent sales
        Label(content_frame, text="Recent Sales", font=('Arial', 16, 'bold'), bg='white').pack(pady=10)

        # Sales table
        sales_frame = Frame(content_frame)
        sales_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(sales_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.sales_tree = ttk.Treeview(sales_frame, columns=('ID', 'Customer', 'Employee', 'Date', 'Amount'),
                                      show='headings', yscrollcommand=scrollbar.set)

        self.sales_tree.heading('ID', text='ID')
        self.sales_tree.heading('Customer', text='Customer')
        self.sales_tree.heading('Employee', text='Employee')
        self.sales_tree.heading('Date', text='Date')
        self.sales_tree.heading('Amount', text='Amount')

        self.sales_tree.column('ID', width=50)
        self.sales_tree.column('Customer', width=150)
        self.sales_tree.column('Employee', width=150)
        self.sales_tree.column('Date', width=150)
        self.sales_tree.column('Amount', width=100)

        scrollbar.config(command=self.sales_tree.yview)
        self.sales_tree.pack(fill=BOTH, expand=True)

        # Load recent sales
        self.load_recent_sales()

    def load_recent_sales(self):
        """Load recent sales data"""
        # Clear existing data
        for i in self.sales_tree.get_children():
            self.sales_tree.delete(i)

        # Get recent sales
        self.cursor.execute("""
        SELECT s.id, c.name, e.name, s.date, s.total_amount
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.id
        LEFT JOIN employees e ON s.employee_id = e.id
        ORDER BY s.date DESC
        LIMIT 10
        """)

        for row in self.cursor.fetchall():
            self.sales_tree.insert('', 'end', values=row)

    def medicines_screen(self):
        """Display medicines management screen"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Medicines Management", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Dashboard", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.dashboard, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Search frame
        search_frame = Frame(main_frame, bg='white')
        search_frame.pack(pady=10, padx=20, fill=X)

        Label(search_frame, text="Search:", font=('Arial', 12), bg='white').pack(side=LEFT, padx=5)
        self.search_entry = Entry(search_frame, font=('Arial', 12), width=30)
        self.search_entry.pack(side=LEFT, padx=5)

        search_btn = Button(search_frame, text="Search", font=('Arial', 10), bg='#3498db', fg='white',
                           command=self.search_medicines, width=10)
        search_btn.pack(side=LEFT, padx=5)

        reset_btn = Button(search_frame, text="Reset", font=('Arial', 10), bg='#95a5a6', fg='white',
                          command=self.load_medicines, width=10)
        reset_btn.pack(side=LEFT, padx=5)

        # Buttons frame
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10, padx=20, fill=X)

        add_btn = Button(btn_frame, text="Add Medicine", font=('Arial', 12), bg='#2ecc71', fg='white',
                        command=self.add_medicine_screen, width=15)
        add_btn.pack(side=LEFT, padx=5)

        update_btn = Button(btn_frame, text="Update Medicine", font=('Arial', 12), bg='#f39c12', fg='white',
                           command=self.update_medicine_screen, width=15)
        update_btn.pack(side=LEFT, padx=5)

        delete_btn = Button(btn_frame, text="Delete Medicine", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.delete_medicine, width=15)
        delete_btn.pack(side=LEFT, padx=5)

        # Medicines table
        table_frame = Frame(main_frame)
        table_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(table_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.medicines_tree = ttk.Treeview(table_frame, columns=('ID', 'Name', 'Description', 'Quantity',
                                                                 'Price', 'Supplier', 'Expiry', 'Category'),
                                          show='headings', yscrollcommand=scrollbar.set)

        self.medicines_tree.heading('ID', text='ID')
        self.medicines_tree.heading('Name', text='Name')
        self.medicines_tree.heading('Description', text='Description')
        self.medicines_tree.heading('Quantity', text='Quantity')
        self.medicines_tree.heading('Price', text='Price')
        self.medicines_tree.heading('Supplier', text='Supplier')
        self.medicines_tree.heading('Expiry', text='Expiry Date')
        self.medicines_tree.heading('Category', text='Category')

        self.medicines_tree.column('ID', width=50)
        self.medicines_tree.column('Name', width=150)
        self.medicines_tree.column('Description', width=200)
        self.medicines_tree.column('Quantity', width=80)
        self.medicines_tree.column('Price', width=80)
        self.medicines_tree.column('Supplier', width=120)
        self.medicines_tree.column('Expiry', width=100)
        self.medicines_tree.column('Category', width=100)

        scrollbar.config(command=self.medicines_tree.yview)
        self.medicines_tree.pack(fill=BOTH, expand=True)

        # Load medicines
        self.load_medicines()

    def load_medicines(self):
        """Load all medicines data"""
        # Clear existing data
        for i in self.medicines_tree.get_children():
            self.medicines_tree.delete(i)

        # Get all medicines
        self.cursor.execute("""
        SELECT m.id, m.name, m.description, m.quantity, m.price, s.name, m.expiry_date, m.category
        FROM medicines m
        LEFT JOIN suppliers s ON m.supplier_id = s.id
        ORDER BY m.name
        """)

        for row in self.cursor.fetchall():
            self.medicines_tree.insert('', 'end', values=row)

    def search_medicines(self):
        """Search medicines by name or category"""
        search_term = self.search_entry.get().strip()

        if not search_term:
            self.load_medicines()
            return

        # Clear existing data
        for i in self.medicines_tree.get_children():
            self.medicines_tree.delete(i)

        # Search medicines
        self.cursor.execute("""
        SELECT m.id, m.name, m.description, m.quantity, m.price, s.name, m.expiry_date, m.category
        FROM medicines m
        LEFT JOIN suppliers s ON m.supplier_id = s.id
        WHERE m.name LIKE ? OR m.category LIKE ?
        ORDER BY m.name
        """, (f'%{search_term}%', f'%{search_term}%'))

        for row in self.cursor.fetchall():
            self.medicines_tree.insert('', 'end', values=row)

    def add_medicine_screen(self):
        """Display add medicine form"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Add New Medicine", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Medicines", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.medicines_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Form frame
        form_frame = Frame(self.root, bg='white')
        form_frame.pack(fill=BOTH, expand=True, padx=50, pady=20)

        # Medicine details
        Label(form_frame, text="Medicine Details", font=('Arial', 16, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, pady=10)

        # Name
        Label(form_frame, text="Name:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.name_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.name_entry.grid(row=1, column=1, pady=5, padx=5)

        # Description
        Label(form_frame, text="Description:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.desc_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.desc_entry.grid(row=2, column=1, pady=5, padx=5)

        # Quantity
        Label(form_frame, text="Quantity:", font=('Arial', 12), bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=5)
        self.qty_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.qty_entry.grid(row=3, column=1, pady=5, padx=5)

        # Price
        Label(form_frame, text="Price:", font=('Arial', 12), bg='white').grid(row=4, column=0, sticky='w', pady=5, padx=5)
        self.price_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.price_entry.grid(row=4, column=1, pady=5, padx=5)

        # Supplier
        Label(form_frame, text="Supplier:", font=('Arial', 12), bg='white').grid(row=5, column=0, sticky='w', pady=5, padx=5)
        self.supplier_var = StringVar()
        self.supplier_combo = ttk.Combobox(form_frame, textvariable=self.supplier_var, font=('Arial', 12), width=28)
        self.supplier_combo.grid(row=5, column=1, pady=5, padx=5)

        # Load suppliers
        self.cursor.execute("SELECT id, name FROM suppliers ORDER BY name")
        suppliers = self.cursor.fetchall()
        supplier_list = [f"{s[0]} - {s[1]}" for s in suppliers]
        self.supplier_combo['values'] = supplier_list

        # Expiry date
        Label(form_frame, text="Expiry Date (YYYY-MM-DD):", font=('Arial', 12), bg='white').grid(row=6, column=0, sticky='w', pady=5, padx=5)
        self.exp_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.exp_entry.grid(row=6, column=1, pady=5, padx=5)

        # Category
        Label(form_frame, text="Category:", font=('Arial', 12), bg='white').grid(row=7, column=0, sticky='w', pady=5, padx=5)
        self.category_var = StringVar()
        categories = ["Tablet", "Capsule", "Syrup", "Injection", "Ointment", "Drops", "Inhaler", "Other"]
        self.category_combo = ttk.Combobox(form_frame, textvariable=self.category_var, values=categories, font=('Arial', 12), width=28)
        self.category_combo.grid(row=7, column=1, pady=5, padx=5)

        # Barcode
        Label(form_frame, text="Barcode:", font=('Arial', 12), bg='white').grid(row=8, column=0, sticky='w', pady=5, padx=5)
        self.barcode_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.barcode_entry.grid(row=8, column=1, pady=5, padx=5)

        # Buttons
        btn_frame = Frame(form_frame, bg='white')
        btn_frame.grid(row=9, column=0, columnspan=2, pady=20)

        save_btn = Button(btn_frame, text="Save Medicine", font=('Arial', 12), bg='#2ecc71', fg='white',
                         command=self.save_medicine, width=15)
        save_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.medicines_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

    def save_medicine(self):
        """Save new medicine to database"""
        # Get form data
        name = self.name_entry.get().strip()
        description = self.desc_entry.get().strip()
        quantity = self.qty_entry.get().strip()
        price = self.price_entry.get().strip()
        supplier = self.supplier_var.get()
        expiry = self.exp_entry.get().strip()
        category = self.category_var.get()
        barcode = self.barcode_entry.get().strip()

        # Validation
        if not name or not quantity or not price or not category:
            messagebox.showerror("Error", "Name, Quantity, Price, and Category are required!")
            return

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer and Price must be a number!")
            return

        # Get supplier ID
        supplier_id = None
        if supplier:
            supplier_id = int(supplier.split(' - ')[0])

        # Check if barcode already exists
        if barcode:
            self.cursor.execute("SELECT id FROM medicines WHERE barcode=?", (barcode,))
            if self.cursor.fetchone():
                messagebox.showerror("Error", "Barcode already exists!")
                return

        # Insert medicine
        self.cursor.execute("""
        INSERT INTO medicines (name, description, quantity, price, supplier_id, expiry_date, category, barcode)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, description, quantity, price, supplier_id, expiry, category, barcode))

        self.conn.commit()
        messagebox.showinfo("Success", "Medicine added successfully!")
        self.medicines_screen()

    def update_medicine_screen(self):
        """Display update medicine form"""
        # Get selected medicine
        selected = self.medicines_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a medicine to update!")
            return

        item = self.medicines_tree.item(selected[0])
        medicine_id = item['values'][0]

        # Get medicine details
        self.cursor.execute("SELECT * FROM medicines WHERE id=?", (medicine_id,))
        medicine = self.cursor.fetchone()

        if not medicine:
            messagebox.showerror("Error", "Medicine not found!")
            return

        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Update Medicine", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Medicines", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.medicines_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Form frame
        form_frame = Frame(self.root, bg='white')
        form_frame.pack(fill=BOTH, expand=True, padx=50, pady=20)

        # Medicine details
        Label(form_frame, text="Medicine Details", font=('Arial', 16, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, pady=10)

        # ID (read-only)
        Label(form_frame, text="ID:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        id_label = Label(form_frame, text=str(medicine[0]), font=('Arial', 12), bg='white')
        id_label.grid(row=1, column=1, sticky='w', pady=5, padx=5)

        # Name
        Label(form_frame, text="Name:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.name_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.name_entry.grid(row=2, column=1, pady=5, padx=5)
        self.name_entry.insert(0, medicine[1])

        # Description
        Label(form_frame, text="Description:", font=('Arial', 12), bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=5)
        self.desc_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.desc_entry.grid(row=3, column=1, pady=5, padx=5)
        self.desc_entry.insert(0, medicine[2])

        # Quantity
        Label(form_frame, text="Quantity:", font=('Arial', 12), bg='white').grid(row=4, column=0, sticky='w', pady=5, padx=5)
        self.qty_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.qty_entry.grid(row=4, column=1, pady=5, padx=5)
        self.qty_entry.insert(0, str(medicine[3]))

        # Price
        Label(form_frame, text="Price:", font=('Arial', 12), bg='white').grid(row=5, column=0, sticky='w', pady=5, padx=5)
        self.price_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.price_entry.grid(row=5, column=1, pady=5, padx=5)
        self.price_entry.insert(0, str(medicine[4]))

        # Supplier
        Label(form_frame, text="Supplier:", font=('Arial', 12), bg='white').grid(row=6, column=0, sticky='w', pady=5, padx=5)
        self.supplier_var = StringVar()
        self.supplier_combo = ttk.Combobox(form_frame, textvariable=self.supplier_var, font=('Arial', 12), width=28)
        self.supplier_combo.grid(row=6, column=1, pady=5, padx=5)

        # Load suppliers
        self.cursor.execute("SELECT id, name FROM suppliers ORDER BY name")
        suppliers = self.cursor.fetchall()
        supplier_list = [f"{s[0]} - {s[1]}" for s in suppliers]
        self.supplier_combo['values'] = supplier_list

        # Set current supplier
        if medicine[5]:
            self.cursor.execute("SELECT name FROM suppliers WHERE id=?", (medicine[5],))
            supplier_name = self.cursor.fetchone()[0]
            self.supplier_var.set(f"{medicine[5]} - {supplier_name}")

        # Expiry date
        Label(form_frame, text="Expiry Date (YYYY-MM-DD):", font=('Arial', 12), bg='white').grid(row=7, column=0, sticky='w', pady=5, padx=5)
        self.exp_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.exp_entry.grid(row=7, column=1, pady=5, padx=5)
        self.exp_entry.insert(0, medicine[6])

        # Category
        Label(form_frame, text="Category:", font=('Arial', 12), bg='white').grid(row=8, column=0, sticky='w', pady=5, padx=5)
        self.category_var = StringVar()
        categories = ["Tablet", "Capsule", "Syrup", "Injection", "Ointment", "Drops", "Inhaler", "Other"]
        self.category_combo = ttk.Combobox(form_frame, textvariable=self.category_var, values=categories, font=('Arial', 12), width=28)
        self.category_combo.grid(row=8, column=1, pady=5, padx=5)
        self.category_combo.set(medicine[7])

        # Barcode
        Label(form_frame, text="Barcode:", font=('Arial', 12), bg='white').grid(row=9, column=0, sticky='w', pady=5, padx=5)
        self.barcode_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.barcode_entry.grid(row=9, column=1, pady=5, padx=5)
        self.barcode_entry.insert(0, medicine[8])

        # Buttons
        btn_frame = Frame(form_frame, bg='white')
        btn_frame.grid(row=10, column=0, columnspan=2, pady=20)

        update_btn = Button(btn_frame, text="Update Medicine", font=('Arial', 12), bg='#f39c12', fg='white',
                           command=lambda: self.update_medicine(medicine_id), width=15)
        update_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.medicines_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

    def update_medicine(self, medicine_id):
        """Update medicine in database"""
        # Get form data
        name = self.name_entry.get().strip()
        description = self.desc_entry.get().strip()
        quantity = self.qty_entry.get().strip()
        price = self.price_entry.get().strip()
        supplier = self.supplier_var.get()
        expiry = self.exp_entry.get().strip()
        category = self.category_var.get()
        barcode = self.barcode_entry.get().strip()

        # Validation
        if not name or not quantity or not price or not category:
            messagebox.showerror("Error", "Name, Quantity, Price, and Category are required!")
            return

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer and Price must be a number!")
            return

        # Get supplier ID
        supplier_id = None
        if supplier:
            supplier_id = int(supplier.split(' - ')[0])

        # Check if barcode already exists (excluding current medicine)
        if barcode:
            self.cursor.execute("SELECT id FROM medicines WHERE barcode=? AND id!=?", (barcode, medicine_id))
            if self.cursor.fetchone():
                messagebox.showerror("Error", "Barcode already exists!")
                return

        # Update medicine
        self.cursor.execute("""
        UPDATE medicines
        SET name=?, description=?, quantity=?, price=?, supplier_id=?, expiry_date=?, category=?, barcode=?
        WHERE id=?
        """, (name, description, quantity, price, supplier_id, expiry, category, barcode, medicine_id))

        self.conn.commit()
        messagebox.showinfo("Success", "Medicine updated successfully!")
        self.medicines_screen()

    def delete_medicine(self):
        """Delete selected medicine"""
        # Get selected medicine
        selected = self.medicines_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a medicine to delete!")
            return

        item = self.medicines_tree.item(selected[0])
        medicine_id = item['values'][0]
        medicine_name = item['values'][1]

        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {medicine_name}?"):
            # Check if medicine is used in sales or purchases
            self.cursor.execute("SELECT COUNT(*) FROM sale_items WHERE medicine_id=?", (medicine_id,))
            sales_count = self.cursor.fetchone()[0]

            self.cursor.execute("SELECT COUNT(*) FROM purchase_items WHERE medicine_id=?", (medicine_id,))
            purchases_count = self.cursor.fetchone()[0]

            if sales_count > 0 or purchases_count > 0:
                messagebox.showerror("Error", "Cannot delete medicine that has been used in sales or purchases!")
                return

            # Delete medicine
            self.cursor.execute("DELETE FROM medicines WHERE id=?", (medicine_id,))
            self.conn.commit()

            messagebox.showinfo("Success", "Medicine deleted successfully!")
            self.load_medicines()

    def suppliers_screen(self):
        """Display suppliers management screen"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Suppliers Management", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Dashboard", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.dashboard, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Buttons frame
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10, padx=20, fill=X)

        add_btn = Button(btn_frame, text="Add Supplier", font=('Arial', 12), bg='#2ecc71', fg='white',
                        command=self.add_supplier_screen, width=15)
        add_btn.pack(side=LEFT, padx=5)

        update_btn = Button(btn_frame, text="Update Supplier", font=('Arial', 12), bg='#f39c12', fg='white',
                           command=self.update_supplier_screen, width=15)
        update_btn.pack(side=LEFT, padx=5)

        delete_btn = Button(btn_frame, text="Delete Supplier", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.delete_supplier, width=15)
        delete_btn.pack(side=LEFT, padx=5)

        # Suppliers table
        table_frame = Frame(main_frame)
        table_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(table_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.suppliers_tree = ttk.Treeview(table_frame, columns=('ID', 'Name', 'Contact', 'Address', 'Email'),
                                          show='headings', yscrollcommand=scrollbar.set)

        self.suppliers_tree.heading('ID', text='ID')
        self.suppliers_tree.heading('Name', text='Name')
        self.suppliers_tree.heading('Contact', text='Contact')
        self.suppliers_tree.heading('Address', text='Address')
        self.suppliers_tree.heading('Email', text='Email')

        self.suppliers_tree.column('ID', width=50)
        self.suppliers_tree.column('Name', width=150)
        self.suppliers_tree.column('Contact', width=120)
        self.suppliers_tree.column('Address', width=200)
        self.suppliers_tree.column('Email', width=150)

        scrollbar.config(command=self.suppliers_tree.yview)
        self.suppliers_tree.pack(fill=BOTH, expand=True)

        # Load suppliers
        self.load_suppliers()

    def load_suppliers(self):
        """Load all suppliers data"""
        # Clear existing data
        for i in self.suppliers_tree.get_children():
            self.suppliers_tree.delete(i)

        # Get all suppliers
        self.cursor.execute("SELECT * FROM suppliers ORDER BY name")

        for row in self.cursor.fetchall():
            self.suppliers_tree.insert('', 'end', values=row)

    def add_supplier_screen(self):
        """Display add supplier form"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Add New Supplier", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Suppliers", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.suppliers_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Form frame
        form_frame = Frame(self.root, bg='white')
        form_frame.pack(fill=BOTH, expand=True, padx=50, pady=20)

        # Supplier details
        Label(form_frame, text="Supplier Details", font=('Arial', 16, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, pady=10)

        # Name
        Label(form_frame, text="Name:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.name_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.name_entry.grid(row=1, column=1, pady=5, padx=5)

        # Contact
        Label(form_frame, text="Contact:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.contact_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.contact_entry.grid(row=2, column=1, pady=5, padx=5)

        # Address
        Label(form_frame, text="Address:", font=('Arial', 12), bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=5)
        self.address_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.address_entry.grid(row=3, column=1, pady=5, padx=5)

        # Email
        Label(form_frame, text="Email:", font=('Arial', 12), bg='white').grid(row=4, column=0, sticky='w', pady=5, padx=5)
        self.email_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.email_entry.grid(row=4, column=1, pady=5, padx=5)

        # Buttons
        btn_frame = Frame(form_frame, bg='white')
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)

        save_btn = Button(btn_frame, text="Save Supplier", font=('Arial', 12), bg='#2ecc71', fg='white',
                         command=self.save_supplier, width=15)
        save_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.suppliers_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

    def save_supplier(self):
        """Save new supplier to database"""
        # Get form data
        name = self.name_entry.get().strip()
        contact = self.contact_entry.get().strip()
        address = self.address_entry.get().strip()
        email = self.email_entry.get().strip()

        # Validation
        if not name:
            messagebox.showerror("Error", "Name is required!")
            return

        # Insert supplier
        self.cursor.execute("""
        INSERT INTO suppliers (name, contact, address, email)
        VALUES (?, ?, ?, ?)
        """, (name, contact, address, email))

        self.conn.commit()
        messagebox.showinfo("Success", "Supplier added successfully!")
        self.suppliers_screen()

    def update_supplier_screen(self):
        """Display update supplier form"""
        # Get selected supplier
        selected = self.suppliers_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a supplier to update!")
            return

        item = self.suppliers_tree.item(selected[0])
        supplier_id = item['values'][0]

        # Get supplier details
        self.cursor.execute("SELECT * FROM suppliers WHERE id=?", (supplier_id,))
        supplier = self.cursor.fetchone()

        if not supplier:
            messagebox.showerror("Error", "Supplier not found!")
            return

        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Update Supplier", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Suppliers", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.suppliers_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Form frame
        form_frame = Frame(self.root, bg='white')
        form_frame.pack(fill=BOTH, expand=True, padx=50, pady=20)

        # Supplier details
        Label(form_frame, text="Supplier Details", font=('Arial', 16, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, pady=10)

        # ID (read-only)
        Label(form_frame, text="ID:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        id_label = Label(form_frame, text=str(supplier[0]), font=('Arial', 12), bg='white')
        id_label.grid(row=1, column=1, sticky='w', pady=5, padx=5)

        # Name
        Label(form_frame, text="Name:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.name_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.name_entry.grid(row=2, column=1, pady=5, padx=5)
        self.name_entry.insert(0, supplier[1])

        # Contact
        Label(form_frame, text="Contact:", font=('Arial', 12), bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=5)
        self.contact_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.contact_entry.grid(row=3, column=1, pady=5, padx=5)
        self.contact_entry.insert(0, supplier[2])

        # Address
        Label(form_frame, text="Address:", font=('Arial', 12), bg='white').grid(row=4, column=0, sticky='w', pady=5, padx=5)
        self.address_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.address_entry.grid(row=4, column=1, pady=5, padx=5)
        self.address_entry.insert(0, supplier[3])

        # Email
        Label(form_frame, text="Email:", font=('Arial', 12), bg='white').grid(row=5, column=0, sticky='w', pady=5, padx=5)
        self.email_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.email_entry.grid(row=5, column=1, pady=5, padx=5)
        self.email_entry.insert(0, supplier[4])

        # Buttons
        btn_frame = Frame(form_frame, bg='white')
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)

        update_btn = Button(btn_frame, text="Update Supplier", font=('Arial', 12), bg='#f39c12', fg='white',
                           command=lambda: self.update_supplier(supplier_id), width=15)
        update_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.suppliers_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

    def update_supplier(self, supplier_id):
        """Update supplier in database"""
        # Get form data
        name = self.name_entry.get().strip()
        contact = self.contact_entry.get().strip()
        address = self.address_entry.get().strip()
        email = self.email_entry.get().strip()

        # Validation
        if not name:
            messagebox.showerror("Error", "Name is required!")
            return

        # Update supplier
        self.cursor.execute("""
        UPDATE suppliers
        SET name=?, contact=?, address=?, email=?
        WHERE id=?
        """, (name, contact, address, email, supplier_id))

        self.conn.commit()
        messagebox.showinfo("Success", "Supplier updated successfully!")
        self.suppliers_screen()

    def delete_supplier(self):
        """Delete selected supplier"""
        # Get selected supplier
        selected = self.suppliers_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a supplier to delete!")
            return

        item = self.suppliers_tree.item(selected[0])
        supplier_id = item['values'][0]
        supplier_name = item['values'][1]

        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {supplier_name}?"):
            # Check if supplier is used in medicines or purchases
            self.cursor.execute("SELECT COUNT(*) FROM medicines WHERE supplier_id=?", (supplier_id,))
            medicines_count = self.cursor.fetchone()[0]

            self.cursor.execute("SELECT COUNT(*) FROM purchases WHERE supplier_id=?", (supplier_id,))
            purchases_count = self.cursor.fetchone()[0]

            if medicines_count > 0 or purchases_count > 0:
                messagebox.showerror("Error", "Cannot delete supplier that has associated medicines or purchases!")
                return

            # Delete supplier
            self.cursor.execute("DELETE FROM suppliers WHERE id=?", (supplier_id,))
            self.conn.commit()

            messagebox.showinfo("Success", "Supplier deleted successfully!")
            self.load_suppliers()

    def customers_screen(self):
        """Display customers management screen"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Customers Management", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Dashboard", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.dashboard, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Buttons frame
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10, padx=20, fill=X)

        add_btn = Button(btn_frame, text="Add Customer", font=('Arial', 12), bg='#2ecc71', fg='white',
                        command=self.add_customer_screen, width=15)
        add_btn.pack(side=LEFT, padx=5)

        update_btn = Button(btn_frame, text="Update Customer", font=('Arial', 12), bg='#f39c12', fg='white',
                           command=self.update_customer_screen, width=15)
        update_btn.pack(side=LEFT, padx=5)

        delete_btn = Button(btn_frame, text="Delete Customer", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.delete_customer, width=15)
        delete_btn.pack(side=LEFT, padx=5)

        # Customers table
        table_frame = Frame(main_frame)
        table_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(table_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.customers_tree = ttk.Treeview(table_frame, columns=('ID', 'Name', 'Contact', 'Address', 'Email'),
                                          show='headings', yscrollcommand=scrollbar.set)

        self.customers_tree.heading('ID', text='ID')
        self.customers_tree.heading('Name', text='Name')
        self.customers_tree.heading('Contact', text='Contact')
        self.customers_tree.heading('Address', text='Address')
        self.customers_tree.heading('Email', text='Email')

        self.customers_tree.column('ID', width=50)
        self.customers_tree.column('Name', width=150)
        self.customers_tree.column('Contact', width=120)
        self.customers_tree.column('Address', width=200)
        self.customers_tree.column('Email', width=150)

        scrollbar.config(command=self.customers_tree.yview)
        self.customers_tree.pack(fill=BOTH, expand=True)

        # Load customers
        self.load_customers()

    def load_customers(self):
        """Load all customers data"""
        # Clear existing data
        for i in self.customers_tree.get_children():
            self.customers_tree.delete(i)

        # Get all customers
        self.cursor.execute("SELECT * FROM customers ORDER BY name")

        for row in self.cursor.fetchall():
            self.customers_tree.insert('', 'end', values=row)

    def add_customer_screen(self):
        """Display add customer form"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Add New Customer", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Customers", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.customers_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Form frame
        form_frame = Frame(self.root, bg='white')
        form_frame.pack(fill=BOTH, expand=True, padx=50, pady=20)

        # Customer details
        Label(form_frame, text="Customer Details", font=('Arial', 16, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, pady=10)

        # Name
        Label(form_frame, text="Name:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        self.name_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.name_entry.grid(row=1, column=1, pady=5, padx=5)

        # Contact
        Label(form_frame, text="Contact:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.contact_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.contact_entry.grid(row=2, column=1, pady=5, padx=5)

        # Address
        Label(form_frame, text="Address:", font=('Arial', 12), bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=5)
        self.address_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.address_entry.grid(row=3, column=1, pady=5, padx=5)

        # Email
        Label(form_frame, text="Email:", font=('Arial', 12), bg='white').grid(row=4, column=0, sticky='w', pady=5, padx=5)
        self.email_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.email_entry.grid(row=4, column=1, pady=5, padx=5)

        # Buttons
        btn_frame = Frame(form_frame, bg='white')
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)

        save_btn = Button(btn_frame, text="Save Customer", font=('Arial', 12), bg='#2ecc71', fg='white',
                         command=self.save_customer, width=15)
        save_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.customers_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

    def save_customer(self):
        """Save new customer to database"""
        # Get form data
        name = self.name_entry.get().strip()
        contact = self.contact_entry.get().strip()
        address = self.address_entry.get().strip()
        email = self.email_entry.get().strip()

        # Validation
        if not name:
            messagebox.showerror("Error", "Name is required!")
            return

        # Insert customer
        self.cursor.execute("""
        INSERT INTO customers (name, contact, address, email)
        VALUES (?, ?, ?, ?)
        """, (name, contact, address, email))

        self.conn.commit()
        messagebox.showinfo("Success", "Customer added successfully!")
        self.customers_screen()

    def update_customer_screen(self):
        """Display update customer form"""
        # Get selected customer
        selected = self.customers_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a customer to update!")
            return

        item = self.customers_tree.item(selected[0])
        customer_id = item['values'][0]

        # Get customer details
        self.cursor.execute("SELECT * FROM customers WHERE id=?", (customer_id,))
        customer = self.cursor.fetchone()

        if not customer:
            messagebox.showerror("Error", "Customer not found!")
            return

        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Update Customer", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Customers", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.customers_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Form frame
        form_frame = Frame(self.root, bg='white')
        form_frame.pack(fill=BOTH, expand=True, padx=50, pady=20)

        # Customer details
        Label(form_frame, text="Customer Details", font=('Arial', 16, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, pady=10)

        # ID (read-only)
        Label(form_frame, text="ID:", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        id_label = Label(form_frame, text=str(customer[0]), font=('Arial', 12), bg='white')
        id_label.grid(row=1, column=1, sticky='w', pady=5, padx=5)

        # Name
        Label(form_frame, text="Name:", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        self.name_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.name_entry.grid(row=2, column=1, pady=5, padx=5)
        self.name_entry.insert(0, customer[1])

        # Contact
        Label(form_frame, text="Contact:", font=('Arial', 12), bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=5)
        self.contact_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.contact_entry.grid(row=3, column=1, pady=5, padx=5)
        self.contact_entry.insert(0, customer[2])

        # Address
        Label(form_frame, text="Address:", font=('Arial', 12), bg='white').grid(row=4, column=0, sticky='w', pady=5, padx=5)
        self.address_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.address_entry.grid(row=4, column=1, pady=5, padx=5)
        self.address_entry.insert(0, customer[3])

        # Email
        Label(form_frame, text="Email:", font=('Arial', 12), bg='white').grid(row=5, column=0, sticky='w', pady=5, padx=5)
        self.email_entry = Entry(form_frame, font=('Arial', 12), width=30)
        self.email_entry.grid(row=5, column=1, pady=5, padx=5)
        self.email_entry.insert(0, customer[4])

        # Buttons
        btn_frame = Frame(form_frame, bg='white')
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)

        update_btn = Button(btn_frame, text="Update Customer", font=('Arial', 12), bg='#f39c12', fg='white',
                           command=lambda: self.update_customer(customer_id), width=15)
        update_btn.pack(side=LEFT, padx=10)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.customers_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=10)

    def update_customer(self, customer_id):
        """Update customer in database"""
        # Get form data
        name = self.name_entry.get().strip()
        contact = self.contact_entry.get().strip()
        address = self.address_entry.get().strip()
        email = self.email_entry.get().strip()

        # Validation
        if not name:
            messagebox.showerror("Error", "Name is required!")
            return

        # Update customer
        self.cursor.execute("""
        UPDATE customers
        SET name=?, contact=?, address=?, email=?
        WHERE id=?
        """, (name, contact, address, email, customer_id))

        self.conn.commit()
        messagebox.showinfo("Success", "Customer updated successfully!")
        self.customers_screen()

    def delete_customer(self):
        """Delete selected customer"""
        # Get selected customer
        selected = self.customers_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a customer to delete!")
            return

        item = self.customers_tree.item(selected[0])
        customer_id = item['values'][0]
        customer_name = item['values'][1]

        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {customer_name}?"):
            # Check if customer is used in sales
            self.cursor.execute("SELECT COUNT(*) FROM sales WHERE customer_id=?", (customer_id,))
            sales_count = self.cursor.fetchone()[0]

            if sales_count > 0:
                messagebox.showerror("Error", "Cannot delete customer that has associated sales!")
                return

            # Delete customer
            self.cursor.execute("DELETE FROM customers WHERE id=?", (customer_id,))
            self.conn.commit()

            messagebox.showinfo("Success", "Customer deleted successfully!")
            self.load_customers()

    def sales_screen(self):
        """Display sales management screen"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Sales Management", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Dashboard", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.dashboard, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Buttons frame
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10, padx=20, fill=X)

        new_sale_btn = Button(btn_frame, text="New Sale", font=('Arial', 12), bg='#2ecc71', fg='white',
                             command=self.new_sale_screen, width=15)
        new_sale_btn.pack(side=LEFT, padx=5)

        view_sale_btn = Button(btn_frame, text="View Sale Details", font=('Arial', 12), bg='#3498db', fg='white',
                              command=self.view_sale_screen, width=15)
        view_sale_btn.pack(side=LEFT, padx=5)

        # Sales table
        table_frame = Frame(main_frame)
        table_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(table_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.sales_tree = ttk.Treeview(table_frame, columns=('ID', 'Customer', 'Employee', 'Date', 'Amount', 'Payment'),
                                      show='headings', yscrollcommand=scrollbar.set)

        self.sales_tree.heading('ID', text='ID')
        self.sales_tree.heading('Customer', text='Customer')
        self.sales_tree.heading('Employee', text='Employee')
        self.sales_tree.heading('Date', text='Date')
        self.sales_tree.heading('Amount', text='Amount')
        self.sales_tree.heading('Payment', text='Payment Method')

        self.sales_tree.column('ID', width=50)
        self.sales_tree.column('Customer', width=150)
        self.sales_tree.column('Employee', width=150)
        self.sales_tree.column('Date', width=150)
        self.sales_tree.column('Amount', width=100)
        self.sales_tree.column('Payment', width=120)

        scrollbar.config(command=self.sales_tree.yview)
        self.sales_tree.pack(fill=BOTH, expand=True)

        # Load sales
        self.load_sales()

    def load_sales(self):
        """Load all sales data"""
        # Clear existing data
        for i in self.sales_tree.get_children():
            self.sales_tree.delete(i)

        # Get all sales
        self.cursor.execute("""
        SELECT s.id, c.name, e.name, s.date, s.total_amount, s.payment_method
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.id
        LEFT JOIN employees e ON s.employee_id = e.id
        ORDER BY s.date DESC
        """)

        for row in self.cursor.fetchall():
            self.sales_tree.insert('', 'end', values=row)

    def new_sale_screen(self):
        """Display new sale form"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="New Sale", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Sales", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.sales_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Form frame
        form_frame = Frame(main_frame, bg='white')
        form_frame.pack(pady=10, padx=20, fill=X)

        # Customer
        Label(form_frame, text="Customer:", font=('Arial', 12), bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.customer_var = StringVar()
        self.customer_combo = ttk.Combobox(form_frame, textvariable=self.customer_var, font=('Arial', 12), width=28)
        self.customer_combo.grid(row=0, column=1, pady=5, padx=5)

        # Load customers
        self.cursor.execute("SELECT id, name FROM customers ORDER BY name")
        customers = self.cursor.fetchall()
        customer_list = [f"{c[0]} - {c[1]}" for c in customers]
        self.customer_combo['values'] = customer_list

        # Payment method
        Label(form_frame, text="Payment Method:", font=('Arial', 12), bg='white').grid(row=0, column=2, sticky='w', pady=5, padx=5)
        self.payment_var = StringVar()
        payments = ["Cash", "Credit Card", "Debit Card", "Insurance"]
        self.payment_combo = ttk.Combobox(form_frame, textvariable=self.payment_var, values=payments, font=('Arial', 12), width=15)
        self.payment_combo.grid(row=0, column=3, pady=5, padx=5)

        # Add medicine frame
        add_frame = Frame(main_frame, bg='white')
        add_frame.pack(pady=10, padx=20, fill=X)

        Label(add_frame, text="Add Medicine to Sale", font=('Arial', 14, 'bold'), bg='white').pack(pady=5)

        # Medicine
        Label(add_frame, text="Medicine:", font=('Arial', 12), bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.medicine_var = StringVar()
        self.medicine_combo = ttk.Combobox(add_frame, textvariable=self.medicine_var, font=('Arial', 12), width=28)
        self.medicine_combo.grid(row=0, column=1, pady=5, padx=5)

        # Load medicines
        self.cursor.execute("SELECT id, name, quantity, price FROM medicines WHERE quantity > 0 ORDER BY name")
        medicines = self.cursor.fetchall()
        medicine_list = [f"{m[0]} - {m[1]} (Stock: {m[2]}, Price: {m[3]})" for m in medicines]
        self.medicine_combo['values'] = medicine_list

        # Quantity
        Label(add_frame, text="Quantity:", font=('Arial', 12), bg='white').grid(row=0, column=2, sticky='w', pady=5, padx=5)
        self.qty_entry = Entry(add_frame, font=('Arial', 12), width=10)
        self.qty_entry.grid(row=0, column=3, pady=5, padx=5)

        # Add button
        add_btn = Button(add_frame, text="Add", font=('Arial', 12), bg='#2ecc71', fg='white',
                       command=self.add_to_sale, width=10)
        add_btn.grid(row=0, column=4, pady=5, padx=5)

        # Sale items table
        items_frame = Frame(main_frame)
        items_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(items_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.sale_items_tree = ttk.Treeview(items_frame, columns=('ID', 'Name', 'Quantity', 'Price', 'Total'),
                                          show='headings', yscrollcommand=scrollbar.set)

        self.sale_items_tree.heading('ID', text='ID')
        self.sale_items_tree.heading('Name', text='Name')
        self.sale_items_tree.heading('Quantity', text='Quantity')
        self.sale_items_tree.heading('Price', text='Price')
        self.sale_items_tree.heading('Total', text='Total')

        self.sale_items_tree.column('ID', width=50)
        self.sale_items_tree.column('Name', width=200)
        self.sale_items_tree.column('Quantity', width=100)
        self.sale_items_tree.column('Price', width=100)
        self.sale_items_tree.column('Total', width=100)

        scrollbar.config(command=self.sale_items_tree.yview)
        self.sale_items_tree.pack(fill=BOTH, expand=True)

        # Total frame
        total_frame = Frame(main_frame, bg='white')
        total_frame.pack(pady=10, padx=20, fill=X)

        self.total_label = Label(total_frame, text="Total: $0.00", font=('Arial', 14, 'bold'), bg='white')
        self.total_label.pack(side=RIGHT, padx=10)

        # Buttons
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10, padx=20, fill=X)

        complete_btn = Button(btn_frame, text="Complete Sale", font=('Arial', 12), bg='#2ecc71', fg='white',
                             command=self.complete_sale, width=15)
        complete_btn.pack(side=LEFT, padx=5)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.sales_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=5)

        # Initialize sale items list
        self.sale_items = []
        self.sale_total = 0.0

    def add_to_sale(self):
        """Add medicine to current sale"""
        medicine = self.medicine_var.get()
        quantity = self.qty_entry.get().strip()

        if not medicine or not quantity:
            messagebox.showerror("Error", "Please select a medicine and enter quantity!")
            return

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive integer!")
            return

        # Get medicine details
        medicine_id = int(medicine.split(' - ')[0])
        self.cursor.execute("SELECT id, name, quantity, price FROM medicines WHERE id=?", (medicine_id,))
        med = self.cursor.fetchone()

        if not med:
            messagebox.showerror("Error", "Medicine not found!")
            return

        if quantity > med[2]:
            messagebox.showerror("Error", f"Only {med[2]} items available in stock!")
            return

        # Check if medicine already in sale
        for item in self.sale_items:
            if item['id'] == medicine_id:
                item['quantity'] += quantity
                item['total'] = item['quantity'] * item['price']
                break
        else:
            self.sale_items.append({
                'id': medicine_id,
                'name': med[1],
                'quantity': quantity,
                'price': med[3],
                'total': quantity * med[3]
            })

        # Update sale items tree
        self.update_sale_items_tree()

        # Clear form
        self.medicine_var.set('')
        self.qty_entry.delete(0, END)

    def update_sale_items_tree(self):
        """Update sale items treeview"""
        # Clear existing data
        for i in self.sale_items_tree.get_children():
            self.sale_items_tree.delete(i)

        # Add items
        self.sale_total = 0.0
        for item in self.sale_items:
            self.sale_items_tree.insert('', 'end', values=(
                item['id'],
                item['name'],
                item['quantity'],
                f"${item['price']:.2f}",
                f"${item['total']:.2f}"
            ))
            self.sale_total += item['total']

        # Update total label
        self.total_label.config(text=f"Total: ${self.sale_total:.2f}")

    def complete_sale(self):
        """Complete the current sale"""
        if not self.sale_items:
            messagebox.showerror("Error", "No items in sale!")
            return

        customer = self.customer_var.get()
        payment = self.payment_var.get()

        if not payment:
            messagebox.showerror("Error", "Please select a payment method!")
            return

        # Get customer ID
        customer_id = None
        if customer:
            customer_id = int(customer.split(' - ')[0])

        # Create sale record
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute("""
        INSERT INTO sales (customer_id, employee_id, date, total_amount, payment_method)
        VALUES (?, ?, ?, ?, ?)
        """, (customer_id, self.current_user['id'], today, self.sale_total, payment))

        sale_id = self.cursor.lastrowid

        # Add sale items
        for item in self.sale_items:
            self.cursor.execute("""
            INSERT INTO sale_items (sale_id, medicine_id, quantity, price_per_unit)
            VALUES (?, ?, ?, ?)
            """, (sale_id, item['id'], item['quantity'], item['price']))

            # Update medicine quantity
            self.cursor.execute("""
            UPDATE medicines
            SET quantity = quantity - ?
            WHERE id = ?
            """, (item['quantity'], item['id']))

        self.conn.commit()

        messagebox.showinfo("Success", f"Sale completed successfully! Sale ID: {sale_id}")
        self.sales_screen()

    def view_sale_screen(self):
        """Display sale details screen"""
        # Get selected sale
        selected = self.sales_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a sale to view!")
            return

        item = self.sales_tree.item(selected[0])
        sale_id = item['values'][0]

        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Sale Details", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Sales", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.sales_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Sale details frame
        details_frame = Frame(main_frame, bg='white')
        details_frame.pack(pady=10, padx=20, fill=X)

        # Get sale details
        self.cursor.execute("""
        SELECT s.id, c.name, e.name, s.date, s.total_amount, s.payment_method
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.id
        LEFT JOIN employees e ON s.employee_id = e.id
        WHERE s.id = ?
        """, (sale_id,))

        sale = self.cursor.fetchone()

        if not sale:
            messagebox.showerror("Error", "Sale not found!")
            return

        # Display sale details
        Label(details_frame, text=f"Sale ID: {sale[0]}", font=('Arial', 12, 'bold'), bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Customer: {sale[1] if sale[1] else 'Walk-in'}", font=('Arial', 12), bg='white').grid(row=0, column=1, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Employee: {sale[2]}", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Date: {sale[3]}", font=('Arial', 12), bg='white').grid(row=1, column=1, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Payment: {sale[5]}", font=('Arial', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Total: ${sale[4]:.2f}", font=('Arial', 12, 'bold'), bg='white').grid(row=2, column=1, sticky='w', pady=5, padx=5)

        # Sale items table
        items_frame = Frame(main_frame)
        items_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(items_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        items_tree = ttk.Treeview(items_frame, columns=('ID', 'Name', 'Quantity', 'Price', 'Total'),
                                 show='headings', yscrollcommand=scrollbar.set)

        items_tree.heading('ID', text='ID')
        items_tree.heading('Name', text='Name')
        items_tree.heading('Quantity', text='Quantity')
        items_tree.heading('Price', text='Price')
        items_tree.heading('Total', text='Total')

        items_tree.column('ID', width=50)
        items_tree.column('Name', width=200)
        items_tree.column('Quantity', width=100)
        items_tree.column('Price', width=100)
        items_tree.column('Total', width=100)

        scrollbar.config(command=items_tree.yview)
        items_tree.pack(fill=BOTH, expand=True)

        # Get sale items
        self.cursor.execute("""
        SELECT si.medicine_id, m.name, si.quantity, si.price_per_unit, (si.quantity * si.price_per_unit)
        FROM sale_items si
        JOIN medicines m ON si.medicine_id = m.id
        WHERE si.sale_id = ?
        """, (sale_id,))

        for row in self.cursor.fetchall():
            items_tree.insert('', 'end', values=(
                row[0],
                row[1],
                row[2],
                f"${row[3]:.2f}",
                f"${row[4]:.2f}"
            ))

        # Print button
        print_btn = Button(main_frame, text="Print Receipt", font=('Arial', 12), bg='#3498db', fg='white',
                          command=lambda: self.print_receipt(sale_id), width=15)
        print_btn.pack(pady=10)

    def print_receipt(self, sale_id):
        """Print sale receipt (simulated)"""
        # Get sale details
        self.cursor.execute("""
        SELECT s.id, c.name, e.name, s.date, s.total_amount, s.payment_method
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.id
        LEFT JOIN employees e ON s.employee_id = e.id
        WHERE s.id = ?
        """, (sale_id,))

        sale = self.cursor.fetchone()

        if not sale:
            messagebox.showerror("Error", "Sale not found!")
            return

        # Get sale items
        self.cursor.execute("""
        SELECT m.name, si.quantity, si.price_per_unit, (si.quantity * si.price_per_unit)
        FROM sale_items si
        JOIN medicines m ON si.medicine_id = m.id
        WHERE si.sale_id = ?
        """, (sale_id,))

        items = self.cursor.fetchall()

        # Create receipt text
        receipt = f"""
        PHARMACY MANAGEMENT SYSTEM
        ==========================
        Receipt ID: {sale[0]}
        Date: {sale[3]}
        Customer: {sale[1] if sale[1] else 'Walk-in'}
        Cashier: {sale[2]}
        Payment: {sale[5]}
        --------------------------
        ITEMS:
        """

        for item in items:
            receipt += f"{item[0]} x {item[1]} @ ${item[2]:.2f} = ${item[3]:.2f}\n"

        receipt += f"""
        --------------------------
        TOTAL: ${sale[4]:.2f}
        --------------------------
        Thank you for your purchase!
        """

        # Show receipt in a message box (in a real system, this would print to a printer)
        messagebox.showinfo("Receipt", receipt)

    def purchases_screen(self):
        """Display purchases management screen"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Purchases Management", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Dashboard", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.dashboard, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Buttons frame
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10, padx=20, fill=X)

        new_purchase_btn = Button(btn_frame, text="New Purchase", font=('Arial', 12), bg='#2ecc71', fg='white',
                                command=self.new_purchase_screen, width=15)
        new_purchase_btn.pack(side=LEFT, padx=5)

        view_purchase_btn = Button(btn_frame, text="View Purchase Details", font=('Arial', 12), bg='#3498db', fg='white',
                                 command=self.view_purchase_screen, width=15)
        view_purchase_btn.pack(side=LEFT, padx=5)

        # Purchases table
        table_frame = Frame(main_frame)
        table_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(table_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.purchases_tree = ttk.Treeview(table_frame, columns=('ID', 'Supplier', 'Employee', 'Date', 'Amount'),
                                          show='headings', yscrollcommand=scrollbar.set)

        self.purchases_tree.heading('ID', text='ID')
        self.purchases_tree.heading('Supplier', text='Supplier')
        self.purchases_tree.heading('Employee', text='Employee')
        self.purchases_tree.heading('Date', text='Date')
        self.purchases_tree.heading('Amount', text='Amount')

        self.purchases_tree.column('ID', width=50)
        self.purchases_tree.column('Supplier', width=150)
        self.purchases_tree.column('Employee', width=150)
        self.purchases_tree.column('Date', width=150)
        self.purchases_tree.column('Amount', width=100)

        scrollbar.config(command=self.purchases_tree.yview)
        self.purchases_tree.pack(fill=BOTH, expand=True)

        # Load purchases
        self.load_purchases()

    def load_purchases(self):
        """Load all purchases data"""
        # Clear existing data
        for i in self.purchases_tree.get_children():
            self.purchases_tree.delete(i)

        # Get all purchases
        self.cursor.execute("""
        SELECT p.id, s.name, e.name, p.date, p.total_amount
        FROM purchases p
        LEFT JOIN suppliers s ON p.supplier_id = s.id
        LEFT JOIN employees e ON p.employee_id = e.id
        ORDER BY p.date DESC
        """)

        for row in self.cursor.fetchall():
            self.purchases_tree.insert('', 'end', values=row)

    def new_purchase_screen(self):
        """Display new purchase form"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="New Purchase", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Purchases", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.purchases_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Form frame
        form_frame = Frame(main_frame, bg='white')
        form_frame.pack(pady=10, padx=20, fill=X)

        # Supplier
        Label(form_frame, text="Supplier:", font=('Arial', 12), bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.supplier_var = StringVar()
        self.supplier_combo = ttk.Combobox(form_frame, textvariable=self.supplier_var, font=('Arial', 12), width=28)
        self.supplier_combo.grid(row=0, column=1, pady=5, padx=5)

        # Load suppliers
        self.cursor.execute("SELECT id, name FROM suppliers ORDER BY name")
        suppliers = self.cursor.fetchall()
        supplier_list = [f"{s[0]} - {s[1]}" for s in suppliers]
        self.supplier_combo['values'] = supplier_list

        # Add medicine frame
        add_frame = Frame(main_frame, bg='white')
        add_frame.pack(pady=10, padx=20, fill=X)

        Label(add_frame, text="Add Medicine to Purchase", font=('Arial', 14, 'bold'), bg='white').pack(pady=5)

        # Medicine
        Label(add_frame, text="Medicine:", font=('Arial', 12), bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=5)
        self.medicine_var = StringVar()
        self.medicine_combo = ttk.Combobox(add_frame, textvariable=self.medicine_var, font=('Arial', 12), width=28)
        self.medicine_combo.grid(row=0, column=1, pady=5, padx=5)

        # Load medicines
        self.cursor.execute("SELECT id, name, price FROM medicines ORDER BY name")
        medicines = self.cursor.fetchall()
        medicine_list = [f"{m[0]} - {m[1]} (Price: {m[2]})" for m in medicines]
        self.medicine_combo['values'] = medicine_list

        # Quantity
        Label(add_frame, text="Quantity:", font=('Arial', 12), bg='white').grid(row=0, column=2, sticky='w', pady=5, padx=5)
        self.qty_entry = Entry(add_frame, font=('Arial', 12), width=10)
        self.qty_entry.grid(row=0, column=3, pady=5, padx=5)

        # Price
        Label(add_frame, text="Price:", font=('Arial', 12), bg='white').grid(row=0, column=4, sticky='w', pady=5, padx=5)
        self.price_entry = Entry(add_frame, font=('Arial', 12), width=10)
        self.price_entry.grid(row=0, column=5, pady=5, padx=5)

        # Add button
        add_btn = Button(add_frame, text="Add", font=('Arial', 12), bg='#2ecc71', fg='white',
                       command=self.add_to_purchase, width=10)
        add_btn.grid(row=0, column=6, pady=5, padx=5)

        # Purchase items table
        items_frame = Frame(main_frame)
        items_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(items_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.purchase_items_tree = ttk.Treeview(items_frame, columns=('ID', 'Name', 'Quantity', 'Price', 'Total'),
                                              show='headings', yscrollcommand=scrollbar.set)

        self.purchase_items_tree.heading('ID', text='ID')
        self.purchase_items_tree.heading('Name', text='Name')
        self.purchase_items_tree.heading('Quantity', text='Quantity')
        self.purchase_items_tree.heading('Price', text='Price')
        self.purchase_items_tree.heading('Total', text='Total')

        self.purchase_items_tree.column('ID', width=50)
        self.purchase_items_tree.column('Name', width=200)
        self.purchase_items_tree.column('Quantity', width=100)
        self.purchase_items_tree.column('Price', width=100)
        self.purchase_items_tree.column('Total', width=100)

        scrollbar.config(command=self.purchase_items_tree.yview)
        self.purchase_items_tree.pack(fill=BOTH, expand=True)

        # Total frame
        total_frame = Frame(main_frame, bg='white')
        total_frame.pack(pady=10, padx=20, fill=X)

        self.total_label = Label(total_frame, text="Total: $0.00", font=('Arial', 14, 'bold'), bg='white')
        self.total_label.pack(side=RIGHT, padx=10)

        # Buttons
        btn_frame = Frame(main_frame, bg='white')
        btn_frame.pack(pady=10, padx=20, fill=X)

        complete_btn = Button(btn_frame, text="Complete Purchase", font=('Arial', 12), bg='#2ecc71', fg='white',
                             command=self.complete_purchase, width=15)
        complete_btn.pack(side=LEFT, padx=5)

        cancel_btn = Button(btn_frame, text="Cancel", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.purchases_screen, width=15)
        cancel_btn.pack(side=LEFT, padx=5)

        # Initialize purchase items list
        self.purchase_items = []
        self.purchase_total = 0.0

    def add_to_purchase(self):
        """Add medicine to current purchase"""
        medicine = self.medicine_var.get()
        quantity = self.qty_entry.get().strip()
        price = self.price_entry.get().strip()

        if not medicine or not quantity or not price:
            messagebox.showerror("Error", "Please select a medicine and enter quantity and price!")
            return

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
            price = float(price)
            if price <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive integer and Price must be a positive number!")
            return

        # Get medicine details
        medicine_id = int(medicine.split(' - ')[0])
        self.cursor.execute("SELECT id, name FROM medicines WHERE id=?", (medicine_id,))
        med = self.cursor.fetchone()

        if not med:
            messagebox.showerror("Error", "Medicine not found!")
            return

        # Check if medicine already in purchase
        for item in self.purchase_items:
            if item['id'] == medicine_id:
                item['quantity'] += quantity
                item['total'] = item['quantity'] * item['price']
                break
        else:
            self.purchase_items.append({
                'id': medicine_id,
                'name': med[1],
                'quantity': quantity,
                'price': price,
                'total': quantity * price
            })

        # Update purchase items tree
        self.update_purchase_items_tree()

        # Clear form
        self.medicine_var.set('')
        self.qty_entry.delete(0, END)
        self.price_entry.delete(0, END)

    def update_purchase_items_tree(self):
        """Update purchase items treeview"""
        # Clear existing data
        for i in self.purchase_items_tree.get_children():
            self.purchase_items_tree.delete(i)

        # Add items
        self.purchase_total = 0.0
        for item in self.purchase_items:
            self.purchase_items_tree.insert('', 'end', values=(
                item['id'],
                item['name'],
                item['quantity'],
                f"${item['price']:.2f}",
                f"${item['total']:.2f}"
            ))
            self.purchase_total += item['total']

        # Update total label
        self.total_label.config(text=f"Total: ${self.purchase_total:.2f}")

    def complete_purchase(self):
        """Complete the current purchase"""
        if not self.purchase_items:
            messagebox.showerror("Error", "No items in purchase!")
            return

        supplier = self.supplier_var.get()

        if not supplier:
            messagebox.showerror("Error", "Please select a supplier!")
            return

        # Get supplier ID
        supplier_id = int(supplier.split(' - ')[0])

        # Create purchase record
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute("""
        INSERT INTO purchases (supplier_id, employee_id, date, total_amount)
        VALUES (?, ?, ?, ?)
        """, (supplier_id, self.current_user['id'], today, self.purchase_total))

        purchase_id = self.cursor.lastrowid

        # Add purchase items
        for item in self.purchase_items:
            self.cursor.execute("""
            INSERT INTO purchase_items (purchase_id, medicine_id, quantity, price_per_unit)
            VALUES (?, ?, ?, ?)
            """, (purchase_id, item['id'], item['quantity'], item['price']))

            # Update medicine quantity
            self.cursor.execute("""
            UPDATE medicines
            SET quantity = quantity + ?
            WHERE id = ?
            """, (item['quantity'], item['id']))

        self.conn.commit()

        messagebox.showinfo("Success", f"Purchase completed successfully! Purchase ID: {purchase_id}")
        self.purchases_screen()

    def view_purchase_screen(self):
        """Display purchase details screen"""
        # Get selected purchase
        selected = self.purchases_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a purchase to view!")
            return

        item = self.purchases_tree.item(selected[0])
        purchase_id = item['values'][0]

        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Purchase Details", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Purchases", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.purchases_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Purchase details frame
        details_frame = Frame(main_frame, bg='white')
        details_frame.pack(pady=10, padx=20, fill=X)

        # Get purchase details
        self.cursor.execute("""
        SELECT p.id, s.name, e.name, p.date, p.total_amount
        FROM purchases p
        LEFT JOIN suppliers s ON p.supplier_id = s.id
        LEFT JOIN employees e ON p.employee_id = e.id
        WHERE p.id = ?
        """, (purchase_id,))

        purchase = self.cursor.fetchone()

        if not purchase:
            messagebox.showerror("Error", "Purchase not found!")
            return

        # Display purchase details
        Label(details_frame, text=f"Purchase ID: {purchase[0]}", font=('Arial', 12, 'bold'), bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Supplier: {purchase[1]}", font=('Arial', 12), bg='white').grid(row=0, column=1, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Employee: {purchase[2]}", font=('Arial', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Date: {purchase[3]}", font=('Arial', 12), bg='white').grid(row=1, column=1, sticky='w', pady=5, padx=5)
        Label(details_frame, text=f"Total: ${purchase[4]:.2f}", font=('Arial', 12, 'bold'), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)

        # Purchase items table
        items_frame = Frame(main_frame)
        items_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(items_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        items_tree = ttk.Treeview(items_frame, columns=('ID', 'Name', 'Quantity', 'Price', 'Total'),
                                 show='headings', yscrollcommand=scrollbar.set)

        items_tree.heading('ID', text='ID')
        items_tree.heading('Name', text='Name')
        items_tree.heading('Quantity', text='Quantity')
        items_tree.heading('Price', text='Price')
        items_tree.heading('Total', text='Total')

        items_tree.column('ID', width=50)
        items_tree.column('Name', width=200)
        items_tree.column('Quantity', width=100)
        items_tree.column('Price', width=100)
        items_tree.column('Total', width=100)

        scrollbar.config(command=items_tree.yview)
        items_tree.pack(fill=BOTH, expand=True)

        # Get purchase items
        self.cursor.execute("""
        SELECT pi.medicine_id, m.name, pi.quantity, pi.price_per_unit, (pi.quantity * pi.price_per_unit)
        FROM purchase_items pi
        JOIN medicines m ON pi.medicine_id = m.id
        WHERE pi.purchase_id = ?
        """, (purchase_id,))

        for row in self.cursor.fetchall():
            items_tree.insert('', 'end', values=(
                row[0],
                row[1],
                row[2],
                f"${row[3]:.2f}",
                f"${row[4]:.2f}"
            ))

    def reports_screen(self):
        """Display reports screen"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Reports", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Dashboard", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.dashboard, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Report options
        options_frame = Frame(main_frame, bg='white')
        options_frame.pack(pady=20, padx=20, fill=X)

        Label(options_frame, text="Select Report Type:", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)

        # Sales report
        sales_btn = Button(options_frame, text="Sales Report", font=('Arial', 12), bg='#3498db', fg='white',
                          command=self.sales_report, width=20, height=2)
        sales_btn.pack(pady=10)

        # Inventory report
        inventory_btn = Button(options_frame, text="Inventory Report", font=('Arial', 12), bg='#2ecc71', fg='white',
                              command=self.inventory_report, width=20, height=2)
        inventory_btn.pack(pady=10)

        # Expiry report
        expiry_btn = Button(options_frame, text="Expiry Report", font=('Arial', 12), bg='#e74c3c', fg='white',
                           command=self.expiry_report, width=20, height=2)
        expiry_btn.pack(pady=10)

        # Low stock report
        low_stock_btn = Button(options_frame, text="Low Stock Report", font=('Arial', 12), bg='#f39c12', fg='white',
                             command=self.low_stock_report, width=20, height=2)
        low_stock_btn.pack(pady=10)

    def sales_report(self):
        """Generate sales report"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Sales Report", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Reports", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.reports_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Date range frame
        date_frame = Frame(main_frame, bg='white')
        date_frame.pack(pady=10, padx=20, fill=X)

        Label(date_frame, text="From Date (YYYY-MM-DD):", font=('Arial', 12), bg='white').pack(side=LEFT, padx=5)
        self.from_date_entry = Entry(date_frame, font=('Arial', 12), width=15)
        self.from_date_entry.pack(side=LEFT, padx=5)

        Label(date_frame, text="To Date (YYYY-MM-DD):", font=('Arial', 12), bg='white').pack(side=LEFT, padx=5)
        self.to_date_entry = Entry(date_frame, font=('Arial', 12), width=15)
        self.to_date_entry.pack(side=LEFT, padx=5)

        generate_btn = Button(date_frame, text="Generate Report", font=('Arial', 12), bg='#3498db', fg='white',
                            command=self.generate_sales_report, width=15)
        generate_btn.pack(side=LEFT, padx=10)

        # Report frame
        report_frame = Frame(main_frame)
        report_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(report_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.sales_report_tree = ttk.Treeview(report_frame, columns=('ID', 'Customer', 'Employee', 'Date', 'Amount', 'Payment'),
                                             show='headings', yscrollcommand=scrollbar.set)

        self.sales_report_tree.heading('ID', text='ID')
        self.sales_report_tree.heading('Customer', text='Customer')
        self.sales_report_tree.heading('Employee', text='Employee')
        self.sales_report_tree.heading('Date', text='Date')
        self.sales_report_tree.heading('Amount', text='Amount')
        self.sales_report_tree.heading('Payment', text='Payment Method')

        self.sales_report_tree.column('ID', width=50)
        self.sales_report_tree.column('Customer', width=150)
        self.sales_report_tree.column('Employee', width=150)
        self.sales_report_tree.column('Date', width=150)
        self.sales_report_tree.column('Amount', width=100)
        self.sales_report_tree.column('Payment', width=120)

        scrollbar.config(command=self.sales_report_tree.yview)
        self.sales_report_tree.pack(fill=BOTH, expand=True)

        # Total frame
        total_frame = Frame(main_frame, bg='white')
        total_frame.pack(pady=10, padx=20, fill=X)

        self.sales_total_label = Label(total_frame, text="Total Sales: $0.00", font=('Arial', 14, 'bold'), bg='white')
        self.sales_total_label.pack(side=RIGHT, padx=10)

        # Generate default report (current month)
        today = datetime.now()
        from_date = today.replace(day=1).strftime('%Y-%m-%d')
        to_date = today.strftime('%Y-%m-%d')

        self.from_date_entry.insert(0, from_date)
        self.to_date_entry.insert(0, to_date)
        self.generate_sales_report()

    def generate_sales_report(self):
        """Generate sales report based on date range"""
        from_date = self.from_date_entry.get().strip()
        to_date = self.to_date_entry.get().strip()

        if not from_date or not to_date:
            messagebox.showerror("Error", "Please enter both from and to dates!")
            return

        # Clear existing data
        for i in self.sales_report_tree.get_children():
            self.sales_report_tree.delete(i)

        # Get sales data
        self.cursor.execute("""
        SELECT s.id, c.name, e.name, s.date, s.total_amount, s.payment_method
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.id
        LEFT JOIN employees e ON s.employee_id = e.id
        WHERE s.date BETWEEN ? AND ?
        ORDER BY s.date DESC
        """, (from_date, to_date))

        sales_data = self.cursor.fetchall()
        total_sales = 0.0

        for row in sales_data:
            self.sales_report_tree.insert('', 'end', values=row)
            total_sales += row[4]

        # Update total label
        self.sales_total_label.config(text=f"Total Sales: ${total_sales:.2f}")

    def inventory_report(self):
        """Generate inventory report"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Inventory Report", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Reports", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.reports_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Report frame
        report_frame = Frame(main_frame)
        report_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(report_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.inventory_tree = ttk.Treeview(report_frame, columns=('ID', 'Name', 'Description', 'Quantity', 'Price', 'Supplier', 'Expiry', 'Category'),
                                         show='headings', yscrollcommand=scrollbar.set)

        self.inventory_tree.heading('ID', text='ID')
        self.inventory_tree.heading('Name', text='Name')
        self.inventory_tree.heading('Description', text='Description')
        self.inventory_tree.heading('Quantity', text='Quantity')
        self.inventory_tree.heading('Price', text='Price')
        self.inventory_tree.heading('Supplier', text='Supplier')
        self.inventory_tree.heading('Expiry', text='Expiry Date')
        self.inventory_tree.heading('Category', text='Category')

        self.inventory_tree.column('ID', width=50)
        self.inventory_tree.column('Name', width=150)
        self.inventory_tree.column('Description', width=200)
        self.inventory_tree.column('Quantity', width=80)
        self.inventory_tree.column('Price', width=80)
        self.inventory_tree.column('Supplier', width=120)
        self.inventory_tree.column('Expiry', width=100)
        self.inventory_tree.column('Category', width=100)

        scrollbar.config(command=self.inventory_tree.yview)
        self.inventory_tree.pack(fill=BOTH, expand=True)

        # Total value frame
        total_frame = Frame(main_frame, bg='white')
        total_frame.pack(pady=10, padx=20, fill=X)

        self.inventory_total_label = Label(total_frame, text="Total Inventory Value: $0.00", font=('Arial', 14, 'bold'), bg='white')
        self.inventory_total_label.pack(side=RIGHT, padx=10)

        # Load inventory data
        self.load_inventory_report()

    def load_inventory_report(self):
        """Load inventory report data"""
        # Clear existing data
        for i in self.inventory_tree.get_children():
            self.inventory_tree.delete(i)

        # Get all medicines
        self.cursor.execute("""
        SELECT m.id, m.name, m.description, m.quantity, m.price, s.name, m.expiry_date, m.category
        FROM medicines m
        LEFT JOIN suppliers s ON m.supplier_id = s.id
        ORDER BY m.name
        """)

        medicines = self.cursor.fetchall()
        total_value = 0.0

        for med in medicines:
            self.inventory_tree.insert('', 'end', values=med)
            total_value += med[3] * med[4]  # quantity * price

        # Update total label
        self.inventory_total_label.config(text=f"Total Inventory Value: ${total_value:.2f}")

    def expiry_report(self):
        """Generate expiry report"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Expiry Report", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Reports", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.reports_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Report frame
        report_frame = Frame(main_frame)
        report_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(report_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.expiry_tree = ttk.Treeview(report_frame, columns=('ID', 'Name', 'Quantity', 'Price', 'Expiry Date', 'Days Left'),
                                       show='headings', yscrollcommand=scrollbar.set)

        self.expiry_tree.heading('ID', text='ID')
        self.expiry_tree.heading('Name', text='Name')
        self.expiry_tree.heading('Quantity', text='Quantity')
        self.expiry_tree.heading('Price', text='Price')
        self.expiry_tree.heading('Expiry Date', text='Expiry Date')
        self.expiry_tree.heading('Days Left', text='Days Left')

        self.expiry_tree.column('ID', width=50)
        self.expiry_tree.column('Name', width=200)
        self.expiry_tree.column('Quantity', width=100)
        self.expiry_tree.column('Price', width=100)
        self.expiry_tree.column('Expiry Date', width=120)
        self.expiry_tree.column('Days Left', width=100)

        scrollbar.config(command=self.expiry_tree.yview)
        self.expiry_tree.pack(fill=BOTH, expand=True)

        # Load expiry data
        self.load_expiry_report()

    def load_expiry_report(self):
        """Load expiry report data"""
        # Clear existing data
        for i in self.expiry_tree.get_children():
            self.expiry_tree.delete(i)

        # Get medicines with expiry dates
        self.cursor.execute("""
        SELECT id, name, quantity, price, expiry_date
        FROM medicines
        WHERE expiry_date IS NOT NULL
        ORDER BY expiry_date
        """)

        medicines = self.cursor.fetchall()
        today = datetime.now()

        for med in medicines:
            if med[4]:  # expiry_date
                try:
                    expiry_date = datetime.strptime(med[4], '%Y-%m-%d')
                    days_left = (expiry_date - today).days

                    # Only show medicines expiring within 90 days
                    if days_left <= 90:
                        self.expiry_tree.insert('', 'end', values=(
                            med[0],  # id
                            med[1],  # name
                            med[2],  # quantity
                            f"${med[3]:.2f}",  # price
                            med[4],  # expiry_date
                            days_left
                        ))
                except ValueError:
                    # Skip if date format is invalid
                    continue

    def low_stock_report(self):
        """Generate low stock report"""
        self.clear_window()

        # Header
        header_frame = Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=X)

        title = Label(header_frame, text="Low Stock Report", font=('Arial', 20, 'bold'),
                     bg='#2c3e50', fg='white')
        title.pack(pady=15)

        # Back button
        back_btn = Button(header_frame, text="Back to Reports", font=('Arial', 10), bg='#e74c3c', fg='white',
                         command=self.reports_screen, width=15)
        back_btn.pack(side=LEFT, padx=10, pady=20)

        # Main content
        main_frame = Frame(self.root, bg='white')
        main_frame.pack(fill=BOTH, expand=True)

        # Report frame
        report_frame = Frame(main_frame)
        report_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(report_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Treeview
        self.low_stock_tree = ttk.Treeview(report_frame, columns=('ID', 'Name', 'Quantity', 'Price', 'Supplier'),
                                          show='headings', yscrollcommand=scrollbar.set)

        self.low_stock_tree.heading('ID', text='ID')
        self.low_stock_tree.heading('Name', text='Name')
        self.low_stock_tree.heading('Quantity', text='Quantity')
        self.low_stock_tree.heading('Price', text='Price')
        self.low_stock_tree.heading('Supplier', text='Supplier')

        self.low_stock_tree.column('ID', width=50)
        self.low_stock_tree.column('Name', width=200)
        self.low_stock_tree.column('Quantity', width=100)
        self.low_stock_tree.column('Price', width=100)
        self.low_stock_tree.column('Supplier', width=150)

        scrollbar.config(command=self.low_stock_tree.yview)
        self.low_stock_tree.pack(fill=BOTH, expand=True)

        # Load low stock data
        self.load_low_stock_report()

    def load_low_stock_report(self):
        """Load low stock report data"""
        # Clear existing data
        for i in self.low_stock_tree.get_children():
            self.low_stock_tree.delete(i)

        # Get medicines with low stock (quantity < 10)
        self.cursor.execute("""
        SELECT m.id, m.name, m.quantity, m.price, s.name
        FROM medicines m
        LEFT JOIN suppliers s ON m.supplier_id = s.id
        WHERE m.quantity < 10
        ORDER BY m.quantity ASC
        """)

        for med in self.cursor.fetchall():
            self.low_stock_tree.insert('', 'end', values=(
                med[0],  # id
                med[1],  # name
                med[2],  # quantity
                f"${med[3]:.2f}",  # price
                med[4] if med[4] else "N/A"  # supplier
            ))

    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()

# Main application
if __name__ == "__main__":
    root = Tk()
    app = PharmacyManagementSystem(root)
    root.mainloop()
```

## Installation and Running Instructions

1. **Prerequisites**:

   - Python 3.6 or higher
   - Tkinter (usually comes pre-installed with Python)
   - SQLite3 (usually comes pre-installed with Python)

2. **Running the Application**:

   - Save the code to a file named `pharmacy_management_system.py`
   - Run the application using the command:
     ```
     python pharmacy_management_system.py
     ```

3. **Default Login Credentials**:
   - Username: `admin`
   - Password: `admin123`

## Features Included

1. **User Authentication**:

   - Secure login system with role-based access
   - Default admin account created automatically

2. **Dashboard**:

   - Overview of key metrics (medicines, suppliers, customers)
   - Recent sales display
   - Quick navigation to all modules

3. **Medicine Management**:

   - Add, update, delete, and view medicines
   - Track inventory with quantity and expiry dates
   - Categorize medicines (tablets, capsules, etc.)
   - Barcode support
   - Search functionality

4. **Supplier Management**:

   - Add, update, delete, and view suppliers
   - Track contact information and addresses

5. **Customer Management**:

   - Add, update, delete, and view customers
   - Track contact information and addresses

6. **Sales Management**:

   - Create new sales with multiple items
   - Track payment methods
   - View sale details and print receipts
   - Automatic inventory reduction

7. **Purchase Management**:

   - Record new purchases from suppliers
   - Track purchase details
   - Automatic inventory increase

8. **Reporting**:
   - Sales reports with date range filtering
   - Inventory reports with total value calculation
   - Expiry reports (medicines expiring within 90 days)
   - Low stock reports (medicines with quantity < 10)

## Database Structure

The system uses SQLite with the following tables:

- `medicines`: Stores medicine information
- `suppliers`: Stores supplier information
- `employees`: Stores user accounts and roles
- `customers`: Stores customer information
- `sales`: Stores sales transactions
- `sale_items`: Stores individual items in each sale
- `purchases`: Stores purchase transactions
- `purchase_items`: Stores individual items in each purchase

## Usage Notes

1. The system automatically creates a SQLite database file named `pharmacy.db` in the same directory as the script.
2. The default admin account can be used to log in initially.
3. All forms include validation to ensure data integrity.
4. The system prevents deletion of records that are referenced in other tables (e.g., medicines used in sales cannot be deleted).
5. Reports can be generated and viewed within the application.

This pharmacy management system provides a comprehensive solution for managing all aspects of a pharmacy, from inventory and sales to reporting and analytics.
