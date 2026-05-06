import asyncio
import time
from scraper import run_scraper
from Ai import run_ai
from emailer import run_emailer

async def main():
    while True:
        try:
            print("Starting scraper...")
            await run_scraper()
            print("Scraper done. Starting AI processing...")
            try:
                run_ai()
            except Exception as e:
                print(f"encountered the following while running ai.py: {e}")
            print("AI processing done. Starting emailer...")
            run_emailer()
            print("Emailer done. Sleeping for 30 minutes...")
            await asyncio.sleep(1800)
        except Exception as e:
            print(f"encountered error: {e}")
            await asyncio.sleep(1000)
if __name__ == "__main__":
    asyncio.run(main())