import streamlit as st
import pdfplumber
import openai
import fitz  
import io
import base64

# OpenAI API key
openai.api_key = "" # Enter you API Key - OpenAI API

# App Title
st.title("📚 PDF AI Assistant")
st.subheader("Upload PDFs (single or multiple) and interact with their content using AI")

# File Upload Mode
upload_mode = st.radio("Choose Upload Mode:", ["Single File", "Multiple Files"])

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

# Function to find matching sections
def find_matching_sections(pdf_text, answer):
    matches = []
    for keyword in answer.split():
        if keyword.lower() in pdf_text.lower():
            matches.append(keyword)
    return list(set(matches))  

# Function to interact with GPT-3.5 Turbo
def ask_gpt(prompt, combined_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant specialized in processing PDF content."},
                {"role": "user", "content": f"Here are the PDF contents:\n{combined_text}\n\n{prompt}"}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

# Function to display a PDF in Streamlit
def display_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f"""
        <iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="900" type="application/pdf"></iframe>
    """
    st.markdown(pdf_display, unsafe_allow_html=True)

# Function to highlight matches in the PDF
def highlight_pdf(file_object, output_pdf, matches):
    try:
        file_object.seek(0)  
        pdf_document = fitz.open(stream=file_object.read(), filetype="pdf")
    except Exception as e:
        raise ValueError(f"Error opening PDF: {e}")

    if pdf_document.page_count == 0:
        raise ValueError("The PDF has zero pages or is invalid.")

    for page in pdf_document:
        for match in matches:
            areas = page.search_for(match)
            for area in areas:
                page.add_highlight_annot(area)

    pdf_document.save(output_pdf)
    pdf_document.close()

# Single File Upload
if upload_mode == "Single File":
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    if uploaded_file:
        with st.spinner("Extracting text from the PDF..."):
            pdf_text = extract_text_from_pdf(uploaded_file)
        st.success("PDF text extracted successfully!")

        # Display extracted text
        with st.expander("📜 View Extracted PDF Text"):
            st.text_area("Extracted Text", pdf_text, height=300)

        # AI Interaction
        user_query = st.text_input("🔍 Ask something about the PDF:")
        
        # Display the AI response in a styled box
        if user_query:
            with st.spinner("Generating AI response..."):
                ai_response = ask_gpt(user_query, pdf_text)
            st.markdown(
                """
                <div style="
                    border: 1px solid #ccc; 
                    border-radius: 10px; 
                    padding: 15px; 
                    margin: 10px 0; 
                    background-color: #f9f9f9; 
                    font-family: Arial, sans-serif; 
                    color: black;">
                    <strong>🤖 AI Response:</strong>
                    <p style="margin-top: 10px;">{}</p>
                </div>
                """.format(ai_response.replace("\n", "<br>")),
                unsafe_allow_html=True,
            )


            # Export the AI response
            if st.button("💾 Download AI Response"):
                buffer = io.BytesIO()
                buffer.write(ai_response.encode())
                buffer.seek(0)
                st.download_button(
                    label="Download AI Response",
                    data=buffer,
                    file_name="ai_response.txt",
                    mime="text/plain"
                )

            # Highlight relevant sections
            if st.button("🔍 Highlight Relevant Sections"):
                matches = find_matching_sections(pdf_text, ai_response)
                highlighted_pdf_path = "highlighted_output.pdf"
                try:
                    highlight_pdf(uploaded_file, highlighted_pdf_path, matches)
                    st.success("Highlighted PDF generated successfully!")

                    # Display the highlighted PDF in Streamlit
                    display_pdf(highlighted_pdf_path)

                    # Add a download button for the highlighted PDF
                    with open(highlighted_pdf_path, "rb") as file:
                        st.download_button(
                            label="Download Highlighted PDF",
                            data=file,
                            file_name=highlighted_pdf_path,
                            mime="application/pdf"
                        )
                except ValueError as e:
                    st.error(f"Error: {e}")

        # Summarization Feature
        if st.button("📝 Summarize PDF"):
            with st.spinner("Summarizing the PDF content..."):
                summary = ask_gpt("Summarize the PDF.", pdf_text)
            st.markdown(
                """
                <div style="
                    border: 1px solid #ccc; 
                    border-radius: 10px; 
                    padding: 15px; 
                    margin: 10px 0; 
                    background-color: #f9f9f9; 
                    font-family: Arial, sans-serif; 
                    color: black;">
                    <strong>📋 PDF Summary:</strong>
                    <p style="margin-top: 10px;">{}</p>
                </div>
                """.format(summary.replace("\n", "<br>")),
                unsafe_allow_html=True,
            )


            # Export the summary
            if st.button("💾 Download Summary"):
                buffer = io.BytesIO()
                buffer.write(summary.encode())
                buffer.seek(0)
                st.download_button(
                    label="Download PDF Summary",
                    data=buffer,
                    file_name="pdf_summary.txt",
                    mime="text/plain"
                )

# Multiple File Upload
if upload_mode == "Multiple Files":
    uploaded_files = st.file_uploader("Upload multiple PDFs", type=["pdf"], accept_multiple_files=True)
    if uploaded_files:
        # Extract and combine text from all PDFs
        all_pdf_texts = {}
        for uploaded_file in uploaded_files:
            with st.spinner(f"Extracting text from {uploaded_file.name}..."):
                pdf_text = extract_text_from_pdf(uploaded_file)
                all_pdf_texts[uploaded_file.name] = pdf_text

        st.success("All PDFs have been processed!")

        # Display PDF contents
        with st.expander("📜 View Extracted PDF Texts"):
            for file_name, pdf_text in all_pdf_texts.items():
                st.markdown(f"### 📄 {file_name}")
                st.text_area(f"Extracted Text from {file_name}", pdf_text, height=200)

        # Combine all PDF text for AI querying
        combined_text = "\n\n".join([f"Document: {name}\n{text}" for name, text in all_pdf_texts.items()])

        # AI Interaction
        user_query = st.text_input("🔍 Ask something about the PDFs:")
        
        # Display the AI response in a styled box
        if user_query:
            with st.spinner("Generating AI response..."):
                ai_response = ask_gpt(user_query, pdf_text)
            st.markdown(
                """
                <div style="
                    border: 1px solid #ccc; 
                    border-radius: 10px; 
                    padding: 15px; 
                    margin: 10px 0; 
                    background-color: #f9f9f9; 
                    font-family: Arial, sans-serif; 
                    color: black;">
                    <strong>🤖 AI Response:</strong>
                    <p style="margin-top: 10px;">{}</p>
                </div>
                """.format(ai_response.replace("\n", "<br>")),
                unsafe_allow_html=True,
            )


            # Export the AI response
            if st.button("💾 Download AI Response"):
                buffer = io.BytesIO()
                buffer.write(ai_response.encode())
                buffer.seek(0)
                st.download_button(
                    label="Download AI Response",
                    data=buffer,
                    file_name="ai_response.txt",
                    mime="text/plain"
                )

            # Highlight relevant sections in multiple PDFs
            if st.button("🔍 Highlight Relevant Sections"):
                for uploaded_file in uploaded_files:
                    file_name = uploaded_file.name
                    if file_name in all_pdf_texts:
                        # Generate matches for the current file
                        matches = find_matching_sections(all_pdf_texts[file_name], ai_response)
                        highlighted_pdf_path = f"highlighted_{file_name}"
                        try:
                            highlight_pdf(uploaded_file, highlighted_pdf_path, matches)
                            st.success(f"Highlighted PDF for {file_name} generated successfully!")

                            # Display the highlighted PDF in Streamlit
                            display_pdf(highlighted_pdf_path)

                            # Add a download button for the highlighted PDF
                            with open(highlighted_pdf_path, "rb") as file:
                                st.download_button(
                                    label=f"Download Highlighted {file_name}",
                                    data=file,
                                    file_name=highlighted_pdf_path,
                                    mime="application/pdf"
                                )
                        except ValueError as e:
                            st.error(f"Error for {file_name}: {e}")

        # Summarization Feature
        if st.button("📝 Summarize PDF"):
            with st.spinner("Summarizing the PDF content..."):
                summary = ask_gpt("Summarize the PDF.", pdf_text)
            st.markdown(
                """
                <div style="
                    border: 1px solid #ccc; 
                    border-radius: 10px; 
                    padding: 15px; 
                    margin: 10px 0; 
                    background-color: #f9f9f9; 
                    font-family: Arial, sans-serif; 
                    color: black;">
                    <strong>📋 PDF Summary:</strong>
                    <p style="margin-top: 10px;">{}</p>
                </div>
                """.format(summary.replace("\n", "<br>")),
                unsafe_allow_html=True,
            )

            # Export the summary
            if st.button("💾 Download Summary"):
                buffer = io.BytesIO()
                buffer.write(summary.encode())
                buffer.seek(0)
                st.download_button(
                    label="Download PDF Summary",
                    data=buffer,
                    file_name="pdf_summary.txt",
                    mime="text/plain"
                )
