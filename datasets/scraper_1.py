import os
import re
from datetime import datetime
from playwright.sync_api import sync_playwright

def sanitize_filename(text):
    return re.sub(r'[^a-zA-Z0-9_\-]', '', text.replace(" ", "_"))

def download_csv_from_section(page, link_text):
    print(f"\n📥 Downloading: {link_text}")
    
    # Click the desired section link
    page.wait_for_selector(f"a:has-text('{link_text}')")
    page.click(f"a:has-text('{link_text}')")

    page.wait_for_load_state("networkidle")

    page.wait_for_selector("button:has-text('Actions')")
    page.click("button:has-text('Actions')")

    page.wait_for_selector("text=Download")
    page.click("text=Download")

    with page.expect_download() as download_info:
        page.wait_for_selector("text=CSV")
        page.click("text=CSV", no_wait_after=True)
    download = download_info.value

    # Create date-stamped filename
    date_str = datetime.now().strftime("%Y-%m-%d")
    clean_filename = f"{sanitize_filename(link_text)}_{date_str}.csv"
    save_path = os.path.join(os.getcwd(), clean_filename)
    download.save_as(save_path)
    print(f"✅ Saved to: {save_path}")

    # Return to homepage
    page.goto('https://efile.fara.gov/ords/fara/f?p=1381:1')
    page.wait_for_selector("a:has-text('Active Registrants')")

with sync_playwright() as p:
    browser = p.chromium.launch()  # headless by default now
    context = browser.new_context(accept_downloads=True)

    context.set_default_timeout(0)
    page = context.new_page()
    page.set_default_timeout(0)

    page.goto('https://efile.fara.gov/ords/fara/f?p=1381:1')
    page.wait_for_selector("a:has-text('Active Registrants')")

    sections = [
        "Active Registrants",
        "Active Registrants by Country or Location Represented",
        "Historical List of All Registrants (Active and Terminated)",
        "Historical List of All Registrants by Country or Location Represented (Active and Terminated)",
        "Active Registrants with Political Contributions",
        "Active Registrants with Political Activities",
        "Terminated Short Form Registrants",
        "Historical List of All Short Form Registrants (Active and Terminated)",
        "Active Short Form Registrants with Political Contributions",
        "Active Foreign Principals",
        "Active Foreign Principals in a Date Range",
        "New Foreign Principals in a Date Range",
        "Terminated Foreign Principals",
        "Terminated Foreign Principals in a Date Range",
        "Historical List of All Foreign Principals (Active and Terminated)"
    ]

    for section in sections:
        try:
            download_csv_from_section(page, section)
        except Exception as e:
            print(f"❌ Failed to download '{section}': {e}")

    browser.close()