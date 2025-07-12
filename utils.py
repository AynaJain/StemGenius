import streamlit as st
import re

def initialize_session_state():
    """
    Initialize session state variables for tracking student progress
    """
    if "questions_asked" not in st.session_state:
        st.session_state.questions_asked = 0
    
    if "problems_solved" not in st.session_state:
        st.session_state.problems_solved = 0
    
    if "quizzes_completed" not in st.session_state:
        st.session_state.quizzes_completed = 0
    
    if "current_quiz" not in st.session_state:
        st.session_state.current_quiz = None
    
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
    
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
    
    if "performance_history" not in st.session_state:
        st.session_state.performance_history = []
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

def render_math_expression(text):
    """
    Render text with LaTeX mathematical expressions
    """
    # Check if text contains LaTeX expressions
    if '$' in text or '\\' in text:
        # Streamlit natively supports LaTeX rendering
        st.markdown(text)
    else:
        st.markdown(text)

def format_difficulty_feedback(assessment):
    """
    Format difficulty assessment feedback for display
    """
    if assessment["assessment"] == "too_easy":
        return "🎯 Consider trying a higher difficulty level!"
    elif assessment["assessment"] == "too_hard":
        return "💡 You might want to try an easier difficulty level first."
    else:
        return "✅ Great! This difficulty level seems perfect for you."

def calculate_adaptive_difficulty(performance_history):
    """
    Calculate recommended difficulty based on performance history
    """
    if not performance_history:
        return "Intermediate"
    
    recent_performance = performance_history[-5:]  # Last 5 attempts
    avg_score = sum(recent_performance) / len(recent_performance)
    
    if avg_score >= 0.85:
        return "Advanced"
    elif avg_score >= 0.65:
        return "Intermediate"
    else:
        return "Beginner"

def validate_openai_key():
    """
    Validate that OpenAI API key is available
    """
    import os
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        return False
    return True

def get_subject_topics(subject):
    """
    Get relevant topics for each subject
    """
    topics = {
        "Calculus": [
            "Limits and Continuity",
            "Derivatives and Differentiation",
            "Integration and Antiderivatives",
            "Applications of Derivatives",
            "Applications of Integration",
            "Sequences and Series"
        ],
        "Linear Algebra": [
            "Vectors and Vector Spaces",
            "Matrices and Matrix Operations",
            "Linear Transformations",
            "Eigenvalues and Eigenvectors",
            "Determinants",
            "Systems of Linear Equations"
        ],
        "Data Science": [
            "Statistics and Probability",
            "Hypothesis Testing",
            "Regression Analysis",
            "Machine Learning Basics",
            "Data Visualization",
            "Statistical Inference"
        ],
        "General Math": [
            "Algebra",
            "Trigonometry",
            "Geometry",
            "Precalculus",
            "Number Theory",
            "Discrete Mathematics"
        ]
    }
    return topics.get(subject, [])

def format_quiz_score(score, total):
    """
    Format quiz score with appropriate styling
    """
    percentage = (score / total) * 100
    
    if percentage >= 90:
        return f"🏆 {score}/{total} ({percentage:.1f}%) - Outstanding!"
    elif percentage >= 80:
        return f"🎉 {score}/{total} ({percentage:.1f}%) - Excellent!"
    elif percentage >= 70:
        return f"👍 {score}/{total} ({percentage:.1f}%) - Good job!"
    elif percentage >= 60:
        return f"👌 {score}/{total} ({percentage:.1f}%) - Keep improving!"
    else:
        return f"💪 {score}/{total} ({percentage:.1f}%) - Keep practicing!"

def get_learning_tips(subject, difficulty):
    """
    Get personalized learning tips based on subject and difficulty
    """
    tips = {
        "Calculus": {
            "Beginner": [
                "Start with understanding limits conceptually",
                "Practice basic derivative rules",
                "Use graphical representations to visualize concepts"
            ],
            "Intermediate": [
                "Focus on application problems",
                "Master integration techniques",
                "Connect derivatives and integrals conceptually"
            ],
            "Advanced": [
                "Work on multivariable calculus",
                "Study advanced integration methods",
                "Explore real-world applications"
            ]
        },
        "Linear Algebra": {
            "Beginner": [
                "Understand vector operations geometrically",
                "Practice matrix arithmetic",
                "Learn to solve basic systems of equations"
            ],
            "Intermediate": [
                "Study linear transformations",
                "Understand eigenvalues and eigenvectors",
                "Work with different vector spaces"
            ],
            "Advanced": [
                "Explore abstract vector spaces",
                "Study advanced matrix decompositions",
                "Apply linear algebra to machine learning"
            ]
        },
        "Data Science": {
            "Beginner": [
                "Learn basic statistical concepts",
                "Practice with real datasets",
                "Understand data visualization principles"
            ],
            "Intermediate": [
                "Study hypothesis testing",
                "Learn regression techniques",
                "Understand machine learning basics"
            ],
            "Advanced": [
                "Explore advanced ML algorithms",
                "Study deep learning concepts",
                "Work on complex data projects"
            ]
        }
    }
    
    return tips.get(subject, {}).get(difficulty, ["Keep practicing and asking questions!"])
