# Flask-based-generative-ai-powered-flashcard-maker

This is a Flask-based web application that allows users to upload a PDF file, extract text from it, and generate flashcards using OpenAI's GPT model. The flashcards are presented in a Q&A format.

## Features

- Upload PDF files to extract text content.
- Generate concise flashcards in Q&A format using OpenAI's GPT model.
- User-friendly web interface built with Flask.

## Requirements

- Python 3.8 or later
- Flask
- PyPDF2
- OpenAI Python library

## Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Oliver-Lai-123/Flask-based-generative-ai-powered-flashcard-maker
   cd Flask-based-generative-ai-powered-flashcard-maker
   ```

2. **Install Dependencies:**
   Use pip to install the required Python libraries from requirements.txt:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure OpenAI API Key:**
   Replace the placeholder `change it` in the app.py with your OpenAI API key.
   
5. **Run the Application:**

   ```bash
   python app.py
   ```

   The application will run on `http://127.0.0.1:5000/` by default.

6. **Access the Application:**
   Open a web browser and go to `http://127.0.0.1:5000/`.

## File Structure

```
.
├── app.py             # Main Flask application
├── templates/         # HTML templates for the web app
│   ├── index.html     # Upload page
│   ├── result.html    # Flashcards display page
│   └── error.html     # Error page
├── uploads/           # Temporary storage for uploaded PDFs
├── requirements.txt   # List of dependencies (optional)
└── README.md          # Project documentation
```

## Usage

1. Navigate to the application homepage.
2. Upload a PDF file using the provided form.
3. The application will extract text from the uploaded PDF and generate flashcards.
4. View the generated flashcards on the results page.

## Notes
- Ensure to include your API key to app.py
- The application truncates text to a maximum length (default: 4000 characters) to meet OpenAI's input size limitations.
- Temporary PDF files are cleaned up after processing.
- Ensure that the uploaded PDFs contain extractable text (not images or scanned documents without OCR).
