"""
This module contains the discussion summary prompt for the Designed by Committee
decision facilitation system. This prompt is used to produce a concise summary
of the current round's discussion.
"""

DISCUSSION_SUMMARY_PROMPT = """Instruction:
Produce a concise discussion summary of the current round.

Guidelines:
- Start your response with one of the phrases from your defined Signature Language.
- Include at least one insightful comment based on the previous discussion. 
- Abstract away disagreement and specificity.
- Reframe tension as healthy discussion or valuable input.

Response Constraints:
- Limit responses to 1-2 brief sentences.
- Do not quote individuals directly."""
