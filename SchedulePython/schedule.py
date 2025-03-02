"""
Employee Scheduling System
--------------------------
Features:
- Reads employee preferences from file
- Assigns shifts while respecting constraints:
  1. No employee works >1 shift/day
  2. Max 5 days/week per employee
  3. Minimum 2 employees per shift
- Handles shift conflicts and understaffing
- Balances workload across employees
- Outputs weekly schedule

Input File Format:
- First line: Total number of employees
- For each employee:
  - Name (single line)
  - 7 lines of shift preferences (one per day)
  - Each day line contains 3 space-separated shifts in preference order
"""

import random
from dataclasses import dataclass, field
from typing import List, Dict

# Constants
DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", 
               "Friday", "Saturday", "Sunday"]
SHIFTS = ["morning", "afternoon", "evening"]

@dataclass
class Employee:
    """Represents an employee with scheduling information"""
    name: str
    preferences: Dict[str, List[str]] = field(default_factory=dict)
    assigned_shifts: List[List[str]] = field(default_factory=list)
    days_worked: int = 0

    def can_work(self, day: str, shift: str) -> bool:
        """Check if employee is eligible to work a specific shift"""
        return (self.days_worked < 5 and 
                not self.has_shift_on_day(day) and 
                not self.is_assigned_to_shift(day, shift))

    def has_shift_on_day(self, day: str) -> bool:
        """Check if employee has any shift on given day"""
        return any(shift[0] == day for shift in self.assigned_shifts)

    def is_assigned_to_shift(self, day: str, shift: str) -> bool:
        """Check if employee is already assigned to specific shift"""
        return any(s[0] == day and s[1] == shift for s in self.assigned_shifts)

class EmployeeScheduler:
    """Main scheduler class containing business logic"""
    
    def __init__(self):
        self.employees: Dict[str, Employee] = {}

    def import_preferences_from_file(self, file_path: str) -> None:
        """
        Read employee preferences from text file
        Args:
            file_path: Path to input file
        Raises:
            ValueError: On invalid input format
            FileNotFoundError: If file doesn't exist
        """
        try:
            with open(file_path, 'r') as f:
                num_employees = int(f.readline().strip())
                if num_employees < 6:
                    print("Warning: Minimum 6 employees recommended for proper coverage")
                
                for _ in range(num_employees):
                    name = f.readline().strip()
                    employee = Employee(name=name)
                    
                    for day in DAYS_OF_WEEK:
                        prefs = f.readline().strip().lower().split()
                        if len(prefs) != 3:
                            raise ValueError(f"Invalid preferences for {name} on {day}")
                        if any(shift not in SHIFTS for shift in prefs):
                            raise ValueError(f"Invalid shift in preferences for {name}")
                        employee.preferences[day] = prefs
                    
                    self.employees[name] = employee
        except FileNotFoundError:
            raise
        except Exception as e:
            raise ValueError(f"Invalid file format: {str(e)}")

    def assign_shifts(self) -> None:
        """Main shift assignment logic with three phases:
        1. Assign based on employee preferences
        2. Fill remaining slots with least-busy employees
        3. Final assignment with capacity checks
        """
        # Phase 1: Preference-based assignment
        for day in DAYS_OF_WEEK:
            for shift in SHIFTS:
                candidates = []
                
                # Collect qualified candidates with preference priority
                for emp in self.employees.values():
                    if emp.can_work(day, shift):
                        try:
                            priority = emp.preferences[day].index(shift)
                            candidates.append((emp.name, priority))
                        except ValueError:
                            continue
                
                # Sort by preference priority
                candidates.sort(key=lambda x: x[1])
                selected = [name for name, _ in candidates]
                
                # Phase 2: Fill remaining slots randomly
                while len(selected) < 2:
                    available = [
                        emp for emp in self.employees.values()
                        if emp.can_work(day, shift) and emp.name not in selected
                    ]
                    
                    if not available:
                        break
                    
                    # Prioritize by days worked and randomize
                    available.sort(key=lambda x: x.days_worked)
                    random.shuffle(available)  # Randomize equally busy employees
                    selected.append(available[0].name)
                
                # Phase 3: Final assignment
                for name in selected[:2]:  # Take max 2 employees
                    emp = self.employees[name]
                    if emp.days_worked < 5:
                        emp.assigned_shifts.append([day, shift])
                        emp.days_worked += 1

    def resolve_conflicts(self) -> None:
        """Conflict resolution and shift filling
        Ensures all shifts have minimum 2 employees
        """
        for day in DAYS_OF_WEEK:
            for shift in SHIFTS:
                while self.count_assigned(day, shift) < 2:
                    candidates = [
                        emp for emp in self.employees.values()
                        if emp.days_worked < 5 and
                        emp.can_work(day, shift) and
                        not emp.has_shift_on_day(day)
                    ]
                    
                    if not candidates:
                        print(f"Critical: Unable to fill {day} {shift}")
                        break
                    
                    # Random selection from least busy employees
                    candidates.sort(key=lambda x: x.days_worked)
                    random.shuffle(candidates)
                    chosen = candidates[0]
                    
                    chosen.assigned_shifts.append([day, shift])
                    chosen.days_worked += 1

    def count_assigned(self, day: str, shift: str) -> int:
        """Count employees assigned to a specific shift"""
        return sum(
            1 for emp in self.employees.values()
            if any(s[0] == day and s[1] == shift for s in emp.assigned_shifts)
        )

    def display_schedule(self) -> None:
        """Display the final schedule in readable format"""
        print("\nFinal Schedule:")
        for day in DAYS_OF_WEEK:
            print(f"\n{day}:")
            for shift in SHIFTS:
                workers = [
                    emp.name for emp in self.employees.values()
                    if any(s[0] == day and s[1] == shift for s in emp.assigned_shifts)
                ]
                print(f"{shift.title():<10}: {', '.join(workers) if workers else 'Unstaffed'}")

    def validate_schedule(self) -> bool:
        """Post-schedule validation
        Returns True if all shifts are properly staffed"""
        all_ok = True
        for day in DAYS_OF_WEEK:
            for shift in SHIFTS:
                count = self.count_assigned(day, shift)
                if count < 2:
                    print(f"Warning: {day} {shift} understaffed ({count} employees)")
                    all_ok = False
        return all_ok

def main():
    """Main execution function"""
    try:
        scheduler = EmployeeScheduler()
        file_path = "employees.txt"  # Update this path as needed
        
        # Load and process data
        scheduler.import_preferences_from_file(file_path)
        scheduler.assign_shifts()
        scheduler.resolve_conflicts()
        
        # Display results
        scheduler.display_schedule()
        
        # Final validation
        if scheduler.validate_schedule():
            print("\nAll shifts properly staffed!")
        else:
            print("\nSome shifts understaffed - check warnings above")

    except FileNotFoundError:
        print("Error: Input file not found")
    except ValueError as e:
        print(f"Input Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")

if __name__ == "__main__":
    main()