import json
import re
from llm_config import llm  


def detect_rubric_language(rubric):
    """
    Detects the language used in the rubric based on Unicode patterns.
    Supports English, Hindi, and Marathi.
    """
    section_text = ""
    if isinstance(rubric, dict) and "rubric" in rubric:
        rubric = rubric["rubric"]

    if isinstance(rubric, list) and rubric:
        section_text = rubric[0].get("section", "") + rubric[0].get("description", "")

    # Marathi Unicode range (Devanagari + Marathi-specific words)
    if re.search(r'[अ-हऀ-ॿ]', section_text):
        if 'च्या' in section_text or 'विवेचन' in section_text or 'निबंध' in section_text:
            return "Marathi"
        elif 'के' in section_text or 'है' in section_text:
            return "Hindi"
        else:
            return "Hindi"  # fallback to Hindi for Devanagari
    else:
        return "English"


def evaluate_essay(essay_text, rubrics):
    """
    Evaluates the essay based on finalized rubrics.
    - Uses rubric-defined weight distribution for content & grammar.
    """
    detected_language = detect_rubric_language(rubrics)
   
    example_format = {
        "score_report": [
            {
                "section": "Introduction",
                "percentage": 10,
                "percentage_awarded": 8,
                "comment": "Good opening, but essay statement could be clearer."
            },
            {
                "section": "Body",
                "percentage": 40,
                "percentage_awarded": 34,
                "comment": "Strong arguments with age-appropriate examples. Slightly more elaboration needed on second point."
            },
            {
                "section": "Conclusion",
                "percentage": 10,
                "percentage_awarded": 9,
                "comment": "Well-rounded conclusion with a clear personal opinion."
            },
            {
                "section": "Grammar and Spelling",
                "percentage": 15,
                "percentage_awarded": 13,
                "comment": "Minor grammar issues, mostly well-written."
            },
            {
                "section": "Coherence and Relevance",
                "percentage": 15,
                "percentage_awarded": 14,
                "comment": "Ideas flowed well and all content stayed on topic."
            },
            {
                "section": "Creativity",
                "percentage": 10,
                "percentage_awarded": 9,
                "comment": "Included a personal story that added originality."
            }
        ],
        "percentage_awarded": 87.0,
        "overall_feedback": "A well-structured essay with thoughtful arguments and good organization. Minor improvements in grammar and clarity of essay could enhance it further."
    }
    

    formatted_rubric = json.dumps(rubrics, indent=2, ensure_ascii=False)
    example_json = json.dumps(example_format, indent=2, ensure_ascii=False)

    prompt = f"""
    You are an expert essay evaluator. Your task is to evaluate the essay based on the provided rubric.

    ### Essay Text:
    {essay_text}

    ### Rubric:
    {formatted_rubric}

    ### Instructions:
    1. Carefully read each section of the rubric. Each section includes:
    - A section title (e.g., "Introduction", "Grammar", "Creativity", etc.)
    - A description of what should be present in that section of the essay.
    - A weightage (percentage) indicating its contribution to the final score.

    2. For **each section**:
    - Locate and assess the corresponding content in the essay.
    - Judge how well the essay meets the expectations described in the rubric.
    - Assign a **percentage_awarded** for that section (out of its given weight).
    - Write a **comment** justifying the score (e.g., strengths, gaps, or suggestions).

    3. After evaluating all sections, compute the **total score** out of 100 based on the awarded percentage for each section.

    4. Provide an **overall_feedback** paragraph that summarizes the essay’s strengths and areas for improvement.
    5. While providing feedback, ensure to use the same language as {detected_language} used in the rubric.
    6. Do not use the term "thesis" or "thesis statement".
    7. Use simple and clear language, avoiding technical jargon or complex terms.
    Follow this JSON format strictly:
    {example_json}

    Note:
    - Ensure the structure and keys are exactly as shown.
    - Feedback must be in the same language as the essay.
    - Avoid repeating rubric descriptions. Focus only on how the essay performs.
    - Use clear and simple words.
    - Avoid using technical jargon or complex terms.
    - Do not use the term "thesis" or "thesis statement".
    Provide only the final JSON output.
    """

    response = llm.invoke(prompt)
    if not response or not response.content.strip():
        raise ValueError("❌ Empty response from LLM in evaluation_service.")

    try:
        # Attempt to extract JSON from code block if present
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", response.content, re.DOTALL)
        json_text = match.group(1) if match else response.content.strip()

        print("🧪 Raw Evaluation Response:\n", response.content)
        return json.loads(json_text)

    except Exception as e:
        print("❌ Failed to parse LLM evaluation response:")
        print(response.content)
        raise e
