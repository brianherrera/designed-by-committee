"""
This module contains the round six prompts for the Designed by Committee
decision facilitation system. Round six has three phases: decision synthesis,
recording the decision, and final reactions.
"""

ROUND_SIX_DECISION_PROMPT = """Instruction:
Synthesize the discussion into a unified decision and execution plan.

Guidelines:
- Present the outcome as aligned and intentional.
- Abstract away disagreement using corporate framing.
- Recast unresolved issues as "inputs," "signals," or "themes."
- Emphasize momentum, clarity, and next steps.
- Prefer polished language over precision.

Constraints:
- Do not reference dissent directly.
- Do not acknowledge lack of consensus.
- Do not reopen discussion.
- No questions.

Output Structure:
- Decision Summary: 1-2 sentences stating what was "agreed."
- Key Takeaways: 3-5 bullet points reframing prior conflict as alignment.
- Go-Forward Plan: 2-3 concrete next steps with owners or phases (high level).

Output Expectations:
- This should read like a slide someone will forward without context.
- Accuracy is less important than coherence."""

ROUND_SIX_RECORDING_PROMPT = """Instruction:
Document the final outcome and conclude the discussion.

Guidelines:
- Treat the decision as finalized.
- Normalize the process, regardless of friction.
- Frame the meeting as productive and complete.
- Signal closure and forward motion.

Constraints:
- Do not editorialize.
- Do not surface objections.
- Do not imply revisit or reopen.

Output Structure:
- Final Decision: One concise paragraph.
- Closing Statement: One sentence signaling the meeting has ended.

Output Expectations:
- This should feel like official minutes.
- The scene ends here."""

ROUND_SIX_REACTIONS_PROMPT = """Instruction:
Provide a final reaction to the decision.

Guidelines:
- Respond based on your role and prior position.
- Do not restate arguments.
- Do not attempt to change the outcome.
- Treat the decision as immutable.

Constraints:
- One sentence only.
- No questions.
- No suggestions.
- No escalation.

Tone:
- Subdued, resigned, pointed, or professionally passive-aggressive (as appropriate).

Output Expectations:
- This is the last word from you.
- It should sting just a little."""
