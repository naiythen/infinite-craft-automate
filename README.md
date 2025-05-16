# Python Infinite Craft Automator using Network Request and undetected-chromedriver

## Description

This Python script automates the process of discovering new elements in the popular web game "Infinite Craft" hosted on neal.fun. It intelligently combines known elements, sends network requests to check for new discoveries, and saves all found elements and their recipes to a local `data.json` file. The script uses `undetected-chromedriver` to help with the initial browser setup and `selenium` for interacting with the webpage, then relies on direct network requests for efficiency.

## Features

* **Automated Element Discovery:** Randomly combines elements from your discovered list to find new ones.
* **Network Request Based:** Primarily uses direct XHR/API calls for checking combinations, making it faster than UI-based automation for this part.
* **`undetected-chromedriver`:** Helps in avoiding basic bot detection during the initial page load and setup.
* **Persistent Storage:** Saves all discovered elements, their emojis, and the recipes used to create them in a `data.json` file.
* **Data Recovery:** In case of `data.json` corruption, the script attempts to back up the corrupted file and can start with a fresh default set of elements.
* **Retry Mechanism:** Automatically retries network requests up to 5 times with a 5-second delay if they fail, enhancing robustness.
* **User-Defined Iterations:** Prompts the user for the number of new combination attempts they want the script to make.
* **Emoji Support:** Stores and can display emojis associated with elements.

## Prerequisites

* **Python:** Version 3.10 or newer (Python 3.12+ recommended to ensure `setuptools` handles `distutils` correctly).
* **Google Chrome:** A recent version of the Google Chrome browser must be installed.
* **`pip`:** Python package installer (usually comes with Python).

## Installation

1.  **Install required Python packages:**
    Find the directory where the EXTRACTED Folder is, then in that directory, right click and select "Open In Terminal"
    Then run:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Navigate to the script directory** in your terminal or command prompt (As Done in Installation).
2.  **Run the script:**
    ```bash
    python Auto.py
    ```
    (Or `py Auto.py`)

3.  **Enter Iterations:** The script will first ask you:
    `How many times do you want to iterate?`
    Enter the number of new combinations you want the script to attempt. Each iteration tries to find one new element or recipe.

4.  **Manual Verification (if needed):**
    The script will open Google Chrome using `undetected-chromedriver` and navigate to `https://neal.fun/infinite-craft/`. It will then pause with the message:
    `Please complete any manual verification in the browser and then press Enter here to continue...`
    At this point, you might need to solve a CAPTCHA or pass any other anti-bot checks that the website presents. Once the game page is fully loaded and interactive, press Enter in the terminal where the script is running.

5.  **Automation Begins:** The script will then start combining elements and making network requests to discover new ones. Progress will be printed to the console.

6.  **Stopping the script:** You can usually stop the script by pressing `Ctrl+C` in the terminal. The script will attempt to close the browser window when it finishes or is interrupted.

## Output

* **Console Output:** The script prints its actions, discovered elements, and any errors to the console.
* **IMPORTANT** The chrome window opened will look like nothing is happening, but if you open the Network Requests in the console, the progress is there. You can also check the progress in the Command Prompt.
* **`data.json`:** This file is created/updated in the same directory as the script. It stores:
    * `elements`: A list of all discovered elements, including their text, emoji, and a `discovered` flag.
    * `darkMode`: A boolean (currently unused by this script but part of the structure).
    * `pinned`: A list (currently unused by this script).
    * `recipes`: A dictionary where each key is a resulting element's text, and the value is a list of recipes (ingredient pairs) that produce that element. Each ingredient includes its text and emoji.

    Example snippet from `data.json`:
    ```json
    {
        "elements": [
            {"text": "Water", "emoji": "💧", "discovered": true},
            {"text": "Fire", "emoji": "🔥", "discovered": true},
            // ... more elements
            {"text": "Steam", "emoji": "💨", "discovered": true}
        ],
        "recipes": {
            "Steam": [
                [
                    {"text": "Water", "emoji": "💧"},
                    {"text": "Fire", "emoji": "🔥"}
                ]
            ]
            // ... more recipes
        }
    }
    ```

## Sharing Your Discoveries

You can contribute your discovered elements and recipes from your `data.json` file to the community by importing your saves to:

* [Infinite Craft Wiki & Browser](https://infinibrowser.wiki/)

*(Note: This project is not affiliated with infinibrowser.wiki.)*

## Dependencies

* [Python](https://www.python.org/)
* [Selenium](https://pypi.org/project/selenium/): For browser automation.
* [undetected-chromedriver](https://pypi.org/project/undetected-chromedriver/): A modified version of Selenium's ChromeDriver to help avoid detection.
* [setuptools](https://pypi.org/project/setuptools/): Required for `distutils` compatibility in newer Python versions, a dependency of `undetected-chromedriver`.

## License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.
See the `LICENSE` file for the full license text. This choice is influenced by the GPL-3.0 license of `undetected-chromedriver`.

## Disclaimer & Important Notes

* **Respect Website Terms:** This script automates interaction with `neal.fun`. Users should be aware of the website's Terms of Service and use this script responsibly. Avoid sending an excessive number of requests in a short period to prevent overloading the server.
* **Functionality Not Guaranteed:** Websites can change their structure or implement new anti-bot measures at any time, which may break this script or parts of its functionality. `undetected-chromedriver` aims to keep up, but it's not foolproof.
* **Local Data:** All discovered data is stored locally in `data.json`. There is no cloud backup feature within this script.
* **Error Handling:** The script includes error handling for common issues like JSON corruption and network request failures, but unhandled exceptions may still occur.
