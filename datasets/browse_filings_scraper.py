import os
import re
from datetime import datetime
from playwright.sync_api import sync_playwright

def sanitize_filename(text):
    return re.sub(r'[^a-zA-Z0-9_\-]', '', text.replace(" ", "_"))

def save_download(download, label):
    # Ensure datasets directory exists
    datasets_dir = os.path.join(os.getcwd(), "datasets")
    os.makedirs(datasets_dir, exist_ok=True)

    # Save with date-stamped filename
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{sanitize_filename(label)}_{date_str}.csv"
    save_path = os.path.join(datasets_dir, filename)
    download.save_as(save_path)
    print(f"✅ Saved to: {save_path}")

# STEP 1: Static Section Downloads
def download_csv_from_section(page, link_text):
    print(f"\n📥 Downloading static section: {link_text}")

    page.wait_for_selector(f"a:has-text('{link_text}')", timeout=120000)
    page.click(f"a:has-text('{link_text}')")
    page.wait_for_load_state("networkidle", timeout=120000)

    page.wait_for_selector("button:has-text('Actions')", timeout=120000)
    page.click("button:has-text('Actions')")

    page.wait_for_selector("text=Download", timeout=120000)
    page.click("text=Download")

    with page.expect_download(timeout=120000) as download_info:
        page.wait_for_selector("text=CSV", timeout=120000)
        page.click("text=CSV", no_wait_after=True)
    download = download_info.value

    save_download(download, link_text)

    # Return to homepage
    page.goto('https://efile.fara.gov/ords/fara/f?p=1381:1', timeout=120000)
    page.wait_for_selector("a:has-text('Active Registrants')", timeout=120000)

# STEP 2: Date-Range Section Downloads
fromdate_fields = {
    "Active Registrants in a Date Range": "P140_FROMDATE",
    "Active Registrants by Country or Location in a Date Range": "P11_FROMDATE",
    "Registrant Supplemental Statements by Country or Location in a Date Range": "P25_FROMDATE",
    "New Registrants in a Date Range": "P6_FROMDATE",
    "Terminated Registrants in a Date Range": "P7_FROMDATE",
    "Active Short Form Registrants in a Date Range": "P142_FROMDATE",
    "New Short Form Registrants in a Date Range": "P124_FROMDATE",
    "Terminated Short Form Registrants in a Date Range": "P126_FROMDATE",
    "Active Foreign Principals in a Date Range": "P130_FROMDATE",
    "New Foreign Principals in a Date Range": "P132_FROMDATE",
    "Terminated Foreign Principals in a Date Range": "P138_FROMDATE"
}

def process_date_range_section(page, section_name):
    print(f"\n📥 Downloading date-range section: {section_name}")

    page.goto("https://efile.fara.gov/ords/fara/f?p=1381:1", timeout=120000)
    page.wait_for_selector(f"a:has-text('{section_name}')", timeout=120000)
    page.click(f"a:has-text('{section_name}')")
    page.wait_for_load_state("networkidle", timeout=120000)

    fromdate_field = fromdate_fields.get(section_name)
    if not fromdate_field:
        raise Exception(f"No FROMDATE mapping found for: {section_name}")

    page.wait_for_selector(f"input[name='{fromdate_field}']", timeout=120000)
    page.fill(f"input[name='{fromdate_field}']", "01/01/1900")

    page.click("button:has-text('Go')")
    page.wait_for_load_state("networkidle", timeout=120000)

    page.wait_for_selector("button:has-text('Actions')", timeout=120000)
    page.click("button:has-text('Actions')")

    page.wait_for_selector("text=Download", timeout=120000)
    page.click("text=Download")

    with page.expect_download(timeout=120000) as download_info:
        page.wait_for_selector("text=CSV", timeout=120000)
        page.click("text=CSV", no_wait_after=True)
    download = download_info.value

    save_download(download, section_name)

# MAIN FLOW
with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()

    # Set default timeout to 2 minutes
    page.set_default_timeout(120000)

    # --- Step 1: Static Sections ---
    static_sections = [
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

    print("\n🟢 STEP 1: Downloading static sections...")
    page.goto("https://efile.fara.gov/ords/fara/f?p=1381:1", timeout=120000)
    page.wait_for_selector("a:has-text('Active Registrants')", timeout=120000)

    for section in static_sections:
        try:
            download_csv_from_section(page, section)
        except Exception as e:
            print(f"❌ Failed to download '{section}': {e}")

    # --- Step 2: Date-Range Sections ---
    print("\n🟢 STEP 2: Downloading date-range sections...")
    for section in fromdate_fields.keys():
        try:
            process_date_range_section(page, section)
        except Exception as e:
            print(f"❌ Failed to process '{section}': {e}")

    browser.close()
