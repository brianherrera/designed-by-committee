"""
This module contains the round two prompt for the Designed by Committee
decision facilitation system. This prompt is used for all committee members
in the second round of discussion.
"""

ROUND_TWO_PROMPT = """Instruction:
Raise a concern about the proposal.

Guidelines:
- Focus on minor or cosmetic aspects such as wording, naming, ordering, visuals, framing, or tone.
- Treat this concern as meaningful to overall success.
- Ground your feedback in specific details from the proposal.
- Do not discuss core functionality, architecture, scope, or feasibility.
- Do not propose alternative solutions or rewrites.

Tone:
- Your level of concern should scale with the current tension.
- As tension increases, treat the issue as increasingly important and time-sensitive.

Response Constraints:
- Write one short paragraph.
- Express a clear point of friction or discomfort.
- End with a pointed, unresolved question that pressures the group to respond.

Output Expectations:
- The feedback should feel reasonable, specific, and slightly disruptive.
- This comment will be preserved and revisited in later rounds."""
