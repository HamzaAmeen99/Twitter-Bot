# 🐦 Twitter (X) Automation Bot
> **A high-performance Selenium automation tool for managing Twitter (X) engagement.**

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/library-Selenium-green.svg)](https://www.selenium.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/HamzaAmeen99/Twitter-Bot/graphs/commit-activity)

---

## 🚀 Project Overview
This repository contains a Python-based automation script that uses **Selenium WebDriver** to interact with Twitter. Whether you're looking to automate engagement or learn browser automation, this bot provides a solid foundation for navigating the Twitter (X) DOM efficiently.

### ✨ Key Features
* **Secure Login**: Automates the login flow, including handling secondary prompts.
* **Keyword Extraction**: Discovers tweets based on specific hashtags or search queries.
* **Auto-Engagement**: Likes and retweets posts to increase account visibility.
* **Smart Delays**: Built-in randomized sleep timers to mimic human behavior and minimize detection risks.
* **Headless Support**: Can be configured to run in the background without a browser UI.

---

## 🌍 Environment Setup (Crucial)

To run this bot, the **ChromeDriver** must be installed and added to your operating system's **Environment Variables (PATH)**. 

### 1. Download ChromeDriver
1. Check your Google Chrome version (Settings > About Chrome).
2. Download the matching driver from the [Official Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/) page.

### 2. Add to System PATH
#### **For Windows Users:**
1. Extract `chromedriver.exe` to a permanent folder (e.g., `C:\WebDriver\`).
2. Search for **"Edit the system environment variables"** in the Windows Start menu.
3. Click **Environment Variables** > Find **Path** in 'System Variables' > Click **Edit**.
4. Click **New** and add the folder path: `C:\WebDriver\`.
5. **Restart** your terminal or VS Code for the changes to take effect.

#### **For macOS/Linux Users:**
1. Move the driver to your local bin:
   ```bash
   sudo mv chromedriver /usr/local/bin/
2.Grant execution permissions:
  ```bash
  chmod +x /usr/local/bin/chromedriver
```
# 🛠️ Installation & Usage

---

### 📦 Step 1: Clone the Repository

```bash
git clone https://github.com/HamzaAmeen99/Twitter-Bot.git
cd Twitter-Bot
```

### 🐍 Step 2: Install Dependencies

Ensure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### ⚙️ Step 3: Configuration

Open the main script and input your credentials in accounts.json file:

# Configuration Example
```python
USERNAME = "your_twitter_handle"
PASSWORD = "your_secret_password"
```
## 🏃 Step 4: Run the Bot
python main.py

# ⚠️ Safety & Disclaimer

Use this tool at your own risk. Automating Twitter accounts can lead to permanent bans if it violates Twitter's Terms of Service.

This project is strictly for **educational purposes only.**
The developer is not responsible for any misuse or account restrictions.

# 👨‍💻 Author

Developed with ❤️ by [Hamza Ameen](https://www.linkedin.com/in/hamza-ameen07/)
