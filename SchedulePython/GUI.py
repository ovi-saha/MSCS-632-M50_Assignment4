"""
Employee Scheduling GUI Application
Integrates with scheduler.py for core logic
"""

# GUI and system imports
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import csv
from schedule import EmployeeScheduler, Employee, DAYS_OF_WEEK, SHIFTS

class SchedulerGUI:
    def __init__(self, root):
        """Initialize main application window"""
        self.root = root
        self.scheduler = EmployeeScheduler()  # Core scheduling logic instance
        self.initialize_gui()

    def initialize_gui(self):
        """Configure main window layout and components"""
        self.root.title("Employee Scheduler v1.0")
        self.root.geometry("1200x800")  # Initial window size
        
        # Main container frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Build UI components
        self.create_input_panel(main_frame)     # Left-side employee management
        self.create_schedule_display(main_frame) # Right-side schedule display
        self.create_controls(main_frame)        # Bottom status bar

    def create_input_panel(self, parent):
        """Create employee management panel (left side)"""
        input_frame = ttk.LabelFrame(parent, text="Employee Management")
        input_frame.pack(side="left", fill="y", padx=5)
        
        # Employee list display using Treeview widget
        self.employee_list = ttk.Treeview(input_frame, columns=("Preferences",), show="headings")
        self.employee_list.heading("#0", text="Employee")  # First column (tree)
        self.employee_list.heading("Preferences", text="Preferences Set")  # Second column
        self.employee_list.pack(padx=5, pady=5, fill="both", expand=True)
        
        # Button container for employee actions
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(pady=5)
        
        # Action buttons with packed layout
        ttk.Button(btn_frame, text="Load File", command=self.load_from_file).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Add New", command=self.add_employee).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Generate", command=self.generate_schedule).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Export", command=self.export_schedule).pack(side="left", padx=2)

    def create_schedule_display(self, parent):
        """Create schedule display area (right side)"""
        display_frame = ttk.LabelFrame(parent, text="Weekly Schedule")
        display_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        # Notebook widget for tabbed day displays
        self.notebook = ttk.Notebook(display_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Create a tab for each day with Treeview schedule
        self.day_views = {}
        for day in DAYS_OF_WEEK:
            # Create frame for each day tab
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=day)
            
            # Treeview for shift assignments
            tree = ttk.Treeview(frame, columns=("Shift", "Employees"), show="headings")
            tree.heading("Shift", text="Shift")
            tree.heading("Employees", text="Employees")
            tree.pack(fill="both", expand=True)
            self.day_views[day] = tree  # Store reference for updates

    def create_controls(self, parent):
        """Create status bar at bottom"""
        self.status = ttk.Label(parent, text="Ready", relief="sunken")
        self.status.pack(side="bottom", fill="x")

    # Employee Management Methods
    def add_employee(self):
        """Add new employee through dialog input"""
        # Get employee name via dialog
        name = simpledialog.askstring("New Employee", "Enter employee name:")
        if name and name not in self.scheduler.employees:
            # Create new Employee instance
            self.scheduler.employees[name] = Employee(name)
            # Collect preferences through dialogs
            self._setup_preferences(name)
            # Refresh employee list display
            self.update_employee_list()

    def _setup_preferences(self, name):
        """Collect shift preferences for each day via dialogs"""
        emp = self.scheduler.employees[name]
        for day in DAYS_OF_WEEK:
            while True:  # Loop until valid input
                # Show input dialog with shift options
                prefs = simpledialog.askstring(
                    f"Preferences for {name}",
                    f"Enter {day} preferences (3 shifts, space-separated):\nOptions: {', '.join(SHIFTS)}",
                    initialvalue=" ".join(SHIFTS)  # Default value
                )
                # Validate and store preferences
                if self._validate_prefs(prefs):
                    emp.preferences[day] = prefs.lower().split()
                    break

    def _validate_prefs(self, prefs):
        """Validate preference input format"""
        if not prefs:  # Empty input check
            return False
        parts = prefs.split()
        # Must have exactly 3 preferences
        if len(parts) != 3:
            messagebox.showerror("Error", "Must enter exactly 3 shifts")
            return False
        # All entries must be valid shift names
        if any(shift.lower() not in SHIFTS for shift in parts):
            messagebox.showerror("Error", "Invalid shifts entered")
            return False
        return True

    def update_employee_list(self):
        """Refresh employee list display"""
        # Clear existing entries
        self.employee_list.delete(*self.employee_list.get_children())
        # Add updated employee data
        for name, emp in self.scheduler.employees.items():
            # Count days with preferences set
            pref_days = sum(1 for _ in emp.preferences.values())
            self.employee_list.insert("", "end", text=name, values=(f"{pref_days}/7 days",))

    # File Operations
    def load_from_file(self):
        """Load employee data from text file"""
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("Text files", "*.txt")],
                title="Select Employee Data File"
            )
            if file_path:
                # Load data through scheduler
                self.scheduler.import_preferences_from_file(file_path)
                # Update UI components
                self.update_employee_list()
                self.status.config(text=f"Loaded {len(self.scheduler.employees)} employees")
        except Exception as e:
            messagebox.showerror("Load Error", str(e))

    # Schedule Operations
    def generate_schedule(self):
        """Generate and display schedule"""
        try:
            # Core scheduling operations
            self.scheduler.assign_shifts()
            self.scheduler.resolve_conflicts()
            # Update GUI display
            self.update_schedule_display()
            self.status.config(text="Schedule generated successfully")
        except Exception as e:
            messagebox.showerror("Generation Error", str(e))

    def update_schedule_display(self):
        """Update schedule display with generated data"""
        for day, tree in self.day_views.items():
            # Clear existing entries
            tree.delete(*tree.get_children())
            # Add new shift assignments
            for shift in SHIFTS:
                # Find employees assigned to this shift
                employees = [
                    emp.name for emp in self.scheduler.employees.values()
                    if any(s[0] == day and s[1] == shift for s in emp.assigned_shifts)
                ]
                # Insert into Treeview
                tree.insert("", "end", values=(shift.title(), ", ".join(employees)))

    def export_schedule(self):
        """Export schedule to CSV file"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")]
            )
            if file_path:
                with open(file_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    # Write header row
                    writer.writerow(["Day", "Shift", "Employees"])
                    # Write data rows
                    for day in DAYS_OF_WEEK:
                        for shift in SHIFTS:
                            employees = [
                                emp.name for emp in self.scheduler.employees.values()
                                if any(s[0] == day and s[1] == shift for s in emp.assigned_shifts)
                            ]
                            writer.writerow([day, shift, ", ".join(employees)])
                self.status.config(text=f"Exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerGUI(root)
    root.mainloop()