from openai import OpenAI

# Agent 4: Summary Generation
def generate_summary(transcript: str, context: dict) -> dict:
    """
    Generates a concise summary based on the transcript and context.
    """
    print(f"[SummaryAgent] Generating summary...")
    
    client = OpenAI()
    
    # Use context to guide the summary
    topic = context.get("topic", "General")
    intent = context.get("intent", "General")
    
    prompt = f"""
    Generate a comprehensive yet concise summary of the following educational video transcript.
    The video is about "{topic}" and appears to be a "{intent}".
    
    Transcript (truncated):
    {transcript[:15000]}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert summarizer. Return a single string summary."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        return {"summary": response.choices[0].message.content.strip()}
    except Exception as e:
        print(f"[SummaryAgent] Error: {e}")
        return {"summary": "Error generating summary.", "error": str(e)}
