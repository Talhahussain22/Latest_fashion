import time
import subprocess

while True:
    print("Running scraper...")
    subprocess.run(["python", "app.py"])
    print("Sleeping for 7 days...")
    time.sleep(7 * 24 * 60 * 60)  # 7 days
