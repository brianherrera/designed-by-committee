"""
Utility functions for working with committee members.

This module provides additional helper functions and utilities
for managing and working with committee member data.
"""

from typing import List, Optional, Dict
import importlib
from dbc.committee import CommitteeMember, COMMITTEE_MEMBERS


def load_system_prompt(member: CommitteeMember) -> str:
    """
    Dynamically load the system prompt for a committee member.
    
    Args:
        member: The committee member to load the prompt for
        
    Returns:
        str: The system prompt content
        
    Raises:
        ImportError: If the system prompt module cannot be imported
        AttributeError: If the expected prompt variable is not found
    """
    try:
        module = importlib.import_module(member.system_prompt_module)
        
        # Use the standardized naming pattern
        prompt_var_name = f"{member.key.upper()}_SYSTEM_PROMPT"
        
        if hasattr(module, prompt_var_name):
            return getattr(module, prompt_var_name)
        
        # If variable not found, raise an error
        available_attrs = [attr for attr in dir(module) if not attr.startswith('_')]
        raise AttributeError(
            f"Could not find system prompt variable '{prompt_var_name}' in {member.system_prompt_module}. "
            f"Available attributes: {available_attrs}"
        )
        
    except ImportError as e:
        raise ImportError(f"Could not import system prompt module for {member.key}: {e}")


def validate_member_configuration(member: CommitteeMember) -> List[str]:
    """
    Validate a committee member's configuration.
    
    Args:
        member: The committee member to validate
        
    Returns:
        List[str]: List of validation errors (empty if valid)
    """
    errors = []
    
    # Check required fields
    if not member.key:
        errors.append("Member key cannot be empty")
    
    if not member.display_name:
        errors.append("Member display_name cannot be empty")
    
    if not member.system_prompt_module:
        errors.append("Member system_prompt_module cannot be empty")
    
    if not member.model_id:
        errors.append("Member model_id cannot be empty")
    
    # Check key format (should be lowercase with underscores)
    if member.key and not member.key.islower():
        errors.append("Member key should be lowercase")
    
    if member.key and ' ' in member.key:
        errors.append("Member key should not contain spaces (use underscores)")
    
    # Try to validate system prompt can be loaded
    if member.system_prompt_module:
        try:
            load_system_prompt(member)
        except (ImportError, AttributeError) as e:
            errors.append(f"System prompt validation failed: {e}")
    
    return errors


def validate_all_members() -> Dict[str, List[str]]:
    """
    Validate all committee member configurations.
    
    Returns:
        Dict[str, List[str]]: Mapping of member keys to their validation errors
    """
    validation_results = {}
    
    for key, member in COMMITTEE_MEMBERS.items():
        errors = validate_member_configuration(member)
        if errors:
            validation_results[key] = errors
    
    # Check for duplicate keys (shouldn't happen with dict, but good to verify)
    keys = [member.key for member in COMMITTEE_MEMBERS.values()]
    if len(keys) != len(set(keys)):
        validation_results['_global'] = ['Duplicate member keys found']
    
    return validation_results
