Project 3 - Activity Planner / Task Manager

(by Nikhil Abraham Mathew)

This is a web-application in which users can create, manage and view tasks/activities for a 30 day duration. If the user wishes to add a shopping task, an option will be available to add a shopping list to this task where items may be added / crossed out later.

Features of this website are:
1. Registration
    - Anonymous visitors can sign up
    - Returning users can sign in

2. Task Management
    - Users can view a calender of the next 30 days
    - Users can access each day's page to add/view/modify the day's tasks
    - Users can add shopping lists as well
    - Count of tasks for each day will be visible on the calender
    - Time left for each task will be displayed (if provided)
    - Task will be deleted after time limit / day expires
    
Instructions to clone and run this website on your system:
1. Clone repository
2. Create a virtualenv and activate it
3. Install dependencies by typing "pip install -r requirements.txt"
4. Type "export FLASK_APP=planner" to set the application
5. Type "flask initdb" to create the database
6. Type "flask run" to start the app
