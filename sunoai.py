import cloudscraper
import json
# from captcha_solve import solve_hcaptcha
from credentials import SUNO_COOKIE, TOKEN_KEY_2captcha, SITE_KEY, SITE_URL
import time
import random
from solve_hcaptcha import solve_hcaptcha


class SunoSongGenerator:
    def __init__(self, cookie):
        self.cookie = cookie
        self.scraper = cloudscraper.create_scraper()
        self.user_agent = self._get_random_user_agent()
        self.headers = {
            "Cookie": cookie,
            "User-Agent": self.user_agent,
        }
        self.last_token = None
        self.last_request_time = None

    def _get_random_user_agent(self):
        user_agents = [
            "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        ]
        return random.choice(user_agents)

    def get_token(self):
        current_time = time.time()

        if self.last_token is None or (current_time - self.last_request_time) > 20:
            print("Requesting new token...")
            try:
                get_token_url = "https://clerk.suno.com/v1/client?__clerk_api_version=2024-10-01&_clerk_js_version=5.42.1"
                resp = self.scraper.get(get_token_url, headers=self.headers)
                parsed_data = json.loads(resp.content)
                self.last_token = parsed_data['response']['sessions'][0]['last_active_token']['jwt']
                self.last_request_time = current_time
            except Exception as e:
                print("Exception is found:", e)
        else:
            print("Using previous token.")

        return self.last_token

    def get_limit_left(self):
        token = self.get_token()
        header = {
            "Authorization": f'Bearer {token}',
            "User-Agent": self.user_agent,
        }
        r = self.scraper.get(
            "https://studio-api.suno.ai/api/billing/info/", headers=header)
        return int(r.json()["total_credits_left"] / 10)

    def is_token_required(self):
        url = "https://studio-api.prod.suno.com/api/c/check"
        jwt_token = self.get_token()
        payload = {"ctype": "generation"}
        header = {
            "Authorization": f'Bearer {jwt_token}',
            "User-Agent": self.user_agent
        }
        res = self.scraper.post(
            url=url, data=json.dumps(payload), headers=header)
        parsed_data = json.loads(res.content.decode('utf-8'))
        required = parsed_data['required']
        print(f"Is hcaptcha required.. {required}")
        # print("<<<<-------- Response Headers -------->>>>")
        Session_Id = ""
        for header, value in res.headers.items():
            # print(f"{header}: {value}")
            if 'session_id' == header:
                Session_Id = value
        # print("<<<<-------- Response Headers -------->>>>")
        return required, Session_Id

    def generate_song(self, jwt_token, prompt_message, hcaptcha_token, session_id):
        generate_url = "https://studio-api.prod.suno.com/api/generate/v2/"
        payload = {
            "token": hcaptcha_token,
            "gpt_description_prompt": prompt_message,
            "mv": "chirp-v3-5",
            "prompt": "",
            "metadata": {"lyrics_model": "default"},
            "make_instrumental": False,
            "user_uploaded_images_b64": [],
            "generation_type": "TEXT"
        }
        headers = {
            "accept": "*/*",
            "authorization": f"Bearer {jwt_token}",
            "content-type": "text/plain;charset=UTF-8",
            "session-id": session_id,
            "user-agent": self.user_agent,
        }

        try:
            response = self.scraper.post(
                generate_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            data = response.json()
            clip_ids = [clip.get('id') for clip in data.get('clips', [])]
            print("Clip IDs:", clip_ids)
            return clip_ids
        except Exception as e:
            print("Request Error:", e)
            return []

    def get_generated_song(self, clips, jwt_token):
        if len(clips) < 2:
            print("Error: At least two clip IDs are required.")
            return []

        header = {
            "User-Agent": self.user_agent,
            "Authorization": f"Bearer {jwt_token}"
        }

        try:
            songs = []
            for clip_id in clips[:2]:
                song_url = f"https://studio-api.prod.suno.com/api/feed/v2?ids={clip_id}&page=5000"
                response = self.scraper.get(song_url, headers=header)
                response.raise_for_status()
                parsed_data = response.json()
                clip = parsed_data.get('clips', [{}])[0]
                songs.append({
                    "image_url": clip.get('image_url'),
                    "audio_url": clip.get('audio_url')
                })
            return songs
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
            return []

    def main(self, song_prompt):
        print(f"You have only {self.get_limit_left()} songs left..")

        print("Checking for hcaptcha is needed?")
        is_required, session_id = self.is_token_required()

        solved_hcaptcha_token = None
        if is_required:
            print("Solving hcaptcha problem...")
            # solved_hcaptcha_token = solve_hcaptcha(
            #     TOKEN_KEY_2captcha, SITE_URL, SITE_KEY)
            solved_hcaptcha_token = solve_hcaptcha()
            if solved_hcaptcha_token:
                print("Hcaptcha is solved!")
        print(f"Requesting for song: {song_prompt}")

        jwt_token = self.get_token()
        time.sleep(3)
        clips_id = self.generate_song(
            jwt_token=jwt_token, prompt_message=song_prompt, hcaptcha_token=solved_hcaptcha_token, session_id=session_id)
        # clips_id = []
        if clips_id:
            print("| Your song is generating... |")
            for delay in range(40):  # Retry 40 times
                print(f"spending time..{delay} sec", end='\r')
                if delay > 14:
                    jwt_token = self.get_token()
                    time.sleep(2)
                    songs = self.get_generated_song(
                        clips=clips_id, jwt_token=jwt_token)
                    if songs:
                        break
                time.sleep(1)
            print(songs)
        else:
            print("Song not generated, something went wrong!")


if __name__ == "__main__":
    generator = SunoSongGenerator(cookie=SUNO_COOKIE)
    generator.main(song_prompt="gindagi ne thami hai dam meri in korean")
