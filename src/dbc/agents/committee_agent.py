from strands import Agent
from strands.models.bedrock import BedrockModel
from dbc.committee import CommitteeMember


class CommitteeAgent:
    def __init__(self, agent: Agent, member: CommitteeMember):
        self.agent = agent
        self.member = member
    
    @classmethod
    def from_member(cls, member: CommitteeMember) -> 'CommitteeAgent':
        """Create a CommitteeAgent from a CommitteeMember definition."""
        # Import system prompt dynamically
        system_prompt_module = __import__(member.system_prompt_module, fromlist=['SYSTEM_PROMPT'])
        system_prompt = system_prompt_module.SYSTEM_PROMPT
        
        # Create Bedrock model
        model = BedrockModel(model_id=member.model_id)
        
        # Create Strands Agent
        agent = Agent(
            system_prompt=system_prompt,
            model=model,
            name=member.display_name
        )

        return cls(agent=agent, member=member)
    
    def __call__(self, prompt: str, **kwargs):
        """Make the agent directly callable."""
        return self.agent(prompt, **kwargs)
