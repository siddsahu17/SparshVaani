from .language_detector_agent import detect_language
from .transcription_agent import transcribe_video
from .context_agent import analyze_context
from .summary_agent import generate_summary
from .notes_agent import generate_study_notes
from .qa_agent import generate_qa
from .braille_agent import convert_to_braille
from .pdf_agent import generate_braille_pdf

# Orchestrator
def run_agent_workflow(youtube_url: str) -> dict:
    """
    Coordinators the execution of all agents.
    """
    results = {}
    print(f"--- Starting Multi-Agent Workflow for {youtube_url} ---")
    
    # 1. Language Detection
    lang_result = detect_language(youtube_url)
    results["language"] = lang_result.get("language", "en")
    print(f"STEP 1: Detected Language: {results['language']}")
    
    # 2. Transcription
    trans_result = transcribe_video(youtube_url, results["language"])
    results["transcript"] = trans_result.get("transcript", "")
    print(f"STEP 2: Transcription Complete (Length: {len(results['transcript'])})")
    
    if not results["transcript"]:
        return {"error": "Transcription failed."}
        
    # 3. Context Analysis
    context_result = analyze_context(results["transcript"])
    results["context"] = context_result
    print(f"STEP 3: Context Analyzed: {context_result.get('topic', 'Unknown')}")
    
    # 4. Summary
    summary_result = generate_summary(results["transcript"], results["context"])
    results["summary"] = summary_result.get("summary", "")
    print(f"STEP 4: Summary Generated")
    
    # 5. Study Notes
    notes_result = generate_study_notes(results["transcript"], results["context"])
    results["notes"] = notes_result.get("notes", [])
    print(f"STEP 5: Notes Generated ({len(results['notes'])} items)")
    
    # 6. Q&A
    qa_result = generate_qa(results["transcript"], results["context"])
    results["qa"] = qa_result.get("questions", [])
    print(f"STEP 6: Q&A Generated ({len(results['qa'])} items)")
    
    # 7. Braille Conversion
    braille_result = convert_to_braille(results["summary"], results["notes"], results["qa"])
    results["braille"] = braille_result
    print(f"STEP 7: Braille Conversion Complete")
    
    # 8. PDF Generation
    pdf_path = generate_braille_pdf(results)
    results["pdf_path"] = pdf_path
    print(f"STEP 8: PDF Generated at {pdf_path}")
    
    print("--- Workflow Complete ---")
    return results
