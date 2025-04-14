# # import libraries

# from openai import OpenAI
# import yaml

# api_key = None
# CONFIG_PATH = r"config.yaml"

# with open(CONFIG_PATH) as file:
#     data = yaml.load(file, Loader=yaml.FullLoader)
#     api_key = data['OPENAI_API_KEY']

# def ats_extractor(resume_data):

#     prompt = '''
#     You are an AI bot designed to act as a professional for parsing resumes. You are given with resume and your job is to extract the following information from the resume:
#     1. full name
#     2. email id
#     3. github portfolio
#     4. linkedin id
#     5. employment details
#     6. technical skills
#     7. soft skills
#     Give the extracted information in json format only
#     '''

#     openai_client = OpenAI(
#         api_key = api_key
#     )    

#     messages=[
#         {"role": "system", 
#         "content": prompt}
#         ]
    
#     user_content = resume_data
    
#     messages.append({"role": "user", "content": user_content})

#     response = openai_client.chat.completions.create(
#                 model="gpt-3.5-turbo",
#                 messages=messages,
#                 temperature=0.0,
#                 max_tokens=1500)
        
#     data = response.choices[0].message.content

#     #print(data)
#     return data





import google.generativeai as genai
import yaml
import json
import re

# Load API key
CONFIG_PATH = r"config.yaml"
with open(CONFIG_PATH) as file:
    data = yaml.load(file, Loader=yaml.FullLoader)
    api_key = data['GEMINI_API_KEY']

# Configure Gemini
genai.configure(api_key=api_key)

def ats_extractor(resume_data):
    prompt = '''
You are an expert resume screening and analysis AI, trained in HR standards and ATS (Applicant Tracking System) optimization.

You are given a resume. Your tasks are:

1. **Evaluate the resume and give it a score out of 100**, based on clarity, completeness, relevance of information, formatting, and ATS-friendliness.
    - SCORE : 
2. **List all mistakes found**

    "Mistakes": 
    "line": "Full text of the line with mistake",
    "issue": "What is wrong",
    "suggestion": "What it should be instead"
    
Give the extracted information in json format only
    '''

    full_prompt = prompt + "\n\n" + resume_data

    model = genai.GenerativeModel('models/gemini-2.0-flash')
    response = model.generate_content(full_prompt)

    # Get the response text
    response_text = response.text.strip()

    # Extract JSON object using regex (safely captures JSON block)
    try:
        if isinstance(response_text, dict):
            return response_text  # already parsed? just return

        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON object found in response.")

        json_text = json_match.group(0)
        parsed_data = json.loads(json_text)
        return parsed_data

    except (json.JSONDecodeError, AttributeError, ValueError, TypeError) as e:
        print("⚠️ Error parsing JSON:", e)
        print("🔎 Raw Response:\n", response_text)
        return None
