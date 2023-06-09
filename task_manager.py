#Notes: 

#Please note you will need to either add some tasks to create the text file.
#Or use my uploaded text file.
#I deleted the previous text files off of Dropbox as they didn't incorporate the task id.
#And therefore caused an error.

#1.Use the following username and password to access the admin rights 
#Username: admin
#Password: password
#2.Ensure you open the whole folder for this task in VS Code otherwise the 
#Program will look in your root directory for the text files.

#=====importing libraries===========

#Import of os for txt files.
#Import of sys for sys.exit.
#Import of datetime and date for the creation of task dates.

import os
import sys
from datetime import datetime, date

datetime_string_format = "%Y-%m-%d"


#Creates tasks.txt if it doesn't exist.
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for t_str in task_data:
    curr_t = {}


    #Split by semicolon and manually add each component.
    #Added taskid to correspond to task number, for the requirements of the task.
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], datetime_string_format)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], datetime_string_format)
    curr_t['completed'] = True if task_components[5] == "Yes" else False
    curr_t['taskid'] = task_components[6]
    task_list.append(curr_t)

#function to get the last task id off the global task_list.
def get_last_task_ID():
    global task_list

    #try clause to allow for index error.
    try:
        #Gets the integer of the last item in the task_list.
        #Which corresponds to "taskid".
        return int(task_list[-1]['taskid'])
    
    except IndexError:
        return int(0)

#Variable for task_number which gets the last task id and adds 1.
#This is for the number for a new task being created.
task_number = get_last_task_ID() +1
        
#Function to update the task.txt file to be called in other functions.
#Writes the file based on changes made in other functions.
#Includes the new taskid string
def update_task_file():

    global task_list

    taskFile = open('tasks.txt', 'w')
    task_list_to_write = []

    #For loop for task in task_list.
    #Copied the exit string above.
    for t in task_list:
        str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(datetime_string_format),
                    t['assigned_date'].strftime(datetime_string_format),
                    "Yes" if t['completed'] else "No",
                    t['taskid']
                    ]
        
        #Appends to task_list_to_write.
        task_list_to_write.append(";".join(str_attrs))
    string_to_save = ""

    for task in task_list_to_write:
        string_to_save += task + "\n"

    #Writes the string to the txt file.
    string_to_save = string_to_save[0: -1]
    taskFile.write(string_to_save)
    taskFile.close()

#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
#If no user.txt file, write one with a default account.
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

#Read in user_data.
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

#Convert to a dictionary.
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("You have entered a user which doesn't exist.")
        continue
    elif username_password[curr_user] != curr_pass:
        print("You have entered an incorrect password.")
        continue
    else:
        print("Login successful.")
        logged_in = True
        

#Function for generating reports.
def generate_reports():

    #Opens task_overview.txt to write.
    taskOverview = open('task_overview.txt', 'w')

    #Write the task report file.
    taskOverview.write(task_report())

    #Close the task report file.
    taskOverview.close()

    #opens user_overview.txt to write.
    userOverview = open('user_overview.txt', 'w')
    
    #Writes the string to the file.
    userOverview.write(user_report())
    
    #Close the report file to save it.
    userOverview.close()


#Function to generate a report string for the taskOverview file in view my tasks format.
def task_report():
    
    
    global task_list

    #Set up a task_report string.
    task_report_string = ""

    #Total number of tasks = length of task list.
    total_number_of_tasks = len(task_list)
    
    #Number of completed tasks.
    completed_tasks = int(0)

    #For each task in the task list.
    for task in task_list:

        #If the value corresponding to the 'completed' is true.
        if task['completed']:

            #increment completed tasks by one.
            completed_tasks += int(1)
            
    #Number of uncompleted tasks.
    uncompleted_tasks = int(0)

    #For each task in the task list.
    for task in task_list:

        #If the value corresponding to the 'completed' is false.
        if not task['completed']:

            #increment uncompleted tasks by one.
            uncompleted_tasks += int(1)

    #Number of tasks that haven't been completed and are overdue.
    #Get todays date.
    curr_date = date.today()

    #Set up a counter.
    count_overdue_tasks = int(0)

    #for each task in the task list.
    for task in task_list:

        #If the task isn't completed and the due date is before today.
        if not task['completed'] and task['due_date'].date() < curr_date:

            #Add one to the counter.
            count_overdue_tasks += 1

    #Percentage of tasks that are incomplete.
    percentage_incomplete = 100 * (uncompleted_tasks/total_number_of_tasks)
    percentage_incomplete = round(percentage_incomplete,1)


    #Percentage of tasks that are overdue.
    percentage_overdue = 100 * (count_overdue_tasks/total_number_of_tasks)
    percentage_overdue = round(percentage_overdue,1) 
    
    #Creation of a task_report_string to write to the txt file.
    task_report_string += 'Completed Tasks: \t\t ' + str(completed_tasks) +"\n"
    task_report_string += 'Uncompleted tasks: \t\t ' + str(uncompleted_tasks) +"\n"
    task_report_string += 'Total tasks: \t\t\t ' + str(total_number_of_tasks)+"\n"
    task_report_string += 'Overdue tasks: \t\t\t ' + str(count_overdue_tasks) +"\n"
    task_report_string += 'Percentage incomplete tasks: \t ' + str(percentage_incomplete) + str('%')+"\n"
    task_report_string += 'Percentage overdue tasks: \t ' + str(percentage_overdue) + str('%')
    return task_report_string

def user_report():

    global task_list

    #Total number of tasks = length of task list.
    total_number_of_tasks = len(task_list)

    #Gets todays date.
    curr_date = date.today()
    
    #Open up the user data.
    user_file = open("user.txt", 'r') 

    #Creates user_file_data, which is a list of users and passwords. 
    user_file_data = user_file.read().split("\n")
    
    #Total number of users.
    total_num_users = len(user_file_data) 
    
    #Creates an empty list of users that we will report.
    user_list = []

    #For loop for each entry in the user_file_data.  
    for data in user_file_data:

        #Splits it on semicolon to create a new list. Where first element is username and second element is password.
        user_data_list = data.split(";")

        #Take the first element which is the username.
        username = user_data_list[0]

        #Appends the username to the user_report_list.
        user_list.append(username)

    tasks_info =[]

    #For loop for each user in the list.
    for user in user_list:

        #Add them to the list with a new line character at the end.
        user_info = {}
        user_info['username'] = str(user)

        #variables for each task criteria.
        num_assigned_tasks_user = int(0)
        num_completed_tasks_user = int(0)
        num_uncompleted_tasks_user = int(0)
        num_overdue_user = int(0)

        #For loop which loops through task_list.
        #Counters which go through each variable and match to the user.
        for task in task_list:
            if task['username'] == str(user):
                num_assigned_tasks_user += int(1)
            if task['username'] == str(user) and task['completed']:
                num_completed_tasks_user += int(1)
            if task['username'] == str(user) and not task['completed']:
                num_uncompleted_tasks_user += int(1)
            if task['username'] == str(user) and not task['completed'] and task['due_date'].date() < curr_date:
                num_overdue_user += int(1)
        user_info['num_assigned_tasks'] = num_assigned_tasks_user
        user_info['num_completed_tasks'] = num_completed_tasks_user
        user_info['num_uncompleted_tasks'] = num_uncompleted_tasks_user
        user_info['num_overdue_tasks'] = num_overdue_user
        
        #Try clause to allow for ZeroDivisionError.
        #Equations to produce the percentage of tasks for the assigned user.
        try:
            percentage_tasks_assigned_user = 100 * (num_assigned_tasks_user/total_number_of_tasks)
        except ZeroDivisionError:
            percentage_tasks_assigned_user = 0
            
        #Rounds the percentage of tasks assigned to the user.
        #Converts it to a string.
        percentage_tasks_assigned_user = round(percentage_tasks_assigned_user,1)
        percentage_tasks_assigned_user = str(percentage_tasks_assigned_user) + "%"
        user_info['percentage_total_tasks_assigned'] = percentage_tasks_assigned_user

        #Try clause to allow for ZeroDivisionError.
        #Equations to produce the percentage of complete tasks assigned to a user.
        try:
            percentage_tasks_complete_user = 100 *(num_completed_tasks_user/num_assigned_tasks_user)
        except ZeroDivisionError:
            percentage_tasks_complete_user = 0 

        #Rounds the percentage of completed tasks assigned to a user.
        #Converts it to a string.
        percentage_tasks_complete_user = round(percentage_tasks_complete_user,1)
        percentage_tasks_complete_user = str(percentage_tasks_complete_user) + "%"
        user_info['percentage_complete'] = percentage_tasks_complete_user

        #Try clause to allow for ZeroDivisionError.
        #Equations to produce the percentage of incomplete tasks assigned to a user.
        try:
            percentage_tasks_uncomplete_user = 100 *(num_uncompleted_tasks_user/num_assigned_tasks_user)
        except ZeroDivisionError:
            percentage_tasks_uncomplete_user = 0

        #Rounds the percentage of uncompleted tasks assigned to a user.
        #Converts it to a string.
        percentage_tasks_uncomplete_user = round(percentage_tasks_uncomplete_user,1)
        percentage_tasks_uncomplete_user = str(percentage_tasks_uncomplete_user) + "%"
        user_info['percentage_uncomplete'] = percentage_tasks_uncomplete_user

        #Try clause to allow for ZeroDivisionError.
        #Equations to produce the percentage of overdue tasks assigned to a user.
        try:
            percentage_tasks_overdue_user = 100 *(num_overdue_user/num_assigned_tasks_user)
        except ZeroDivisionError:
            percentage_tasks_overdue_user = 0 

        #Rounds the percentage of overdue tasks assigned to a user.
        #Converts it to a string.
        percentage_tasks_overdue_user = round(percentage_tasks_overdue_user,1)
        percentage_tasks_overdue_user = str(percentage_tasks_overdue_user) + "%"
        user_info['percentage_overdue'] = percentage_tasks_overdue_user
 
        #Appends the strings to user_info.
        tasks_info.append(user_info)
        
    #Creates a report string.
    user_report_string = ""
    user_report_string += 'Total users: \t ' + str(total_num_users)+"\n"
    user_report_string += 'Total tasks: \t ' + str(total_number_of_tasks)+"\n\n"

    #For loop to cycle through user in tasks_info.
    #Which adds all the calculations to the file.
    for user in tasks_info:
        user_report_string += "Username: \t\t\t\t" + str(user['username'])+str("\n")
        user_report_string += "User tasks: \t\t\t\t" + str(user['num_assigned_tasks'])+str("\n")
        user_report_string += "Percentage of total tasks assigned: \t" + str(user['percentage_total_tasks_assigned'])+str("\n")
        user_report_string += "Completion rate: \t\t\t" + str(user['percentage_complete']) + str("\n")
        user_report_string += "Percentage tasks uncompleted:\t\t" + str(user['percentage_uncomplete']) + str("\n")
        user_report_string += "Percentage tasks overdue:\t\t" + str(user['percentage_overdue']) + str("\n\n")

    #Closes the user file.
    user_file.close()

    #Print clause to tell the user the reports are generated.
    print('Reports generated.\n')
    return user_report_string
  
#Function for displaying all the statistics.
def display_statistics():
    if curr_user == "admin":

        print(task_report())
        print()
        print(user_report())
    else:
        print("Only the admin can produce reports.")

#Function for registering a new username.
def reg_user():
     
     while True:
   
        #Request input of a new username/
        new_username = input("New username: ")

        #If clause to allow for the username pre-existing.
        if new_username not in username_password.keys():
            break

        #Else clause to send them back through the while loop if the username exists already.
        else:
            print("You have entered a username which exists already.")
            print("Please enter a different username.")
            continue

     #Request input of a new password
     new_password = input("New password: ")

     #Request input of password confirmation.
     confirm_password = input("Confirm password: ")

    #Checks if the new password and confirmed password are the same.
     if new_password == confirm_password:
            
            #If clause for if they are the same, it will add them to the user.txt file,
            print("The following new username has been added: ")
            print(str(new_username))
            username_password[new_username] = new_password

            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))

     #Else clause for the passwords not matching.
     else:
         print("The passwords you have entered, do not match.")

#Function for adding a new task.
def add_task():
    global task_number

    #While loop for assigning a user to be added to a task.
    #Allowance for being able to exit the while loop with -1.
    while True:
        task_username = str(input("Username to be assigned to the task. Enter -1 if finished adding tasks:\n"))
        if task_username == "-1":
            break

        #Elif clause in case the user isn't valid.
        elif task_username not in username_password.keys():
            print("Username does not exist. Please enter a valid username.")
            continue

        #Input clause for task title and task description.
        task_title = input("Please enter the title of task: ")
        task_description = input("Please enter a description of the task: ")

        #Try clause and while loop to add the task_due_date.
        while True:
            try:
                task_due_date = input("Please enter the due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, datetime_string_format)
                break

            #Except to allow for an invalid datetime.
            except ValueError:
                print("You have entered an invalid datetime format.")
                print("Please use the format specified.")

        #Adds a task ID to the task.
        task_id = str(task_number)
        task_number += 1
        
        #Adds the current date.
        curr_date = date.today()
    
        #Formatting.
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False,
            "taskid": task_id
        }

        #Appends the task to task_list.
        #Then writes it to the txt file.               
        task_list.append(new_task)
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(datetime_string_format),
                    t['assigned_date'].strftime(datetime_string_format),
                    "Yes" if t['completed'] else "No",
                    t['taskid']
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("Task successfully added.")

#Function for viewing all tasks.
def view_all():
    
    #For loop to loop through tasks in the task_list.
    #Which then prints to display all tasks.
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(datetime_string_format)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(datetime_string_format)}\n"
        disp_str += f"Task Description: {t['description']}\n"
        disp_str += f"Task ID: \t {t['taskid']}\n"
        print(disp_str)

#Function for viewing your own tasks.
def view_mine():

    global task_list

    #For loop to loop through all tasks in the task_list.
    for t in task_list:

        #If clause to match the username with the current user.
        #Then prints all tasks assigned to the current user.
        if t['username'] == curr_user:
            disp_str = f"Task: \t\t\t {t['title']}\n"
            disp_str += f"Assigned to: \t\t {t['username']}\n"
            disp_str += f"Date Assigned:\t\t {t['assigned_date'].strftime(datetime_string_format)}\n"
            disp_str += f"Due Date:  \t\t {t['due_date'].strftime(datetime_string_format)}\n"
            disp_str += f"Task Description:\t {t['description']}\n"
            disp_str += f"Task ID: \t\t {t['taskid']}\n"
            print(disp_str)

    #While loop for selecting specific tasks.
    while True:

        try:
            print("Do you wish you do select a specific task?")

            #Allows for the user wishing to exit to the main menu.
            task_selection = int(input("Select the task number or -1 to return to the main menu. \n"))
            if task_selection == int(-1):
                break

            #Else clause if they proceed with selecting a task.
            else: 
                try:
                    selected_task = task_list[task_selection-1]

                    #Variable task_action to allow them to mark tasks as complete or edit them.
                    task_action = input("If you want to mark a task as complete, enter 'complete'. If you wish to edit task enter 'edit'.\n")
                    if task_action == "complete":
                        selected_task['completed'] = "True"
                        #Function to update the task file.
                        update_task_file()

                    elif task_action =="edit":
                        if selected_task['completed'] == True:
                            print('This task is already complete and cannot be edited.')
                            break

                        #Else clause to allow the user to edit the assigned user or due date.
                        else:
                            while True:
                                edit_option = int(input('Do you wish to edit the assigned user (enter 1) or the due date (enter 2)?\n'))

                                #If clause for changing the assigned user.
                                #Allows for username not being valid.
                                if edit_option == int(1):
                                    newUsername = input('Which username would you like to assign this task to?\n')
                                    if newUsername not in username_password.keys():
                                        print('That username does not exist. Please try again')
                                        continue

                                    #Else clause for the update_task_file function.
                                    else:
                                        selected_task['username'] = newUsername
                                        update_task_file()
                                        break

                                #Elif clause for changing the due date on a task.
                                elif edit_option == int(2):
                                    try:
                                        newDueDate = input("Please enter the new due date of task (YYYY-MM-DD): \n")
                                        newDueDate = datetime.strptime(newDueDate,datetime_string_format)
                                        selected_task['due_date'] = newDueDate
                                        
                                        #Function for updating the task file.
                                        update_task_file()
                                        break

                                    #Except clause for an invalid due date.
                                    except ValueError:
                                        print("You have entered an invalid datetime format.")
                                        print("Please use the format specified.")
                                        continue                
                                    
                                else:
                                    print("Invalid entry, please enter '1' for editing assigned user or '2' for editing due date")
                                    continue
                    else:
                        print('Invalid entry')
                except IndexError:
                    print('The entered task number does not exist. Please try again.')
                    continue
        except ValueError:
            print('You did not edit a valid number, try again.')
            continue

while True:
    #Presenting the menu to the user.
    #Makes sure that the user input is converted to lower case.
    #Uses the above functions.
    print()
    menu = input('''Enter one of the following options below:
r - register user
a - adding a task
va - view all tasks
vm - view my task
gr - generate reports
ds - display statistics
e - exit
: ''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()
            
    elif menu == 'vm':
        view_mine()

    elif menu == 'e':
        print('Goodbye.')
        sys.exit()
        
    elif menu == 'gr':
        generate_reports()

    elif menu == 'ds':
        display_statistics()

    else:
        print("You have selected an option which doesn't exist.")
        print("Please try again.")