# MSCS-632-M50_Assignment4
This repo is Assignment 4 for Advanced Programming Languages (MSCS-632-M50)
## The Schedule directory is for Java implementation
In this directory, the **EmplyoeeScheduler class** and **employees.txt** are located inside the **src** directory. **EmplyoeeScheduler class** is the Public class where all methods, including the main method, are declared inside. The **Employee class** is the class to store the employee data. Both of the classes are defined in the **EmplyoeeScheduler.java** file. The **employees.txt** is the user input file, which is the employee's preferences file. It defines each day's employee shift preferences, such as "morning, evening, and afternoon." Below is the input file format if the user needs to edit the number of employees and their preferences:
 Input File Format:
 * First line: Total number of employees
 * For each employee:
 * Name (single line)
 * 7 lines of shift preferences (one per day)
 * Each day line contains three space-separated shifts in preference order.
#### After entering the data into the **employees.txt** file, 
The user needs to verify the input file path, which is "/Users/avijit/Desktop/Schedule/src/employees.txt" inside the main method in this case. Users need to update the file path to match the location of the **employee.txt** file in the system. Then, they can run the **EmplyoeeScheduler.java** file, and it will give the output where it follows all the assignment four guidelines. Also, in the employees.txt file, the user can allow employees to indicate shift preferences with a priority ranking (e.g., morning is their first preference, evening is their second), which is implemented in the **assignShifts()** method.
## The SchedulePython directory is for Python implementation
There are a total of three working files in this directory. They are **schedule.py, GUI.py, employees.txt**. schedule.py is the main implementation of the application, and GUI.py is the graphical implementation of the application where the user can run this and load and input file; after that, the user can generate the schedule by clicking generate schedule. Users can see the timing by clicking the day, such as Monday, Tuesday, or Wednesday. This feature is optional and only for users who want to enter data and get the report by GUI. If users wish to enter data without GUI, they can open the employee.txt file and edit the data by following the guidelines below.
Input File Format:
 * First line: Total number of employees
 * For each employee:
 * Name (single line)
 * 7 lines of shift preferences (one per day)
 * Each day line contains 3 space-separated shifts in preference order.
#### Once the input file edit is done by the user
In this case, they can verify the file path name, which is **"employee.txt"**, and then run the program. It will give the desired output as per the condition.
