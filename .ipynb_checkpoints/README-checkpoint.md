# The-Database-Diners

**COMP 421 Project Proposal**

**Group Name:** Group 2, aka “The Database Diners”

**Project Name:** Dining Hall Database

**Group Members:**
- Kayla Casey
- Haley Parker
- Ryan Schmelzle 
- Yashvi Tanneru
  
**Project Description:** Our project aims to develop a relational database system for a dining hall, similar to those found on campus (i.e. Lenoir Dining Hall and Chase Dining Hall). This would alleviate the need for various websites and systems for students to do everyday tasks, such as checking how much money is left in their meal account, what is on the menu for each meal on a specific day, and checking out a to-go box. This database will manage several tables to track the key aspects of UNC dining hall operations. We plan to include the following:
Menu Management: Track daily menu items, the quantity of each item available, calories per serving, price, and preparation time.
Student Accounts: Track individual student data, including meal account balances (dollars available), the number of to-go boxes currently checked out, and their dining history (dates visited).

**Calendar Integration:** Provide a calendar view that shows the menu for specific dates, along with details on each food item.
Transactions and Updates: When students make transactions, the system will update their accounts accordingly, managing meal balance deductions, to-go box checkouts, and validating data to prevent overdrafts or excessive checkouts.

**Administrative Features:** Manage the database with functions to add new students, remove graduated students, and update menu items. The system will include triggers to automate actions, such as preventing overdrafts and limiting to-go box checkouts.

Additionally we plan to use multiple tables within our database and reference them using primary and foreign keys using the proposed tables and fields as a starting point:

## Students (Table): Tracks the information related to individual students.

**Fields:**
- student_id (Primary Key, INT)
– pid
- student_name (VARCHAR)
- meal_balance (DECIMAL) – how much money the student has left on their meal account
- to_go_boxes (INT) – how many to-go boxes the student currently has checked out
- last_visit_date (DATE) – date of the student's most recent visit

## Menu (Table): Contains information about food items available in the dining hall on specific dates and meals (e.g., breakfast, lunch, dinner).

**Fields:**
- item_id (Primary Key, INT)
- item_name (VARCHAR) 
- calories_per_serving (INT)
- meal_type (ENUM: breakfast, lunch, dinner)
- available_date (DATE) – the date the item is available

## Transactions (Table): Records each transaction where a student purchases a meal swipe or checks out a to-go box.

**Fields:**
- transaction_id (Primary Key, INT)
- student_id (Foreign Key, INT) – links to the Students table
- item_id (Foreign Key, INT) – links to the Menu table
- transaction_type (ENUM: meal swipe, to-go box checkout)
- transaction_date (DATE)
- amount (DECIMAL) – since the cost of ever meal swipe is standardized this will be a default value

## Dining History (Table): Tracks the dining hall visits and items purchased by students.

**Fields:**
- history_id (Primary Key, INT)
- student_id (Foreign Key, INT) – links to the Students table
- transaction_date (Foreign Key, DATE) – date of the visit
- transaction_type (Foreign Key, ENUM: meal swipe, to-go box checkout)
- item_id (Foreign Key, INT)
- meal_type (Foreign Key, ENUM: breakfast, lunch, dinner)

## Key Features:
- Add new records (e.g., new students, new menu items)
- Delete records (e.g., removing graduated students)
- Update existing records (e.g., modifying menu items or student data such as money on their accounts)
- Display records (e.g., viewing student meal accounts or menu details)
- Data validation (e.g., checking for meal balance sufficiency)
- Implement triggers (e.g., prevent account overdrafts such as making a purchase that would push their meal account balance below zero, limit to-go boxes)

**Future Development:** As the course progresses, we will incorporate more advanced topics into our project, such as:

**Procedures:** Writing stored procedures to automate repetitive tasks such as adding a new student or updating menu items.

**Transactions:** Adding transactions for procedures such as purchasing a meal to ensure that partial updates are not performed (ex: student making a purchase and then checking for meal balance after) to maintain data integrity.

**Secure Password Storage:** Implementing security measures for storing sensitive data like student login information and any other personal data.








