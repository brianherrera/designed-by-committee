import time
from strands import Agent
from strands.models.bedrock import BedrockModel
from dbc.committee import CommitteeMember

from botocore.exceptions import ClientError


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
    
    def _invoke_with_retry(self, prompt: str, **kwargs):
        """
        Invoke agent with automatic retry for AWS Bedrock subscription activation.
        
        AWS Bedrock on-demand models require an automatic subscription that takes
        ~2 minutes to activate on first invocation. AWS deprecated the console page
        where this could be done manually, so the subscription is now created
        automatically on first API call. This method handles the initial
        AccessDeniedException with exponential backoff retry logic.
        
        Args:
            prompt: The prompt to send to the agent
            **kwargs: Additional arguments to pass to the agent
            
        Returns:
            Agent response
            
        Raises:
            Exception: If all retries are exhausted or a non-retryable error occurs
        """
        retry_delays = [5, 30, 60]
        max_attempts = len(retry_delays) + 1

        last_error = None
        
        for attempt in range(max_attempts):
            try:
                return self.agent(prompt, **kwargs)
            except ClientError as e:
                last_error = e

                # Check if this is the last attempt
                if attempt == max_attempts - 1:
                    break

                error_code = e.response['Error']['Code']
                delay = retry_delays[attempt]

                if (error_code == 'AccessDeniedException' and 'aws-marketplace' in str(e)):
                    print(f"Model subscription activating for {self.member.display_name} (first-time setup)...")
                elif (error_code == 'ThrottlingException'):
                    print(f"Encountered throttling exception for {self.member.display_name}")
                else:
                    print(f"Error encountered when trying to invoke models: {error_code}")
                    raise

                print(f"Retrying in {delay} seconds... (attempt {attempt + 1}/{max_attempts})")
                time.sleep(delay)

        print(f"Retries exhausted for {self.member.display_name}.")
        raise last_error
    
    def __call__(self, prompt: str, **kwargs):
        """Make the agent directly callable, returning text content."""
        response = self._invoke_with_retry(prompt, **kwargs)
        # Extract text content from response
        if hasattr(response, 'message') and isinstance(response.message, dict):
            if 'content' in response.message and len(response.message['content']) > 0:
                return response.message['content'][0]['text']
        return response
