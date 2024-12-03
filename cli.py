import subprocess
import argparse

# Define commit function
def commit_changes(commit_message, author):
    try:
        # Run git commands
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message, "--author", author], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Changes committed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error during commit: {e}")
        exit(1)

def main():
    # Set up CLI argument parsing
    parser = argparse.ArgumentParser(description="A simple Python CLI for Git commits.")
    parser.add_argument("message", type=str, help="Commit message")
    parser.add_argument("--author", type=str, default="hasnaink-07 <halwakk07@gmail.com>", help="Author of the commit")
    args = parser.parse_args()

    # Commit the changes with the given message and author
    commit_changes(args.message, args.author)

if __name__ == "__main__":
    main()
