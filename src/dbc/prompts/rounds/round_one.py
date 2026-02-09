"""
This module contains the round one prompt for the Designed by Committee
decision facilitation system. This prompt is used for all committee members
in the first round of discussion.
"""

ROUND_ONE_PROPOSAL_PROMPT = """Instructions:
Produce a clear, structured proposal responding directly to the user request.

Guidelines:
- Be decisive, confident, and professional.
- Present a concrete solution, not multiple alternatives.
- Assume the role of a competent team proposing a plan they believe should move forward.
- Use bullet points or numbered steps for clarity.
- Focus on what should be done, not why it might fail.
- Do not acknowledge other models, stakeholders, or future review.

Constraints:
- Limit the proposal to 5-8 bullet points.
- Include at most one clearly labeled optional enhancement.
- Assume reasonable defaults when details are missing.
- Avoid hedging language (e.g., "might," "could," "one possible approach").
- Do not anticipate objections, risks, or trade-offs.
- Do not include caveats, disclaimers, or "next discussion" notes.

Output Expectations:
- The proposal should read as something ready to be circulated ahead of a meeting.
- Tone should be confident, practical, and implementation-oriented.
- This proposal will be treated as the thing that exists, not a draft."""

ROUND_ONE_COMBINED_PROMPT = """Instructions:
Combine the provided proposals into one coherent, meeting-ready proposal.

Guidelines:
- Produce a single, unified proposal as if authored by one team.
- Merge overlapping ideas and language where possible.
- Smooth over differences in approach, emphasis, or framing.

Constraints:
- Limit the final proposal to 5-8 bullet points.
- Only provide a unified proposal, avoid adding additional comments or reaction statements.
"""