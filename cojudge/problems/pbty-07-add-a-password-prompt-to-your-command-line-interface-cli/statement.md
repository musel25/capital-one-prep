Let's get serious. Your Command Line Interface (CLI) works and you want to authenticate who is using your application.

Here is a simple example of how to receive credentials via a password prompt.

Refer to [Typer password documentation](https://typer.tiangolo.com/tutorial/options/password/) for more help.

Enjoy!

**Constraints:**

- Export a single-command `app`. Required options `--username` and `--password` prompt with `Username` and `Password`. Hide and confirm the password. After a mismatch, prompt again. Explicit options need no prompt. Print `Authenticated as USERNAME` on success. Never print the password. End-of-input or Ctrl-C must abort with a nonzero exit code.
