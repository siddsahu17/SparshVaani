from openai import OpenAI
import json

# Agent 6: Q&A / Exam Prep
def generate_qa(transcript: str, context: dict) -> dict:
    """
    Generates Q&A pairs for exam preparation.
    """
    print(f"[QAAgent] Generating Q&A...")
    
    client = OpenAI()
    topic = context.get("topic", "General")
    
    prompt = f"""
    Generate 5 important exam-style questions and answers based on the transcript about "{topic}".
    Return ONLY a JSON object with a key "questions" containing a list of objects, each with "question" and "answer" keys.
    
    Transcript (truncated):
    {transcript[:15000]}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a teacher creating an exam. Output valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        content = response.choices[0].message.content.strip()
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "")
            
        return json.loads(content)
    except Exception as e:
        print(f"[QAAgent] Error: {e}")
        return {"questions": [], "error": str(e)}
