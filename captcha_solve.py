from twocaptcha import TwoCaptcha
from credentials import *

site_key = SITE_KEY
page_url = SITE_URL
api_key = TOKEN_KEY_2captcha


def hcaptcha_solve(api_key, site_url, site_key):

    solver = TwoCaptcha(api_key)
    try:
        print("Solving hcaptcha ...")
        result = solver.hcaptcha(sitekey=site_key, url=site_url, invisible=1)
        print(result)
        data = result
        token = result['code']
        print("hCaptcha solved! Token:", token)
        # print(result)
        return token

    except Exception as e:
        print("An error occurred while solving hCaptcha:", str(e))
        return None


hcaptcha_solve(api_key=api_key, page_url=page_url, site_key=site_key)
