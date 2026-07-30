# Spider Movie Invite (Streamlit)

A responsive superhero-inspired invitation app built with Streamlit.
It uses original visuals only (webs, spider icon, skyline, sparkles, speech bubble) and avoids copyrighted Marvel artwork or logos.

## Features

- Invitation text:
  - "Will you come with me to watch the Spider-Man movie on 31/07 evening? 🕷️❤️"
- Fully responsive UI for phones, tablets, laptops, and desktops
- Original red/blue/black/white comic theme
- "Yes ❤️" and "No 🕸️" buttons, with a runaway/impossible-to-click "No" button
- "Yes" celebration animations (confetti, floating hearts, swinging spider)
- Success message:
  - "YAY!! ❤️ See you at the movie! 🕷️🍿"
- Secure Gmail SMTP email notifications for Yes responses using Streamlit secrets
- Session-safe answer submission with duplicate prevention

## Project Files

- app.py
- requirements.txt
- README.md
- .gitignore
- .streamlit/config.toml
- .streamlit/secrets.toml.example

## 1) Run Locally

1. Open a terminal in this project folder.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create your local secrets file:

```bash
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

4. Edit .streamlit/secrets.toml with your real values.
5. Start the app:

```bash
streamlit run app.py
```

## 2) Create a Gmail App Password

1. Sign in to your Google account.
2. Enable 2-Step Verification.
3. Go to Google Account -> Security -> App passwords.
4. Create an app password (Mail).
5. Copy the generated 16-character password.

## 3) Local Secrets Format

Use this format in .streamlit/secrets.toml and in Streamlit Cloud Secrets:

```toml
EMAIL_SENDER = "[yourgmail@gmail.com](mailto:yourgmail@gmail.com)"
EMAIL_RECIPIENT = "[yournotificationemail@gmail.com](mailto:yournotificationemail@gmail.com)"
EMAIL_APP_PASSWORD = "your-16-character-app-password"
```

For real usage, replace those with actual email strings and your real app password.

## 4) Add Secrets in Streamlit Community Cloud

1. Open your deployed app settings.
2. Go to App Settings -> Secrets.
3. Paste the same TOML keys from above using your real credentials.
4. Save and restart the app if prompted.

## 5) Deploy to Streamlit Community Cloud

1. Push this project to a GitHub repository.
2. Open Streamlit Community Cloud.
3. Click New app.
4. Select your repository, branch, and set main file path to app.py.
5. Deploy.

## 6) Test the Public Link on Mobile and Laptop

1. Open the public URL on an iPhone or Android device (portrait mode first).
2. Confirm no horizontal scrolling and that buttons are easy to tap.
3. Rotate to landscape and verify layout still fits.
4. Open the same URL on a laptop/desktop browser and confirm centered layout.
5. Click "Yes ❤️" once and confirm:
   - celebration animation appears
   - both buttons become disabled
   - email notification is received

## Security Notes

- Do not commit .streamlit/secrets.toml.
- .gitignore already excludes .streamlit/secrets.toml.
- The app never displays credentials to recipients.
- Email send failures are handled safely without crashing the UI.
