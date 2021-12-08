import os
import click
import time
import selenium.webdriver as webdriver

from selenium.common.exceptions import NoSuchElementException
from slacker import post_message

def wait_seconds(seconds=10.0):
    print('\tWaiting {}s...'.format(seconds))
    while seconds > 0:
        seconds -= 1
        time.sleep(1.0)
        print('\tWaiting {}s...'.format(seconds))

def check_if_logo_has_loaded(driver, timeout=10.0):
    time_elapsed = 0.0
    while time_elapsed < timeout:
        try:
            logo_elem = driver.find_element_by_id('logo')
            if logo_elem.text == 'APPLY FOR A U.S. VISA':
                return True
        except NoSuchElementException:
            wait_seconds(1.0)
            time_elapsed += 1.0
    return False

def login_if_required(driver, username=None, password=None, timeout=1.0):
    try:
        logo_elem = driver.find_element_by_class_name('loginPanel')
        login_username = driver.find_element_by_id('loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:username')
        login_username.send_keys(username)

        login_pwd = driver.find_element_by_id('loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:password')
        login_pwd.send_keys(password)

        tnc_checkbox = driver.find_element_by_name('loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:j_id167')
        tnc_checkbox.click()

        input("Press Enter to continue...")

        login_button = driver.find_element_by_id('loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:loginButton')
        login_button.click()
        wait_seconds(1.0)
    except NoSuchElementException:
        print('Maybe already logged in?')

    continue_link = None
    te = 0.0
    while te < timeout:
        try:
            continue_link = driver.find_element_by_link_text("Continue")
            break
        except NoSuchElementException:
            wait_seconds(1.0)
            te += 1.0

    if continue_link:
        continue_link.click()
    else:
        print('Already clicked Continue')
        # raise Exception("Continue link not found")

    wait_seconds(1.0)
    confirm_button = None
    te = 0.0
    while te < timeout:
        try:
            confirm_button = driver.find_element_by_class_name("ui-dialog-buttonset")
            break
        except NoSuchElementException:
            wait_seconds(1.0)
            te += 1.0

    if confirm_button:
        confirm_button.click()
        wait_seconds(1.0)
    else:
        print('Already confirmed?')
        # raise Exception("Confirm button not found")


    continue_button = None
    te = 0.0
    while te < timeout:
        try:
            continue_button = driver.find_element_by_id('j_id0:SiteTemplate:theForm:continue_btn')
            break
        except NoSuchElementException:
            wait_seconds(1.0)
            te += 1.0

    if continue_button:
        continue_button.click()
        wait_seconds(2.0)
    else:
        print('Already on Scheduling page?')
        # raise Exception("Continue button not found")

    dashboard = None
    te = 0.0
    while te < timeout:
        try:
            dashboard = driver.find_element_by_id("dashboard")
            if dashboard:
                return dashboard.text
        except NoSuchElementException:
            wait_seconds(1.0)
            te += 1.0

    raise Exception('Dashboard not found.')

@click.command()
@click.option('--site-url', help="Url to navigate to")
@click.option('--username', help="Username")
@click.option('--pwd', help="Password")
@click.option('--search-text', help="Text to search for on the dashboard")
@click.option('--refresh-interval', type=float, default=10.0, help="Wait time before refresh")
def start(site_url, username, pwd, search_text, refresh_interval):
    print(site_url)
    driver = webdriver.Chrome()
    driver.get(site_url)

    if not check_if_logo_has_loaded(driver):
        print("Page didn't load successfully.")

    dashboard_text = login_if_required(driver, username=username, password=pwd)

    while search_text in dashboard_text:
        dashboard_text = login_if_required(driver, username=username, password=pwd)

        wait_seconds(refresh_interval)
        driver.refresh()

    print('Something!!!!')

    te = 0.0
    while te < 5.0:
        post_message('Something!!!!')
        wait_seconds(1.0)
        te += 1.0

    import pdb; pdb.set_trace()
    #driver.close()
if __name__ == '__main__':
    start()
