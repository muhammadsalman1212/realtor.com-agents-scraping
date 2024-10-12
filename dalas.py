import csv
import time
from playwright.sync_api import sync_playwright

# Proxy details
for i in range(182, 242):

    proxy = {
        'server': 'http://p.webshare.io:80',
        'username': 'rsghfdon-rotate',
        'password': 'r34zy54pcli3'
    }

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(proxy=proxy, headless=False)  # Launch browser with proxy
            page = browser.new_page()

            # Block images to save data
            def block_images(route):
                if route.request.resource_type == "image":
                    route.abort()  # Block image requests
                else:
                    route.continue_()  # Allow other requests

            # Intercept all network requests to block images
            page.route("**/*", block_images)

            print(f"Scraping page no {i}")

            # Open website with browser
            page.goto(f"https://www.realtor.com/realestateagents/fort-worth-avenue_dallas_tx/rep-seller/photo-1/pg-{i}", timeout=0)

            # Give the page some time to load
            time.sleep(5)

            # Get all agents on the page
            agent_cards = page.query_selector_all('//div[@data-testid="component-agentCard"]')

            agents = []

            for card in agent_cards:
                # Extract agent name
                name_element = card.query_selector(
                    '.jsx-3873707352.agent-list-card-title-text.clearfix a[aria-label="link name"] .jsx-3873707352 span'
                )
                name = name_element.inner_text() if name_element else "Not Found"

                # Extract company name
                company_element = card.query_selector(
                    '.jsx-3873707352.agent-group .base__StyledType-rui__sc-108xfm0-0'
                )
                company = company_element.inner_text() if company_element else "Not Found"

                # Extract phone number
                phone_element = card.query_selector(
                    '.jsx-3873707352.office-details-section .phone-icon .agent-phone'
                )
                phone = phone_element.inner_text() if phone_element else "Not Found"

                # Ensure that if the name or company is not found, we still check for the phone number
                if name == "Not Found" or company == "Not Found":
                    phone = "Not Found" if phone == "Not Found" else phone

                # Append to agents list
                agents.append({
                    "name": name,
                    "phone": phone,
                    "company": company
                })

            # Print and save the results
            for agent in agents:
                print(f"Agent Name: {agent['name']}")
                print(f"Phone Number: {agent['phone']}")
                print(f"Company Name: {agent['company']}")
                print('-' * 30)

                # Save agent data to the CSV file inside the loop
                header = ['Agent Name', 'Phone Number', 'Company Name', 'City']
                with open('Dallas-FortWorth.csv', 'a+', encoding='utf-8', newline='') as file:
                    writer = csv.writer(file)
                    if file.tell() == 0:  # Check if file is empty and write header
                        writer.writerow(header)
                    writer.writerow([agent['name'], agent['phone'], agent['company'], 'Dallas-Fort Worth'])

            # Close browser after scraping the page
            browser.close()

    except Exception as e:
        print(f"Skipped page no {i} due to error: {e}")
