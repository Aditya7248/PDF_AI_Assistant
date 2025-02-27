# PDF AI Assistant 📚🤖

🚀 **Interact with your PDFs like never before!** Extract text, ask intelligent questions, highlight key sections, and generate summaries—all powered by OpenAI GPT-3.5. Seamlessly handle single or multiple PDFs and get instant insights with a user-friendly interface. 📃🌐

---

## **Features**

- **Text Extraction**:
  - Process single or multiple PDFs effortlessly.
  - Extract text from all pages using `pdfplumber`.

- **AI-Powered Interactions**:
  - Ask questions about your PDF content and get contextual responses.
  - Summarize PDFs into concise and meaningful insights.

- **Highlight Key Sections**:
  - Highlight relevant keywords/phrases in the original PDF.
  - Download the highlighted version for quick reference.

- **Error Handling**:
  - Handles invalid or non-text PDFs gracefully.
  - Provides clear prompts for issues like invalid file types.

---

## **Installation**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Aditya7248/PDF_AI_Assistant.git
   cd PDF_AI_Assistant
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up OpenAI API Key**:
   - For security reasons, users must provide their own OpenAI API key.
   - Create a `.env` file in the root directory.
   - Add your OpenAI API key:
     ```plaintext
     OPENAI_API_KEY=your_openai_api_key
     ```

---

## **Usage**

1. **Run the Application**:
   ```bash
   streamlit run main.py
   ```

2. **Interact with Your PDFs**:
   - Upload a PDF file (or multiple files).
   - Ask questions like: *"What is this document about?"* or *"Summarize this PDF."*
   - Highlight keywords/phrases and download the annotated PDF.

🎉 **Pro Tip:** Use the "Summarize" feature to get a quick overview of lengthy documents!

---

## **Example Interaction**

### **Screenshots**:
![App Screenshot](https://github.com/Aditya7248/PDF_AI_Assistant/blob/main/image%20and%20video/main%20screen1.png
)  
### **Demo Video**:
[PDF_AI_Assistant_Demo](https://github.com/user-attachments/assets/6f3aebf1-f2db-4fa5-8c0b-d697865a3faf) 


---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Contributions**

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## **Acknowledgements**

- [OpenAI](https://platform.openai.com/)
- [Streamlit](https://streamlit.io/)
- [pdfplumber](https://github.com/jsvine/pdfplumber)
- [PyMuPDF](https://pymupdf.readthedocs.io/)
- [Dotenv](https://pypi.org/project/python-dotenv/)

---

For questions or support, contact:
**Aditya Tiwari**
- LinkedIn: [LinkedIn](https://www.linkedin.com/in/aditya-tiwari-24b4b924a/)
- Email: tiwariaditya2707@gmail.com

