import subprocess


def run_process(args: list[str]):
    result = subprocess.run(args, capture_output=True, text=True)
    print(" ".join(result.args))
    print("\n".join([result.stdout, result.stderr]))
