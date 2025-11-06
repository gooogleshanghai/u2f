from __future__ import annotations

import argparse
import json
from pathlib import Path

from .orchestrator import Orchestrator


def main():
    parser = argparse.ArgumentParser(description="Run U2Facilitator agent pipeline.")
    parser.add_argument("--input", type=Path, required=True, help="Path to JSON input.")
    parser.add_argument("--output", type=Path, help="Optional path to write JSON result.")
    parser.add_argument("--interactive", "-i", action="store_true", 
                       help="Enable interactive mode with human-in-the-loop at each agent stage.")
    args = parser.parse_args()

    payload = json.loads(args.input.read_text(encoding="utf-8"))
    
    if args.interactive:
        print("\n" + "🚀 Interactive Mode - You will participate in decisions after each agent stage".center(80, "="))
        print()
    
    orchestrator = Orchestrator(interactive=args.interactive)
    result_json = orchestrator.run_to_json(
        enabler_story=payload["enabler_story"],
        potential_fix=payload["potential_fix"],
        human_preferences=payload.get("human_preferences"),
    )

    if args.output:
        args.output.write_text(result_json, encoding="utf-8")
        if args.interactive:
            print(f"\n✅ Result saved to: {args.output}")
    else:
        if args.interactive:
            print("\n" + "📄 Final Result".center(80, "="))
        print(result_json)


if __name__ == "__main__":
    main()
