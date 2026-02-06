🐦 Twitter (X) Automation Bot
A robust Python-based automation tool built with Selenium to manage Twitter (X) interactions. This bot can automate logging in, searching for tweets via keywords, and performing actions like liking and retweeting.

🚀 Features
Automated Authentication: Securely logs into your Twitter account.

Keyword Targeting: Searches for specific hashtags or phrases.

Engagement Automation: Automatically likes and retweets relevant content.

Stealth Mode: Incorporates random delays and human-like behavior to reduce detection.

Headless Mode: Option to run the bot without a visible browser window.

🛠️ Tech Stack
Language: Python 3.x

Browser Automation: Selenium WebDriver

Web Driver: ChromeDriver

🌍 Environment Setup (Important)
For the bot to run, your system needs to know where the ChromeDriver is located.

1. Download the Driver
Download the version that matches your Google Chrome version from the Official Chrome for Testing page.

2. Add to OS Environment Variables
You must add the folder containing your chromedriver to your system's PATH variable so Selenium can find it automatically:

Windows:
Move chromedriver.exe to a permanent folder (e.g., C:\WebDriver\).

Open the Start Menu, search for "Edit the system environment variables", and open it.

Click Environment Variables.

Under System Variables, find Path and click Edit.

Click New and paste the folder path (C:\WebDriver\).

Click OK on all windows and restart your Terminal/CMD.

macOS / Linux:
Move the driver to /usr/local/bin:

Bash
sudo mv chromedriver /usr/local/bin/
Give it execution permissions:

Bash
chmod +x /usr/local/bin/chromedriver
⚙️ Installation
Clone the Repo

Bash
git clone https://github.com/HamzaAmeen99/Twitter-Bot.git
cd Twitter-Bot
Install Requirements

Bash
pip install -r requirements.txt
Configuration Update your credentials and search parameters in the script (or your .env file):

Python
# Example configuration
username = "YOUR_USERNAME"
password = "YOUR_PASSWORD"
query = "#Python #Automation"
🚀 Usage
Simply run the main script to start the automation:

Bash
python main.py
⚠️ Disclaimer
This project is for educational purposes only. Automating Twitter accounts using Selenium may violate Twitter's Terms of Service. Use this tool at your own risk; the developer is not responsible for any account suspensions.

Developed with ❤️ by Hamza Ameen