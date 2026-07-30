# Spider-Man Movie Invitation (Streamlit)

This app is a responsive Spider-Man-inspired invitation built with Streamlit. It uses original visuals only (webs, sparkles, hearts, skyline silhouettes, comic bubbles, and spider animations) and does not use copyrighted Marvel or official movie assets.

## 1. Install dependencies

1. Open a terminal in this project folder.
2. Install requirements:

  pip install -r requirements.txt

## 2. Run the app locally

1. Start Streamlit:

  streamlit run app.py

2. Open the local URL shown in your terminal.

## 3. Enable two-step verification on Google

1. Sign in to the Google account you will use as the sender email.
2. Open Google Account settings.
3. Go to Security.
4. Turn on 2-Step Verification.

## 4. Create a Gmail App Password

1. Stay in Google Account Security settings.
2. Open App passwords.
3. Create an app password for Mail.
4. Copy the generated 16-character password.

## 5. Create local .streamlit/secrets.toml

1. Make sure the .streamlit folder exists.
2. Create a local file named .streamlit/secrets.toml.
3. Add the following keys:

  EMAIL_SENDER = "your-sender-gmail-address@gmail.com"
  EMAIL_RECIPIENT = "shavinijoseph2004@gmail.com"
  EMAIL_APP_PASSWORD = "your-16-character-gmail-app-password"

4. Save the file.

## 6. Add secrets in Streamlit Community Cloud

1. Open your app in Streamlit Community Cloud.
2. Open Settings or the Secrets section.
3. Paste the same three keys and values used locally.
4. Save the secrets and restart the app if prompted.

## 7. Upload safely to GitHub

1. Confirm .streamlit/secrets.toml is ignored by git.
2. Commit only source files, documentation, and .streamlit/secrets.toml.example.
3. Push your repository to GitHub.

## 8. Deploy on Streamlit Community Cloud

1. Open Streamlit Community Cloud.
2. Click New app.
3. Select your GitHub repository and branch.
4. Set the main file path to app.py.
5. Deploy and wait for the build to finish.
6. Share the generated public app URL.

## 9. Test on iPhone, Android, and laptop

1. Open the public URL on an iPhone in portrait mode.
2. Open the same URL on an Android phone in portrait mode.
3. Rotate both phones and confirm layout still fits the viewport.
4. Open the same URL on a laptop browser.
5. Verify there is no horizontal scrolling and text stays readable.
6. Verify the No button escapes quickly on both touch and mouse devices.
7. Verify the Yes button grows smoothly after each No escape.

## 10. Verify email notification delivery

1. Enter a valid name and press Continue.
2. Press Yes ❤️ once.
3. Confirm the celebration screen appears.
4. Check inbox for shavinijoseph2004@gmail.com.
5. Verify subject is: Spider-Man invitation response: YES ❤️
6. Verify the body includes name, answer YES, Australia/Melbourne timestamp, and source note.

## Security checklist

1. Never commit .streamlit/secrets.toml.
2. Store sender credentials only in Streamlit secrets.
3. Keep recipient fixed as shavinijoseph2004@gmail.com.
4. Do not expose SMTP errors or credentials in visitor-facing messages.
