import time

import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
driver.get("https://www.bbc.com/")

time.sleep(2)

# BBC
bbc_headlines = driver.find_elements(By.CLASS_NAME, 'media__link')

bbc_headlines_dict = {}

for headline in bbc_headlines:
    bbc_headlines_dict[headline.text] = headline.get_attribute("href")

for headline, href in bbc_headlines_dict.items():
    print(f"Headline: {headline}\nHref: {href}\n")

# CNN
driver.get("https://edition.cnn.com/")

cnn_headlines = driver.find_elements(By.CSS_SELECTOR, 'a.container__link[data-link-type="article"]')

cnn_headlines_dict = {}

for element in cnn_headlines:
    try:
        headline_element = element.find_element(By.CSS_SELECTOR, 'span[data-editable="headline"]')
        headline = headline_element.text.strip()

        if headline and "VIDEO" not in headline and "GALLERY" not in headline and "[Gallery]" not in headline:
            href = element.get_attribute("href")
            cnn_headlines_dict[headline] = href
    except:
        pass  # Skip elements without a headline

for headline, href in cnn_headlines_dict.items():
    print(f"Headline: {headline}\nHref: {href}\n")

# FOX
driver.get("https://www.foxnews.com/")
fox_headlines = driver.find_elements(By.CSS_SELECTOR, 'a[data-omtr-intcmp*="fnhpbt"]')

fox_headlines_dict = {}

for element in fox_headlines:
    text = element.text
    href = element.get_attribute("href")

    if text:
        fox_headlines_dict[text] = href

for text, href in fox_headlines_dict.items():
    print(f"Text: {text}\nHref: {href}\n")

driver.quit()

headless_options = Options()
headless_options.add_argument("--headless")
headless_driver = webdriver.Chrome(options=headless_options)

bbc_articles = {}

for headline, link in bbc_headlines_dict.items():
    headless_driver.get(link)

    time.sleep(5)

    paragraphs = headless_driver.find_elements(By.TAG_NAME, "p")
    paragraphs_text = [paragraph.text.strip() for paragraph in paragraphs if paragraph.text.strip()]

    bbc_articles[headline] = paragraphs_text

for headline, text in bbc_articles.items():
    print(f"Headline: {headline}\nText: {text}")