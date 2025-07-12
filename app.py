import streamlit as st
import os
from stem_tutor import STEMTutor
from quiz_generator import QuizGenerator
from utils import initialize_session_state, render_math_expression

# Initialize session state
initialize_session_state()

# Configure page
st.set_page_config(
    page_title="EduPrompt - AI STEM Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize components
@st.cache_resource
def get_tutor():
    return STEMTutor()

@st.cache_resource
def get_quiz_generator():
    return QuizGenerator()

tutor = get_tutor()
quiz_gen = get_quiz_generator()

# Sidebar navigation
st.sidebar.title("🎓 EduPrompt")
st.sidebar.markdown("Your AI-powered STEM tutor")

# Learning mode selection
mode = st.sidebar.selectbox(
    "Select Learning Mode",
    ["Interactive Q&A", "Step-by-Step Explanations", "Quiz Practice", "Progress Tracking"]
)

# Subject selection
subject = st.sidebar.selectbox(
    "Select Subject",
    ["Calculus", "Linear Algebra", "Data Science", "General Math"]
)

# Difficulty level
difficulty = st.sidebar.selectbox(
    "Difficulty Level",
    ["Beginner", "Intermediate", "Advanced"]
)

# Main content area
st.title("EduPrompt - AI STEM Tutor")

if mode == "Interactive Q&A":
    st.header("Ask Your STEM Questions")
    st.markdown("Ask any question about calculus, linear algebra, or data science. I'll provide detailed explanations!")
    
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant" and "math" in message.get("content", ""):
                render_math_expression(message["content"])
            else:
                st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask your STEM question here..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = tutor.answer_question(prompt, subject, difficulty)
                render_math_expression(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Update student progress
                st.session_state.questions_asked += 1

elif mode == "Step-by-Step Explanations":
    st.header("Step-by-Step Problem Solving")
    st.markdown("Enter a problem and I'll break it down into clear, manageable steps.")
    
    problem = st.text_area(
        "Enter your problem:",
        placeholder="e.g., Find the derivative of f(x) = x^2 * sin(x)",
        height=100
    )
    
    if st.button("Get Step-by-Step Solution", type="primary"):
        if problem:
            with st.spinner("Generating step-by-step solution..."):
                explanation = tutor.explain_step_by_step(problem, subject, difficulty)
                render_math_expression(explanation)
                
                # Update progress
                st.session_state.problems_solved += 1
        else:
            st.warning("Please enter a problem to solve.")

elif mode == "Quiz Practice":
    st.header("Quiz Practice")
    st.markdown("Test your knowledge with adaptive quizzes!")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        quiz_type = st.selectbox(
            "Quiz Type",
            ["Multiple Choice", "Problem Solving", "Mixed"]
        )
        
        num_questions = st.slider("Number of Questions", 1, 10, 5)
    
    with col2:
        if st.button("Generate New Quiz", type="primary"):
            with st.spinner("Generating quiz..."):
                quiz = quiz_gen.generate_quiz(subject, difficulty, quiz_type, num_questions)
                st.session_state.current_quiz = quiz
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
    
    # Display current quiz
    if "current_quiz" in st.session_state and st.session_state.current_quiz:
        quiz = st.session_state.current_quiz
        
        st.subheader(f"Quiz: {quiz['title']}")
        
        # Quiz questions
        for i, question in enumerate(quiz["questions"]):
            st.markdown(f"**Question {i+1}:**")
            render_math_expression(question["question"])
            
            if question["type"] == "multiple_choice":
                answer = st.radio(
                    "Select your answer:",
                    question["options"],
                    key=f"q_{i}",
                    disabled=st.session_state.get("quiz_submitted", False)
                )
                st.session_state.quiz_answers[i] = answer
            
            elif question["type"] == "problem_solving":
                answer = st.text_area(
                    "Enter your solution:",
                    key=f"q_{i}",
                    disabled=st.session_state.get("quiz_submitted", False)
                )
                st.session_state.quiz_answers[i] = answer
            
            st.markdown("---")
        
        # Submit quiz
        if not st.session_state.get("quiz_submitted", False):
            if st.button("Submit Quiz", type="primary"):
                with st.spinner("Evaluating your answers..."):
                    results = quiz_gen.evaluate_quiz(quiz, st.session_state.quiz_answers)
                    st.session_state.quiz_results = results
                    st.session_state.quiz_submitted = True
                    st.session_state.quizzes_completed += 1
                    st.rerun()
        
        # Display results
        if st.session_state.get("quiz_submitted", False) and "quiz_results" in st.session_state:
            results = st.session_state.quiz_results
            
            st.subheader("Quiz Results")
            
            # Score
            score = results["score"]
            total = results["total"]
            percentage = (score / total) * 100
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Score", f"{score}/{total}")
            with col2:
                st.metric("Percentage", f"{percentage:.1f}%")
            with col3:
                if percentage >= 80:
                    st.success("Excellent! 🎉")
                elif percentage >= 60:
                    st.info("Good job! 👍")
                else:
                    st.warning("Keep practicing! 💪")
            
            # Detailed feedback
            st.subheader("Detailed Feedback")
            for i, feedback in enumerate(results["feedback"]):
                with st.expander(f"Question {i+1} - {'✅ Correct' if feedback['correct'] else '❌ Incorrect'}"):
                    st.markdown(f"**Your answer:** {feedback['user_answer']}")
                    st.markdown(f"**Correct answer:** {feedback['correct_answer']}")
                    st.markdown(f"**Explanation:** {feedback['explanation']}")

elif mode == "Progress Tracking":
    st.header("Your Learning Progress")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Questions Asked",
            st.session_state.questions_asked,
            delta=1 if st.session_state.questions_asked > 0 else 0
        )
    
    with col2:
        st.metric(
            "Problems Solved",
            st.session_state.problems_solved,
            delta=1 if st.session_state.problems_solved > 0 else 0
        )
    
    with col3:
        st.metric(
            "Quizzes Completed",
            st.session_state.quizzes_completed,
            delta=1 if st.session_state.quizzes_completed > 0 else 0
        )
    
    # Progress insights
    st.subheader("Learning Insights")
    
    if st.session_state.questions_asked > 0:
        st.success(f"You've been actively learning! Keep up the great work!")
        
        # Suggest next steps
        st.subheader("Suggested Next Steps")
        
        if st.session_state.quizzes_completed < 3:
            st.info("📝 Try taking a quiz to test your knowledge!")
        
        if st.session_state.problems_solved < 5:
            st.info("🧮 Practice more step-by-step problem solving!")
        
        if st.session_state.questions_asked < 10:
            st.info("❓ Don't hesitate to ask more questions!")
    
    else:
        st.info("Start your learning journey by asking questions or taking quizzes!")

# Sidebar help
st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Tips")
st.sidebar.markdown("""
- Use LaTeX notation for math expressions
- Be specific in your questions for better answers
- Try different difficulty levels to challenge yourself
- Review quiz feedback to improve
""")

st.sidebar.markdown("### 📚 Subjects Covered")
st.sidebar.markdown("""
- **Calculus**: Derivatives, integrals, limits
- **Linear Algebra**: Matrices, vectors, transformations
- **Data Science**: Statistics, probability, ML basics
""")
