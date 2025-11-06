"""
Interactive Human-in-the-Loop Example

Demonstrates how to use custom human feedback callback functions
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from u2f_code.context import ConversationContext
from u2f_code.orchestrator import Orchestrator


def custom_feedback_callback(stage: str, output: Any, ctx: ConversationContext) -> dict[str, Any]:
    """
    Custom human feedback callback function
    
    Can customize different interaction methods based on needs:
    - GUI interface
    - Web interface
    - Automated rules
    - Remote collaboration
    """
    print(f"\n🔔 Stage: {stage}")
    print(f"📊 Output: {output}")
    
    # Example: Automated rule - If discovery stage finds more than 3 defects, auto-trigger retry
    if stage == "discovery" and output.critical_defects.count("\n") > 3:
        print("⚠️  Too many defects detected, auto-triggering retry...")
        return {
            "continue": True,
            "feedback": "Please analyze the core problem more carefully to reduce the number of defects",
            "action": "retry"
        }
    
    # Use default interaction for other cases
    return {
        "continue": True,
        "feedback": "",
        "action": "proceed"
    }


def run_with_web_interface():
    """Example: Interactive mode integrated with Web interface"""
    
    def web_callback(stage: str, output: Any, ctx: ConversationContext) -> dict[str, Any]:
        # Can call Flask/FastAPI web frameworks here
        # Send results to frontend, wait for user feedback from web interface
        
        # Simulate web interaction
        print(f"📡 Sending to Web interface: {stage}")
        # response = web_api.get_user_feedback(stage, output)
        
        return {
            "continue": True,
            "feedback": "User feedback from web interface",
            "action": "proceed"
        }
    
    orchestrator = Orchestrator(interactive=True, human_feedback_callback=web_callback)
    # ... Run workflow


def run_with_ai_assistant():
    """Example: Use AI assistant to aid decision-making"""
    
    def ai_assisted_callback(stage: str, output: Any, ctx: ConversationContext) -> dict[str, Any]:
        # AI assistant analyzes current results and provides suggestions
        # suggestions = ai_analyzer.analyze(stage, output)
        
        print(f"\n🤖 AI Assistant Suggestion: ...")
        print(f"👤 Your Decision: ...")
        
        return {
            "continue": True,
            "feedback": "Human decision combined with AI suggestions",
            "action": "proceed"
        }
    
    orchestrator = Orchestrator(interactive=True, human_feedback_callback=ai_assisted_callback)
    # ... Run workflow


def main():
    """Standard interactive execution example"""
    
    # Method 1: Use default console interaction
    orchestrator = Orchestrator(interactive=True)
    
    # Method 2: Use custom callback
    # orchestrator = Orchestrator(interactive=True, human_feedback_callback=custom_feedback_callback)
    
    # Read input
    input_file = Path("u2f_code/sample_story.json")
    payload = json.loads(input_file.read_text(encoding="utf-8"))
    
    # Run
    result = orchestrator.run(
        enabler_story=payload["enabler_story"],
        potential_fix=payload["potential_fix"],
        human_preferences=payload.get("human_preferences"),
    )
    
    # Output result
    print("\n" + "="*80)
    print("🎉 Final Result")
    print("="*80)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
