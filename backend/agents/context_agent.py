import json
from openai import OpenAI

# Agent 3: Context Understanding
def analyze_context(transcript: str) -> dict:
    """
    Analyzes the transcript to extract topic, subtopics, key concepts, and intent.
    """
    print(f"[ContextAgent] Analyzing context...")
    
    client = OpenAI()
    
    if not transcript or len(transcript) < 50:
        return {"topic": "Unknown", "subtopics": [], "key_points": [], "intent": "Unknown"}

    prompt = f"""
    Analyze the following educational video transcript and extract structured context.
    Return ONLY a JSON object with the following keys:
    - "topic": String (Main topic)
    - "subtopics": List of Strings
    - "key_points": List of Strings (Core concepts taught)
    - "intent": String (e.g., "Lecture", "Tutorial", "Vlog", "News")

    Transcript (first 15000 chars):
    {transcript[:15000]}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an educational AI assistant. Output valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        content = response.choices[0].message.content.strip()
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "")
            
        return json.loads(content)
    except Exception as e:
        print(f"[ContextAgent] Error: {e}")
        return {"error": str(e)}
