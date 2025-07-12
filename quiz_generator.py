import os
import json
from openai import OpenAI
import streamlit as st

class QuizGenerator:
    def __init__(self):
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"
    
    def generate_quiz(self, subject, difficulty, quiz_type, num_questions):
        """
        Generate a quiz with specified parameters
        """
        try:
            system_prompt = f"""You are an expert STEM educator creating quizzes for {subject}.
            Create a quiz with {num_questions} questions at {difficulty} level.
            
            Quiz specifications:
            - Subject: {subject}
            - Difficulty: {difficulty}
            - Type: {quiz_type}
            - Number of questions: {num_questions}
            
            For Multiple Choice questions, provide 4 options with exactly one correct answer.
            For Problem Solving questions, provide clear problem statements.
            
            Return your response as JSON in this exact format:
            {{
                "title": "Quiz title",
                "subject": "{subject}",
                "difficulty": "{difficulty}",
                "questions": [
                    {{
                        "type": "multiple_choice",
                        "question": "Question text with LaTeX if needed",
                        "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
                        "correct_answer": "A) Option 1",
                        "explanation": "Why this is correct"
                    }},
                    {{
                        "type": "problem_solving",
                        "question": "Problem statement",
                        "correct_answer": "Sample solution",
                        "explanation": "Detailed explanation"
                    }}
                ]
            }}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Generate a {quiz_type} quiz with {num_questions} questions"}
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
                max_tokens=2000
            )
            
            quiz_data = json.loads(response.choices[0].message.content)
            return quiz_data
            
        except Exception as e:
            # Return a fallback quiz structure
            return {
                "title": f"Error generating quiz: {str(e)}",
                "subject": subject,
                "difficulty": difficulty,
                "questions": []
            }
    
    def evaluate_quiz(self, quiz, user_answers):
        """
        Evaluate user answers and provide detailed feedback
        """
        try:
            results = {
                "score": 0,
                "total": len(quiz["questions"]),
                "feedback": []
            }
            
            for i, question in enumerate(quiz["questions"]):
                user_answer = user_answers.get(i, "")
                correct_answer = question["correct_answer"]
                
                # For multiple choice, direct comparison
                if question["type"] == "multiple_choice":
                    is_correct = user_answer == correct_answer
                    results["score"] += 1 if is_correct else 0
                    
                    results["feedback"].append({
                        "correct": is_correct,
                        "user_answer": user_answer,
                        "correct_answer": correct_answer,
                        "explanation": question["explanation"]
                    })
                
                # For problem solving, use AI to evaluate
                elif question["type"] == "problem_solving":
                    evaluation = self._evaluate_problem_solving(
                        question["question"], 
                        user_answer, 
                        correct_answer
                    )
                    
                    is_correct = evaluation["correct"]
                    results["score"] += evaluation["partial_credit"]
                    
                    results["feedback"].append({
                        "correct": is_correct,
                        "user_answer": user_answer,
                        "correct_answer": correct_answer,
                        "explanation": evaluation["explanation"]
                    })
            
            return results
            
        except Exception as e:
            return {
                "score": 0,
                "total": len(quiz["questions"]),
                "feedback": [{"error": f"Error evaluating quiz: {str(e)}"}]
            }
    
    def _evaluate_problem_solving(self, question, user_answer, correct_answer):
        """
        Use AI to evaluate problem-solving answers
        """
        try:
            system_prompt = """You are an expert STEM educator evaluating student responses.
            Compare the student's answer to the correct answer and provide fair assessment.
            
            Consider:
            - Mathematical accuracy
            - Approach and methodology
            - Partial credit for correct steps
            - Common mistakes
            
            Respond with JSON in this format:
            {
                "correct": true/false,
                "partial_credit": 0.0-1.0,
                "explanation": "detailed feedback including what was correct/incorrect"
            }
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Question: {question}\nStudent answer: {user_answer}\nCorrect answer: {correct_answer}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
                max_tokens=500
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            return {
                "correct": False,
                "partial_credit": 0.0,
                "explanation": f"Error evaluating answer: {str(e)}"
            }
    
    def generate_adaptive_question(self, subject, current_difficulty, performance_history):
        """
        Generate adaptive questions based on student performance
        """
        try:
            # Adjust difficulty based on performance
            if performance_history:
                avg_score = sum(performance_history) / len(performance_history)
                if avg_score > 0.8:
                    adjusted_difficulty = "Advanced" if current_difficulty != "Advanced" else "Advanced"
                elif avg_score < 0.6:
                    adjusted_difficulty = "Beginner" if current_difficulty != "Beginner" else "Beginner"
                else:
                    adjusted_difficulty = current_difficulty
            else:
                adjusted_difficulty = current_difficulty
            
            system_prompt = f"""Create a single adaptive question for {subject} at {adjusted_difficulty} level.
            
            The question should:
            1. Test key concepts appropriately for this difficulty
            2. Be engaging and educational
            3. Include proper mathematical notation if needed
            
            Return JSON in this format:
            {{
                "question": "Question text",
                "type": "multiple_choice",
                "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
                "correct_answer": "A) Option 1",
                "explanation": "Detailed explanation"
            }}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Generate an adaptive question for current performance level"}
                ],
                response_format={"type": "json_object"},
                temperature=0.8,
                max_tokens=800
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            return {
                "question": f"Error generating adaptive question: {str(e)}",
                "type": "multiple_choice",
                "options": ["A) Error", "B) Error", "C) Error", "D) Error"],
                "correct_answer": "A) Error",
                "explanation": "An error occurred while generating this question."
            }
