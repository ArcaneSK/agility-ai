import argparse
from interfaces import cli, api

def main():
    """
    Main function for application execution
    """
    parser = argparse.ArgumentParser(description="LLM conversational command client.")
    parser.add_argument('-i', '--interface', choices=['api', 'cli'], default='cli', help="Select an interface voice, api, or cli.")

    # CLI Arguments
    parser.add_argument("-l", "--loadconv", help="Load stored conversation when using the CLI interface.")
    parser.add_argument("-s", "--loadsysprompt", action="store_true", help="Load stored system prompt when using the CLI interface.")

    args = parser.parse_args()

    if args.interface == 'api':
        api.run()
    else:
        cli.run(conversation_id=args.loadconv, load_prompt=args.loadsysprompt)

if __name__ == "__main__":
    main()