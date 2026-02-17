# Designed by Committee

Designed by Committee is a value-add alignment initiative by Outcome Systems, Inc., a business strategy consulting firm specializing in alignment.

This process delivers measurable improvements in organizational cohesion by formalizing the collaborative decision-making process.

## How Does It Work?

Designed by Committee accepts a single prompt and guides it through a multi-round discussion leveraging a cross-functional team of AI models.

The final round produces a consensus-driven recommendation, along with the decision framework and stakeholder feedback that drove alignment.

## Committee Members

Each session is attended by a standing committee of stakeholders, representing a range of organizational priorities:

- **Morgan Calendar**: Facilitator, keeper of the meeting 
- **Nina Edgecase**: How does this work at scale?
- **Casey Friday**: Ship first, ask questions later
- **Sam PowerPoint**: Executive Summary: Repeating what you just said
- **Fontaine Kerning**: Can I get the icon in cornflower blue?
- **Pat AttackSurface**: Shipping is a threat vector 
- **Max Token**: This should be an agentic workflow

Each committee member is instantiated using a distinct AI model chosen to reflect a diversity of perspectives and priorities.

## Usage

Designed by Committee is a command-line tool powered by [Strands Agents](https://github.com/strands-agents/sdk-python).

```bash
dbc kickoff "Design a web portal"
```

Before running your first meeting, complete the [Setup Guide](SETUP.md) to configure AWS permissions and credentials.

## Sample Committee Dialogue

```text
MORGAN CALENDAR (Meeting Facilitator):
Let's stay on time. I'm going to pull in specific stakeholders to react to key elements of this proposal.

NINA EDGECASE (Principal Engineer):
I'm concerned about several assumptions here. Are we solving a real problem or an imagined one?

FONTAINE KERNING (Principal Designer):
The spacing feels cramped. If we don't fix the visual hierarchy, adoption will suffer.

MAX TOKEN (AI Platform Lead):
This is a solved problem with LLMs — and I'm not seeing nearly enough AI integration in this proposal.

CASEY FRIDAY (Product Manager):
Perfect is the enemy of good. Ship search in 8–10 weeks. AI can come later.

PAT ATTACKSURFACE (Security Architect):
Have we threat modeled this? Casey wants keyword search first, but Max is pushing AI-first architecture.

SAM POWERPOINT (Director of Strategy):
What I'm hearing is a strategic opportunity to build the runway while flying the plane.
```

See the full transcript:
[Dev Portal Example](examples/dev-portal-full-transcript.txt)

## Notes

* Discussion flow is self-directed, with members dynamically shaping the discussion in real time
* There is a hard stop in the final round and the committee must deliver a go-forward plan
* Token usage may exceed the practical value of the outcome

The committee optimizes for alignment, not efficiency.
