from openai import OpenAI
import json

# Agent 5: Study Notes
def generate_study_notes(transcript: str, context: dict) -> dict:
    """
    Generates structured study notes.
    """
    print(f"[NotesAgent] Generating study notes...")
    
    client = OpenAI()
    topic = context.get("topic", "General")
    
    prompt = f"""
    Create detailed, bullet-point study notes for the following video transcript about "{topic}".
    Focus on key definitions, processes, and important facts.
    Return ONLY a JSON object with a key "notes" containing a list of strings.
    
    Transcript (truncated):
    {transcript[:15000]}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a study aid generator. Output valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        content = response.choices[0].message.content.strip()
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "")
            
        return json.loads(content)
    except Exception as e:
        print(f"[NotesAgent] Error: {e}")
        return {"notes": [], "error": str(e)}
