"""CLI entry point for Designed by Committee."""
import argparse
import sys
from dbc.committee import COMMITTEE_MEMBERS
from dbc.workflow import CommitteeMeeting, CommitteeMeetingSwarm


def kickoff(args):
    """Kickoff a swarm-based committee meeting (default workflow)."""
    # Get user prompt
    user_prompt = " ".join(args.prompt)
    if not user_prompt:
        print("Enter your request for the committee:")
        user_prompt = input("> ")

    if not user_prompt.strip():
        print("Error: No prompt provided", file=sys.stderr)
        sys.exit(1)
    
    # Create and run swarm meeting
    meeting = CommitteeMeetingSwarm.from_members(COMMITTEE_MEMBERS)
    
    try:
        meeting.run(
            user_prompt,
            show_thinking=args.show_thinking,
            questions_per_agent=args.questions_per_agent
        )
    except KeyboardInterrupt:
        print("\nMeeting interrupted due to unscheduled stakeholder input.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\nMeeting encountered an unresolved blocking issue: {e}", file=sys.stderr)
        sys.exit(1)


def kickoff_legacy(args):
    """Kickoff a committee meeting using legacy workflow."""
    # Get user prompt
    user_prompt = " ".join(args.prompt)
    if not user_prompt:
        print("Enter your request for the committee:")
        user_prompt = input("> ")

    if not user_prompt.strip():
        print("Error: No prompt provided", file=sys.stderr)
        sys.exit(1)
    
    # Create and run meeting
    meeting = CommitteeMeeting.from_members(COMMITTEE_MEMBERS)
    
    try:
        meeting.run(user_prompt)
    except KeyboardInterrupt:
        print("Meeting interrupted due to unscheduled stakeholder input.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Meeting encountered an unresolved blocking issue:{e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="dbc",
        description="Multi-agent committee decision facilitation system"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Kickoff subcommand (default swarm workflow)
    kickoff_parser = subparsers.add_parser(
        "kickoff",
        help="Start a new committee meeting (default)"
    )
    kickoff_parser.add_argument(
        "prompt",
        nargs="*",
        help="The request or question for the committee"
    )
    kickoff_parser.add_argument(
        "--show-thinking",
        action="store_true",
        help="Show <thinking> blocks for debugging meeting setup"
    )
    kickoff_parser.add_argument(
        "--questions-per-agent",
        type=int,
        default=2,
        help="Number of clarification questions each agent can ask during Phase 1 (default: 2)"
    )
    kickoff_parser.set_defaults(func=kickoff)
    
    # Kickoff-legacy subcommand (original workflow)
    kickoff_legacy_parser = subparsers.add_parser(
        "kickoff-legacy",
        help="Start a new committee meeting using legacy workflow (structured rounds)"
    )
    kickoff_legacy_parser.add_argument(
        "prompt",
        nargs="*",
        help="The request or question for the committee"
    )
    kickoff_legacy_parser.set_defaults(func=kickoff_legacy)
    
    args = parser.parse_args()
    
    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main()
