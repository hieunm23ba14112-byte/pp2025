try:
    # If run as module: python -m pw4.main
    from .output import CLI  # type: ignore
except Exception:
    # If run as script: python pw4/main.py
    from output import CLI

if __name__ == "__main__":
    # After run python 3.student.mark.py, you should press Enter, q to use fully this CLI.
    # Now, three first function aren't avaleble.
    # The option is so boring!
    CLI().start()