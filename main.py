from transcript_service import get_video_id, fetch_transcript
from rag_engine import ComplianceRAG
from compliance import rule_based_audit
from llm import ollama_audit
from report import print_report, save_report

def main():
    print("\n" + "=" * 47)
    print("        YOUTUBE COMPLIANCE CHECKER         ")
    print("=" * 47)
    

    url = input("Enter YouTube URL: ").strip()
    if not url:
        print("Please enter a YouTube URL.")
        return

    try:
        video_id = get_video_id(url)
        print(f"\nVideo ID: {video_id}")
    except ValueError as e:
        print(f"Error: {e}")
        return

    print("\n[1/4] Getting YouTube transcript...")
    try:
        transcript_items = fetch_transcript(video_id)
    except Exception as e:
        print(f"Could not get transcript: {e}")
        print("\nTip: The video must have captions/subtitles available.")
        return

    transcript = " ".join(item["text"] for item in transcript_items)
    print(f"Transcript received: {len(transcript_items)} segments")

    print("\n[2/4] Loading compliance documents...")
    rag = ComplianceRAG("data")
    rag.load_documents()
    print(f"Knowledge base chunks: {len(rag.chunks)}")

    print("\n[3/4] Finding relevant rules...")
    context = rag.retrieve(transcript, top_k=5)
    print(f"Relevant rule chunks found: {len(context)}")

    print("\n[4/4] Running compliance analysis...")
    result = ollama_audit(transcript, context)

    # If local Ollama is not running, use a completely offline fallback.
    if result is None:
        print("Ollama not available. Using offline rule-based analysis.")
        result = rule_based_audit(transcript)

    result["video_id"] = video_id
    result["video_url"] = url

    print_report(result)

    output_file = save_report(result)
    print(f"\nReport saved to: {output_file}")

if __name__ == "__main__":
    main()
