from __future__ import annotations

import json
from typing import Any, Callable

from .agents.discovery import DiscoveryAgent
from .agents.exploration import ExplorationAgent
from .agents.integration import IntegrationAgent
from .context import ConversationContext
from .search import SearchAugmentor


class Orchestrator:
    def __init__(self, interactive: bool = False, human_feedback_callback: Callable | None = None):
        """
        Initialize Orchestrator
        
        Args:
            interactive: Enable interactive mode with human feedback after each agent stage
            human_feedback_callback: Custom human feedback callback function receiving (stage, output, ctx) parameters
        """
        search = SearchAugmentor()
        self.discovery = DiscoveryAgent()
        self.exploration = ExplorationAgent(search=search)
        self.integration = IntegrationAgent(search=search)
        self.interactive = interactive
        self.human_feedback_callback = human_feedback_callback

    def _get_human_feedback(self, stage: str, output: Any, ctx: ConversationContext) -> dict[str, Any]:
        """
        Get human feedback
        
        Args:
            stage: Current stage name ('discovery', 'exploration', 'integration')
            output: Output result of the current stage
            ctx: Conversation context
            
        Returns:
            Dictionary containing human feedback: {'continue': bool, 'feedback': str, 'action': str}
            - continue: Whether to continue execution
            - feedback: Human's text feedback
            - action: 'proceed' (continue), 'retry' (retry current stage), 'modify' (modify and continue)
        """
        if self.human_feedback_callback:
            return self.human_feedback_callback(stage, output, ctx)
        
        # Default console interaction implementation
        return self._default_console_feedback(stage, output, ctx)
    
    def _default_console_feedback(self, stage: str, output: Any, ctx: ConversationContext) -> dict[str, Any]:
        """Default console human-in-the-loop interaction implementation"""
        print("\n" + "="*80)
        print(f"🤖 Agent Stage Completed: {stage.upper()}")
        print("="*80)
        
        if stage == "discovery":
            print(f"\n📋 Core Problem:\n{output.core_problem}")
            print(f"\n💡 Baseline Solution:\n{output.baseline_solution}")
            print(f"\n⚠️  Critical Defects:\n{output.critical_defects}")
        elif stage == "exploration":
            print(f"\n🔍 Exploration Analysis:\n{output.analysis}")
            print(f"\n✅ Validated UUs:\n{output.validated_uus}")
        elif stage == "integration":
            print(f"\n🎯 Integration Synthesis:\n{output.synthesis}")
        
        print("\n" + "-"*80)
        print("Please choose next action:")
        print("  1. Proceed - Continue to next stage")
        print("  2. Retry - Re-execute current stage")
        print("  3. Feedback - Provide feedback and continue")
        print("  4. Stop - Terminate execution")
        
        choice = input("\nChoice [1/2/3/4]: ").strip()
        
        feedback_text = ""
        action = "proceed"
        
        if choice == "2":
            action = "retry"
            feedback_text = input("💬 Enter retry reason or improvement suggestions: ").strip()
        elif choice == "3":
            action = "feedback"
            feedback_text = input("💬 Enter your feedback: ").strip()
        elif choice == "4":
            action = "stop"
            print("🛑 Execution terminated by user")
            return {"continue": False, "feedback": "", "action": "stop"}
        
        return {
            "continue": True,
            "feedback": feedback_text,
            "action": action
        }

    def run(
        self,
        *,
        enabler_story: str,
        potential_fix: str,
        human_preferences: str | None = None,
    ) -> dict[str, Any]:
        ctx = ConversationContext(
            enabler_story=enabler_story,
            potential_fix=potential_fix,
            human_preferences=human_preferences,
        )
        
        # Discovery stage
        while True:
            ctx.discovery = self.discovery.run(ctx)
            
            if self.interactive:
                feedback = self._get_human_feedback("discovery", ctx.discovery, ctx)
                if not feedback["continue"]:
                    return self._build_result(ctx, terminated=True)
                
                if feedback["action"] == "retry":
                    # Add human feedback to preferences
                    if feedback["feedback"]:
                        ctx.human_preferences = (ctx.human_preferences or "") + f"\n[Discovery Feedback]: {feedback['feedback']}"
                    continue
                elif feedback["action"] == "feedback":
                    if feedback["feedback"]:
                        ctx.human_preferences = (ctx.human_preferences or "") + f"\n[Discovery Feedback]: {feedback['feedback']}"
            
            break

        # Exploration & Integration loop
        while True:
            # Exploration stage
            while True:
                ctx.exploration = self.exploration.run(ctx)
                
                if ctx.exploration.requires_discovery_reset:
                    ctx.discovery = self.discovery.run(ctx, restart=True)
                    continue
                
                if self.interactive:
                    feedback = self._get_human_feedback("exploration", ctx.exploration, ctx)
                    if not feedback["continue"]:
                        return self._build_result(ctx, terminated=True)
                    
                    if feedback["action"] == "retry":
                        if feedback["feedback"]:
                            ctx.human_preferences = (ctx.human_preferences or "") + f"\n[Exploration Feedback]: {feedback['feedback']}"
                        continue
                    elif feedback["action"] == "feedback":
                        if feedback["feedback"]:
                            ctx.human_preferences = (ctx.human_preferences or "") + f"\n[Exploration Feedback]: {feedback['feedback']}"
                
                break

            # Integration stage
            while True:
                ctx.integration = self.integration.run(ctx)
                
                if self.interactive:
                    feedback = self._get_human_feedback("integration", ctx.integration, ctx)
                    if not feedback["continue"]:
                        return self._build_result(ctx, terminated=True)
                    
                    if feedback["action"] == "retry":
                        if feedback["feedback"]:
                            ctx.human_preferences = (ctx.human_preferences or "") + f"\n[Integration Feedback]: {feedback['feedback']}"
                        continue
                    elif feedback["action"] == "feedback":
                        if feedback["feedback"]:
                            ctx.human_preferences = (ctx.human_preferences or "") + f"\n[Integration Feedback]: {feedback['feedback']}"
                
                break
            
            # Check Integration callback
            if ctx.integration.callback == "exploration":
                continue
            if ctx.integration.callback == "discovery":
                ctx.discovery = self.discovery.run(ctx, restart=True)
                continue
            break

        return self._build_result(ctx, terminated=False)
    
    def _build_result(self, ctx: ConversationContext, terminated: bool = False) -> dict[str, Any]:
        """Build final result"""
        return {
            "core_problem": ctx.discovery.core_problem if ctx.discovery else "",
            "baseline_solution": ctx.discovery.baseline_solution if ctx.discovery else "",
            "critical_defects": ctx.discovery.critical_defects if ctx.discovery else "",
            "exploration_analysis": ctx.exploration.analysis if ctx.exploration else "",
            "integration_synthesis": ctx.integration.synthesis if ctx.integration else "",
            "search_log": ctx.search_log,
            "terminated_by_user": terminated,
            "final_human_preferences": ctx.human_preferences,
        }

    def run_to_json(self, **kwargs) -> str:
        result = self.run(**kwargs)
        return json.dumps(result, indent=2, ensure_ascii=False)
