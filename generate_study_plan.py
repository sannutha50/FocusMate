from database import setup_database, generate_study_plan, insert_study_plan, insert_user

if __name__ == "__main__":
    setup_database()  # Ensure database and tables are set up
    print("Backend is running...")

    # Get user input dynamically from the console
    user_input = input("Enter your study goals: ").strip()
    if not user_input:
        print("No study goals provided. Exiting.")
        exit(1)

    # Generate the study plan based on the user input
    study_plan = generate_study_plan(user_input)

    # Insert a sample user (for demonstration purposes)
    user_id = insert_user("sample_user", "password123")
    if user_id is None:
        print("Failed to insert or retrieve user. Exiting.")
        exit(1)

    # Insert the generated study plan for the sample user into the database
    insert_study_plan(user_id, user_input, study_plan)

    print("Study plan generated and stored for user ID", user_id)
    print("Study Plan:")
    print(study_plan)
