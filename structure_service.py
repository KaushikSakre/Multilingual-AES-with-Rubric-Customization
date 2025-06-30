import os
import json
from llm_config import llm  # Import the initialized LLM
import re
example_input1 = {
  "topic": "The Role of Technology in Modern Education",
  "standard": "10th Grade",
  "difficulty_level": "Medium",
  "language": "English"}
english_sample = {"rubric": [
    {
      "section": "Introduction",
      "description": "Clearly introduces the topic and presents the main idea of the essay.",
      "percentage": 10
    },
    {
      "section": "Main Body - Arguments and Examples",
      "description": "Presents logical arguments supported by examples, explaining how technology impacts education.",
      "percentage": 40
    },
    {
      "section": "Conclusion",
      "description": "Summarizes key points and gives a closing thought related to the essay topic.",
      "percentage": 10
    },
    {
      "section": "Grammar and Vocabulary",
      "description": "Correct use of grammar, punctuation, and age-appropriate vocabulary.",
      "percentage": 15
    },
    {
      "section": "Coherence and Organization",
      "description": "Smooth flow of ideas with clear structure and well-connected paragraphs.",
      "percentage": 15
    },
    {
      "section": "Relevance and Originality",
      "description": "All content is relevant to the topic and includes original thoughts or examples.",
      "percentage": 10
    }
  ]
}
example_input2 = {
  "topic": "शालेय शिक्षणातील तंत्रज्ञानाचे महत्त्व",
  "standard": "10th Grade",
  "difficulty_level": "Medium",
  "language": "Marathi"}
marathi_sample = {"rubric": [
    {
      "section": "प्रस्तावना",
      "description": "विषयाची स्पष्ट ओळख आणि उद्दिष्ट मांडणी",
      "percentage": 10
    },
    {
      "section": "मुद्दे व विवेचन",
      "description": "युक्तिवादांची सुसंगत मांडणी व योग्य उदाहरणांचा वापर",
      "percentage": 40
    },
    {
      "section": "निष्कर्ष",
      "description": "विवेचनाचे सारांश आणि स्पष्ट निष्कर्ष",
      "percentage": 10
    },
    {
      "section": "व्याकरण",
      "description": "योग्य वाक्यरचना, विरामचिन्हांचा वापर",
      "percentage": 15
    },
    {
      "section": "सुसंगती",
      "description": "संपूर्ण निबंधामधील प्रवाह आणि सुसंगती",
      "percentage": 15
    },
    {
      "section": "मौलिकता",
      "description": "नवीन विचार, स्वतःची मते व उदाहरणांचा समावेश",
      "percentage": 10
    }
  ]
}
def generate_essay_structure(topic, difficulty, standard, language):
    """
    Generates an essay structure dynamically based on the provided parameters.
    """
    language_instruction = f"""
    The rubric must be fully written in **{language}**.
    Do not use English if the language is Marathi or Hindi.
    All section titles and descriptions must be in {language}.
    """
    prompt = f"""
    Act as an expert essay rubric designer. You have experience in creating detailed essay structures for various
    topics, difficulty levels(easy, medium, hard) and for different standards(e.g., 8th grade, 12th grade)where admins may later modify them for refinement before use in assessments.
    Creates appropriate rubrics in different languages.(English, Marathi, Hindi).
    User will provide: 
    topic:{topic} 
    difficulty level:{difficulty}
    standard:{standard}
    Language:{language} 
    {language_instruction}
    your task is to create a detailed essay structure.
    Follow these instructions:
    1. Generate a detailed Rubric with section-wise weightage and details.
    2. Ensure the total percentage weight is 100%.
    3. Include both the content(Introduction, Main body, conclusion) and language criteria(grammar,coherence, relevance, organization) of the essay. **Ensure that the language criteria are evaluated based on the specific norms and expectations of the chosen language.**
    4. Include a breakdown of each section with its percentage weightage and details.
    5. Use simple and understandable language.
    6. Avoid using complex jargon or technical terms.
    7. Ensure the difficulty level and standard are appropriate for the topic.
    8. Keep the rubrics language consistent with the input language.
    9. Provide the output in a structured JSON format.
    if language.lower() == "marathi":
        example_output = f"\nExample output format (Marathi):\n{marathi_sample}"
    elif language.lower() == "hindi":
        example_output = "\n(Note: use same sample as for marathi )\n"
    else:
        example_output = f"\nExample output format (English):\n{english_sample}"
        
    - **Return only pure valid JSON** (no text, no comments, no extra explanation).
    - **Use double quotes (") only.**
    - No extra spaces inside keys.
    - No extra output except JSON.


    """
    response = llm.invoke(prompt)
    if not response or not response.content:
        raise ValueError("❌ Empty response from LLM in generate_essay_structure.")

    raw = str(response.content).strip()  # ✅ Convert to string safely

    print("🔍 Raw LLM Output:\n", raw)

    # Try to extract JSON from markdown if needed
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
    json_text = match.group(1) if match else raw

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        print("❌ JSON Decode Error:", e)
        print("📎 Problematic content:\n", raw)
        return {"error": "Invalid JSON returned from LLM"}
  # Ensure parsed JSON in API


def edit_essay_structure(original_structure, current_structure, user_edits, previous_edits=""):
    """
    Edits the essay structure incrementally.
    - Ensures weight remains 100%.
    - Keeps track of previous modifications.
    - Returns only the modified sections with a summary of changes.
    """
    prompt = f"""
    You are modifying an essay structure **without altering its logical flow**. 
    Apply the requested modifications **on top of the most recent version** while keeping past edits intact.

    ### Original Structure
    {json.dumps(original_structure, indent=2, ensure_ascii=False)}

    ### Current Version (Most Recent)
    {json.dumps(current_structure, indent=2, ensure_ascii=False)}


    ### **User Edits**
    {user_edits}

    ### **Editing Guidelines**
    - Apply changes incrementally without discarding previous edits.
    - Ensure **total weightage remains exactly 100%**.
    - Adjust weight distribution proportionally if a section is removed/increased.
    - Do **not** add new sections unless explicitly requested.
    - Return a **structured JSON output**:
      {{
          "updated_structure": {{
              "section_name": {{"weight": X, "details": ["Updated details"]}}
          }},
          "modifications": ["Step-by-step changes applied"]
      }}
    """
    response = llm.invoke(prompt)
    return response.content  # Ensure it's parsed JSON
