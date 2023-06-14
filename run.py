import argparse
from interfaces import cli, api, voice

def main():
    """
    Main function for application execution
    """
    parser = argparse.ArgumentParser(description="LLM conversational command client.")
    parser.add_argument('-i', '--interface', choices=['voice', 'api', 'cli'], default='cli', help="Select an interface voice, api, or cli.")
    parser.add_argument("-l", "--loadprompt", action="store_true", help="Load stored system prompt when using the CLI interface")

    args = parser.parse_args()

    if args.interface == 'voice':
        # voice.run()
        print("Voice functionality not yet implemented.")
    elif args.interface == 'api':
        api.run()
    else:
        cli.run(load_prompt=args.loadprompt)

if __name__ == "__main__":
    main()