"""
This module contains the user interrupt prompt for the Designed by Committee
decision facilitation system. This prompt is used to gather stakeholder
clarification between round two and round three.
"""

USER_INTERRUPT_PROMPT = """Instruction:
Formulate a single clarification question for the user.

Guidelines:
- Identify the area of greatest perceived ambiguity or misalignment across the discussion.
- Ask exactly one open-ended clarification question.
- Frame the question as necessary to move forward.
- Focus on questions about priority and where the USER thinks the committee should make tradeoffs.
- Phrase your response like you're talking directly to the user on behalf of the committee.

Constraints:
- Use professional, process-oriented corporate language.
- Address the target of your response as USER.

Avoid:
- Yes/no questions.
- Compound or multi-part questions.

Output Expectations:
- Limit responses to 1-2 brief sentences.
- The question should feel reasonable, necessary, and slightly underspecified.
"""
