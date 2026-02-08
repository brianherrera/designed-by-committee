"""CLI entry point for Designed by Committee."""
import argparse
import sys
from dbc.committee import COMMITTEE_MEMBERS
from dbc.workflow import CommitteeMeeting


def kickoff(args):
    """Kickoff a committee meeting."""
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
    
    # Kickoff subcommand
    kickoff_parser = subparsers.add_parser(
        "kickoff",
        help="Start a new committee meeting"
    )
    kickoff_parser.add_argument(
        "prompt",
        nargs="*",
        help="The request or question for the committee"
    )
    kickoff_parser.set_defaults(func=kickoff)
    
    args = parser.parse_args()
    
    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main()
