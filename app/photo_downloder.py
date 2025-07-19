import os, uuid, time, requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
os.makedirs(download_folder, exist_ok=True)
def download_photo(post_url, username, password):
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
    try:
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
        if "video" in media_url:
            filename = f"photo_{uuid.uuid4().hex}.mp4"
        else:
            filename = f"photo_{uuid.uuid4().hex}.jpg"
        filepath = os.path.join(download_folder, filename)
        response = requests.get(media_url, stream=True)
        with open(filepath, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return filepath
    except Exception as e:
        print(f"Download Error: {e}")
        return None
    finally:
        driver.quit()
