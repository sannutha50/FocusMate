import mysql.connector
from transformers import BertTokenizer, BertModel
import torch

def connect_db():
    # Connect to the database "project"
    return mysql.connector.connect(
        host="localhost",
        user="root",         # Change if needed
        password="1234",     # Change if needed
        database="project"
    )

def setup_database():
    db = connect_db()
    cursor = db.cursor()
    
    # Create the users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE,
            password VARCHAR(255)
        )
    """)
    
    # Create the study_plans table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_plans (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            goals TEXT,
            plan TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Create the tasks table (for the GUI)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            subject VARCHAR(255),
            task TEXT,
            deadline DATE,
            priority VARCHAR(50),
            completed BOOLEAN DEFAULT FALSE
        )
    """)
    
    db.commit()
    db.close()

# ---------- TASK FUNCTIONS (used in study_planner.py) ----------

def add_task(subject, task, deadline, priority):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO tasks (subject, task, deadline, priority, completed)
        VALUES (%s, %s, %s, %s, %s)
    """, (subject, task, deadline, priority, False))
    db.commit()
    db.close()

def get_tasks():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tasks WHERE completed = FALSE ORDER BY deadline ASC")
    tasks = cursor.fetchall()
    db.close()
    return tasks

def mark_task_completed(task_id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("UPDATE tasks SET completed = TRUE WHERE id = %s", (task_id,))
    db.commit()
    db.close()

def delete_task(task_id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    db.commit()
    db.close()

# ---------- STUDY PLAN FUNCTIONS (used in generate_study_plan.py) ----------

def generate_study_plan(user_input):
    # Initialize tokenizer and model (this example uses BERT for demonstration)
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertModel.from_pretrained("bert-base-uncased")
    
    inputs = tokenizer(user_input, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    
    # In a real scenario, you'd process 'outputs' to craft a study plan.
    # Here we simply return a string based on the input.
    study_plan = "Generated study plan based on input: " + user_input
    return study_plan

def insert_study_plan(user_id, goals, plan):
    db = connect_db()
    cursor = db.cursor()
    sql = "INSERT INTO study_plans (user_id, goals, plan) VALUES (%s, %s, %s)"
    values = (user_id, goals, plan)
    cursor.execute(sql, values)
    db.commit()
    db.close()

def insert_user(username, password):
    db = connect_db()
    cursor = db.cursor()
    sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
    values = (username, password)
    try:
        cursor.execute(sql, values)
        db.commit()
    except mysql.connector.Error as err:
        # If the user already exists, an error might occur.
        print("User insertion error:", err)
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    db.close()
    if user:
        return user[0]
    else:
        return None
