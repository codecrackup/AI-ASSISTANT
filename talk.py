from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import os
import chat

# Path to your HTML file
html_file = os.path.abspath("talk.html")

# Setup Chrome options for fake media (optional)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])

# Launch browser
def speech():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("file://" + html_file)
    sleep(2)

    # Continuous speech reading loop
    print("Assistant is listening...")
    last_text = ""

    try:
        while 1:        
            text = driver.find_element(By.ID, "output").text.strip()
            if text and text != last_text and text.lower() != "say something...":
                print(f"You said: {text}")
                last_text = text
                chat.chat_func(last_text)
            sleep(0.5)

    except KeyboardInterrupt:
        print("Stopping...")
        driver.quit()


speech()