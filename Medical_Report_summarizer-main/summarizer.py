import openai

class MedicalReportSummarizer:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key

    def summarize_text(self, text):
        prompt = (
            "You are a helpful assistant that summarizes medical reports. "
            "Here is the medical report:\n\n{text}\n\n"
            "Please provide a summary in the following format:\n\n"
            "1. Patient Information:\n"
            "   - Age: [Provide age here]\n"
            "   - Date of Consultation: [Provide date of consultation here]\n"
            "   - Consultant: [Provide consultant's name here]\n"
            "\n"
            "2. Chief Complaint:\n"
            "   - [Provide chief complaint here]\n"
            "\n"
            "3. Current Condition:\n"
            "   - Diagnosis: [Provide diagnosis here]\n"
            "   - Assessment: [Provide assessment here]\n"
            "\n"
            "4. Physical Exam:\n"
            "   - [Provide physical exam details here]\n"
            "\n"
            "5. Lab Results:\n"
            "   - [Provide lab results here]\n"
            "\n"
            "6. Medications:\n"
            "   - Inpatient: [List inpatient medications]\n"
            "   - Home: [List home medications]\n"
            "\n"
            "7. Social and Environmental Screening:\n"
            "   - [Provide social and environmental screening details]\n"
            "\n"
            "8. Notes:\n"
            "   - [Provide additional notes here]\n"
            "\n"
            "9. Consultation Recommendation:\n"
            "   - [Provide consultation recommendations here]\n"
            "\n"
            "10. Signature:\n"
            "   - [Provide signature details]\n"
        ).format(text=text)

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes medical reports in a structured format."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1024,
                temperature=0.7,
            )
            summary = response.choices[0].message['content'].strip()
            return summary
        except Exception as e:
            print("Error in API request:", e)
            return None