import os
import uuid
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

download_folder = os.path.join(os.path.expanduser("~"), "downloads")
os.makedirs(download_folder, exist_ok=True)

def download_media(media_url, ext):
    filename = f"photo_{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(download_folder, filename)
    try:
        with requests.get(media_url, stream=True, timeout=15) as media_response:
            media_response.raise_for_status()
            with open(filepath, "wb") as f:
                for chunk in media_response.iter_content(1024):
                    f.write(chunk)
        return filepath
    except Exception as e:
        print(f"[Error while saving media] {e}")
        return None

def download_photo(post_url, username=None, password=None):
    # First attempt: requests + BeautifulSoup
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(post_url, headers=headers, timeout=10)
        if res.ok:
            soup = BeautifulSoup(res.text, "html.parser")
            tag = soup.find("meta", property="og:video") or soup.find("meta", property="og:image")
            if tag and tag.get("content"):
                media_url = tag["content"]
                ext = "mp4" if "video" in media_url else "jpg"
                path = download_media(media_url, ext)
                if path:
                    print("Downloaded with requests")
                    return path
    except Exception as e:
        print(f"[Requests failed] {e}")

    # Fallback: Selenium only if absolutely needed
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.binary_location = "/usr/bin/chromium"
        
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 10)

        driver.get("https://www.instagram.com/accounts/login/")
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
        wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()

        time.sleep(5)  # keep this minimal
        driver.get(post_url)
        time.sleep(4)

        media_element = driver.find_element(By.XPATH, "//video | //img")
        media_url = media_element.get_attribute("src")
        ext = "mp4" if "video" in media_url else "jpg"
        filepath = download_media(media_url, ext)

        print("Downloaded with Selenium")
        return filepath
    except (TimeoutException, WebDriverException) as e:
        print(f"[Selenium failed] {e}")
        return None
    finally:
        try:
            driver.quit()
        except:
            pass
