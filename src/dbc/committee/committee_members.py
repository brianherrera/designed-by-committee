"""
Committee member definitions for the Designed by Committee system.

This module contains all committee member configurations.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class CommitteeMember:
    """
    Represents a committee member with their configuration.
    
    Attributes:
        key: Unique identifier for the committee member
        display_name: Human-readable name displayed in output
        prompt_module: Importable module path for the system prompt
        model_id: Bedrock model key for this member
        title: Job title or role of the committee member
    """
    key: str
    display_name: str
    prompt_module: str
    model_id: str
    title: str


# Committee member definitions
COMMITTEE_MEMBERS: Dict[str, CommitteeMember] = {
    'morgan_calendar': CommitteeMember(
        key='morgan_calendar',
        display_name='Morgan Calendar',
        prompt_module='dbc.prompts.committee.morgan_calendar',
        model_id='us.anthropic.claude-3-7-sonnet-20250219-v1:0',
        title='Meeting Facilitator'
    ),
    'nina_edgecase': CommitteeMember(
        key='nina_edgecase',
        display_name='Nina Edgecase',
        prompt_module='dbc.prompts.committee.nina_edgecase',
        model_id='global.anthropic.claude-opus-4-5-20251101-v1:0',
        title='Principal Engineer'
    ),
    'casey_friday': CommitteeMember(
        key='casey_friday',
        display_name='Casey Friday',
        prompt_module='dbc.prompts.committee.casey_friday',
        model_id='us.amazon.nova-pro-v1:0',
        title='Product Manager'
    ),
    'sam_powerpoint': CommitteeMember(
        key='sam_powerpoint',
        display_name='Sam PowerPoint',
        prompt_module='dbc.prompts.committee.sam_powerpoint',
        model_id='us.meta.llama4-scout-17b-instruct-v1:0',
        title='Director of Strategy'
    ),
    'fontaine_kerning': CommitteeMember(
        key='fontaine_kerning',
        display_name='Fontaine Kerning',
        prompt_module='dbc.prompts.committee.fontaine_kerning',
        model_id='us.writer.palmyra-x5-v1:0',
        title='Principal Designer'
    ),
    'pat_attacksurface': CommitteeMember(
        key='pat_attacksurface',
        display_name='Pat AttackSurface',
        prompt_module='dbc.prompts.committee.pat_attacksurface',
        model_id='global.anthropic.claude-sonnet-4-5-20250929-v1:0',
        title='Security Architect'
    ),
    'max_token': CommitteeMember(
        key='max_token',
        display_name='Max Token',
        prompt_module='dbc.prompts.committee.max_token',
        model_id='us.meta.llama4-maverick-17b-instruct-v1:0',
        title='AI Platform Lead'
    ),
}
