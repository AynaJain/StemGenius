import os
import json
from openai import OpenAI
import streamlit as st

class STEMTutor:
    def __init__(self):
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"
    
    def answer_question(self, question, subject, difficulty):
        """
        Provide detailed answers to STEM questions with adaptive difficulty
        """
        try:
            system_prompt = f"""You are an expert STEM tutor specializing in {subject}. 
            Your student is at {difficulty} level. Provide clear, educational answers that:
            
            1. Are appropriate for {difficulty} level students
            2. Use proper mathematical notation (LaTeX format when needed)
            3. Include relevant examples or analogies
            4. Encourage further learning
            5. Are pedagogically sound
            
            For mathematical expressions, use LaTeX format like $x^2$ or $$\\frac{{d}}{{dx}}f(x)$$
            
            Subject focus: {subject}
            Difficulty: {difficulty}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"I apologize, but I encountered an error while processing your question: {str(e)}. Please try again or rephrase your question."
    
    def explain_step_by_step(self, problem, subject, difficulty):
        """
        Provide step-by-step explanations for complex problems
        """
        try:
            system_prompt = f"""You are an expert STEM tutor providing step-by-step solutions.
            Break down the problem into clear, logical steps appropriate for {difficulty} level students.
            
            Your response should:
            1. Clearly identify what needs to be solved
            2. Break the solution into numbered steps
            3. Explain the reasoning behind each step
            4. Use proper mathematical notation (LaTeX format)
            5. Provide the final answer
            6. Include any important tips or common mistakes to avoid
            
            Subject: {subject}
            Difficulty: {difficulty}
            
            Format your response with clear step divisions and mathematical expressions using LaTeX.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Please solve this step by step: {problem}"}
                ],
                temperature=0.5,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"I apologize, but I encountered an error while generating the step-by-step solution: {str(e)}. Please try again."
    
    def assess_difficulty(self, user_response, correct_answer):
        """
        Assess if the current difficulty is appropriate based on user performance
        """
        try:
            system_prompt = """You are an educational assessment expert. 
            Based on the user's response compared to the correct answer, determine if the current difficulty level is appropriate.
            
            Respond with JSON in this format:
            {
                "assessment": "too_easy|appropriate|too_hard",
                "confidence": 0.0-1.0,
                "reasoning": "brief explanation"
            }
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"User response: {user_response}\nCorrect answer: {correct_answer}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            return {
                "assessment": "appropriate",
                "confidence": 0.5,
                "reasoning": f"Error in assessment: {str(e)}"
            }
    
    def generate_hint(self, problem, subject, difficulty):
        """
        Generate helpful hints for problems without giving away the answer
        """
        try:
            system_prompt = f"""You are a helpful STEM tutor providing hints for {subject} problems.
            Generate a helpful hint that guides the student toward the solution without giving it away.
            
            The hint should:
            1. Be appropriate for {difficulty} level students
            2. Point toward the key concept or method needed
            3. Not solve the problem directly
            4. Encourage the student to think through the next step
            
            Subject: {subject}
            Difficulty: {difficulty}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Provide a hint for this problem: {problem}"}
                ],
                temperature=0.6,
                max_tokens=200
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"I apologize, but I encountered an error while generating a hint: {str(e)}. Please try working through the problem step by step."
