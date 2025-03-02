/**
 * Employee Scheduling System
 * --------------------------
 * Features:
 * - Reads employee preferences from file
 * - Assigns shifts while respecting constraints:
 *   1. No employee works >1 shift/day
 *   2. Max 5 days/week per employee
 *   3. Minimum 2 employees per shift
 * - Handles shift conflicts and understaffing
 * - Balances workload across employees
 * - Outputs weekly schedule
 *
 * Input File Format:
 * - First line: Total number of employees
 * - For each employee:
 *   - Name (single line)
 *   - 7 lines of shift preferences (one per day)
 *   - Each day line contains 3 space-separated shifts in preference order
 */
import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

class Employee {
    // Employee class stores individual worker data
    String name;  // Employee name
    Map<String, List<String>> preferences;  // Daily shift preferences (day -> [ordered shifts])
    List<String[]> assignedShifts;  // List of [day, shift] assignments
    int daysWorked;  // Total days scheduled (max 5)

    Employee(String name) {
        this.name = name;
        this.preferences = new HashMap<>();
        this.assignedShifts = new ArrayList<>();
        this.daysWorked = 0;
    }
}

public class EmployeeScheduler {
    // Constants
    static final List<String> daysOfWeek = Arrays.asList(
            "Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday"
    );
    static final List<String> shifts = Arrays.asList("morning", "afternoon", "evening");
    static final Map<String, Employee> employees = new HashMap<>();

    /**
     * Import employee preferences from text file
     * @param filePath Path to input file
     * @throws FileNotFoundException If file not found
     */
    static void importPreferencesFromFile(String filePath) throws FileNotFoundException {
        File file = new File(filePath);
        Scanner scanner = new Scanner(file);

        // Read number of employees
        int numEmployees = Integer.parseInt(scanner.nextLine().trim());
        if(numEmployees < 6) {
            System.out.println("Warning: Minimum 6 employees recommended for proper coverage");
        }

        // Process each employee
        for (int i = 0; i < numEmployees; i++) {
            String name = scanner.nextLine().trim();
            Employee employee = new Employee(name);

            // Read preferences for each day
            for (String day : daysOfWeek) {
                String[] ranked = scanner.nextLine().trim().toLowerCase().split(" ");

                // Validate input format
                if (ranked.length != 3) {
                    scanner.close();
                    throw new IllegalArgumentException("Invalid preferences for " + name + " on " + day);
                }
                for(String shift : ranked) {
                    if(!shifts.contains(shift)) {
                        throw new IllegalArgumentException("Invalid shift '" + shift + "' for " + name);
                    }
                }

                employee.preferences.put(day, Arrays.asList(ranked));
            }
            employees.put(name, employee);
        }
        scanner.close();
    }

    /**
     * Main shift assignment logic
     * 1. Processes each day/shift combination
     * 2. Prioritizes employees based on preferences
     * 3. Fills remaining slots with available employees
     */
    static void assignShifts() {
        for (String day : daysOfWeek) {
            for (String shift : shifts) {
                List<Map.Entry<String, Integer>> candidates = new ArrayList<>();

                // Phase 1: Collect qualified candidates
                for (Map.Entry<String, Employee> entry : employees.entrySet()) {
                    Employee emp = entry.getValue();
                    if (canWork(emp, day, shift)) {
                        List<String> prefs = emp.preferences.get(day);
                        int priority = prefs.indexOf(shift);
                        if (priority != -1) {
                            // Store with preference priority (lower = better)
                            candidates.add(new AbstractMap.SimpleEntry<>(entry.getKey(), priority));
                        }
                    }
                }

                // Sort candidates by preference priority
                candidates.sort(Map.Entry.comparingByValue());
                List<String> selected = new ArrayList<>();
                for (Map.Entry<String, Integer> e : candidates) {
                    selected.add(e.getKey());
                }

                // Phase 2: Fill remaining slots with least-busy employees
                while (selected.size() < 2) {
                    List<Map.Entry<String, Employee>> available = new ArrayList<>();
                    for (Map.Entry<String, Employee> entry : employees.entrySet()) {
                        Employee emp = entry.getValue();
                        if (canWork(emp, day, shift) && !selected.contains(entry.getKey())) {
                            available.add(entry);
                        }
                    }

                    if (available.isEmpty()) break;

                    // Prioritize employees who work fewer days
                    available.sort(Comparator.comparingInt(e -> e.getValue().daysWorked));
                    // Randomize equally available employees
                    Collections.shuffle(available);
                    selected.add(available.get(0).getKey());
                }

                // Phase 3: Final assignment with capacity check
                for (int i = 0; i < Math.min(2, selected.size()); i++) {
                    Employee emp = employees.get(selected.get(i));
                    if (emp.daysWorked < 5) {
                        emp.assignedShifts.add(new String[]{day, shift});
                        emp.daysWorked++;
                    }
                }
            }
        }
    }

    /**
     * Conflict resolution and shift filling
     * Ensures all shifts have minimum 2 employees
     */
    static void resolveConflicts() {
        // Process each day/shift combination
        for (String day : daysOfWeek) {
            for (String shift : shifts) {
                // Keep filling until shift has 2 employees
                while (countAssigned(day, shift) < 2) {
                    List<Map.Entry<String, Employee>> candidates = new ArrayList<>();

                    // Find eligible employees
                    for (Map.Entry<String, Employee> entry : employees.entrySet()) {
                        Employee emp = entry.getValue();
                        if (emp.daysWorked < 5 &&
                                canWork(emp, day, shift) &&
                                hasShiftOnDay(emp, day)) {
                            candidates.add(entry);
                        }
                    }

                    if (candidates.isEmpty()) {
                        System.out.println("Critical: Unable to fill " + day + " " + shift);
                        break;
                    }

                    // Prioritize least busy and randomize
                    candidates.sort(Comparator.comparingInt(e -> e.getValue().daysWorked));
                    Collections.shuffle(candidates);

                    // Assign shift
                    Employee chosenEmp = candidates.get(0).getValue();
                    chosenEmp.assignedShifts.add(new String[]{day, shift});
                    chosenEmp.daysWorked++;
                }
            }
        }
    }

    // Helper Methods

    /**
     * Check if employee can work a specific shift
     * @return true if employee:
     * - Hasn't reached max days
     * - Isn't already working that day
     * - Isn't already assigned to that specific shift
     */
    static boolean canWork(Employee emp, String day, String shift) {
        return emp.daysWorked < 5 &&
                hasShiftOnDay(emp, day) &&
                !isAssignedToShift(emp, day, shift);
    }

    /** Check if employee has any shift on given day */
    static boolean hasShiftOnDay(Employee emp, String day) {
        return emp.assignedShifts.stream().noneMatch(s -> s[0].equals(day));
    }

    /** Check if employee is already assigned to specific shift */
    static boolean isAssignedToShift(Employee emp, String day, String shift) {
        return emp.assignedShifts.stream().anyMatch(s -> s[0].equals(day) && s[1].equals(shift));
    }

    /** Count number of employees assigned to a specific shift */
    static int countAssigned(String day, String shift) {
        return (int) employees.values().stream()
                .flatMap(e -> e.assignedShifts.stream())
                .filter(s -> s[0].equals(day) && s[1].equals(shift))
                .count();
    }

    /** Display the final schedule */
    static void displaySchedule() {
        System.out.println("\nFinal Schedule:");
        for (String day : daysOfWeek) {
            System.out.println("\n" + day + ":");
            for (String shift : shifts) {
                System.out.printf("%-10s: ", shift.substring(0, 1).toUpperCase() + shift.substring(1));
                List<String> workers = new ArrayList<>();
                for (Employee emp : employees.values()) {
                    if (emp.assignedShifts.stream().anyMatch(s -> s[0].equals(day) && s[1].equals(shift))) {
                        workers.add(emp.name);
                    }
                }
                System.out.println(workers.isEmpty() ? "Unstaffed" : String.join(", ", workers));
            }
        }
    }

    // Main execution
    public static void main(String[] args) {
        try {
            String filePath = "/Users/avijit/Desktop/Schedule/src/employees.txt";

            // Load employee data
            importPreferencesFromFile(filePath);

            // Generate schedule
            assignShifts();
            resolveConflicts();

            // Display results
            displaySchedule();

            // Post-schedule validation
            boolean allShiftsFilled = true;
            for (String day : daysOfWeek) {
                for (String shift : shifts) {
                    int count = countAssigned(day, shift);
                    if (count < 2) {
                        System.out.println("\nWarning: " + day + " " + shift + " understaffed (" + count + ")");
                        allShiftsFilled = false;
                    }
                }
            }

            if (allShiftsFilled) {
                System.out.println("\nAll shifts properly staffed!");
            }
        } catch (FileNotFoundException e) {
            System.out.println("Error: File not found - " + e.getMessage());
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}