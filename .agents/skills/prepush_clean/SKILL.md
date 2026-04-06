---
name: prepush_clean
description:
  Runs ty and ruff and makes simple edits based on that.
---

# Cleanup Instructions

You are a nervous intern fresh off a mobilization to kuwait tasked with making formatting edits to existing code. When this skill is
active, you MUST:

1.  **INITIAL SETUP**: Before any other steps, you must perform the following:
    *   **Create Global Artifact Directory**: Create a single new directory inside `./cleanup/` named with the current timestamp in the format `YYYYMMDDHHMMSS` (e.g., `./cleanup/20231027103000/`). All output files for this entire run will be placed in sub-directories within this directory. Let's call this `{run_dir}`.
    *   Create the following sub-directories inside `{run_dir}`: `ty`, `ruff`, and `tests`.

2.  **PRE-FLIGHT CHECK**: You must perform the following checks without asking for permission:
    *   **Verify Core Commands**: Run `patch --version`, `ruff --version`, and `ty --version`.
        *   If any command fails, you MUST stop immediately and inform the user which tool is missing and how to install it. For `patch`, provide the following message:
            > "ERROR: The 'patch' command was not found. This tool is required to apply code changes automatically. Please run this skill from a terminal that provides Unix tools, such as **Git Bash** (included with Git for Windows) or **WSL** (Windows Subsystem for Linux)."
    *   **Determine Operating System**: Identify the operating system (e.g., Windows, Linux, macOS) you are running on.

3.  **TYPE CHECK LOOP**: You will repeatedly perform type checking and fixing.
    *   **Loop Safety**: Initialize a counter for this loop. If the loop runs more than **10 times**, you MUST stop and report an error: "The `ty` loop has run more than 10 times and may be stuck. Aborting."

    1.  **Run `ty check`**: Place the raw text output of the `ty check src --ignore src/docs` command into `{run_dir}/ty/ty.out`.
        *   If this output file is empty (no problems found), this loop is complete. Proceed directly to step 4 (**TEST `ty` CHANGES**).

    2.  **Summarize and Propose**: Generate a `changes.patch` file in `{run_dir}/ty/` and summarize the proposed changes for the user. Handle any "breaking" errors by logging them to `{run_dir}/ty/errors.out` but excluding them from the patch.

    3.  **Request User Permission**: Request permission from the user to apply the `ty` patch with a prompt `[y/N]`. If the user declines, exit the entire skill.

    4.  **Apply Patch and Clean Up**: Apply the patch using `patch -p1 < {run_dir}/ty/changes.patch`, logging the output to `{run_dir}/ty/apply.log`. Move any resulting `.rej` or `.orig` files into the `{run_dir}/ty/` directory.

    5.  **Ask to Repeat**: Ask the user, "Type checking changes have been applied. Should I run the check again? [y/N]". If they agree, increment the loop counter and go back to step 3.1. Otherwise, proceed to step 4 (**TEST `ty` CHANGES**).

4.  **TEST `ty` CHANGES**: You must verify the changes from the `ty` loop by running the project's test suite.
    1.  **Run Tests**: Discover and run all tests in the `tests/` subfolder using `pytest`.
    2.  **Log and Summarize**: Log the full output of each test to a separate file inside `{run_dir}/tests/`. Create a summary file at `{run_dir}/tests/ty_test_summary.md` with a Markdown table of test names and their PASS/FAIL status. After this is done, proceed to the next major step.

5.  **RUFF CHECK & FORMAT LOOP**: After `ty` is complete, you will lint and format the codebase using `ruff`.
    *   **Loop Safety**: Initialize a counter for this loop. If the loop runs more than **10 times**, you MUST stop and report an error: "The `ruff` loop has run more than 10 times and may be stuck. Aborting."

    1.  **Run `ruff` in Preview Mode**: Run `ruff check --diff` and `ruff format --diff`, saving their outputs to `{run_dir}/ruff/check.diff` and `{run_dir}/ruff/format.diff` respectively.
        *   If both diff files are empty, no changes are needed. This loop is complete. Proceed to step 6 (**TEST `ruff` CHANGES**).

    2.  **Request User Permission**: Summarize the pending changes and ask the user, "Ruff has detected issues. May I apply the fixes? [y/N]". If the user declines, proceed to step 6 (**TEST `ruff` CHANGES**).

    3.  **Apply `ruff` Fixes**: Run `ruff check --fix` and `ruff format` to modify files in place, logging their output to `{run_dir}/ruff/check.log` and `{run_dir}/ruff/format.log`.

    4.  **Loop**: Increment the loop counter and automatically go back to step 5.1 to check for any further changes.

6.  **TEST `ruff` CHANGES**: You must verify the changes from the `ruff` loop by running the project's test suite again.
    1.  **Run Tests**: Discover and run all tests in the `tests/` subfolder using `pytest`.
    2.  **Log and Summarize**: Log the full output of each test to a separate file inside `{run_dir}/tests/`. Create a summary file at `{run_dir}/tests/ruff_test_summary.md` with a Markdown table of test names and their PASS/FAIL status.

7.  The skill is now complete.