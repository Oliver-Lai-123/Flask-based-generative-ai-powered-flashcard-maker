from flask import Flask, render_template, request, redirect, url_for
import PyPDF2
from openai import OpenAI
import os
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
client = OpenAI(api_key="change it") #change it 

class FlashcardGenerator:
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        """Extract text content from a PDF file."""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                logger.info(f"Successfully extracted {len(text)} characters from PDF")
                return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise

    @staticmethod
    def generate_flashcards(text: str) -> str:
        """Generate flashcards using OpenAI's GPT model."""
        try:
            # Limit text length if necessary
            max_length = 4000  # Adjust this value based on your needs
            if len(text) > max_length:
                logger.warning(f"Text too long ({len(text)} chars), truncating to {max_length}")
                text = text[:max_length]

            logger.info("Sending request to OpenAI API")
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Create flashcards in a Q&A format from the provided text. Format each flashcard as 'Q: [question]\nA: [answer]\n\n'"},
                    {"role": "user", "content": f"Create 5-10 concise flashcards from this text:\n\n{text}"}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            flashcards = response.choices[0].message.content.strip()
            logger.info("Successfully generated flashcards")
            return flashcards

        except Exception as e:
            logger.error(f"Error generating flashcards: {str(e)}")
            raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        if 'pdf_file' not in request.files:
            logger.warning("No file uploaded")
            return redirect(url_for('index'))
        
        pdf_file = request.files['pdf_file']
        if pdf_file.filename == '':
            logger.warning("Empty filename")
            return redirect(url_for('index'))
        
        # Create uploads directory if it doesn't exist
        upload_dir = os.path.join(app.root_path, "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save the uploaded file
        pdf_path = os.path.join(upload_dir, pdf_file.filename)
        pdf_file.save(pdf_path)
        logger.info(f"Saved PDF file to {pdf_path}")
        
        # Generate flashcards
        generator = FlashcardGenerator()
        extracted_text = generator.extract_text_from_pdf(pdf_path)
        
        if not extracted_text.strip():
            raise ValueError("No text could be extracted from the PDF")
            
        flashcards = generator.generate_flashcards(extracted_text)
        
        # Clean up
        os.remove(pdf_path)
        logger.info("Cleaned up temporary PDF file")
        
        return render_template('result.html', flashcards=flashcards)
        
    except Exception as e:
        logger.error(f"Error in generate route: {str(e)}")
        error_message = f"An error occurred: {str(e)}"
        return render_template('error.html', message=error_message)

if __name__ == '__main__':
    app.run(debug=True)