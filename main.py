from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pymongo import MongoClient
import uuid
import socket
from datetime import datetime
import time

client = MongoClient("mongodb://localhost:27017/")  
db = client["twitter_data"]
collection = db["trending_topics"]

proxy_username = "yuvii_077"
proxy_password = "aaaaaaaa"
proxy_url = f"http://{proxy_username}:{proxy_password}@uk.proxymesh.com:31280"

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)

driver = webdriver.Chrome(options=options)
try:
    driver.get("https://twitter.com/login")
    wait = WebDriverWait(driver, 20)

    username_field = wait.until(EC.presence_of_element_located((By.NAME, "text")))
    username_field.send_keys("dummy134550")  
    next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
    next_button.click()

    time.sleep(2)
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_field.send_keys("RAMAN@200")  
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Log in']")))
    login_button.click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href='/home']")))
    print("Logged in successfully.")

    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    trends = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//div[@aria-label='Timeline: Trending now']//div[@data-testid='trend']//span"
         )
    ))
    print(f"Found {len(trends)} trending items:")

    unique_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_address = socket.gethostbyname(socket.gethostname())

    trending_data = {
        "unique_id": unique_id,
        "date_time": timestamp,
        "ip_address": ip_address,
        "trends": []
    }

    for index, trend in enumerate(trends[:5], start=1):
        try:
            text = trend.text.strip()
            print(f"{index}. {text}")
            trending_data["trends"].append({"rank": index, "topic": text})
    
            
        except Exception as e:
            print(f"Error reading trend #{index}: {e}")

    if trending_data["trends"]:
        collection.insert_one(trending_data)
        print("Trending data successfully stored in MongoDB:", trending_data)
        
        

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
    
    
    
    
    
    
    
    
    
    
    
    
