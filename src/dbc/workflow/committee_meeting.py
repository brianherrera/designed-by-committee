from typing import Dict
import sys
import time
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
    DISCUSSION_SUMMARY_PROMPT,
    USER_INTERRUPT_PROMPT
)


class CommitteeMeeting:
    """Orchestrates multi-agent committee interactions."""
    
    def __init__(self, agents: Dict[str, CommitteeAgent]):
        """Initialize with pre-created agents."""
        self.agents = agents
        self.response_history = []
        self.user_input = ""
    
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
    
    def _print_round_separator(self, round_number: int, description: str):
        """Print a visual separator for round transitions."""
        print("\n" + "=" * 80)
        print(f"Round {round_number}: {description}")
        print("=" * 80 + "\n")

    def _print_slowly(self, text: str, delay: float = 0.005):
        """
        Print text character by character to simulate a real-time transcript.
        
        Args:
            text: The text to print
            delay: Delay in seconds between each character (default: 0.02)
        """
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write('\n')
        sys.stdout.flush()

    def _collect_responses(self, agent_keys: list[str], prompt: str, print_responses: bool = True) -> list[tuple[str, any]]:
        """
        Collect responses from specified agents and print formatted output.
        
        Args:
            agent_keys: List of agent keys to query
            prompt: The prompt to send to each agent
            print_responses: Whether to print the responses (default: True)
        
        Returns:
            List of tuples containing (agent_key, response)
        """
        responses = [(key, self.agents[key](prompt)) for key in agent_keys]
        
        # Print formatted responses with slow typing effect
        if print_responses:
            for key, response in responses:
                agent_name = self.agents[key].agent.name.upper()
                print()
                timestamp = time.strftime('%H:%M:%S')
                self._print_slowly(f"[{timestamp}] {agent_name}: {response}")
                print()  # Extra newline for spacing
        
        return responses
    
    def _round_one(self) -> str:
        """
        Round 1: Generate initial proposals.
        
        Committee members create initial proposals
        responding to the user request. Sam Powerpoint then combines them.
        
        Returns:
            Sam Powerpoint's combined proposal message.
        """
        self._print_round_separator(1, "Generating proposal...")
        proposal_prompt = self.combine_prompts(
            ROUND_ONE_PROPOSAL_PROMPT,
            f"User prompt:\n{self.user_prompt}",
        )

        agent_keys = ['nina_edgecase', 'casey_friday', 'fontaine_kerning']
        responses = self._collect_responses(agent_keys, proposal_prompt, False)

        combined_proposals = "\n\n".join([
            f"{self.agents[key].agent.name}: {response}"
            for key, response in responses
        ])

        self._collect_responses(['morgan_calendar'], "Provide a brief intro statement (one sentence) before the proposal is shared with the team.")
        
        # Create a unified proposal
        unified_proposal_prompt = self.combine_prompts(
            ROUND_ONE_COMBINED_PROMPT,
            combined_proposals,
        )
        unified_proposal_response = self._collect_responses(['sam_powerpoint'], unified_proposal_prompt)

        input("Please review the initial proposal above.\nPress Enter to bring the committee into the discussion.")

        return unified_proposal_response[0][1]
    
    def _round_two(self) -> str:
        """
        Round 2: Initial feedback and user input.

        Present the proposal to the committee for feedback.
        The user is prompted for input to guide the discussion.

        Returns:
            The user's input
        """
        self._print_round_separator(2, "Gathering initial feedback...")

        self._collect_responses(['morgan_calendar'], "Provide a brief statement (one sentence) that the committee will start discussion of the proposal.")

        feedback_prompt = self.combine_prompts(
            ROUND_TWO_PROMPT,
            f"Current Tension Level: Low",
            f"Proposal under discussion:\n{self.proposal}",
        )

        agent_keys = ['nina_edgecase',  'casey_friday', 'pat_attacksurface', 
                    'fontaine_kerning', 'noah_actually']
        
        responses = self._collect_responses(agent_keys, feedback_prompt)

        # Combine responses
        combined_responses = "\n\n".join([
            f"{self.agents[key].agent.name}: {response}"
            for key, response in responses
        ])

        self.response_history.append(combined_responses)

        # Summarize discussion
        sam_prompt = self.combine_prompts(
            DISCUSSION_SUMMARY_PROMPT,
            f"Current Tension Level: Low",
            f"Proposal under discussion:\n{self.proposal}",
            f"Responses from committee members:\n{combined_responses}"
        )
        self._collect_responses(['sam_powerpoint'], sam_prompt)

        input("Please review the committee discussion above.\nPress Enter to continue deliberation.")

        # Prompt the user for input
        print("[**USER INPUT REQUIRED**]\n\n")

        user_input_prompt = self.combine_prompts(
            USER_INTERRUPT_PROMPT,
            f"Responses from committee members:\n{combined_responses}"
        )
        self._collect_responses(['morgan_calendar'], user_input_prompt)

        return input("Enter response:\n> ")
    
    def _round_three(self):
        """
        Round 3: Interpret user input and continue discussion.

        Committee members interpret and discuss the user's input.

        Args:
            user_input: The user's input from round two.
        """
        self._print_round_separator(3, "Responding to user input...")

        self._collect_responses(['morgan_calendar'], "Provide a brief statement (one sentence) that the committee will consider the user's input as part of their discussion.")

        stakeholder_response_prompt = self.combine_prompts(
            ROUND_THREE_PROMPT,
            f"Stakeholder clarification:\n{self.user_input}",
            f"Current Tension Level: Mid",
            f"Proposal under discussion:\n{self.proposal}",
        )

        agent_keys = ['nina_edgecase',  'casey_friday', 'pat_attacksurface', 
                    'fontaine_kerning', 'noah_actually']
        responses = self._collect_responses(agent_keys, stakeholder_response_prompt)

        # Combine responses
        combined_responses = "\n\n".join([
            f"{self.agents[key].agent.name}: {response}"
            for key, response in responses
        ])
        self.response_history.append(combined_responses)

        # Summarize discussion
        sam_prompt = self.combine_prompts(
            DISCUSSION_SUMMARY_PROMPT,
            f"Current Tension Level: Mid",
            f"Proposal under discussion:\n{self.proposal}",
            f"Responses from committee members:\n{combined_responses}"
        )
        self._collect_responses(['sam_powerpoint'], sam_prompt)

        input("Please review the committee discussion above.\nPress Enter to continue deliberation.")

    def _round_four(self):
        """
        Round 4: Cross-Committee Escalation

        Committee members escalate their concerns by reacting to prior
        feedback from other committee members.
        """
        self._print_round_separator(4, "Cross-committee discussion...")

        self._collect_responses(['morgan_calendar'], "Provide a brief statement (one sentence) that the committee will continue discussions providing feedback on each other's comments.")

        # Combine all previous responses
        all_previous_responses = "\n\n---\n\n".join([
            f"Previous discussion round feedback:\n{feedback}"
            for feedback in self.response_history
        ])
        
        reaction_prompt = self.combine_prompts(
            ROUND_FOUR_PROMPT,
            f"Current Tension Level: Mid",
            f"Proposal under discussion:\n{self.proposal}",
            f"Stakeholder clarification:\n{self.user_input}",
            f"All previous feedback from committee:\n{all_previous_responses}",
        )

        agent_keys = ['nina_edgecase',  'casey_friday', 'pat_attacksurface', 
                    'fontaine_kerning', 'noah_actually']
        responses = self._collect_responses(agent_keys, reaction_prompt)

        # Combine responses
        combined_responses = "\n\n".join([
            f"{self.agents[key].agent.name}: {response}"
            for key, response in responses
        ])
        self.response_history.append(combined_responses)

        # Summarize discussion
        sam_prompt = self.combine_prompts(
            DISCUSSION_SUMMARY_PROMPT,
            f"Current Tension Level: Mid",
            f"Proposal under discussion:\n{self.proposal}",
            f"Responses from committee members:\n{combined_responses}"
        )
        self._collect_responses(['sam_powerpoint'], sam_prompt)

        input("Please review the committee discussion above.\nPress Enter to continue deliberation.")

    def _round_five(self):
        """
        Round 5: Final statements
        
        Committee members reassert their positions before time runs out.
        """
        self._print_round_separator(5, "Committee members clarifying final positions...")

        self._collect_responses(['morgan_calendar'], "Provide a brief call-out (one sentence) this is the final round of discussion before the committee delivers their go-forward plan.")

        # Combine all previous responses
        all_previous_responses = "\n\n---\n\n".join([
            f"Previous discussion round feedback:\n{feedback}"
            for feedback in self.response_history
        ])
        
        final_position_prompt = self.combine_prompts(
            ROUND_FIVE_PROMPT,
            f"Current Tension Level: High",
            f"Proposal under discussion:\n{self.proposal}",
            f"Stakeholder clarification:\n{self.user_input}",
            f"All previous feedback from committee:\n{all_previous_responses}",
        )

        agent_keys = ['nina_edgecase', 'casey_friday', 'pat_attacksurface',
                      'fontaine_kerning', 'noah_actually']
        responses = self._collect_responses(agent_keys, final_position_prompt)

        # Combine responses
        combined_responses = "\n\n".join([
            f"{self.agents[key].agent.name}: {response}"
            for key, response in responses
        ])
        self.response_history.append(combined_responses)

        # Summarize discussion
        sam_prompt = self.combine_prompts(
            DISCUSSION_SUMMARY_PROMPT,
            f"Current Tension Level: High",
            f"Proposal under discussion:\n{self.proposal}",
            f"Responses from committee members:\n{combined_responses}"
        )
        self._collect_responses(['sam_powerpoint'], sam_prompt)

        input("Please review the committee’s final positions above.\nPress Enter to review the committee decision and go-forward plan.")
        
    def _round_six(self):
        """
        Round 6: Decision summary
        
        A go-forward plan is synthesized from the discussion and is documented.
        """
        self._print_round_separator(6, "Preparing committee decision and recommended path forward...")

        # Combine all previous responses
        all_previous_responses = "\n\n---\n\n".join([
            f"Previous discussion round feedback:\n{feedback}"
            for feedback in self.response_history
        ])
        
        decision_prompt = self.combine_prompts(
            ROUND_SIX_DECISION_PROMPT,
            f"Current Tension Level: High",
            f"Stakeholder clarification:\n{self.user_input}",
            f"All previous feedback from committee:\n{all_previous_responses}",
        )
        self._collect_responses(['sam_powerpoint'], decision_prompt)
    
        self._collect_responses(['morgan_calendar'], "Provide a brief statement to formally close the meeting.")
    
    def run(self, user_prompt: str):
        """Run the full meeting workflow."""
        self.user_prompt = user_prompt

        # Round 1: Generate initial proposals
        self.proposal = self._round_one()

        # Round 2: Initial feedback and user input
        self.user_input = self._round_two()

        # Round 3: Interpret user input
        self._round_three()

        # Round 4: Cross-committee escalation
        self._round_four()

        # Round 5: Final statements
        self._round_five()

        # Round 6: Decision summary
        self._round_six()

        print("[**Meeting has ended.**]")



