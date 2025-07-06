def run():
    import subprocess
    import os

    print("Running plotly_get_chrome...")
    subprocess.run(["plotly_get_chrome"], check=True)

    # Set environment variable so Kaleido knows where to find Chrome
    chrome_path = os.path.expanduser("~/.plotly/kaleido/chrome/chrome")
    os.environ["KAL_CHROME_PATH"] = chrome_path
    print(f"Set KAL_CHROME_PATH to {chrome_path}")
