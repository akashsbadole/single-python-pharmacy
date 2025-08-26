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