from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ヘッドレスモードの設定
options = Options()
options.add_argument('--headless')
options.add_argument("--no-sandbox")

executable_path = '/usr/bin/chromedriver'

def test():
  with webdriver.Chrome(executable_path=executable_path, options=options) as driver:
    driver.get("https://www.google.com/")
    print(driver.window_handles)
    driver.execute_script("window.open()") 
    print(driver.window_handles)
test()
