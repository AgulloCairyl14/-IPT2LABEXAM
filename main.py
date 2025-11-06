import mysql.connector
from mysql.connector import Error

# Connect to MySQL
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",       # Replace with your MySQL username
        password="your_password",   # Replace with your MySQL password
        database="agullo-iptech"
    )

# Input validation
def validate_age(age):
    return age.isdigit() and 18 <= int(age) <= 70

def validate_phone(phone):
    return re.match(r"\(\d{3}\) \d{3}-\d{4}", phone)

def validate_email(email):
    return "@" in email and "." in email

# Add new resume
def add_resume():
    print("\n=== Add New Resume ===")
    full_name = input("Full Name: ").strip()
    age = input("Age: ").strip()
    while not validate_age(age):
        age = input("Invalid age. Enter age (18–70): ").strip()
    address = input("Address: ").strip()
    phone = input("Phone ((XXX) XXX-XXXX): ").strip()
    while not validate_phone(phone):
        phone = input("Invalid format. Try again: ").strip()
    email = input("Email: ").strip()
    while not validate_email(email):
        email = input("Invalid email. Try again: ").strip()
    job_title = input("Job Title: ").strip()
    summary = input("Professional Summary: ").strip()

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO resumes (full_name, age, address, phone, email, job_title, summary)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (full_name, int(age), address, phone, email, job_title, summary))
        resume_id = cursor.lastrowid

        # Experience
        while True:
            print("\n--- Add Experience ---")
            job = input("Job Title: ")
            company = input("Company: ")
            years = input("Years (e.g., 2020–2023): ")
            cursor.execute("""
                INSERT INTO experience (resume_id, job_title, company, years)
                VALUES (%s, %s, %s, %s)
            """, (resume_id, job, company, years))
            if input("Enter another experience? (y/n): ").lower() != 'y':
                break

        # Education
        while True:
            print("\n--- Add Education ---")
            degree = input("Degree: ")
            institution = input("Institution: ")
            year = input("Year: ")
            cursor.execute("""
                INSERT INTO education (resume_id, degree, institution, year)
                VALUES (%s, %s, %s, %s)
            """, (resume_id, degree, institution, year))
            if input("Enter another education? (y/n): ").lower() != 'y':
                break

        # Skills
        print("\n--- Add Skills ---")
        while True:
            skill = input("Enter skill (or 'done' to finish): ").strip()
            if skill.lower() == 'done':
                break
            cursor.execute("INSERT INTO skills (resume_id, skill) VALUES (%s, %s)", (resume_id, skill))

        conn.commit()
        print("\n✅ Resume saved successfully!")
    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
    finally:
        cursor.close()
        conn.close()

# View all resumes
def view_resumes():
    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM resumes")
        resumes = cursor.fetchall()

        for res in resumes:
            print("\n=== Resume ===")
            print(f"Name: {res['cairyl_agullo']}")
            print(f"Age: {res['22']}")
            print(f"Address: {res['101 remigio street maysilo malabon city']}")
            print(f"Phone: {res['09704773566']}")
            print(f"Email: {res['cairylagullo@gmail.com']}")
            print(f"Job Title: {res['job_title']}")
            print(f"Summary: {res['summary']}\n")

            cursor.execute("SELECT * FROM experience WHERE resume_id = %s", (res['id'],))
            experiences = cursor.fetchall()
            print("Experience:")
            for exp in experiences:
                print(f"- {exp['job_title']} at {exp['company']} ({exp['years']})")

            cursor.execute("SELECT * FROM education WHERE resume_id = %s", (res['id'],))
            education = cursor.fetchall()
            print("\nEducation:")
            for edu in education:
                print(f"- {edu['degree']}, {edu['institution']} ({edu['year']})")

            cursor.execute("SELECT skill FROM skills WHERE resume_id = %s", (res['id'],))
            skills = [row['skill'] for row in cursor.fetchall()]
            print("\nSkills:")
            print(", ".join(skills))
            print("\n" + "="*40)

    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
    finally:
        cursor.close()
        conn.close()

# Main menu
def main():
    while True:
        print("\n=== Resume Builder ===")
        print("1. Add New Resume")
        print("2. View All Resumes")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ").strip()
        if choice == '1':
            add_resume()
        elif choice == '2':
            view_resumes()
        elif choice == '3':
            print("👋 Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()