
# PDF to CSV Extractor
The script of this repository extracts specific data from PDF files and writes it to a CSV file. The PDF file should have a specific format, and the data is extracted based on predefined labels.


![pdf_template](https://user-images.githubusercontent.com/73304837/217801727-0b61f57c-3eba-4021-9a14-8481fa1e3cec.png)


## Usage
The script is executed from the command line. The PDF file path is passed as an argument. The extracted data is saved to a CSV file with the same name as the PDF file, in the same directory using the following code:
```
python pdf_to_csv_extractor.py /path/to/pdf/file.pdf
```

![Screenshot from 2023-02-09 05-56-11](https://user-images.githubusercontent.com/73304837/218604194-05cf1c91-02b2-4d95-8968-63fd5d6fbf6f.png)


## Requirements
This script requires the following libraries:
click
pandas
fitz

These can be installed using pip:
pip install click pandas PyMuPDF
PDF File Format

## Output
The script creates a CSV file with the following columns:
Main Billing/Entity
Client ID
Addressee
Salutation
Address
Email
Filter
Partner Name
Category
Turnover
Cost
Associates
The CSV file is saved in the same directory as the input PDF file, with the same name but with the .csv extension.

## Troubleshooting
If the input file is not a valid PDF file or if the PDF file does not have the correct format, an error message is displayed.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
