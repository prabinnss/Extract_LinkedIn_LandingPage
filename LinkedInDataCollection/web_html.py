import asyncio
import os

import pandas as pd
import asyncio
from time import sleep
from playwright.async_api import async_playwright

async def save_page_as_html(page, url, file_path):
    try:
        print(f"Opening URL: {url}")
        await page.goto(url, timeout=90000)  # Increase timeout to 90 seconds
        # Wait for the main content to be loaded by waiting for a key element
        sleep(10)
        await page.wait_for_selector('body', timeout=90000)  # Adjust the selector as needed
        html_content = await page.content()
        # Save the page content to a file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Saved {url} as {file_path}")
    except Exception as e:
        print(f"Failed to open {url}: {e}")
        sleep(10)
        # await page.wait_for_selector('body', timeout=90000)  # Adjust the selector as needed
        html_content = await page.content()
        # Save the page content to a file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Saved {url} as {file_path}")

async def main(csv_file):
    df = pd.read_csv(csv_file)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Enable headless=False for debugging
        page = await browser.new_page()

        # Open LinkedIn login page manually
        login_url = "https://www.linkedin.com/login"
        print(f"Opening LinkedIn login page for manual interaction: {login_url}")
        await page.goto(login_url, timeout=90000)  # Increase timeout to 90 seconds

        print("Please log in and press Enter to continue...")
        input()

        # # Now navigate to the first URL after login
        # first_cpaid = df.iloc[0]['license_no']
        # first_url = df.iloc[0]['linkedinwebsite']
        # first_file_path = f"output/linkedInprofiles/saved_page_1_{first_cpaid}.html"
        # await save_page_as_html(page, first_url, first_file_path)

        print("Please type 'gonext' and press Enter to continue...")
        input()

        ct=0
        # Process the rest of the URLs
        for index in range(0, len(df)):
            cpaid = df.iloc[index]['license_no']
            url = df.iloc[index]['linkedinwebsite']
            file_path = f"output/linkedInprofiles/saved_page_{cpaid}.html"
            isFileExist = os.path.exists(file_path)
            if isFileExist:
                print("skipped, file retrieved already.")
                continue

            await save_page_as_html(page, url, file_path)
            ct=ct+1
            if ct>500:
                # break
                sleep(3600)
                ct=0
                continue
            sleep(60)  # Wait for some seconds before processing the next URL

        # Wait for user input before closing the browser
        print("Type 'done' to close the browser:")
        while True:
            user_input = input()
            if user_input.lower() == 'done':
                break

        await browser.close()

# Example usage
asyncio.run(main('urls_clean_to_be_done.csv.csv'))



# url="https://www.linkedin.com/in/carmen-hambrick-mba-cpa/"