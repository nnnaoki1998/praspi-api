from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# ヘッドレスモードの設定
options = Options()
options.add_argument('--headless')
options.add_argument("--no-sandbox")

executable_path = '/usr/bin/chromedriver'

def login(driver, customer_id, login_id, password):
  driver.get("https://www.e4628.jp/")
  driver.find_element(By.ID, "y_companycd").send_keys(customer_id) # お客様ID
  driver.find_element(By.ID, "y_logincd").send_keys(login_id)  # ログインID
  driver.find_element(By.ID, "password").send_keys(password) # パスワード
  driver.find_element(By.ID, "id_passlogin").submit()

def logout(driver):
  driver.find_element(By.CSS_SELECTOR, "img[onclick = \"javascript:document.getElementById('logout_form').submit();\"]").click()
  driver.quit()

def punchin(customer_id, login_id, password):
  with webdriver.Chrome(executable_path=executable_path, options=options) as driver:
    login(driver, customer_id, login_id, password)
    try:
      driver.find_element(By.CSS_SELECTOR, "button[onclick = \"javascript:return(trDoStamping(1));\"]").click()
      is_success_punchin = True
    except:
      is_success_punchin = False
    logout(driver)
    return is_success_punchin

def punchout(customer_id, login_id, password):
  with webdriver.Chrome(executable_path=executable_path, options=options) as driver:
    login(driver, customer_id, login_id, password)
    try:
      driver.find_element(By.CSS_SELECTOR, "button[onclick = \"javascript:return(trDoStamping(2));\"]").click()
      is_success_punchout = True
    except:
      is_success_punchout = False
    logout(driver)
    return is_success_punchout
