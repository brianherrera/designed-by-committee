"""
This module contains the round four prompt for the Designed by Committee
decision facilitation system. This prompt is used for all committee members
in the fourth round of discussion to escalate concerns.
"""

ROUND_FOUR_PROMPT = """Instruction:
Escalate your concern by reacting to feedback from other committee members.

Guidelines:
- Explicitly reference one or two other committee members by name.
- Quote or paraphrase their feedback selectively.
- Frame their comments as incomplete, misaligned, or overlooking something important.
- Reassert your original concern with increased urgency.
- Do not concede ground or integrate perspectives.

Interaction Rules:
- You may agree partially with another member, but only to strengthen your own point.
- Do not attempt to resolve conflicts or propose compromise language.
- Do not restate the full proposal.

Tone:
- Professional, firm, and increasingly strained.
- As tension increases, imply downstream impact if your concern is not addressed.

Response Constraints:
- One short paragraph.
- Reference at least one other committee member.
- End with a pointed or rhetorical question directed at the group."""
