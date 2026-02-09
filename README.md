# Designed by Committee

Designed by Committee is a value-add alignment initiative by Outcome Systems, Inc., a business strategy consulting firm specializing in alignment.

It is a decision facilitation solution designed to incorporate multiple perspectives in support of forward progress.

## How Does It Work?

Designed by Committee accepts a single prompt and guides it through a multi-round discussion leveraging a cross-functional team of AI models.

By routing ideas through a structured alignment workflow, it ensures proposals are reviewed, debated, and refined.

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
dbc kickoff "Design a landing page for a productivity app"
```

The tool assumes AWS credentials and Bedrock access are already configured.

## Notes

* User clarifications may introduce new ambiguity
* Tensions may increase as discussions progress through each round
* There is a hard stop in the final round and the committee must reach alignment on a go-forward plan during this time

Success is not guaranteed.
