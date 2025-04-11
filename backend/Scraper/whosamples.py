from playwright.sync_api import sync_playwright

url = "https://www.whosampled.com/sample/1023/MF-DOOM-Rhymes-Like-Dimes-Quincy-Jones-James-Ingram-One-Hundred-Ways/"

def save_html_snapshot(url, filename="whosampled_snapshot.html"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_load_state("networkidle")
        html = page.content()
        browser.close()

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Snapshot saved to {filename}")

if __name__ == "__main__":
    save_html_snapshot(url)