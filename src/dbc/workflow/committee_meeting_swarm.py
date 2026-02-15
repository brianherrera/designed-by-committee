"""
Swarm-based committee meeting orchestration.

This module implements an autonomous, agent-driven committee meeting workflow
using the Strands multi-agent swarm pattern. Unlike the static workflow in
the prototype (committee_meeting.py), this allows agents to self-organize and hand off to
each other dynamically.
"""

from typing import Dict
import asyncio
import sys
import time
from strands.multiagent import Swarm
from dbc.committee import CommitteeMember
from dbc.agents import CommitteeAgent
from dbc.workflow.clarification_tool import create_clarification_tool
from dbc.workflow.swarm_config import AGENT_DESCRIPTIONS, PHASE_CONFIG, SWARM_CONFIG


class CommitteeStreamHandler:
    """Custom handler for committee meeting swarm events."""
    
    def __init__(self, agents_dict: Dict[str, CommitteeAgent], show_thinking: bool = False):
        self.agents_dict = agents_dict
        # Create a reverse mapping from agent name to key
        self.name_to_key = {
            agent.agent.name: key
            for key, agent in agents_dict.items()
        }
        self.current_speaker = None
        self.buffer = []
        self.result = None
        self.show_thinking = show_thinking
        self.in_thinking_block = False
        self.partial_tag_buffer = ""  # Buffer for partial tags at chunk boundaries
        
    async def handle_event(self, event: dict):
        """Process swarm streaming events."""
        event_type = event.get('type')
        
        if event_type == 'multiagent_node_start':
            # New agent taking control
            node_id = event['node_id']
            self._print_speaker_header(node_id)
            self.current_speaker = node_id
            # Reset thinking block state and buffer for new speaker
            self.in_thinking_block = False
            self.partial_tag_buffer = ""
            
        elif event_type == 'multiagent_node_stream':
            # Agent generating response - stream arrives incrementally from LLM
            inner_event = event.get('event', {})
            if 'data' in inner_event:
                text = inner_event['data']
                if text:
                    # Filter thinking blocks unless show_thinking is enabled
                    if not self.show_thinking:
                        text = self._filter_thinking_blocks(text)
                    
                    if text:  # Only print if there's text after filtering
                        sys.stdout.write(text)
                        sys.stdout.flush()
                
        elif event_type == 'multiagent_handoff':
            # Agent handing off to another
            from_nodes = event.get('from_node_ids', [])
            to_nodes = event.get('to_node_ids', [])
            self._print_handoff(from_nodes, to_nodes)
            
        elif event_type == 'multiagent_result':
            # Swarm completed
            self.result = event.get('result')
            # Only print meeting end message if this is the final phase
    
    def _print_speaker_header(self, node_id: str):
        """Print formatted header for new speaker."""
        # node_id is the agent's name, convert to key
        agent_key = self.name_to_key.get(node_id, node_id)
        
        if agent_key in self.agents_dict:
            agent = self.agents_dict[agent_key]
            timestamp = time.strftime('%H:%M:%S')
            print(f"\n[{timestamp}] {agent.agent.name.upper()} ({agent.member.title}):")
        else:
            print(f"\n[Unknown Agent: {node_id}]")
        
        
    def _print_handoff(self, from_nodes: list, to_nodes: list):
        """Print handoff notification."""
        if from_nodes and to_nodes:
            print(f"\n\n[Handoff: {', '.join(from_nodes)} → {', '.join(to_nodes)}]\n")
    
    def _filter_thinking_blocks(self, text: str) -> str:
        """
        Filter out <thinking> blocks from streamed text with robust boundary handling.
        
        Handles partial tags split across chunk boundaries by buffering potential
        partial tags and prepending them to the next chunk.
        """
        # Prepend any buffered partial tag from previous chunk
        text = self.partial_tag_buffer + text
        self.partial_tag_buffer = ""
        
        result = []
        i = 0
        
        while i < len(text):
            # Check if we're entering a thinking block
            if not self.in_thinking_block:
                # Look for <thinking> tag (case-insensitive, need at least 10 chars)
                if i <= len(text) - 10:
                    if text[i:i+10].lower() == '<thinking>':
                        self.in_thinking_block = True
                        i += 10
                        continue
                # Buffer potential partial opening tag at end of chunk
                elif i > len(text) - 10:
                    remaining = text[i:]
                    # Check if remaining text could be start of '<thinking>'
                    opening_tag = '<thinking>'
                    for tag_len in range(1, len(opening_tag)):
                        if remaining.lower() == opening_tag[:tag_len].lower():
                            self.partial_tag_buffer = remaining
                            return ''.join(result)
            
            # Check if we're exiting a thinking block
            if self.in_thinking_block:
                # Look for </thinking> tag (case-insensitive, need at least 11 chars)
                if i <= len(text) - 11:
                    if text[i:i+11].lower() == '</thinking>':
                        self.in_thinking_block = False
                        i += 11
                        # Skip any trailing whitespace/newlines after closing tag
                        while i < len(text) and text[i] in ('\n', ' ', '\r', '\t'):
                            i += 1
                        continue
                # Buffer potential partial closing tag at end of chunk
                elif i > len(text) - 11:
                    remaining = text[i:]
                    # Check if remaining text could be start of '</thinking>'
                    closing_tag = '</thinking>'
                    for tag_len in range(1, len(closing_tag)):
                        if remaining.lower() == closing_tag[:tag_len].lower():
                            self.partial_tag_buffer = remaining
                            return ''.join(result)
                
                # If we're in a thinking block, skip this character
                i += 1
                continue
            
            # If not in thinking block, keep the character
            result.append(text[i])
            i += 1
        
        return ''.join(result)


class CommitteeMeetingSwarm:
    """Swarm-based committee meeting orchestration."""
    
    def __init__(self, agents: Dict[str, CommitteeAgent]):
        self.agents = agents
        self.swarm = None
        self.state = {}
        
    @classmethod
    def from_members(cls, members: Dict[str, CommitteeMember]):
        """Create swarm meeting from committee member definitions."""
        # Create agents with descriptions and streaming enabled
        agents = {
            key: CommitteeAgent.from_member(
                member, 
                description=AGENT_DESCRIPTIONS[key],
                enable_streaming=True
            )
            for key, member in members.items()
        }
        return cls(agents)
    
    def _initialize_swarm(self):
        """Initialize the swarm with all agents (called once)."""
        # Extract Strands Agent objects
        agent_list = [agent.agent for agent in self.agents.values()]
        
        # Create swarm with default entry point (will be overridden per phase)
        self.swarm = Swarm(
            agent_list,
            entry_point=self.agents['sam_powerpoint'].agent,
            max_handoffs=SWARM_CONFIG['max_handoffs'],
            max_iterations=SWARM_CONFIG['max_iterations'],
            execution_timeout=SWARM_CONFIG['execution_timeout'],
            node_timeout=SWARM_CONFIG['node_timeout'],
            repetitive_handoff_detection_window=SWARM_CONFIG['repetitive_handoff_detection_window'],
            repetitive_handoff_min_unique_agents=SWARM_CONFIG['repetitive_handoff_min_unique_agents']
        )
    
    def _initialize_state(self, user_prompt: str):
        """Initialize meeting state."""
        self.state = {
            'phase': 1,
            'phase_name': 'Proposal Generation',
            'tension_level': 'Low',
            'user_prompt': user_prompt,
            'user_input': None,
            'proposal': None,
            'handoff_count': 0,
            'phase_history': [],
            'agent_questions_asked': {},      # {agent_key: count}
            'clarification_history': [],      # [{agent_key, agent_name, question, response}]
            'max_questions_per_agent': 1,     # Configurable limit
        }
    
    def _build_clarification_context(self) -> str:
        """Build context string from clarification history."""
        if not self.state.get('clarification_history'):
            return ""
        
        context = "\n\nClarifications received during proposal generation:\n"
        for clarification in self.state['clarification_history']:
            context += f"- {clarification['agent_name']} asked: {clarification['question']}\n"
            context += f"  User responded: {clarification['response']}\n"
        
        return context
    
    def _print_clarification_summary(self):
        """Print summary of clarifications received during Phase 1."""
        if not self.state.get('clarification_history'):
            return
        
        print("\n" + "=" * 80)
        print("CLARIFICATIONS RECEIVED")
        print("=" * 80)
        
        for i, clarification in enumerate(self.state['clarification_history'], 1):
            print(f"\n{i}. {clarification['agent_name']} asked:")
            print(f"   Q: {clarification['question']}")
            print(f"   A: {clarification['response']}")
        
        print("\n" + "=" * 80 + "\n")
    
    def _build_phase_prompt(self, phase_number: int) -> str:
        """Build the prompt for a specific phase."""
        phase_config = PHASE_CONFIG[phase_number]
        
        if phase_number == 1:
            # Phase 1: Proposal Generation
            return f"""COMMITTEE MEETING - Phase 1: {phase_config['name']}

REQUEST:
{self.state['user_prompt']}

PHASE CONTEXT:
- Objective: {phase_config['objective']}
- Tension Level: {phase_config['tension_level']}

--- ROLE-SPECIFIC INSTRUCTIONS ---

IF YOU ARE SAM POWERPOINT (FACILITATOR):
- Your role is to FACILITATE proposal generation, not create it yourself.

DO NOT create the proposal yourself. Your role is to coordinate specialists and synthesize their input.

IF YOU ARE A SPECIALIST (Nina Edgecase, Casey Friday, or Fontaine Kerning):
- Provide your domain expertise on the request above. Focus on your area of specialization.
- Hand off to specialists to gather their proposals
- Keep your input focused and concise. You're contributing to a proposal that will be reviewed by the full committee.

--- SHARED GUIDELINES ---

Remember: You're in a committee meeting. Other members will review and debate this proposal.

REQUIRED ACTIONS:
1. Briefly acknowledge the request (1-2 sentences)
2. Hand off to specialists to gather their proposals:
   - Nina Edgecase for technical architecture and implementation approach
   - Casey Friday for product/MVP scope and timeline
   - Fontaine Kerning for design/UX perspective
3. After gathering specialist input, synthesize their proposals into a unified initial proposal

CRITICAL - Clarification Questions:
You have access to the request_user_clarification tool. DO NOT make assumptions
when information is unclear or ambiguous - ASK THE USER instead.

Guidelines for using clarification questions:
- If ANY aspect of the request is unclear, vague, or could be interpreted multiple ways - ASK
- If you're unsure about scope, scale, constraints, or success criteria - ASK
- If you find yourself making assumptions about what the user wants - STOP and ASK
- If multiple valid approaches exist and you need direction - ASK
- Make your questions clear, specific, and focused on eliminating ambiguity

Each committee member has a limited number of questions, so prioritize the most
important clarifications. However, it's better to ask and be certain than to
assume and build the wrong thing.

Remember: Assumptions lead to rework. Questions lead to clarity."""
        
        elif phase_number == 2:
            # Phase 2: Initial Review
            clarification_context = self._build_clarification_context()
            return f"""COMMITTEE MEETING - Phase 2: {phase_config['name']}

PHASE CONTEXT:
- Objective: {phase_config['objective']}
- Tension Level: {phase_config['tension_level']}

PROPOSAL UNDER DISCUSSION:
{self.state.get('proposal', 'No proposal recorded yet')}
{clarification_context}

--- ROLE-SPECIFIC INSTRUCTIONS ---

IF YOU ARE THE FACILITATOR (Sam Powerpoint or Morgan Calendar):
Guide the committee through initial feedback. Hand off to committee members to gather their perspectives.

DO NOT provide feedback yourself. Your role is to coordinate discussion and synthesize input from the committee.

IF YOU ARE A COMMITTEE MEMBER (Nina, Casey, Pat, Fontaine, or Max):
- Provide your initial feedback on the proposal above.
- Hand off to specialists to gather their proposals
- Keep your response brief - around one paragraph. Focus on key concerns and feedback.

--- SHARED GUIDELINES ---

CLARIFICATION QUESTIONS:
If you need additional information from the user to provide meaningful feedback, use the request_user_clarification tool. You have a limited number of questions available.

IMPORTANT: Keep responses brief - around one paragraph per committee member. Focus on key concerns and feedback."""
        
        elif phase_number == 3:
            # Phase 3: Cross-Committee Deliberation
            clarification_context = self._build_clarification_context()
            return f"""COMMITTEE MEETING - Phase 3: {phase_config['name']}

PHASE CONTEXT:
- Objective: {phase_config['objective']}
- Tension Level: {phase_config['tension_level']}

PROPOSAL UNDER DISCUSSION:
{self.state.get('proposal', 'No proposal recorded yet')}

STAKEHOLDER CLARIFICATION:
{self.state.get('user_input', 'No user input provided')}
{clarification_context}

--- ROLE-SPECIFIC INSTRUCTIONS ---

IF YOU ARE THE FACILITATOR (Morgan Calendar or Sam Powerpoint):
- You MUST hand off to committee members to start the discussion.
- DO NOT provide your own analysis or close the phase.

IF YOU ARE A COMMITTEE MEMBER (Nina, Casey, Pat, Fontaine, or Max):
Engage in cross-committee discussion. React to specific points from your colleagues:
- Build on or challenge ideas from other members
- Raise concerns about approaches suggested by others
- Propose alternatives or refinements
- Identify tensions between different perspectives (technical vs. timeline, security vs. UX, etc.)
- Keep your response brief - around one paragraph. React to specific points from colleagues, not just general commentary.

--- SHARED GUIDELINES ---

REQUIRED ACTIONS:
1. Hand off to at least 3 committee members (Nina, Casey, Pat, Fontaine, or Max)
2. Ensure each member has a chance to react to specific points from colleagues
3. Hand off to Sam to generate a summary of the discussion
4. Only after gathering multiple perspectives should you consider the phase complete

CLARIFICATION QUESTIONS:
If you need additional information from the user to support your arguments or address concerns, use the request_user_clarification tool. You have a limited number of questions available."""
        
        elif phase_number == 4:
            # Phase 4: Final Positions
            clarification_context = self._build_clarification_context()
            return f"""COMMITTEE MEETING - Phase 4: {phase_config['name']}

PHASE CONTEXT:
- Objective: {phase_config['objective']}
- Tension Level: {phase_config['tension_level']}

This is the final round of discussion before the committee delivers their go-forward plan.

PROPOSAL UNDER DISCUSSION:
{self.state.get('proposal', 'No proposal recorded yet')}

STAKEHOLDER CLARIFICATION:
{self.state.get('user_input', 'No user input provided')}
{clarification_context}

--- ROLE-SPECIFIC INSTRUCTIONS ---

IF YOU ARE THE FACILITATOR (Morgan Calendar):
DO NOT provide your own summary or analysis. Your ONLY role is to hand off to each committee member.

DO NOT skip any committee member. DO NOT provide your own commentary. Your role is ONLY to facilitate handoffs.

IF YOU ARE A COMMITTEE MEMBER (Nina, Casey, Pat, Fontaine, or Max):
State your final position on the proposal. This is your last chance to influence the decision:
- Clearly state whether you support, oppose, or conditionally support the proposal
- Highlight your most critical concerns or requirements
- Specify any non-negotiable constraints from your domain
- Be concise but definitive
- Keep your response brief - around one paragraph. State your final position clearly and concisely.

IF YOU ARE SAM POWERPOINT:
After all committee members have stated their positions, acknowledge that you've heard all perspectives and prepare to move to the final decision phase. DO NOT make the decision yet - that happens in Phase 5.

--- SHARED GUIDELINES ---

YOU MUST COMPLETE THESE HANDOFFS:
1. Hand off to Nina Edgecase for technical concerns and architectural position
2. Hand off to Casey Friday for product perspective and timeline stance
3. Hand off to Pat Attacksurface for security and compliance position
4. Hand off to Fontaine Kerning for design and user experience stance
5. Hand off to Max Token for AI/automation considerations
6. After ALL five positions are heard, hand off to Sam Powerpoint to prepare for the final decision phase

CLARIFICATION QUESTIONS:
If you need critical information from the user to finalize your position, use the request_user_clarification tool. You have a limited number of questions available."""
        
        elif phase_number == 5:
            # Phase 5: Decision
            clarification_context = self._build_clarification_context()
            return f"""COMMITTEE MEETING - Phase 5: {phase_config['name']}

PHASE CONTEXT:
- Objective: {phase_config['objective']}
- Tension Level: {phase_config['tension_level']}

The committee must now create a consensus-driven recommendation and go-forward plan.

ORIGINAL PROPOSAL:
{self.state.get('proposal', 'No proposal recorded yet')}

STAKEHOLDER CLARIFICATION:
{self.state.get('user_input', 'No user input provided')}
{clarification_context}

--- ROLE-SPECIFIC INSTRUCTIONS ---

IF YOU ARE SAM POWERPOINT:
Your role is to create the final synthesis and recommendation:
1. Generate the final unified proposal with all committee feedback integrated
2. Review the key tensions, agreements, and positions from the discussion
3. Synthesize these into a clear, actionable go-forward plan
4. If you need facilitation support, hand off to Morgan Calendar
5. Create a comprehensive recommendation that addresses the stakeholder's needs

Structure your recommendation clearly with:
- Executive summary of the decision
- Key changes from the original proposal
- How major concerns were addressed
- Clear next steps and deliverables

IF YOU ARE MORGAN CALENDAR:
Hand off to Sam Powerpoint to create the synthesis and final recommendation. Your facilitation role is complete.

--- SHARED GUIDELINES ---

CLARIFICATION QUESTIONS:
If you need final clarification from the user to complete the recommendation, use the request_user_clarification tool. You have a limited number of questions available.

IMPORTANT: This is the final deliverable - make it comprehensive, clear, and actionable."""
        
        return "Continue the committee discussion."
    
    def _print_phase_separator(self, phase_number: int):
        """Print a visual separator for phase transitions."""
        phase_config = PHASE_CONFIG[phase_number]
        print("\n" + "=" * 80)
        print(f"Phase {phase_number}: {phase_config['name']}")
        print("=" * 80 + "\n")
    
    def _add_clarification_tools_to_agents(self):
        """Add clarification tools to all agents except the facilitator (Morgan Calendar).
        
        Tools are registered once and persist across all phases, allowing agents to
        request clarifications throughout the entire meeting.
        """
        agents_with_clarification = ['sam_powerpoint', 'nina_edgecase', 'casey_friday', 'fontaine_kerning', 'pat_attacksurface', 'max_token']
        
        for agent_key in agents_with_clarification:
            if agent_key in self.agents:
                agent = self.agents[agent_key]
                
                # Create per-agent tool instance using factory function
                clarification_tool = create_clarification_tool(
                    agent_key=agent_key,
                    agent_name=agent.agent.name,
                    state=self.state,
                    max_questions=self.state['max_questions_per_agent']
                )
                
                # Register tool with the agent's tool registry
                agent.agent.tool_registry.register_tool(clarification_tool)
    
    async def _run_phase_swarm(self, phase_number: int, show_thinking: bool = False):
        """Run a single phase of the swarm."""
        phase_config = PHASE_CONFIG[phase_number]
        
        # Update state
        self.state['phase'] = phase_number
        self.state['phase_name'] = phase_config['name']
        self.state['tension_level'] = phase_config['tension_level']
        
        # Print phase separator
        self._print_phase_separator(phase_number)
        
        # Add clarification tools once before first phase (tools persist across all phases)
        if phase_number == 1 and self.state['max_questions_per_agent'] > 0:
            self._add_clarification_tools_to_agents()
        
        # Update swarm configuration for this phase
        entry_point_key = phase_config.get('entry_point', 'sam_powerpoint')
        self.swarm.entry_point = self.agents[entry_point_key].agent
        self.swarm.max_handoffs = phase_config.get('max_handoffs', SWARM_CONFIG['max_handoffs'])
        
        # Build phase prompt
        phase_prompt = self._build_phase_prompt(phase_number)
        
        # Stream the swarm execution (mark if this is the final phase)
        handler = CommitteeStreamHandler(self.agents, show_thinking=show_thinking)
        
        async for event in self.swarm.stream_async(
            phase_prompt,
            invocation_state=self.state
        ):
            await handler.handle_event(event)
        
        return handler.result
    
    async def run_async(self, user_prompt: str, show_thinking: bool = False, questions_per_agent: int = 1):
        """Run the swarm-based committee meeting asynchronously."""
        self._initialize_state(user_prompt)
        self.state['max_questions_per_agent'] = questions_per_agent
        
        # Initialize swarm once for all phases
        self._initialize_swarm()
        
        # Phase 1: Proposal Generation
        phase1_result = await self._run_phase_swarm(1, show_thinking=show_thinking)
        
        # Store proposal if available
        if phase1_result:
            self.state['proposal'] = str(phase1_result)
        
        # Display clarification summary
        self._print_clarification_summary()
        
        input("\nPlease review the initial proposal above.\nPress Enter to bring the committee into the discussion.")
        
        # Phase 2: Initial Review
        phase2_result = await self._run_phase_swarm(2, show_thinking=show_thinking)
        
        input("\nPlease review the committee discussion above.\nPress Enter to continue deliberation.")
        
        # Phase 3: Cross-Committee Deliberation
        phase3_result = await self._run_phase_swarm(3, show_thinking=show_thinking)
        
        input("\nPlease review the committee discussion above.\nPress Enter to continue deliberation.")

        # Phase 4: Final Positions
        phase5_result = await self._run_phase_swarm(4, show_thinking=show_thinking)
        
        input("\nPlease review the committee's final positions above.\nPress Enter to review the committee decision and go-forward plan.")
        
        # Phase 5: Decision
        final_result = await self._run_phase_swarm(5, show_thinking=show_thinking)

        print("\n\n[**Meeting has ended.**]")
        
        return final_result
    
    def run(self, user_prompt: str, show_thinking: bool = False, questions_per_agent: int = 2):
        """Run the swarm-based committee meeting (synchronous wrapper).
        
        Args:
            user_prompt: The user's request to the committee
            show_thinking: Whether to display agent thinking blocks
            questions_per_agent: Number of clarification questions each agent can ask (default: 2)
        """
        return asyncio.run(self.run_async(user_prompt, show_thinking=show_thinking, questions_per_agent=questions_per_agent))
