from strands import Agent
from strands.models.bedrock import BedrockModel
from dbc.committee import CommitteeMember


class CommitteeAgent:
    def __init__(
        self,
        agent: Agent,
        member: CommitteeMember,
        round_prompts: dict = None,
        description: str = None,
        enable_streaming: bool = False
    ):
        self.agent = agent
        self.member = member
        self.round_prompts = round_prompts or {}
        self.description = description
        self.enable_streaming = enable_streaming
    
    @classmethod
    def from_member(
        cls,
        member: CommitteeMember,
        description: str = None,
        enable_streaming: bool = False
    ) -> 'CommitteeAgent':
        """
        Create a CommitteeAgent from a CommitteeMember definition.
        
        Args:
            member: CommitteeMember configuration
            description: Optional description for swarm coordination
            enable_streaming: If True, enables output streaming (for swarm).
                            If False, suppresses output (for manual formatting).
        """
        # Import system prompt and optional round prompts dynamically
        prompt_module = __import__(member.prompt_module, fromlist=['SYSTEM_PROMPT', 'ROUND_PROMPTS'])
        system_prompt = prompt_module.SYSTEM_PROMPT
        
        # Load round-specific prompts if they exist
        round_prompts = getattr(prompt_module, 'ROUND_PROMPTS', {})
        
        # Create Bedrock model
        model = BedrockModel(model_id=member.model_id)
        
        # Create Strands Agent with conditional callback handler
        agent_kwargs = {
            'model': model,
            'name': member.display_name,
            'system_prompt': system_prompt,
        }
        
        # Suppress default output. We will handle output formatting
        agent_kwargs['callback_handler'] = None
        
        # Add description if provided (for swarm)
        if description:
            agent_kwargs['description'] = description
        
        agent = Agent(**agent_kwargs)

        return cls(
            agent=agent,
            member=member,
            round_prompts=round_prompts,
            description=description,
            enable_streaming=enable_streaming
        )
    
    def __call__(self, prompt: str, **kwargs):
        """Make the agent directly callable, returning text content."""
        response = self.agent(prompt, **kwargs)
        # Extract text content from response
        if hasattr(response, 'message') and isinstance(response.message, dict):
            if 'content' in response.message and len(response.message['content']) > 0:
                return response.message['content'][0]['text']
        return response

