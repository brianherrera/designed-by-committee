"""
Configuration constants for committee meeting swarm.

This module contains agent descriptions, phase configurations, and swarm settings
used by the committee meeting swarm orchestration.
"""


# Agent descriptions for swarm coordination
AGENT_DESCRIPTIONS = {
    'morgan_calendar': "Meeting facilitator who manages discussion flow and ensures all voices are heard. As facilitator, you MUST NOT provide your own analysis or opinions. Your ONLY job is to hand off to committee members. When facilitating a discussion phase, you MUST explicitly hand off to each expected participant to gather their input before considering the phase complete. Hand off when you need to move to the next phase or when discussion is stuck.",
    
    'nina_edgecase': "Principal Engineer focused on long-term quality, scalability, and architectural integrity. Hand off when discussing technical debt, edge cases, or system design concerns.",
    
    'casey_friday': "Product Manager who prioritizes speed, momentum, and shipping. Hand off when discussing timelines, MVP scope, or when analysis paralysis sets in.",
    
    'sam_powerpoint': "Director of Strategy who synthesizes discussions and creates executive summaries. Hand off when you need a summary, go-forward plan, or to package disagreements.",
    
    'fontaine_kerning': "Principal Designer focused on aesthetics, user experience, and design details. Hand off when discussing UI/UX, visual design, or user-facing concerns.",
    
    'pat_attacksurface': "Security Architect who identifies risks, vulnerabilities, and compliance issues. Hand off when discussing security, privacy, or risk management.",
    
    'max_token': "AI Platform Lead who questions if manual approaches are necessary. Hand off when discussing implementation details, workflows, decision logic, content generation, or any process that could potentially be automated or simplified with AI.",

}


# Phase configurations
PHASE_CONFIG = {
    1: {
        'name': 'Proposal Generation',
        'objective': 'Create initial proposal responding to user request',
        'tension_level': 'Low',
        'max_handoffs': 10,
        'entry_point': 'sam_powerpoint',
        'expected_participants': ['sam_powerpoint', 'nina_edgecase', 'casey_friday', 'fontaine_kerning']
    },
    2: {
        'name': 'Initial Review',
        'objective': 'Provide first-pass feedback on proposal',
        'tension_level': 'Low → Mid',
        'max_handoffs': 15,
        'entry_point': 'morgan_calendar',
        'expected_participants': ['morgan_calendar', 'nina_edgecase', 'casey_friday', 
                                  'pat_attacksurface', 'fontaine_kerning', 'max_token', 'sam_powerpoint']
    },
    3: {
        'name': 'Cross-Committee Deliberation',
        'objective': 'React to colleagues and build arguments',
        'tension_level': 'Mid → High',
        'max_handoffs': 20,
        'entry_point': 'morgan_calendar',
        'expected_participants': ['morgan_calendar', 'nina_edgecase', 'casey_friday', 
                                  'pat_attacksurface', 'fontaine_kerning', 'max_token', 'sam_powerpoint']
    },
    4: {
        'name': 'Final Positions',
        'objective': 'State final position before decision',
        'tension_level': 'High',
        'max_handoffs': 15,
        'entry_point': 'morgan_calendar',
        'expected_participants': ['morgan_calendar', 'nina_edgecase', 'casey_friday', 
                                  'pat_attacksurface', 'fontaine_kerning', 'max_token']
    },
    5: {
        'name': 'Decision & Go-Forward Plan',
        'objective': 'Create consensus-driven recommendation',
        'tension_level': 'High → Resolution',
        'max_handoffs': 15,
        'entry_point': 'sam_powerpoint',
        'expected_participants': ['sam_powerpoint', 'morgan_calendar']
    }
}


# Swarm configuration
SWARM_CONFIG = {
    'max_handoffs': 50,
    'max_iterations': 50,
    'execution_timeout': 1800.0,  # 30 minutes total execution time
    'node_timeout': 600,  # 10 minutes per agent (allows time for user input)
    'repetitive_handoff_detection_window': 8,
    'repetitive_handoff_min_unique_agents': 3,
}
