# Interactive Mode Usage Guide

## Overview

The U2Facilitator now supports interactive mode, allowing human-in-the-loop participation at each agent stage (Discovery, Exploration, Integration).

## Quick Start

### 1. Non-Interactive Mode (Original)
```bash
poetry run python -m u2f_code.cli --input sample_story.json --output result.json
```

### 2. Interactive Mode (New)
```bash
poetry run python -m u2f_code.cli --input sample_story.json --output result.json --interactive
# or use short flag
poetry run python -m u2f_code.cli --input sample_story.json -i
```

## How It Works

### Interactive Flow

```
┌─────────────────────────────────────────────────────┐
│  1. Discovery Agent Runs                            │
│     ↓                                                │
│  2. Show Results to Human                           │
│     ↓                                                │
│  3. Human Chooses Action:                           │
│     • Proceed → Continue to next stage              │
│     • Retry → Re-run Discovery with feedback        │
│     • Feedback → Add feedback and continue          │
│     • Stop → Terminate execution                    │
│     ↓                                                │
│  4. Exploration Agent Runs                          │
│     ↓                                                │
│  5. Show Results to Human                           │
│     ↓                                                │
│  6. Human Chooses Action (same options)             │
│     ↓                                                │
│  7. Integration Agent Runs                          │
│     ↓                                                │
│  8. Show Results to Human                           │
│     ↓                                                │
│  9. Human Chooses Action (same options)             │
│     ↓                                                │
│  10. Final Result                                   │
└─────────────────────────────────────────────────────┘
```

### User Actions at Each Stage

When an agent stage completes, you'll see:

```
================================================================================
🤖 Agent Stage Completed: DISCOVERY
================================================================================

📋 Core Problem:
[Analysis output...]

💡 Baseline Solution:
[Solution output...]

⚠️  Critical Defects:
[Defects output...]

--------------------------------------------------------------------------------
Please choose next action:
  1. Proceed - Continue to next stage
  2. Retry - Re-execute current stage
  3. Feedback - Provide feedback and continue
  4. Stop - Terminate execution

Choice [1/2/3/4]:
```

#### Option Details:

- **1. Proceed**: Continue to the next agent stage without changes
- **2. Retry**: Re-run the current stage (you'll be prompted to provide feedback/reason)
- **3. Feedback**: Provide feedback that will be injected into `human_preferences` for subsequent stages
- **4. Stop**: Terminate execution immediately and return current results

## Programmatic Usage

### Method 1: Default Console Interaction

```python
from u2f_code.orchestrator import Orchestrator

orchestrator = Orchestrator(interactive=True)
result = orchestrator.run(
    enabler_story="...",
    potential_fix="...",
    human_preferences="..."
)
```

### Method 2: Custom Callback Function

```python
from u2f_code.orchestrator import Orchestrator
from u2f_code.context import ConversationContext
from typing import Any

def my_custom_callback(stage: str, output: Any, ctx: ConversationContext) -> dict[str, Any]:
    """
    Custom human feedback handler
    
    Returns:
        {
            'continue': bool,      # Whether to continue execution
            'feedback': str,       # Human feedback text
            'action': str         # 'proceed', 'retry', or 'stop'
        }
    """
    # Your custom logic here
    # Could integrate with: GUI, Web UI, Slack bot, etc.
    
    return {
        "continue": True,
        "feedback": "Custom feedback here",
        "action": "proceed"
    }

orchestrator = Orchestrator(
    interactive=True, 
    human_feedback_callback=my_custom_callback
)
```

### Method 3: Automated Rules

```python
def automated_callback(stage: str, output: Any, ctx: ConversationContext) -> dict[str, Any]:
    # Auto-retry if discovery finds too many defects
    if stage == "discovery" and output.critical_defects.count("\n") > 5:
        return {
            "continue": True,
            "feedback": "Too many defects - please refine analysis",
            "action": "retry"
        }
    
    # Auto-proceed for other cases
    return {
        "continue": True,
        "feedback": "",
        "action": "proceed"
    }

orchestrator = Orchestrator(
    interactive=True,
    human_feedback_callback=automated_callback
)
```

## Output Format

The result includes additional fields when interactive mode is used:

```json
{
  "core_problem": "...",
  "baseline_solution": "...",
  "critical_defects": "...",
  "exploration_analysis": "...",
  "integration_synthesis": "...",
  "search_log": [...],
  "terminated_by_user": false,
  "final_human_preferences": "innovation first\n[Discovery Feedback]: ..."
}
```

- `terminated_by_user`: `true` if user chose "Stop" action
- `final_human_preferences`: Accumulated human preferences including all feedback from interactive sessions

## Use Cases

### 1. Research & Development
- Manually guide agent reasoning at each stage
- Experiment with different feedback approaches
- Fine-tune agent behavior

### 2. High-Stakes Decisions
- Review critical analysis before proceeding
- Add domain expertise at key decision points
- Ensure alignment with business requirements

### 3. Training & Evaluation
- Observe agent reasoning process
- Provide corrective feedback
- Build evaluation datasets

### 4. Web/GUI Integration
- Implement custom callback for web interface
- Enable remote collaboration
- Support async human-agent interaction

## Example: Web Interface Integration

```python
from flask import Flask, request, jsonify
from u2f_code.orchestrator import Orchestrator
import queue

app = Flask(__name__)
feedback_queue = queue.Queue()

def web_callback(stage: str, output: Any, ctx: ConversationContext) -> dict[str, Any]:
    # Send to web frontend
    send_to_frontend(stage, output)
    
    # Wait for human response from web UI
    feedback = feedback_queue.get()  # Blocking
    return feedback

@app.route('/feedback', methods=['POST'])
def receive_feedback():
    feedback = request.json
    feedback_queue.put(feedback)
    return jsonify({"status": "received"})

# Run orchestrator in background thread with web_callback
```

## See Also

- `interactive_example.py` - Complete examples with different callback implementations
- `sample_story.json` - Sample input format
- `orchestrator.py` - Core implementation

## Tips

1. **Start with Interactive Mode**: Use `-i` flag initially to understand agent behavior
2. **Provide Specific Feedback**: More specific feedback leads to better retry results
3. **Build Custom Callbacks**: For production, implement callback that fits your workflow
4. **Log Interactions**: Save interactive sessions for analysis and improvement
