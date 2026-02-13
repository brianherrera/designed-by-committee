"""
Clarification tool factory for committee agents.

This module provides a factory function to create per-agent clarification tools
that allow agents to request user input during the proposal generation phase.
"""

from strands import tool


def create_clarification_tool(agent_key: str, agent_name: str, state: dict, max_questions: int = 1):
    """Factory function to create a per-agent clarification tool.
    
    Args:
        agent_key: Unique key for the agent
        agent_name: Display name of the agent
        state: Shared state dictionary
        max_questions: Maximum questions allowed per agent
        
    Returns:
        A tool function decorated with @tool
    """
    @tool
    def request_user_clarification(question: str) -> str:
        """Request clarification from the user when information is missing, unclear, or ambiguous.
        
        IMPORTANT: If you're unsure about ANY aspect of the request, ASK rather than assume.
        You have limited questions available - use them to eliminate ambiguity and ensure you
        understand the user's actual needs before making assumptions.
        
        When to ask:
        - Requirements are vague or could be interpreted multiple ways
        - Technical details are missing (scale, performance needs, constraints)
        - User intent is unclear (what problem are they really trying to solve?)
        - Multiple valid approaches exist and you need direction
        - Success criteria are not defined
        
        Args:
            question: The clarification question to ask the user
            
        Returns:
            The user's response to your question
        """
        # Initialize tracking
        if 'agent_questions_asked' not in state:
            state['agent_questions_asked'] = {}
        
        # Check limit
        questions_asked = state['agent_questions_asked'].get(agent_key, 0)
        if questions_asked >= max_questions:
            return "[System: You have already used your clarification question. Please proceed with available information.]"
        
        # Increment counter
        state['agent_questions_asked'][agent_key] = questions_asked + 1
        
        # Display question
        print(f"\n{'=' * 80}")
        print(f"[**CLARIFICATION REQUESTED BY {agent_name.upper()}**]")
        print(f"{'=' * 80}")
        print(f"\n{question}\n")
        print(f"Your response (10min timeout):")
        user_response = input("> ")
        print()
        
        # Store in history
        if 'clarification_history' not in state:
            state['clarification_history'] = []
        
        state['clarification_history'].append({
            'agent_key': agent_key,
            'agent_name': agent_name,
            'question': question,
            'response': user_response
        })
        
        return user_response
    
    return request_user_clarification
