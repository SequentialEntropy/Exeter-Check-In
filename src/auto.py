import time
from datetime import datetime, timedelta
import random
from main import main
from threading import Thread

USERS = [
    "refresh_token.txt"
]

MIN_WAIT_MINS = 0
MAX_WAIT_MINS = 20

def check_in(refresh_token_path):
    seconds = random.randrange(MIN_WAIT_MINS * 60, MAX_WAIT_MINS * 60) # Waits randomly between 0 to 20 minutes
    run_time = datetime.now() + timedelta(seconds=seconds)
    print(f"Waiting for {seconds} seconds... Scheduled for {run_time}", flush=True)
    time.sleep(seconds)

    print(f"Running main script at {datetime.now()}", flush=True)
    main(refresh_token_path=refresh_token_path)

def scheduler():
    while True:
        now = datetime.now()
        
        # Check if the current minute is 35
        if now.minute == 35:
            for user in USERS:
                Thread(target=check_in, args=[user]).start()
            time.sleep(60)  # Wait a minute to avoid running multiple times in the same minute
        else:
            time.sleep(30)  # Check every 30 seconds if it's the 35th minute

if __name__ == "__main__":
    print("Running auto scheduler...", flush=True)
    scheduler()