import os
from langchain.llms import Gemini
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from PyPDF2 import PdfReader

# Set up Gemini API
gemini = Gemini(api_key="your_gemini_api_key")

def extract_text_from_pdf(pdf_file):
    # Function to extract text from a PDF file
    text = ""
    with open(pdf_file, "rb") as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def generate_quiz_questions(text_content, num_questions=30):
    # Function to generate quiz questions based oson provided text content
    questions = []
    prompt_template = ChatPromptTemplate(
        template="You are a lecturer and should explain these themes. As a Fundamentals of Electrical Engineering lecturer, let's explore important themes. Deeply explain the lecture and solve some questions. Prepare me for the final exam based on this content: {text_content}"
    )
    for _ in range(num_questions):
        chain = LLMChain(llm=gemini, prompt=prompt_template)
        response = chain.run({"text_content": text_content})
        questions.append(response.strip())
    return questions

def process_pdf_files_in_folder(folder_path, output_file):

    with open(output_file, "w") as file:
        for filename in os.listdir(folder_path):
            if filename.endswith(".pdf"):
                pdf_file = os.path.join(folder_path, filename)
                text_content = extract_text_from_pdf(pdf_file)
                questions = generate_quiz_questions(text_content, num_questions=1)
                for idx, question in enumerate(questions):
                    file.write(f"{question}\n")
                file.write("\n")

def main():
    # Main function to orchestrate the process
    resource_folder = "/Users/bahauddin/Coding/quiz_creator"
    output_file = "Test_3.txt"
    process_pdf_files_in_folder(resource_folder, output_file)

if __name__ == "__main__":
    main()
