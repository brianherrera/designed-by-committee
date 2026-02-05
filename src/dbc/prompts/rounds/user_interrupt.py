"""
This module contains the user interrupt prompt for the Designed by Committee
decision facilitation system. This prompt is used to gather stakeholder
clarification between round two and round three.
"""

USER_INTERRUPT_PROMPT = """Instruction:
Formulate a single clarification question for the stakeholder.

Guidelines:
- Identify the area of greatest perceived ambiguity or misalignment across the discussion.
- Ask exactly one open-ended clarification question.
- Frame the question as necessary to move forward.
- Keep the question broad enough to invite interpretation.

Constraints:
- Use professional, process-oriented corporate language.
- Do not suggest possible answers or examples.
- Do not narrow scope, define criteria, or impose constraints.
- Do not attempt to resolve disagreement.
- Do not reference individual committee members or positions.

Avoid:
- Yes/no questions.
- Compound or multi-part questions.
- Language that would meaningfully reduce ambiguity.
- Any phrasing that commits the group to a specific direction.

Tone:
- Polite and neutral.
- Calmly urgent.
- Imply that this clarification will “help with alignment” without guaranteeing it.

Output Expectations:
- A single paragraph containing one question.
- The question should feel reasonable, necessary, and slightly underspecified.
"""
