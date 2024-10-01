from extracter import process_pdf
from summarizer import MedicalReportSummarizer


def summarize_medical_report(pdf_file_path):
    api_key = 'your key'
    summarizer = MedicalReportSummarizer(api_key)
    show_boxes = False
    extracted_text = process_pdf(pdf_file_path, show_boxes)
    if not extracted_text:
        return "No text extracted from PDF."
    summary = summarizer.summarize_text(extracted_text)
    if not summary:
        return "Failed to summarize the extracted text."
    print(summary)
    return summary




