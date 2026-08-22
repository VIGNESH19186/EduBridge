"""
Seeds the database with realistic demo data:
    - Demo student & teacher accounts
    - Subjects & topics
    - Practice questions (multiple difficulties)
    - A sample quiz
    - Varied student progress/attempt history so analytics look realistic
    - Ingested educational content documents (for RAG grounding)

Run via: python scripts/seed_database.py
"""
import json
import random
import datetime

from backend.database.database import Base, engine, SessionLocal
from backend.models.user import User, RoleEnum
from backend.models.student import Student
from backend.models.teacher import Teacher
from backend.models.class_model import ClassModel, ClassMember
from backend.models.subject import Subject
from backend.models.topic import Topic
from backend.models.question import Question
from backend.models.quiz import Quiz, QuizQuestion
from backend.models.attempt import Attempt, Answer
from backend.models.recommendation import StudentProgress
from backend.models.document import Document, DocumentChunk
from backend.utils.security import hash_password
from backend.services import rag_service
from ai.rag.ingest import extract_text_from_file
from ai.rag.chunker import chunk_text

SUBJECT_TOPICS = {
    "Mathematics": ["Fractions", "Linear Equations", "Quadratic Equations", "Differential Calculus", "Graphs"],
    "Physics": ["Newton's Laws of Motion", "Energy & Work", "Waves"],
    "Chemistry": ["Chemical Bonds", "Acids & Bases"],
    "Biology": ["Photosynthesis", "Cell Structure"],
    "Computer Science": ["Algorithms & Control Flow", "Data Structures"],
    "English": ["Grammar Basics", "Essay Writing"],
}

QUESTION_BANK = {
    "Quadratic Equations": [
        {"prompt": "Solve: x² - 5x + 6 = 0", "options": ["1, 6", "2, 3", "3, 4", "2, 4"],
         "correct_answer": "2, 3", "explanation": "Factors as (x-2)(x-3)=0, giving x=2 and x=3.",
         "difficulty": "beginner"},
        {"prompt": "Solve: x² - 4x + 4 = 0", "options": ["2 (double root)", "4, -4", "1, 4", "0, 4"],
         "correct_answer": "2 (double root)", "explanation": "Factors as (x-2)²=0, so x=2 is a double root.",
         "difficulty": "beginner"},
        {"prompt": "Using the quadratic formula, solve 2x² + 3x - 2 = 0", "options": ["0.5, -2", "1, -2", "0.5, 2", "-0.5, 2"],
         "correct_answer": "0.5, -2", "explanation": "x = (-3 ± sqrt(9+16))/4 = (-3 ± 5)/4, giving 0.5 and -2.",
         "difficulty": "intermediate"},
    ],
    "Differential Calculus": [
        {"prompt": "What is the derivative of x³?", "options": ["3x²", "x²", "3x", "x³"],
         "correct_answer": "3x²", "explanation": "By the power rule, bring down the exponent and reduce it by 1.",
         "difficulty": "beginner"},
        {"prompt": "What is the derivative of 5x⁴?", "options": ["20x³", "5x³", "20x⁴", "4x³"],
         "correct_answer": "20x³", "explanation": "Multiply the coefficient by the exponent: 5*4=20, reduce exponent to 3.",
         "difficulty": "intermediate"},
    ],
    "Fractions": [
        {"prompt": "Simplify: 8/12", "options": ["2/3", "3/4", "4/6", "1/2"],
         "correct_answer": "2/3", "explanation": "Divide numerator and denominator by their GCD, 4.",
         "difficulty": "beginner"},
    ],
    "Newton's Laws of Motion": [
        {"prompt": "What happens to an object's velocity when no net force acts on it?", "options": ["It stays constant", "It increases", "It decreases", "It becomes zero"],
         "correct_answer": "It stays constant", "explanation": "This is Newton's First Law (law of inertia).",
         "difficulty": "beginner"},
    ],
    "Photosynthesis": [
        {"prompt": "Which gas do plants release during photosynthesis?", "options": ["Oxygen", "Carbon dioxide", "Nitrogen", "Hydrogen"],
         "correct_answer": "Oxygen", "explanation": "Photosynthesis converts CO2 and water into glucose and oxygen.",
         "difficulty": "beginner"},
    ],
    "Algorithms & Control Flow": [
        {"prompt": "What is the time complexity of a single for-loop over n items?", "options": ["O(n)", "O(n²)", "O(log n)", "O(1)"],
         "correct_answer": "O(n)", "explanation": "The loop body runs once per item, growing linearly with n.",
         "difficulty": "beginner"},
    ],
}

DEMO_STUDENT_NAMES = [
    "Aditi Sharma", "Rahul Verma", "Priya Nair", "Karan Mehta", "Sneha Iyer",
    "Arjun Rao", "Neha Gupta", "Vikram Singh", "Ananya Das", "Rohan Kapoor",
]


def get_content_files():
    return [
        ("Open Educational Mathematics", "Mathematics", "Differential Calculus",
         "data/educational_content/mathematics/differential_calculus.md"),
        ("Open Educational Mathematics", "Mathematics", "Quadratic Equations",
         "data/educational_content/mathematics/quadratic_equations.md"),
        ("Open Educational Mathematics", "Mathematics", "Fractions",
         "data/educational_content/mathematics/fractions.md"),
        ("Open Educational Physics", "Physics", "Newton's Laws of Motion",
         "data/educational_content/science/newtons_laws.md"),
        ("Open Educational Biology", "Biology", "Photosynthesis",
         "data/educational_content/science/photosynthesis.md"),
        ("Open Educational Computer Science", "Computer Science", "Algorithms & Control Flow",
         "data/educational_content/computer_science/algorithms.md"),
        ("Open Educational English", "English", "Grammar Basics",
         "data/educational_content/english/grammar_basics.md"),
    ]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        if db.query(User).filter(User.email == "student@example.com").first():
            print("Database already seeded. Skipping.")
            return

        print("Seeding subjects & topics...")
        subject_objs, topic_objs = {}, {}
        for subject_name, topics in SUBJECT_TOPICS.items():
            subject = Subject(name=subject_name, description=f"{subject_name} curriculum")
            db.add(subject)
            db.flush()
            subject_objs[subject_name] = subject
            for topic_name in topics:
                topic = Topic(name=topic_name, subject_id=subject.id, difficulty="beginner")
                db.add(topic)
                db.flush()
                topic_objs[topic_name] = topic
        db.commit()

        print("Seeding practice questions...")
        for topic_name, questions in QUESTION_BANK.items():
            topic = topic_objs.get(topic_name)
            if not topic:
                continue
            for q in questions:
                db.add(Question(
                    topic_id=topic.id, question_type="mcq", prompt=q["prompt"],
                    options=json.dumps(q["options"]), correct_answer=q["correct_answer"],
                    explanation=q["explanation"], difficulty=q["difficulty"],
                ))
        db.commit()

        print("Seeding demo teacher account...")
        teacher_user = User(
            name="Ms. Kavya Reddy", email="teacher@example.com",
            hashed_password=hash_password("password123"),
            role=RoleEnum.teacher, preferred_language="English",
        )
        db.add(teacher_user)
        db.commit()
        db.refresh(teacher_user)
        teacher = Teacher(user_id=teacher_user.id, department="Mathematics & Science")
        db.add(teacher)
        db.commit()
        db.refresh(teacher)

        demo_class = ClassModel(name="Grade 10 - Section A", subject_id=subject_objs["Mathematics"].id,
                                 teacher_id=teacher.id)
        db.add(demo_class)
        db.commit()
        db.refresh(demo_class)

        print("Seeding demo student account (primary demo login)...")
        primary_student_user = User(
            name="Demo Student", email="student@example.com",
            hashed_password=hash_password("password123"),
            role=RoleEnum.student, preferred_language="English",
        )
        db.add(primary_student_user)
        db.commit()
        db.refresh(primary_student_user)
        primary_student = Student(user_id=primary_student_user.id, grade_level="Grade 10",
                                   learning_streak_days=12)
        db.add(primary_student)
        db.commit()
        db.refresh(primary_student)
        db.add(ClassMember(class_id=demo_class.id, student_id=primary_student.id))

        all_students = [primary_student]

        print("Seeding additional demo students with varied performance...")
        for name in DEMO_STUDENT_NAMES:
            email = name.lower().replace(" ", ".") + "@example.com"
            user = User(name=name, email=email, hashed_password=hash_password("password123"),
                        role=RoleEnum.student, preferred_language="English")
            db.add(user)
            db.commit()
            db.refresh(user)
            student = Student(user_id=user.id, grade_level="Grade 10",
                               learning_streak_days=random.randint(0, 20))
            db.add(student)
            db.commit()
            db.refresh(student)
            db.add(ClassMember(class_id=demo_class.id, student_id=student.id))
            all_students.append(student)
        db.commit()

        print("Seeding varied progress & attempt history for realistic analytics...")
        all_topics = list(topic_objs.values())
        for student in all_students:
            for topic in random.sample(all_topics, k=min(4, len(all_topics))):
                mastery = round(random.uniform(30, 95), 1)
                accuracy = round(mastery + random.uniform(-10, 10), 1)
                accuracy = max(0.0, min(100.0, accuracy))
                solved = random.randint(5, 40)

                db.add(StudentProgress(
                    student_id=student.id, subject_id=topic.subject_id, topic_id=topic.id,
                    mastery_percent=mastery, accuracy_percent=accuracy, questions_solved=solved,
                ))

                # a few attempts in the last several days for weekly-activity charts
                for i in range(random.randint(1, 4)):
                    days_ago = random.randint(0, 6)
                    attempt = Attempt(
                        student_id=student.id, topic_id=topic.id,
                        score_percent=accuracy, accuracy=accuracy,
                        created_at=datetime.datetime.utcnow() - datetime.timedelta(days=days_ago),
                    )
                    db.add(attempt)
        db.commit()

        print("Seeding a sample quiz...")
        quiz = Quiz(title="Quadratic Equations - Practice Quiz",
                     subject_id=subject_objs["Mathematics"].id,
                     topic_id=topic_objs["Quadratic Equations"].id,
                     difficulty="beginner", time_limit_minutes=15,
                     created_by_teacher_id=teacher.id)
        db.add(quiz)
        db.commit()
        db.refresh(quiz)
        quiz_qs = db.query(Question).filter(Question.topic_id == topic_objs["Quadratic Equations"].id).all()
        for q in quiz_qs:
            db.add(QuizQuestion(quiz_id=quiz.id, question_id=q.id))
        db.commit()

        print("Ingesting educational content documents for RAG grounding...")
        for title, subject, topic, rel_path in get_content_files():
            document = Document(title=title, subject=subject, topic=topic,
                                 author="EduBridge Content Team", source_url="",
                                 license="Open Educational Resource", file_path=rel_path)
            db.add(document)
            db.commit()
            db.refresh(document)

            text = extract_text_from_file(rel_path)
            chunks = chunk_text(text)
            for idx, chunk in enumerate(chunks):
                section = "Introduction"
                if "## Section:" in text:
                    # naive section title extraction to make citations meaningful
                    for line in text.split("\n"):
                        if line.strip().startswith("## Section:") and chunk[:40] in text[text.find(line):text.find(line) + 1000]:
                            section = line.replace("## Section:", "").strip()
                db.add(DocumentChunk(document_id=document.id, chunk_index=idx, content=chunk, section=section))
            db.commit()

        rag_service.build_index(db)

        print("\n✅ Seed complete.")
        print("Demo accounts (password: password123):")
        print("  Student: student@example.com")
        print("  Teacher: teacher@example.com")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
