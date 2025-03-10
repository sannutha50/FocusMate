from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",      # Change to your MySQL username
    password="1234",  # Change to your MySQL password
    database="studbud"
)

cursor = db.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS study_plans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    goals TEXT NOT NULL,
    plan TEXT NOT NULL
)
""")
db.commit()

@app.route('/generate_plan/', methods=['POST'])
def generate_plan():
    data = request.get_json()
    user_id = data.get("user_id")
    goals = data.get("goals")
    
    if not user_id or not goals:
        return jsonify({"error": "Invalid input"}), 400
    
    plan = f"Study plan for {goals} is created!"
    
    # Store in MySQL
    cursor.execute("INSERT INTO study_plans (user_id, goals, plan) VALUES (%s, %s, %s)", (user_id, goals, plan))
    db.commit()
    
    return jsonify({"plan": plan})

@app.route('/get_plans/', methods=['GET'])
def get_plans():
    cursor.execute("SELECT user_id, goals, plan FROM study_plans")
    result = cursor.fetchall()
    
    study_plans = [{"user_id": row[0], "goals": row[1], "plan": row[2]} for row in result]
    return jsonify(study_plans)

@app.route('/')
def home():
    return "Welcome to StudBud AI Study Planner API with MySQL!"

if __name__ == "__main__":
    app.run(debug=True, port=5001)
