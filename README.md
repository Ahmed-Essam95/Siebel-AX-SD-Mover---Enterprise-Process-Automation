# 💼 Security Deposit Bot

An advanced **Python automation bot** built with **Selenium WebDriver** to automate the full **Security Deposit Move Cycle** between **Siebel** and **AX systems** for telecom operations.

This bot handles the entire end-to-end process automatically — from reading SR numbers, logging into Siebel and AX, validating accounts, reversing and reposting deposits, sending customer notifications, and closing SRs.

---

## 🚀 Features

- 🔐 Automated login to **Siebel** and **AX** portals  
- ⚙️ Handles Siebel SR search, validation, and status updates  
- 🔄 Executes full security deposit movement between accounts  
- 📊 Extracts and validates account data dynamically  
- 🧾 Sends SMS to customers once the action is done  
- 💾 Automatically saves screenshots on errors  
- 🕒 Displays total processing time per SR and for the whole cycle  
- 🧠 Smart recovery logic to re-login after any browser crash or session loss  

---

## 🧩 Tech Stack

| Component | Description |
|------------|-------------|
| **Language** | Python 3.x |
| **Automation** | Selenium WebDriver |
| **Data Processing** | Pandas |
| **UI Input** | Tkinter (for secure password entry) |

---

## 📂 Project Structure

Security Deposit Bot/
│
├── Security Deposit Bot.py # Main automation script
├── SR_Source.txt # Input file containing SR numbers (one per line)
├── Manual Guide.pdf # Project documentation
└── chromedriver.exe # Chrome driver required for Selenium


## 📸 Error Handling

If any SR fails:
A screenshot is saved in the current directory (named after the SR number).
The bot automatically attempts to recover and continue from the next SR.


## 🧑‍💻 Author

Ahmed Essam
Automation Developer | Python & Selenium
