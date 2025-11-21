import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import os
import threading

class InventoryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("900x650")
        self.root.configure(bg='#f5f5f5')
        
        # C program executable name
        self.c_program = "inventory_system.exe"
        
        # Check if C program exists, if not compile it
        self.compile_c_program()
        
        # Create login interface
        self.create_login_interface()
    
    def compile_c_program(self):
        """Compile the C program if it doesn't exist"""
        if not os.path.exists(self.c_program):
            try:
                result = subprocess.run([
                    "gcc", "FPFLP.c", "-o", self.c_program
                ], capture_output=True, text=True, shell=True)
                
                if result.returncode != 0:
                    messagebox.showwarning(
                        "Compilation Warning", 
                        "C program couldn't be compiled. Some features may not work.\n"
                        "Make sure you have GCC installed."
                    )
            except Exception as e:
                messagebox.showwarning(
                    "Compilation Warning", 
                    f"Could not compile C program: {str(e)}\n"
                    "Some features may not work."
                )
    
    def create_login_interface(self):
        """Create the login interface"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main login frame
        login_frame = tk.Frame(self.root, bg='#f5f5f5', padx=40, pady=40)
        login_frame.pack(expand=True)
        
        # Title
        title_label = tk.Label(
            login_frame, 
            text="Inventory Management System", 
            font=("Arial", 20, "bold"),
            bg='#f5f5f5',
            fg='#2c3e50'
        )
        title_label.pack(pady=30)
        
        # Login box
        login_box = tk.Frame(login_frame, bg='white', padx=30, pady=30, relief='raised', bd=1)
        login_box.pack(pady=20)
        
        # Username
        tk.Label(login_box, text="Username:", font=("Arial", 12), bg='white').pack(anchor='w', pady=(0, 5))
        self.username_entry = tk.Entry(login_box, width=25, font=("Arial", 12))
        self.username_entry.pack(pady=(0, 15))
        self.username_entry.insert(0, "admin")
        
        # Password
        tk.Label(login_box, text="Password:", font=("Arial", 12), bg='white').pack(anchor='w', pady=(0, 5))
        self.password_entry = tk.Entry(login_box, width=25, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=(0, 20))
        self.password_entry.insert(0, "Fast1234")
        
        # Login button
        login_btn = tk.Button(
            login_box, 
            text="Login", 
            command=self.login,
            bg='#3498db',
            fg='white',
            font=("Arial", 12, "bold"),
            width=15,
            height=2
        )
        login_btn.pack(pady=10)
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.login())
    
    def login(self):
        """Handle login"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == "admin" and password == "Fast1234":
            self.create_main_interface()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")
    
    def create_main_interface(self):
        """Create the main application interface"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create main container
        main_container = tk.Frame(self.root, bg='#f5f5f5')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_container, bg='#2c3e50', padx=20, pady=15)
        header_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(
            header_frame, 
            text="Inventory Management System", 
            font=("Arial", 18, "bold"),
            bg='#2c3e50',
            fg='white'
        ).pack(side='left')
        
        # Create tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill='both', expand=True)
        
        # Create all tabs
        self.create_dashboard_tab()
        self.create_add_item_tab()
        self.create_manage_tab()
        self.create_reports_tab()
        
        # Load initial data
        self.refresh_inventory()
    
    def create_dashboard_tab(self):
        """Create the dashboard/inventory view tab"""
        self.dashboard_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_tab, text="Dashboard")
        
        # Controls frame
        controls_frame = ttk.Frame(self.dashboard_tab)
        controls_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(controls_frame, text="Refresh Inventory", command=self.refresh_inventory).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="Run C Console Version", command=self.run_c_console).pack(side='left', padx=5)
        
        # Inventory display
        inventory_frame = ttk.LabelFrame(self.dashboard_tab, text="Current Inventory", padding=10)
        inventory_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.inventory_text = scrolledtext.ScrolledText(
            inventory_frame, 
            width=80, 
            height=20, 
            font=("Consolas", 10)
        )
        self.inventory_text.pack(fill='both', expand=True)
    
    def create_add_item_tab(self):
        """Create the add item tab"""
        self.add_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.add_tab, text="Add Item")
        
        form_frame = ttk.Frame(self.add_tab, padding=20)
        form_frame.pack(expand=True)
        
        # Item ID
        ttk.Label(form_frame, text="Item ID:", font=("Arial", 11)).grid(row=0, column=0, sticky='w', pady=12)
        self.add_id_entry = ttk.Entry(form_frame, width=25, font=("Arial", 11))
        self.add_id_entry.grid(row=0, column=1, padx=15, pady=12)
        
        # Item Name
        ttk.Label(form_frame, text="Item Name:", font=("Arial", 11)).grid(row=1, column=0, sticky='w', pady=12)
        self.add_name_entry = ttk.Entry(form_frame, width=25, font=("Arial", 11))
        self.add_name_entry.grid(row=1, column=1, padx=15, pady=12)
        
        # Quantity
        ttk.Label(form_frame, text="Quantity:", font=("Arial", 11)).grid(row=2, column=0, sticky='w', pady=12)
        self.add_quantity_entry = ttk.Entry(form_frame, width=25, font=("Arial", 11))
        self.add_quantity_entry.grid(row=2, column=1, padx=15, pady=12)
        
        # Price
        ttk.Label(form_frame, text="Price ($):", font=("Arial", 11)).grid(row=3, column=0, sticky='w', pady=12)
        self.add_price_entry = ttk.Entry(form_frame, width=25, font=("Arial", 11))
        self.add_price_entry.grid(row=3, column=1, padx=15, pady=12)
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=30)
        
        ttk.Button(button_frame, text="Add Item", command=self.add_item).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_add_form).pack(side='left', padx=10)
    
    def create_manage_tab(self):
        """Create the manage inventory tab"""
        self.manage_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.manage_tab, text="Manage Items")
        
        # Sell Item Frame
        sell_frame = ttk.LabelFrame(self.manage_tab, text="Sell Item", padding=15)
        sell_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(sell_frame, text="Item ID:").grid(row=0, column=0, sticky='w', pady=8)
        self.sell_id_entry = ttk.Entry(sell_frame, width=15)
        self.sell_id_entry.grid(row=0, column=1, padx=10, pady=8)
        
        ttk.Label(sell_frame, text="Quantity:").grid(row=0, column=2, sticky='w', pady=8)
        self.sell_quantity_entry = ttk.Entry(sell_frame, width=15)
        self.sell_quantity_entry.grid(row=0, column=3, padx=10, pady=8)
        
        ttk.Button(sell_frame, text="Sell Item", command=self.sell_item).grid(row=0, column=4, padx=10, pady=8)
        
        # Restock Frame
        restock_frame = ttk.LabelFrame(self.manage_tab, text="Restock Item", padding=15)
        restock_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(restock_frame, text="Item ID:").grid(row=0, column=0, sticky='w', pady=8)
        self.restock_id_entry = ttk.Entry(restock_frame, width=15)
        self.restock_id_entry.grid(row=0, column=1, padx=10, pady=8)
        
        ttk.Label(restock_frame, text="Quantity to Add:").grid(row=0, column=2, sticky='w', pady=8)
        self.restock_quantity_entry = ttk.Entry(restock_frame, width=15)
        self.restock_quantity_entry.grid(row=0, column=3, padx=10, pady=8)
        
        ttk.Button(restock_frame, text="Restock", command=self.restock_item).grid(row=0, column=4, padx=10, pady=8)
        
        # Remove Frame
        remove_frame = ttk.LabelFrame(self.manage_tab, text="Remove Item", padding=15)
        remove_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(remove_frame, text="Item ID to Remove:").grid(row=0, column=0, sticky='w', pady=8)
        self.remove_id_entry = ttk.Entry(remove_frame, width=15)
        self.remove_id_entry.grid(row=0, column=1, padx=10, pady=8)
        
        ttk.Button(remove_frame, text="Remove Item", command=self.remove_item).grid(row=0, column=2, padx=10, pady=8)
    
    def create_reports_tab(self):
        """Create the reports tab"""
        self.reports_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.reports_tab, text="Reports")
        
        # Report buttons
        button_frame = ttk.Frame(self.reports_tab, padding=10)
        button_frame.pack(fill='x')
        
        ttk.Button(button_frame, text="Sales Report", command=self.sales_report).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Revenue Report", command=self.revenue_report).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Save Inventory", command=self.save_inventory).pack(side='left', padx=5)
        
        # Reports display
        report_display_frame = ttk.Frame(self.reports_tab)
        report_display_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.report_text = scrolledtext.ScrolledText(
            report_display_frame, 
            width=80, 
            height=20, 
            font=("Consolas", 10)
        )
        self.report_text.pack(fill='both', expand=True)
    
    def run_c_command(self, inputs, success_message):
        """Run C program with given inputs and show result"""
        def run_command():
            try:
                # Prepare input string
                input_str = "\n".join(str(x) for x in inputs) + "\n"
                
                # Run the C program
                result = subprocess.run(
                    [self.c_program],
                    input=input_str,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                # Check result and show message
                if result.returncode == 0:
                    self.root.after(0, lambda: messagebox.showinfo("Success", success_message))
                    self.root.after(0, self.refresh_inventory)
                else:
                    error_msg = result.stderr if result.stderr else "Unknown error occurred"
                    self.root.after(0, lambda: messagebox.showerror("Error", f"Operation failed:\n{error_msg}"))
                    
            except subprocess.TimeoutExpired:
                self.root.after(0, lambda: messagebox.showerror("Error", "Operation timed out"))
            except Exception as error:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Operation failed: {str(error)}"))
        
        # Run in separate thread to prevent freezing
        thread = threading.Thread(target=run_command, daemon=True)
        thread.start()
    
    def add_item(self):
        """Add a new item to inventory"""
        try:
            item_id = int(self.add_id_entry.get())
            name = self.add_name_entry.get()
            quantity = int(self.add_quantity_entry.get())
            price = float(self.add_price_entry.get())
            
            if not name:
                messagebox.showerror("Error", "Please enter item name")
                return
            
            # Input sequence for C program: login -> add item -> exit
            inputs = [
                "admin", "Fast1234",  # Login
                1,                    # Add item option
                item_id, name, quantity, price,  # Item details
                10                    # Exit
            ]
            
            self.run_c_command(inputs, f"Item '{name}' added successfully!")
            self.clear_add_form()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for ID, Quantity, and Price")
    
    def sell_item(self):
        """Sell an item"""
        try:
            item_id = int(self.sell_id_entry.get())
            quantity = int(self.sell_quantity_entry.get())
            
            inputs = [
                "admin", "Fast1234",  # Login
                2,                    # Sell item option
                item_id, quantity,    # Sale details
                10                    # Exit
            ]
            
            self.run_c_command(inputs, f"Sold {quantity} units of item {item_id}")
            self.sell_id_entry.delete(0, tk.END)
            self.sell_quantity_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
    
    def restock_item(self):
        """Restock an item"""
        try:
            item_id = int(self.restock_id_entry.get())
            quantity = int(self.restock_quantity_entry.get())
            
            inputs = [
                "admin", "Fast1234",  # Login
                4,                    # Restock option
                item_id, quantity,    # Restock details
                10                    # Exit
            ]
            
            self.run_c_command(inputs, f"Restocked {quantity} units to item {item_id}")
            self.restock_id_entry.delete(0, tk.END)
            self.restock_quantity_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
    
    def remove_item(self):
        """Remove an item"""
        try:
            item_id = int(self.remove_id_entry.get())
            
            inputs = [
                "admin", "Fast1234",  # Login
                6,                    # Remove item option
                item_id,              # Item to remove
                10                    # Exit
            ]
            
            self.run_c_command(inputs, f"Item {item_id} removed successfully")
            self.remove_id_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid item ID")
    
    def sales_report(self):
        """Generate sales report"""
        inputs = [
            "admin", "Fast1234",  # Login
            8,                    # Sales report option
            10                    # Exit
        ]
        
        self.generate_report(inputs, "Sales Report")
    
    def revenue_report(self):
        """Generate revenue report"""
        inputs = [
            "admin", "Fast1234",  # Login
            5,                    # Revenue report option
            10                    # Exit
        ]
        
        self.generate_report(inputs, "Revenue Report")
    
    def generate_report(self, inputs, report_name):
        """Generate and display a report"""
        def run_report():
            try:
                input_str = "\n".join(str(x) for x in inputs) + "\n"
                
                result = subprocess.run(
                    [self.c_program],
                    input=input_str,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    report_content = f"=== {report_name} ===\n\n{result.stdout}"
                    self.root.after(0, lambda: self.display_report(report_content))
                else:
                    error_msg = result.stderr if result.stderr else "Failed to generate report"
                    self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
                    
            except Exception as error:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Report generation failed: {str(error)}"))
        
        thread = threading.Thread(target=run_report, daemon=True)
        thread.start()
    
    def display_report(self, content):
        """Display report content"""
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(1.0, content)
    
    def save_inventory(self):
        """Save inventory to file"""
        inputs = [
            "admin", "Fast1234",  # Login
            9,                    # Save option
            10                    # Exit
        ]
        
        self.run_c_command(inputs, "Inventory saved successfully!")
    
    def refresh_inventory(self):
        """Refresh inventory display by reading the file directly"""
        try:
            if os.path.exists("inventory.txt"):
                with open("inventory.txt", "r") as f:
                    content = f.read()
                
                # Parse and display inventory
                lines = content.strip().split('\n')
                if lines:
                    try:
                        item_count = int(lines[0])
                        display_text = "=== CURRENT INVENTORY ===\n\n"
                        
                        for i in range(1, min(item_count + 1, len(lines))):
                            if ',' in lines[i]:  # Make sure it's an item line
                                parts = lines[i].split(',')
                                if len(parts) >= 4:
                                    item_id = parts[0]
                                    name = parts[1]
                                    quantity = parts[2]
                                    price = parts[3]
                                    display_text += f"ID: {item_id}, Name: {name}, Qty: {quantity}, Price: ${price}\n"
                        
                        self.inventory_text.delete(1.0, tk.END)
                        self.inventory_text.insert(1.0, display_text)
                    except ValueError:
                        self.inventory_text.delete(1.0, tk.END)
                        self.inventory_text.insert(1.0, "Inventory file format error")
            else:
                self.inventory_text.delete(1.0, tk.END)
                self.inventory_text.insert(1.0, "No inventory data found. Add some items first.")
                
        except Exception as e:
            self.inventory_text.delete(1.0, tk.END)
            self.inventory_text.insert(1.0, f"Error reading inventory: {str(e)}")
    
    def clear_add_form(self):
        """Clear the add item form"""
        self.add_id_entry.delete(0, tk.END)
        self.add_name_entry.delete(0, tk.END)
        self.add_quantity_entry.delete(0, tk.END)
        self.add_price_entry.delete(0, tk.END)
    
    def run_c_console(self):
        """Run the original C console program"""
        try:
            subprocess.run([self.c_program])
            self.refresh_inventory()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run C program: {str(e)}")

def main():
    root = tk.Tk()
    app = InventoryGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()