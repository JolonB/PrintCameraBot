import argparse

parser = argparse.ArgumentParser(description="Camera bot script.")
parser.add_argument(
    "-b", "--boot-main", help="Run the main script.", action="store_true"
)
parser.add_argument(
    "-c", "--cam-test", help="Run the camera test script.", action="store_true"
)
parser.add_argument(
    "-a",
    "--auth",
    help="Run the 2-factor authentication code script",
    action="store_true",
)
parser.add_argument(
    "-f",
    "--config-file",
    help="The path to the config file. This could be useful with multiple printers (and email addresses)",
    default="config.json",
)
args = parser.parse_args()

if __name__ == "__main__":
    args_provided = args.boot_main + args.cam_test + args.auth
    if args_provided > 1:
        print("Please select only one script to run.")
        exit(1)

    input_val = 0
    if args_provided == 0:
        while input_val not in {"1", "2", "3"}:
            input_val = input(
                "Would you like to:\n1. Run the main script\n2. Run the camera test"
                "\n3. Run the 2-factor authentication setup\nEnter 1, 2, or 3: "
            )
    input_val = int(input_val)

    if args.boot_main or input_val == 1:
        from scripts.bot_daemon import main
    elif args.cam_test or input_val == 2:
        from scripts.camera_test import main
    elif args.auth or input_val == 3:
        from scripts.setup_2fa import main

    # Pass through the config file path and whether use CLI mode (if no
    # arguments are provided)
    main(config_file=args.config_file, interactive=(not args_provided))
