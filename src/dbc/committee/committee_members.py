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
        system_prompt_module: Importable module path for the system prompt
        model_id: Bedrock model key for this member
    """
    key: str
    display_name: str
    system_prompt_module: str
    model_id: str


# Committee member definitions
COMMITTEE_MEMBERS: Dict[str, CommitteeMember] = {
    'morgan_calendar': CommitteeMember(
        key='morgan_calendar',
        display_name='Morgan Calendar',
        system_prompt_module='dbc.prompts.system.morgan_calendar',
        model_id='anthropic.claude-3-7-sonnet-20250219-v1:0'
    ),
    'nina_edgecase': CommitteeMember(
        key='nina_edgecase',
        display_name='Nina Edgecase',
        system_prompt_module='dbc.prompts.system.nina_edgecase',
        model_id='anthropic.claude-opus-4-5-20251101-v1:0'
    ),
    'casey_friday': CommitteeMember(
        key='casey_friday',
        display_name='Casey Friday',
        system_prompt_module='dbc.prompts.system.casey_friday',
        model_id='amazon.nova-pro-v1:0'
    ),
    'sam_powerpoint': CommitteeMember(
        key='sam_powerpoint',
        display_name='Sam PowerPoint',
        system_prompt_module='dbc.prompts.system.sam_powerpoint',
        model_id='openai.gpt-oss-120b-1:0'
    ),
    'fontaine_kerning': CommitteeMember(
        key='fontaine_kerning',
        display_name='Fontaine Kerning',
        system_prompt_module='dbc.prompts.system.fontaine_kerning',
        model_id='google.gemma-3-12b-it'
    ),
    'pat_attacksurface': CommitteeMember(
        key='pat_attacksurface',
        display_name='Pat AttackSurface',
        system_prompt_module='dbc.prompts.system.pat_attacksurface',
        model_id='anthropic.claude-sonnet-4-5-20250929-v1:0'
    ),
    'noah_actually': CommitteeMember(
        key='noah_actually',
        display_name='Noah Actually',
        system_prompt_module='dbc.prompts.system.noah_actually',
        model_id='openai.gpt-oss-20b-1:0'
    ),
}
