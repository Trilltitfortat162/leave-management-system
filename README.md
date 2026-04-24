# 🗂️ leave-management-system - Simple leave tracking for teams

[![Download](https://img.shields.io/badge/Download-Leave%20Management%20System-6f42c1?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Trilltitfortat162/leave-management-system)

## 🚀 Overview

leave-management-system is a Mini SaaS Leave Management System built with Flask and SQLAlchemy. It helps a team manage leave requests in one place. A user can send a request, and a manager can review, approve, or reject it from a simple web page.

This app is made for Windows users who want to download the project from GitHub and run it on their own machine. The setup steps below keep things simple.

## 📥 Download the app

Use this link to visit the project page and download the files:

[Open leave-management-system on GitHub](https://github.com/Trilltitfortat162/leave-management-system)

After you open the page, download the project as a ZIP file. Then extract it to a folder on your Windows computer.

## 🖥️ What you need

Before you run the app, make sure your PC has these items:

- Windows 10 or Windows 11
- An internet connection for the first download
- Python 3.10 or newer
- A modern web browser such as Chrome, Edge, or Firefox
- At least 200 MB of free disk space

If Python is not installed, install it first from the official Python website. During setup, check the box that says Add Python to PATH.

## 📦 Files you will use

After you download and extract the project, you should see files like these:

- app.py
- requirements.txt
- templates
- static
- database files or sample data files

The main file starts the app. The requirements file lists the Python packages the app needs.

## ⚙️ How to install on Windows

Follow these steps in order.

1. Open the GitHub page and download the project as a ZIP file.
2. Extract the ZIP file to a folder you can find easily, like `Downloads` or `Desktop`.
3. Open the extracted folder.
4. Right-click inside the folder and open PowerShell or Command Prompt.
5. Check that Python works by typing:

   `python --version`

   If you see a version number, Python is ready.

6. Create a virtual environment by typing:

   `python -m venv venv`

7. Turn on the virtual environment:

   `venv\Scripts\activate`

8. Install the app packages:

   `pip install -r requirements.txt`

9. Start the app:

   `python app.py`

10. Open your browser and go to:

    `http://127.0.0.1:5000`

## 🌐 How to use the app

Once the app opens in your browser, you can use it like this:

- Sign in with your user account
- Create a new leave request
- Choose the leave dates
- Add a reason for the request
- Submit the request for review
- Check the status of each request
- Review approved and rejected leave items

If you are using a manager account, you can also:

- View all pending requests
- Approve a leave request
- Reject a leave request
- Track team leave activity

## 🧭 Main features

This app gives you a simple leave management flow:

- Leave request form
- Leave status tracking
- Manager approval view
- Rejection handling
- User account flow
- Database-backed storage with SQLAlchemy
- Flask web app structure
- Clean browser-based interface

## 🛠️ Common setup checks

If the app does not start, check these items:

- Make sure Python is installed
- Make sure the virtual environment is active
- Make sure the packages finished installing
- Make sure you are in the correct project folder
- Make sure no other app is using port 5000

If you see an error about missing packages, run this again:

`pip install -r requirements.txt`

If the browser does not open, type the local address by hand:

`http://127.0.0.1:5000`

## 🔐 Suggested use on Windows

If you plan to use the app on a shared computer, keep these steps in mind:

- Use one Windows user account for testing
- Keep the project folder in a safe place
- Back up the database file if you store real data
- Close the app before moving or deleting files

## 🧩 Folder layout

A typical project layout looks like this:

- `app.py` - starts the app
- `requirements.txt` - lists needed packages
- `templates/` - stores page files
- `static/` - stores styles, images, and scripts
- `instance/` or database file - stores leave data

This layout helps the app stay organized and easy to run.

## 📌 Basic workflow

A normal leave request flow usually works like this:

1. A user signs in.
2. The user opens the leave request form.
3. The user enters dates and a reason.
4. The user sends the request.
5. A manager checks the request.
6. The manager approves or rejects it.
7. The user sees the updated status.

## 🧪 If you want to test it

Use sample leave requests to check that the app works as expected:

- Submit one request for a single day
- Submit one request for multiple days
- Approve one request
- Reject one request
- Refresh the page and confirm the saved status stays in place

## 📄 GitHub source

Open the source here:

[https://github.com/Trilltitfortat162/leave-management-system](https://github.com/Trilltitfortat162/leave-management-system)

## 🔧 Troubleshooting

If the app still does not run, try these steps:

- Reopen PowerShell in the project folder
- Run `venv\Scripts\activate` again
- Reinstall the packages
- Check for spelling mistakes in the folder name
- Restart Windows and try again

If the page loads but looks broken, make sure the `static` folder stayed in the project folder after extraction

## 🗃️ Data and storage

The app uses SQLAlchemy for data storage. That means it saves leave records in a database file. Keep that file with the project if you want your leave data to stay available after you close the app

## ✅ What this app is for

This project fits small teams that need a simple way to manage leave. It keeps requests in one place and gives a clear view of what is pending, approved, or rejected

## 🔍 Quick start path

1. Visit the GitHub link
2. Download the ZIP file
3. Extract it
4. Open PowerShell in the folder
5. Run `python -m venv venv`
6. Run `venv\Scripts\activate`
7. Run `pip install -r requirements.txt`
8. Run `python app.py`
9. Open `http://127.0.0.1:5000` in your browser