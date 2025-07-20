import random
import undetected_chromedriver as uc
# from selenium import webdriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up the Chrome options and driver


def solve_hcaptcha():
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)
    driver.set_window_size(300, 600)
    options.add_argument("--log-level=3")

    try:
        driver.get("https://suno.com")

        # Wait for the 'h-captcha-response' element to appear
        print("solving captcha..2")
        captcha_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@name="h-captcha-response"]'))
        )

        # Get the ID attribute of the captcha field
        captcha_id = captcha_field.get_attribute("id")

        # Split the ID to extract the dynamic part (after the '-')
        captcha_id_dynamic = captcha_id.split('-')[-1].strip()

        # Execute hcaptcha functions
        script_1 = f'hcaptcha.execute("{captcha_id_dynamic}");'

        # Execute the script to trigger the captcha challenge
        time.sleep(2)
        driver.execute_script(script_1)
        time.sleep(2)

        # Loop until the CAPTCHA token is available
        # print(captcha_id_dynamic)
        notToken = True
        while notToken:
            iframe = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//iframe[contains(@src, "hcaptcha")]')
                )
            )

            # Check if the iframe has the 'data-hcaptcha-response' attribute
            hcaptcha_response = iframe.get_attribute(
                "data-hcaptcha-response")
            if hcaptcha_response:
                notToken = False
                driver.close()
            time.sleep(2)
        print({'id_captcha': captcha_id_dynamic, 'token': hcaptcha_response})
        return hcaptcha_response

    except Exception as e:
        print("Something went wrong with the driver:", str(e))
