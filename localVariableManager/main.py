# Build-In Modules
import argparse

# Local Modules
import localVariableManager.manager as manager

def main():
    """
    Main function to parse args and take action
    """
    # Build our a list of arguments and parse them
    usage = "CLI for managing and maintaining tokens and key/certs."
    argparser = argparse.ArgumentParser(usage=usage)
    argparser.add_argument(
        "-add",
        help="Adds a file to lcm [needs --name as well]",
        nargs=1,
    )
    argparser.add_argument(
        "-name",
        help="Name to be used",
        nargs=1,
    )
    argparser.add_argument(
        "-delete",
        help="Delete a saved file",
        nargs=1,
    )
    argparser.add_argument(
        "-setenv",
        help="Expose a saved file as an environmental variable [needs --name as well]",
        nargs=1,
    )
    args = argparser.parse_args()

    # Parse our args and take action
    if args.add:
        if not args.name:
            print("[Error] No name provided!")
        elif not manager.add(args.add, args.name):
            print(f"[Error] Unable to add {args.name}")
        else:
            print(f"Successfully added {args.name}")
    elif args.delete:
        if manager.delete(args.delete):
            print(f"Successfully deleted {args.delete}")
        else:
            print(f"[Error] Unable to delete {args.name}")
    elif args.setenv:
        name = args.name
        if not name:
            print(f"No name provided using {args.delete}")
            name = args.delete
        if manager.setenv(args.setenv, name):
            print(f"Successfully set {args.delete}")
        else:
            print(f"[Error] Unable to delete {args.delete}")
