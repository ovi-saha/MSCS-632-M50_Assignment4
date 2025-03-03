# MSCS-632-M50_Assignment4
This repo is Assignment 4 for Advanced Programming Languages (MSCS-632-M50)
## The Schedule directory is for Java implementation
In this directory **EmplyoeeScheduler class** is the Public class where all methods including the main method declear in side it. The **Employee class** is the class to store the employee data. Both of the classes are define in **EmplyoeeScheduler.java** file. The **employees.txt** is the user input file which is employess preferences file. It defines each day's shift preferences for employees such as "morning eveninng afternoon". Below are the input file format if user need to edit the number of employees and there preferences:
 Input File Format:
 * - First line: Total number of employees
 * - For each employee:
 *   - Name (single line)
 *   - 7 lines of shift preferences (one per day)
 *   - Each day line contains 3 space-separated shifts in preference order
After entering the data to the **employees.txt** file, user need to verify the input file path which is "/Users/avijit/Desktop/Schedule/src/employees.txt" inside the main method, in this case. User need update the file path as per the location of the **employee.txt** file in the system, then they can run the **EmplyoeeScheduler.java** file and it will give the output where it follows all the assignment 4 guidelines. Also, in employees.txt file user has the opportunity to allow employees to indicate shift preferences with a priority ranking (e.g., morning is their first preference, evening is their second) which is implemented in **assignShifts()** method.
## The SchedulePython directory is for Pyhton implementation
There are total three working files in this directory. They are **schedule.py, GUI.py, employees.txt**. schedule.py is the main implementation of the application, GUI.py is the graphical implementation of the application where user can run this and load and input file, after that by clicking generate schedule user can generate the schdule. User can see the timing by clicking the day such as Monday, Tuesday or Wednesday. This feature is optional, only for them where user want to enter data and get the report by GUI. If user wants to enter data without GUI, they can simply open the employee.txt file and edit the data by folowing the guideline below
Input File Format:
 * - First line: Total number of employees
 * - For each employee:
 *   - Name (single line)
 *   - 7 lines of shift preferences (one per day)
 *   - Each day line contains 3 space-separated shifts in preference order
Once the input file edit is done by the user, they can veryify the file path name which is **"employee.txt"** in this case and then run the program. It will give desire output as per the condition.
