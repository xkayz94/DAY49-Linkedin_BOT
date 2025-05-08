from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import os
from dotenv import load_dotenv

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get(
    "https://www.linkedin.com/jobs/search/?currentJobId=4197024817&f_AL=true&geoId=90009496&keywords=Python%20Developer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R")
actions = ActionChains(driver)


# Maximize window if needed
# driver.maximize_window()

def close_btn():
    dismiss_button = driver.find_element(By.CSS_SELECTOR, 'button[data-test-modal-close-btn]')
    dismiss_button.click()


time.sleep(4)
login = driver.find_element(By.CSS_SELECTOR, '[data-modal=base-sign-in-modal]')
login.click()

e_mail = driver.find_element(By.ID, "base-sign-in-modal_session_key")
e_mail.click()
e_mail.send_keys(os.environ['LINKEDIN_USERNAME'])

password = driver.find_element(By.ID, "base-sign-in-modal_session_password")
password.click()
password.send_keys(os.environ['LINKEDIN_PASSWORD'], Keys.ENTER)

# If Captcha
input("Press Enter when you have solved the Captcha")

# For every div in job list (why shows only 7, randomly css structure?) left window
time.sleep(4)
listing = driver.find_elements(By.CSS_SELECTOR, "li.scaffold-layout__list-item")
print(len(listing))

for job_offer in listing:

    time.sleep(2)
    job_offer.click()
    apply_btn = driver.find_element(By.CSS_SELECTOR, '.jobs-apply-button')
    apply_btn.click()
    time.sleep(2)

    # Dismiss job offer with next steps needed
    # next_step = driver.find_element(By.CSS_SELECTOR, value='span[artdeco-button__text]')
    # ActionChains(driver).scroll_to_element(next_step).perform()
    next_step = driver.find_element(By.CSS_SELECTOR, 'button.artdeco-button--primary[aria-label]')

    # Pobierz wartość atrybutu aria-label
    button_label = next_step.get_attribute('aria-label')
    try:
        if button_label == 'Submit application':
            print('apply')  # tried for test if implement but no result
            phone_number = driver.find_element(By.CSS_SELECTOR, value='input[id*="phoneNumber-nationalNumber"]')
            phone_number.clear()
            phone_number.send_keys('765321433')
            next_step.click()
            time.sleep(1)

            close_btn()
            continue



        # close if needed else steps
        elif button_label == 'Continue to next step':
            close_btn()
            discard_button = driver.find_element(By.CSS_SELECTOR,
                                                 'button[data-control-name="discard_application_confirm_btn"]')
            discard_button.click()
            # close job card from left window
            close_left_btn = driver.find_element(By.CSS_SELECTOR, value='div button.job-card-container__action')
            close_left_btn.click()
            # continue
            # Else should navigate phone number input if above code didn't execute
            time.sleep(2)
            continue

    except NoSuchElementException:
        print('you have applied')
        close_left_btn = driver.find_element(By.CSS_SELECTOR, value='div button.job-card-container__action')
        close_left_btn.click()
        # continue
        # Else should navigate phone number input if above code didn't execute
        time.sleep(2)
        continue


driver.quit()










