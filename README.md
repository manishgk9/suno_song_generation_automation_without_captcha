# 🎶 Suno Song Generation Automation (with Cookie & hCaptcha Solver)

This project automates the process of generating songs from [suno.com](https://suno.com) using **only your session cookie** and a custom-built **hCaptcha solver**. It mimics real browser behavior via `cloudscraper`, extracts JWT tokens, solves captchas (if required), and generates/downloads songs using Suno's internal APIs.

---

## ✨ Features

- 🍪 **Cookie-Based Auth** – No login required, just use your `__Secure-next-auth.session-token`
- 🔐 **JWT Token Extraction** – From Clerk’s session API
- 🧩 **hCaptcha Solver** – Solves hCaptcha automatically using your custom AI or 2Captcha
- 🎵 **Song Generation** – Submits song prompts and retrieves clip/audio URLs
- 💻 **Command Line Interface** – Headless, fast automation from terminal
- 🌐 **Cloudscraper** – Bypasses Cloudflare and behaves like a browser

---

## 📦 Dependencies

Install all dependencies using:

```bash
pip install -r requirements.txt
````

**Example `requirements.txt`:**

```
cloudscraper
python-dotenv
requests
```

---

## 🔐 Environment & Credentials

Create a `credentials.py` file in the root directory with the following constants:

```python
SUNO_COOKIE = "your_suno_cookie_here"
TOKEN_KEY_2captcha = "your_2captcha_api_key"
SITE_KEY = "site_key_for_hcaptcha"
SITE_URL = "https://studio.suno.com"
```

> 💡 You can retrieve `SUNO_COOKIE` from your browser cookies:
> Look for `__Secure-next-auth.session-token` under `suno.com` domain in DevTools > Application > Cookies.

---

## 🧠 Script Flow

1. Load session cookie and headers with random user-agent
2. Hit Clerk API to get a fresh JWT token
3. Call `/api/c/check` to verify if hCaptcha is required
4. If required, solve hCaptcha using your `solve_hcaptcha()` method
5. Submit prompt to `/api/generate/v2/`
6. Poll the `/api/feed/v2` endpoint to retrieve audio and image links

---

## 🚀 Run the Script

```bash
python suno_main.py
```

> Replace the `song_prompt` in the script or make it accept command-line args.

---

## 📝 Example Prompt in Script

```python
generator.main(song_prompt="gindagi ne thami hai dam meri in korean")
```

You can change this to any custom prompt of your choice.

---

## 🎧 Output

* Audio clips and image URLs will be printed once the song is generated.
* Optionally extend to auto-download the `.mp3` files or store metadata.

---

## 🛡️ Disclaimer

This tool is intended **for educational and research purposes only**.
Bypassing hCaptcha or automating song generation may violate [Suno's](https://suno.com) terms of service. Use at your own risk.

---

## 👤 Author

**Manish Yadav**
GitHub: [manishgk9](https://github.com/manishgk9)

---

## 📄 License

MIT License – do what you want, but give credit.

---

## 🛠️ To-Do

* [ ] CLI support for passing prompt
* [ ] Retry mechanism on failed captcha or song generation
* [ ] Auto-download generated song files
* [ ] Docker support for headless runs

```
