from playwright.sync_api import sync_playwright
import pandas as pd
def accept_cookies(page):
    #page.wait_for_timeout(5000)
    print("[PROGRAM : accepting cookies ...]")
    texts = ["Tout accepter", "Accepter tout", "J'accepte"]
    for text in texts:
        btn = page.locator(f'button:has-text("{text}")').first
        if btn.count():
            print(f"[PROGRAM : btw.count = {btn.count()}]")
            try:
                print(f"[PROGRAM : {text} button clicked]")
                btn.click(timeout=3000)
                return
            except Exception:
                print("[PROGRAM : button wasn't clicked]")
                pass

def collect_items(page = None,visible_selector=None,wait_threshold = 3,max_scrolls=200):
    seen_hrefs = set()
    prev_seens = 0
    wait = 0
    output_items = []
    for _ in range(max_scrolls):
        batch_items = page.locator(visible_selector).evaluate_all("""
                els => els.map(e => ({
                href: e.href || e.getAttribute('href') || '',
                title: (e.getAttribute('title') || e.textContent || '').trim()
                }))
            """)
        for item in batch_items :
            item_href = item.get("href") or ""
            if item_href not in seen_hrefs :
                seen_hrefs.add(item_href)
                output_items.append(item)
        if len(seen_hrefs) == prev_seens :
            wait += 1
            if wait >= wait_threshold :
                break
        else :
            wait = 0
        prev_seens = len(seen_hrefs)
        page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)
    return output_items


def scrape_page(url : str = None,selector : str = None):
    if not url or not selector:
        raise ValueError("URL and SELECTOR must be provided.")
    with sync_playwright() as p:
        # Open a controllable Chromium instance in headless mode
        context = p.chromium.launch_persistent_context(
            user_data_dir="user-data-seloger",     # new folder
            channel="chrome",
            headless=True,                        # start headed for diagnosis
            viewport={"width": 1366, "height": 900},
            locale="fr-FR",
            timezone_id="Europe/Paris",
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-first-run",
                "--no-default-browser-check",
            ],
        )
        context.add_init_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        
        try :
            print("[PROGRAM : page wait for selector(s) ...]")
            page.wait_for_selector(selector, state="attached", timeout=15000)
            print("[PROGRAM : selector(s) found]")
            print("[PROGRAM : triggering lazy load ...]")
            page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            page.wait_for_timeout(500)
            print("[PROGRAM : done lazy load triggering]")
            accept_cookies(page)
            items_found = collect_items(page=page,visible_selector=f'{selector}:visible')
            print(f"{len(items_found)} item(s) found at url : {url}")
            #print("first item values : ",list(cards[0].values) if cards else [])
        except Exception:
            print(f"[PROGRAM : No item found at url : {url}]")
            context.close()
            return None
        """
        for i,item in enumerate(items_found) :
            if i+1 == len(items_found):
                print(item["title"])
        """
        #print("cookies accepted ?")
        #page.wait_for_timeout(2000)
        #page.screenshot(path="seloger_open_page2.png", full_page=True)
        context.close()
        return items_found
def scrape_pages(nb_pages : int = 1,url : str = None,selector : str = None):
    properties = []
    for i in range(nb_pages):
        properties_per_page = scrape_page(url=url+str(i+1),selector=selector)
        if properties_per_page :
            properties.extend(properties_per_page)
        else :
            return properties
    return properties

if __name__ == "__main__":
    TESTID = 'card-mfe-covering-link-testid'
    selector = f'[data-testid="{TESTID}"]' 
    url = "https://www.seloger.com/classified-search?distributionTypes=Buy&locations=AD08FR31096&page="
    properties = scrape_pages(nb_pages=10,url = url,selector=selector)
    #properties = scrape_page(url=url+"1",selector=selector)
    df_properties = pd.DataFrame(properties)
    # CSV
    df_properties.to_csv("seloger_properties_paris_size10.csv", index=False, encoding="utf-8")

    # JSON (records = one object per row)
    df_properties.to_json("seloger_properties_paris_size10.json", orient="records", force_ascii=False, indent=2)

    #print(df_properties["title"])
