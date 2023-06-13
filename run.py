import argparse
from interfaces import voice, api, cli

def main():
    parser = argparse.ArgumentParser(description="Choose an interface for the application.")
    parser.add_argument('-i', '--interface', choices=['voice', 'api', 'cli'], default='cli', help="Select an interface voice, api, or cli.")

    args = parser.parse_args()

    if args.interface == 'voice':
        voice.run()
    elif args.interface == 'api':
        api.run()
    else:
        cli.run()

if __name__ == "__main__":
    main()