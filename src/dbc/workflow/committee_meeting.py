from typing import Dict
from dbc.committee import CommitteeMember
from dbc.agents import CommitteeAgent
from dbc.prompts.rounds import (
    ROUND_ONE_PROPOSAL_PROMPT,
    ROUND_ONE_COMBINED_PROMPT,
    ROUND_TWO_PROMPT,
    ROUND_THREE_PROMPT,
    ROUND_FOUR_PROMPT,
    ROUND_FIVE_PROMPT,
    ROUND_SIX_DECISION_PROMPT,
    ROUND_SIX_REACTIONS_PROMPT,
    ROUND_SIX_RECORDING_PROMPT,
    USER_INTERRUPT_PROMPT
)


class CommitteeMeeting:
    """Orchestrates multi-agent committee interactions."""
    
    def __init__(self, agents: Dict[str, CommitteeAgent]):
        """Initialize with pre-created agents."""
        self.agents = agents
        self.response_history = []
    
    @classmethod
    def from_members(cls, members: Dict[str, CommitteeMember] = None):
        """Create meeting from committee member definitions."""
        agents = {
            key: CommitteeAgent.from_member(member)
            for key, member in members.items()
        }
        return cls(agents)
    
    def combine_prompts(self, *prompts: str) -> str:
        """
        Combine multiple prompts into a single string.
        
        Args:
            *prompts: Variable number of prompt strings to combine.
                     Can include round prompts, tension prompts, proposal prompts, etc.
        
        Returns:
            A single string with all prompts joined by double newlines.
        """
        return "\n\n".join(prompt for prompt in prompts if prompt)
    
    def _round_one(self) -> str:
        """
        Round 1: Generate initial proposals.
        
        Committee members create initial proposals
        responding to the user request. Sam Powerpoint then combines them.
        
        Returns:
            Sam Powerpoint's combined proposal message.
        """
        prompt = self.combine_prompts(
            ROUND_ONE_PROPOSAL_PROMPT,
            f"User prompt:\n{self.user_prompt}",
        )
        
        proposal_responses = {
            'Nina': self.agents['nina_edgecase'](prompt),
            'Casey': self.agents['casey_friday'](prompt),
            'Fontaine': self.agents['fontaine_kerning'](prompt)
        }
        
        # Combine proposals into a single string
        combined_proposals = "\n\n".join([
            f"{agent_name}: {response.message}"
            for agent_name, response in proposal_responses.items()
        ])
        
        # Sam Powerpoint creates a unified proposal
        sam_powerpoint_response = self.agents['sam_powerpoint'](
            self.combine_prompts(
                ROUND_ONE_COMBINED_PROMPT,
                combined_proposals,
            )
        )
        
        return sam_powerpoint_response.message
    
    def _round_two(self) -> str:
        """
        Round 2: Initial feedback and user input.

        Present the proposal to the committee for feedback.
        The user is prompted for input to guide the discussion.

        Returns:
            The user's input
        """
        prompt = self.combine_prompts(
            ROUND_TWO_PROMPT,
            f"Current Tension Level: Low",
            f"Proposal under discussion:\n{self.proposal}",
        )

        # Get feedback from committee members
        responses = {
            'Nina': self.agents['nina_edgecase'](prompt),
            'Pat': self.agents['pat_attacksurface'](prompt),
            'Casey': self.agents['casey_friday'](prompt),
            'Noah': self.agents['noah_actually'](prompt),
            'Fontaine': self.agents['fontaine_kerning'](prompt),
        }

        # Combine responses
        combined_responses = "\n\n".join([
            f"{agent_name}: {response.message}"
            for agent_name, response in responses.items()
        ])
        self.response_history.append(combined_responses)

        # Summarize discussion
        sam_prompt = self.combine_prompts(
            ROUND_TWO_PROMPT,
            f"Current Tension Level: Low",
            f"Proposal under discussion:\n{self.proposal}",
            f"Responses from committee members:\n{combined_responses}"
        )
        self.agents['sam_powerpoint'](sam_prompt)

        # Prompt the user for input
        self.agents['morgan_calendar'](
            self.combine_prompts(
                USER_INTERRUPT_PROMPT,
                f"Responses from committee members:\n{combined_responses}"
            )
        )

        return input("Enter response: ")
    
    def _round_three(self, user_input: str):
        """
        Round 3: Interpret user input and continue discussion.

        Committee members interpret and discuss the user's input.

        Args:
            user_input: The user's input from round two.
        """
        prompt = self.combine_prompts(
            ROUND_THREE_PROMPT,
            f"Stakeholder clarification:\n{user_input}",
            f"Current Tension Level: Mid",
            f"Proposal under discussion:\n{self.proposal}",
        )

        # Get feedback from committee members
        responses = {
            'Nina': self.agents['nina_edgecase'](prompt),
            'Pat': self.agents['pat_attacksurface'](prompt),
            'Casey': self.agents['casey_friday'](prompt),
            'Noah': self.agents['noah_actually'](prompt),
            'Fontaine': self.agents['fontaine_kerning'](prompt),
        }

        # Combine responses
        combined_responses = "\n\n".join([
            f"{agent_name}: {response.message}"
            for agent_name, response in responses.items()
        ])
        self.response_history.append(combined_responses)

        # Summarize discussion
        sam_prompt = self.combine_prompts(
            ROUND_THREE_PROMPT,
            f"Current Tension Level: Mid",
            f"Proposal under discussion:\n{self.proposal}",
            f"Responses from committee members:\n{combined_responses}"
        )
        self.agents['sam_powerpoint'](sam_prompt)

    def _round_four(self):
        """
        Round 4: Cross-Committee Escalation

        Committee members escalate their concerns by reacting to prior
        feedback from other committee members.
        """
        # Combine all previous responses
        all_previous_responses = "\n\n---\n\n".join([
            f"Previous committee feedback:\n{feedback}"
            for feedback in self.response_history
        ])
        
        prompt = self.combine_prompts(
            ROUND_FOUR_PROMPT,
            f"Current Tension Level: Mid",
            f"Proposal under discussion:\n{self.proposal}",
            f"All previous feedback from committee:\n{all_previous_responses}",
        )

        # Get feedback from committee members
        responses = {
            'Nina': self.agents['nina_edgecase'](prompt),
            'Pat': self.agents['pat_attacksurface'](prompt),
            'Casey': self.agents['casey_friday'](prompt),
            'Noah': self.agents['noah_actually'](prompt),
            'Fontaine': self.agents['fontaine_kerning'](prompt),
        }

        # Combine responses
        combined_responses = "\n\n".join([
            f"{agent_name}: {response.message}"
            for agent_name, response in responses.items()
        ])
        self.response_history.append(combined_responses)

        # Summarize discussion
        sam_prompt = self.combine_prompts(
            ROUND_FOUR_PROMPT,
            f"Current Tension Level: Mid",
            f"Proposal under discussion:\n{self.proposal}",
            f"Responses from committee members:\n{combined_responses}"
        )
        self.agents['sam_powerpoint'](sam_prompt)

    def _round_five(self):
        """
        Round 5: Final statements
        
        Committee members reassert their positions before time runs out. 
        """
        # Combine all previous responses
        all_previous_responses = "\n\n---\n\n".join([
            f"Previous committee feedback:\n{feedback}"
            for feedback in self.response_history
        ])
        
        prompt = self.combine_prompts(
            ROUND_FIVE_PROMPT,
            f"Current Tension Level: High",
            f"Proposal under discussion:\n{self.proposal}",
            f"All previous feedback from committee:\n{all_previous_responses}",
        )

        responses = {
            'Nina': self.agents['nina_edgecase'](prompt),
            'Casey': self.agents['casey_friday'](prompt),
            'Pat': self.agents['pat_attacksurface'](prompt),
            'Noah': self.agents['noah_actually'](prompt),
            'Fontaine': self.agents['fontaine_kerning'](prompt),
        }

        # Combine responses
        combined_responses = "\n\n".join([
            f"{agent_name}: {response.message}"
            for agent_name, response in responses.items()
        ])
        self.response_history.append(combined_responses)

        # Summarize discussion
        sam_prompt = self.combine_prompts(
            ROUND_FIVE_PROMPT,
            f"Current Tension Level: High",
            f"Proposal under discussion:\n{self.proposal}",
            f"Responses from committee members:\n{combined_responses}"
        )
        self.agents['sam_powerpoint'](sam_prompt)
        
    def _round_six(self):
        """
        Round 6: Decision summary
        
        A go-forward plan is synthesized from the discussion and is documented.
        """
        # Combine all previous responses
        all_previous_responses = "\n\n---\n\n".join([
            f"Previous committee feedback:\n{feedback}"
            for feedback in self.response_history
        ])
        
        decision_prompt = self.combine_prompts(
            ROUND_SIX_DECISION_PROMPT,
            f"Current Tension Level: High",
            f"All previous feedback from committee:\n{all_previous_responses}",
        )
        decision_response = self.agents['sam_powerpoint'](decision_prompt)

        record_prompt = self.combine_prompts(
            ROUND_SIX_RECORDING_PROMPT,
            f"Current Tension Level: High",
            f"Decision summary: {decision_response.message}",
        )
        self.agents['morgan_calendar'](record_prompt)

        reaction_prompt = self.combine_prompts(
            ROUND_SIX_REACTIONS_PROMPT,
            f"Current Tension Level: High",
            f"Decision summary: {decision_response.message}",
        )

        self.agents['nina_edgecase'](reaction_prompt),
        self.agents['casey_friday'](reaction_prompt),
        self.agents['pat_attacksurface'](reaction_prompt),
        self.agents['noah_actually'](reaction_prompt),
        self.agents['fontaine_kerning'](reaction_prompt),
    
        self.agents['morgan_calendar']("Provide a brief statement to formally close the meeting.")
    
    def run(self, user_prompt: str):
        """Run the full meeting workflow."""
        self.user_prompt = user_prompt

        # Round 1: Generate initial proposals
        self.proposal = self._round_one()

        # Round 2: Initial feedback and user input
        user_input = self._round_two()

        # Round 3: Interpret user input
        self._round_three(user_input)

        # Round 4: Cross-committee escalation
        self._round_four()

        # Round 5: Final statements
        self._round_five()

        # Round 6: Decision summary
        self._round_six()



