# EduPrompt - AI STEM Tutor

An AI-powered STEM tutoring application built with Streamlit that provides interactive learning experiences for students. The application leverages OpenAI's GPT-4o model to deliver personalized tutoring, step-by-step explanations, and quiz generation across various STEM subjects including Calculus, Linear Algebra, Data Science, and General Math.

## 🌐 Live Demo

**Visit the live application:** [EduPrompt](http://stemgenius.pro)

## ✨ Features

- **Interactive Q&A**: Ask questions and get detailed explanations with mathematical notation
- **Step-by-Step Explanations**: Break down complex problems into manageable steps
- **Quiz Practice**: Test your knowledge with adaptive quizzes
- **Progress Tracking**: Monitor your learning progress and performance
- **Multiple Subjects**: Support for Calculus, Linear Algebra, Data Science, and General Math
- **Adaptive Difficulty**: Content tailored to Beginner, Intermediate, and Advanced levels

## 🚀 Local Development

### Prerequisites

- Python 3.11 or higher
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/stemgenius.git
   cd stemgenius
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**
   
   You'll need an OpenAI API key to use this application. You can get one by signing up at [OpenAI's website](https://platform.openai.com/).
   
   **Option A: Environment variable (recommended)**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   
   **Option B: Create a .env file**
   ```bash
   echo "OPENAI_API_KEY=your-api-key-here" > .env
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   The application will be available at `http://localhost:8501`

## 🏗️ Project Structure

- `app.py` - Main Streamlit application
- `stem_tutor.py` - STEMTutor class for answering questions and explanations
- `quiz_generator.py` - QuizGenerator class for creating and evaluating quizzes
- `utils.py` - Utility functions for session management and content rendering
- `requirements.txt` - Python dependencies
- `pyproject.toml` - Project configuration

## 🧠 How It Works

### Core Components

1. **STEMTutor Class**: Provides personalized tutoring responses and step-by-step explanations
2. **QuizGenerator Class**: Creates customized quizzes based on subject, difficulty, and question type
3. **Session Management**: Tracks user progress and maintains conversation history
4. **LaTeX Rendering**: Supports mathematical notation for better learning experience

### AI Integration

- **Model**: OpenAI GPT-4o
- **Features**: Adaptive difficulty, subject-specific expertise, mathematical notation support
- **Response Format**: Structured JSON for quizzes, natural language for explanations

## 🎯 Usage

1. **Select Learning Mode**: Choose from Interactive Q&A, Step-by-Step Explanations, Quiz Practice, or Progress Tracking
2. **Choose Subject**: Select from Calculus, Linear Algebra, Data Science, or General Math
3. **Set Difficulty**: Choose Beginner, Intermediate, or Advanced level
4. **Start Learning**: Ask questions, solve problems, or take quizzes!

## 🔧 API Requirements

This application requires an OpenAI API key with access to the GPT-4o model. The API key should be set as an environment variable named `OPENAI_API_KEY`.

## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **AI**: OpenAI GPT-4o
- **Language**: Python 3.11+
- **Dependencies**: See `requirements.txt`

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Made with ❤️ for STEM education** 
