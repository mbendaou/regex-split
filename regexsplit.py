from flask import Flask, request, render_template
import os
import re
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter

from flask import Flask, render_template

app = Flask(__name__, template_folder='/Users/mohamed/Desktop/Python/')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload():
    # Get the uploaded file
    f = request.files['file']

    # Save the uploaded file to disk
    filename = f.filename
    f.save(filename)

    # Define the regular expression to search for
    regex = r"ID:\s\d{5}\s?"

    # Open the PDF file in read-binary mode
    with open(filename, "rb") as pdf_file:
        # Read the PDF file into memory
        pdf_data = BytesIO(pdf_file.read())

        # Create a PdfReader object to read the PDF file
        pdf_reader = PdfReader(pdf_data)

        # Initialize a dictionary to store the matches found
        matches_dict = {}

        # Loop through each page in the PDF file
        for page_num, page in enumerate(pdf_reader.pages):
            # Extract the text from the page
            page_text = page.extract_text()

            # Search for the regular expression in the page text
            if re.search(regex, page_text):
                # Add the match to the dictionary
                match = re.findall(regex, page_text)[0]
                if match not in matches_dict:
                    matches_dict[match] = PdfWriter()
                matches_dict[match].add_page(page)

        # Save the PDF files for each group of matches
        for match, writer in matches_dict.items():
            output_filename = re.sub(r'\D', '', match.strip()) + ".pdf"
            with open(output_filename, "wb") as output_file:
                writer.write(output_file)

        # Return a message to the user
        message = f"Found {len(matches_dict)} instances of the regular expression."
        return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
