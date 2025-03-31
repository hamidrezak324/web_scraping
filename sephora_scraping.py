from playwright.sync_api import sync_playwright
import pandas as pd

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.sephora.com/shop/luminizer-luminous-makeup")
    page.wait_for_timeout(5000)

    input("پاپ‌آپ‌ها رو دستی ببند و Enter بزن...")

    # Click Load More
    load_more_locator = page.locator("//button[contains(., 'Load More')] | //button[contains(., 'Show More')]")
    while load_more_locator.count() > 0:
        try:
            load_more_locator.first.click()
            print("دکمه Load More کلیک شد!")
            page.wait_for_timeout(5000)
        except Exception as e:
            print(f"خطا در کلیک Load More: {e}")
            break

    # Scrolling
    scroll_position = 0
    while True:
        scroll_position += 1000
        page.evaluate(f"window.scrollTo(0, {scroll_position})")
        page.wait_for_timeout(3000)
        total_height = page.evaluate("document.body.scrollHeight")
        if scroll_position >= total_height:
            print("اسکرول به آخر رسید!")
            break

    # Extract products
    tiles = page.locator(".ProductTile-content").all()
    print(f"تعداد محصولات پیدا شده: {len(tiles)}")

    products = []
    for tile in tiles:
        try:
            brand = tile.locator("span.css-1e2863e").inner_text()
            name = tile.locator("span.css-1ma869u").inner_text()
            products.append({"brand": brand, "product_name": name})
            print(f"برند: {brand} - محصول: {name}")
        except Exception as e:
            print(f"خطا در استخراج: {e}")

    # Save CSV format
    if products:
        df = pd.DataFrame(products)
        df.to_csv("set.csv", index=False, encoding="utf-8")
        print("داده‌ها با موفقیت در فایل set.csv ذخیره شدند!")
    else:
        print("هیچ داده‌ای برای ذخیره وجود نداشت.")

    browser.close()