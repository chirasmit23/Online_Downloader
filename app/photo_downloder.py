import os
import uuid
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
os.makedirs(download_folder, exist_ok=True)
def download_photo(post_url, username, password):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(post_url, headers=headers, timeout=10)
        if response.ok:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")
            tag = soup.find("meta", property="og:video") or soup.find("meta", property="og:image")
            if tag and tag.get("content"):
                media_url = tag["content"]
                ext = "mp4" if "video" in media_url else "jpg"
                filename = f"photo_{uuid.uuid4().hex}.{ext}"
                filepath = os.path.join(download_folder, filename)
                media_response = requests.get(media_url, stream=True)
                with open(filepath, "wb") as f:
                    for chunk in media_response.iter_content(1024):
                        f.write(chunk)
                print("downloaded with requests")
                return filepath
    except Exception as e:
        print(f"[Requests download failed] {e}")
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.binary_location = "/usr/bin/chromium"
        driver = webdriver.Chrome(
            service=Service("/usr/bin/chromedriver"),
            options=chrome_options
        )
        driver.get("https://www.instagram.com/accounts/login/")
        WebDriverWait(driver, 12).until(
            EC.presence_of_element_located((By.NAME, "username"))
        ).send_keys(username)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        ).send_keys(password)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
        ).click()
        time.sleep(8)
        driver.get(post_url)
        time.sleep(8)
        media_element = driver.find_element(By.XPATH, "//video | //img")
        media_url = media_element.get_attribute("src")
        ext = "mp4" if "video" in media_url else "jpg"
        filename = f"photo_{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(download_folder, filename)
        media_response = requests.get(media_url, stream=True)
        with open(filepath, "wb") as f:
            for chunk in media_response.iter_content(1024):
                f.write(chunk)
        print("Downloaded with selenium")
        return filepath
    except Exception as e:
        print(f"selenium download failed {e}")
        return None
    finally:
        try:
            driver.quit()
        except:
            pass
