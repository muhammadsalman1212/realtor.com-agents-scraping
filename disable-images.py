import time

from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Headless mode enabled
        page = browser.new_page()

        # Request interception to block images
        def block_images(route):
            if route.request.resource_type == "image":
                route.abort()  # Block image requests
            else:
                route.continue_()  # Allow other requests

        page.route("**/*", block_images)  # Intercept all network requests

        # Navigate to the desired page
        page.goto("http://github.com/")

        print(page.title())  # Output the page title to verify it loaded

        time.sleep(4334)
run()
