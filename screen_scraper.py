import os
from selenium import webdriver

# get variables from env file
USERNAME = os.getenv("WIFI_USERNAME")
PASSWORD = os.getenv("WIFI_PASSWORD")
ADDRESS = os.getenv("WIFI_ADDRESS")

# create driver
driver = webdriver.Chrome()
driver.get(ADDRESS)

# login
username_el = driver.find_elements_by_name("loginUsername")
password_el = driver.find_elements_by_name("loginText")

username_el.send_keys(USERNAME)
password_el.send_keys(PASSWORD)

sumbit_el = driver.find_elements_by_id("btn")
sumbit_el.click()

# click on wifi tab
wifi_el = driver.find_elements_by_id("wire_a")
wifi_el.click()

# enter new password in password boxes
password_boxes = [driver.find_elements_by_name(
    "w10WpaPsk"), driver.find_elements_by_name("w11WpaPsk")]
for password_box in password_boxes:
    password_box.send_keys("PO13PLEP3333PLe")
    # click save
save_buttons = driver.find_elements_by_class_name("moto-change-button")
for button in save_buttons:
    button.click()
