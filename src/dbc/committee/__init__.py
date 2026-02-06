"""
Committee module for Designed by Committee.

This module contains the definitions and utilities for managing
committee members in the decision facilitation system.
"""

from .committee_members import (
    CommitteeMember,
    COMMITTEE_MEMBERS,
)

from .utils import (
    load_system_prompt,
    validate_member_configuration,
    validate_all_members,
)
