import os
import subprocess


def run_github_actions_locally():
    # Set up the environment
    run_list_output = subprocess.run(["gh", "run", "list"], capture_output=True, text=True)
    run_list = run_list_output.stdout.splitlines()
    failed_run_id = None

    # Find the failed run ID
    for run in run_list:
        if "failed" in run:
            failed_run_id = run.split()[0]
            break

    if failed_run_id is None:
        print("No failed workflow runs found.")
        return

    # Download the workflow artifacts
    download_command = ["gh", "run", "download", failed_run_id]
    subprocess.run(download_command)

    # Extract the artifacts
    artifact_file = f"{failed_run_id}.tar.gz"
    extract_command = ["tar", "-xf", artifact_file]
    subprocess.run(extract_command)

    # Execute necessary steps for debugging
    # Add your specific debugging steps here

    # Cleanup
    os.remove(artifact_file)


if __name__ == "__main__":
    run_github_actions_locally()
