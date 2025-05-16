# Your Name/GitHub Username
# Copyright (C) 2025 Your Name/GitHub Username
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import urllib.parse
import random
import json
import os
import time 
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--log-level=3")
json_file_path = "data.json"
def load_json(file_path_to_load):
    if not os.path.exists(file_path_to_load):
        default_data = {
            "elements": [
                {"text": "Water", "emoji": "💧", "discovered": False},
                {"text": "Fire", "emoji": "🔥", "discovered": False},
                {"text": "Wind", "emoji": "🌬️", "discovered": False},
                {"text": "Earth", "emoji": "🌍", "discovered": False},
            ],
            "darkMode": True,
            "pinned": [],
            "recipes": {}
        }
        try:
            with open(file_path_to_load, "w", encoding='utf-8') as f:
                json.dump(default_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error creating default JSON file '{file_path_to_load}': {e}")
            input("Press Enter to acknowledge and exit...")
            exit(1)
        return default_data
    else:
        try:
            with open(file_path_to_load, "r", encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error loading JSON from '{file_path_to_load}': {e}")
            backup_path = file_path_to_load + '.backup'
            try:
                if os.path.exists(backup_path):
                    os.remove(backup_path) 
                os.rename(file_path_to_load, backup_path)
                print(f"Corrupted JSON file has been backed up to {backup_path}.")
            except PermissionError as pe:
                print(f"Permission denied: Unable to rename '{file_path_to_load}' to '{backup_path}': {pe}")
                print("Please close any programs using 'data.json' and try again.")
                input("Press Enter to exit...")
                exit(1)
            except Exception as oe:
                print(f"Error creating backup of corrupted file '{file_path_to_load}': {oe}")
            default_data_after_corruption = {
                "elements": [
                    {"text": "Water", "emoji": "💧", "discovered": False},
                    {"text": "Fire", "emoji": "🔥", "discovered": False},
                    {"text": "Wind", "emoji": "🌬️", "discovered": False},
                    {"text": "Earth", "emoji": "🌍", "discovered": False},
                ],
                "darkMode": True, "pinned": [], "recipes": {}
            }
            try:
                with open(file_path_to_load, "w", encoding='utf-8') as f_new:
                    json.dump(default_data_after_corruption, f_new, indent=4, ensure_ascii=False)
                print(f"Created new JSON file with default data at '{file_path_to_load}' due to corruption.")
                input("A JSON error occurred. A backup was attempted, and a new default file was created. Press Enter to continue with new data...")
            except Exception as ce:
                print(f"Critical error: Could not create new default JSON at '{file_path_to_load}' after corruption: {ce}")
                input("Press Enter to exit...")
                exit(1)
            return default_data_after_corruption
        except Exception as e_gen:
            print(f"An unexpected error occurred while loading JSON from '{file_path_to_load}': {e_gen}")
            input("Press Enter to exit...")
            exit(1)
def save_json_atomic(data_to_save, file_path_to_save):
    temp_file_path = file_path_to_save + '.tmp'
    try:
        with open(temp_file_path, "w", encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)
        os.replace(temp_file_path, file_path_to_save)
    except Exception as e:
        print(f"Error saving JSON atomically to '{file_path_to_save}': {e}")
        input("Press Enter to acknowledge this save error. Data might not have been saved...")
def get_initial_words(data_source):
    if data_source and "elements" in data_source:
        return [element["text"] for element in data_source["elements"]]
    return []
def get_emoji(data_source, element_text):
    if data_source and "elements" in data_source:
        for element in data_source["elements"]:
            if element["text"].lower() == element_text.lower():
                return element["emoji"]
    return ""
data = load_json(json_file_path)
words = list(set(get_initial_words(data)))
word_to_emoji = {}
if data and "elements" in data:
    word_to_emoji = {element["text"]: element["emoji"] for element in data["elements"]}
iterations = 0
try:
    iterations_input = input("How many times do you want to iterate? ")
    iterations = int(iterations_input)
except ValueError as e:
    print(f"Invalid input for iterations: '{iterations_input}'. Please enter an integer. Error: {e}")
    input("Press Enter to exit...")
    exit(1)
except EOFError:
    print("No input received for iterations (EOF). Defaulting to 0 iterations.")
    iterations = 0
tried_combinations = set()
existing_recipes = set()
if data and "recipes" in data:
    for result_key, recipes_list in data.get("recipes", {}).items():
        if isinstance(recipes_list, list):
            for recipe_pair in recipes_list:
                if isinstance(recipe_pair, list) and len(recipe_pair) == 2:
                    try:
                        ingredients = tuple(sorted([ingredient["text"].lower() for ingredient in recipe_pair]))
                        existing_recipes.add(ingredients)
                    except TypeError: 
                        print(f"Warning: Malformed recipe pair for '{result_key}', skipping: {recipe_pair}")
driver = None
if iterations > 0 :
    try:
        driver = uc.Chrome(options=chrome_options)
        driver.get("https://neal.fun/infinite-craft/")
    except Exception as e:
        print(f"Failed to initialize Chrome driver or navigate: {e}")
        input("Press Enter to exit...")
        if driver:
            try:
                driver.quit()
            except Exception: pass
        exit(1)
    try:
        input("Please complete any manual verification in the browser and then press Enter here to continue...")
    except EOFError:
        print("Skipping manual verification prompt (EOFError). Assuming non-interactive mode.")
def send_combination_request(word1, word2, current_driver):
    if not current_driver:
        print("Driver not available for sending request.")
        return None
    if word1.lower() == "nothing" or word2.lower() == "nothing":
        print(f"Skipping combination {word1} + {word2} because one word is 'nothing'.")
        return None
    word1_encoded = urllib.parse.quote_plus(word1)
    word2_encoded = urllib.parse.quote_plus(word2)
    url = f"https://neal.fun/api/infinite-craft/pair?first={word1_encoded}&second={word2_encoded}"
    max_retries = 5
    for attempt in range(max_retries):
        try:
            script = f
            result_json = current_driver.execute_async_script(script)
            response_data = json.loads(result_json)
            if int(response_data['status']) == 200:
                data_response = json.loads(response_data['responseText'])
                result_word_api = data_response.get('result', '').strip()
                result_emoji_api = data_response.get('emoji', '').strip()
                is_new_api = data_response.get('isNew', False)
                if result_word_api.lower() == "nothing":
                    print(f"Skipping result 'nothing' from combination {word1} + {word2}.")
                    return None 
                return {"word1": word1, "word2": word2, "result_word": result_word_api, "result_emoji": result_emoji_api, "is_new": is_new_api}
            else:
                print(f"Attempt {attempt + 1}/{max_retries}: Request for '{word1} + {word2}' failed with status {response_data['status']}.")
                if attempt == max_retries - 1:
                    print(f"Max retries reached for '{word1} + {word2}'. Failing this combination.")
                    input(f"Persistent request failure for '{word1} + {word2}' after {max_retries} attempts (Status: {response_data['status']}). Press Enter to continue...")
                    return None 
        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries}: Exception during request for '{word1} + {word2}': {type(e).__name__} - {e}")
            if attempt == max_retries - 1:
                print(f"Max retries reached for '{word1} + {word2}' due to persistent exceptions. Failing this combination.")
                input(f"Persistent exception for '{word1} + {word2}' after {max_retries} attempts ({type(e).__name__}). Press Enter to continue...")
                return None
        if attempt < max_retries - 1:
            print(f"Retrying in 5 seconds...")
            time.sleep(5)
    return None 
def process_result(api_result):
    global data, words, word_to_emoji, existing_recipes
    if not api_result or not api_result.get("result_word"):
        return False
    word1 = api_result['word1']
    word2 = api_result['word2']
    result_word_processed = api_result['result_word']
    result_emoji_processed = api_result['result_emoji']
    new_combination_tuple = tuple(sorted([word1.lower(), word2.lower()]))
    item_added_or_updated = False
    try:
        current_data_from_file = load_json(json_file_path)
        existing_element_in_file = next((el for el in current_data_from_file.get("elements", []) if el["text"].lower() == result_word_processed.lower()), None)
        if existing_element_in_file:
            recipes_for_result_in_file = current_data_from_file.get("recipes", {}).get(result_word_processed, [])
            combination_already_exists_for_this_result = False
            for recipe in recipes_for_result_in_file:
                if isinstance(recipe, list) and len(recipe) == 2:
                    try:
                        existing_combination_ingredients = tuple(sorted([ing["text"].lower() for ing in recipe]))
                        if new_combination_tuple == existing_combination_ingredients:
                            combination_already_exists_for_this_result = True
                            break
                    except (TypeError, KeyError):
                         print(f"Warning: Malformed recipe encountered for '{result_word_processed}' during check: {recipe}")
            if combination_already_exists_for_this_result:
                print(f"Combination {word1} + {word2} -> '{result_word_processed}' already exists in recipes, skipping.")
            else:
                print(f"Word '{result_word_processed}' already exists, adding new recipe: {word1} + {word2}.")
                new_recipe_entry = [
                    {"text": word1, "emoji": get_emoji(current_data_from_file, word1) or "❓"},
                    {"text": word2, "emoji": get_emoji(current_data_from_file, word2) or "❓"}
                ]
                current_data_from_file.setdefault("recipes", {}).setdefault(result_word_processed, []).append(new_recipe_entry)
                save_json_atomic(current_data_from_file, json_file_path)
                data = current_data_from_file 
                existing_recipes.add(new_combination_tuple)
                item_added_or_updated = True
                print(f"Saved new recipe for '{result_word_processed}' ({word1} + {word2}).")
        else:
            print(f"New word found: {result_word_processed} {result_emoji_processed}")
            current_data_from_file.setdefault("elements", []).append({
                "text": result_word_processed,
                "emoji": result_emoji_processed,
                "discovered": True 
            })
            current_data_from_file.setdefault("recipes", {})[result_word_processed] = [[
                {"text": word1, "emoji": get_emoji(current_data_from_file, word1) or "❓"},
                {"text": word2, "emoji": get_emoji(current_data_from_file, word2) or "❓"}
            ]]
            save_json_atomic(current_data_from_file, json_file_path)
            data = current_data_from_file
            if result_word_processed not in words:
                words.append(result_word_processed)
            word_to_emoji[result_word_processed] = result_emoji_processed
            existing_recipes.add(new_combination_tuple)
            item_added_or_updated = True
            print(f"Saved new word '{result_word_processed}' and its recipe.")
        return item_added_or_updated
    except Exception as e:
        print(f"Error processing result for '{result_word_processed}' from {word1} + {word2}: {type(e).__name__} - {e}")
        input("Press Enter to continue...")
        return False
def run_iterations_sequentially():
    global words, data, driver
    if iterations == 0:
        print("No iterations requested.")
        return
    if not driver:
        print("Driver not initialized. Cannot run iterations.")
        return
    processed_in_session_count = 0
    for i in range(iterations):
        print(f"\nIteration {i+1}/{iterations}")
        max_attempts_per_iteration = 1000 
        attempt_for_new_pair = 0 
        processed_new_in_this_iteration = False
        current_words_pool_for_iteration = list(set(get_initial_words(load_json(json_file_path))))
        if not current_words_pool_for_iteration or len(current_words_pool_for_iteration) < 2 :
            print("Not enough unique words available at the start of iteration. May need more base elements.")
            if i == 0 and len(current_words_pool_for_iteration) < 2 :
                 print("Cannot proceed without at least two elements. Exiting iterations.")
                 return 
            elif len(current_words_pool_for_iteration) < 2:
                 print("Skipping this iteration due to lack of elements.")
                 continue 
        while attempt_for_new_pair < max_attempts_per_iteration and not processed_new_in_this_iteration:
            if len(current_words_pool_for_iteration) < 2:
                 print("Ran out of word pairs for this iteration. Refreshing pool.")
                 current_words_pool_for_iteration = list(set(get_initial_words(load_json(json_file_path))))
                 if len(current_words_pool_for_iteration) < 2:
                     print("Still not enough words after refresh during iteration. Breaking attempt loop.")
                     break 
            word1 = random.choice(current_words_pool_for_iteration)
            word2 = random.choice(current_words_pool_for_iteration)
            attempt_for_new_pair += 1 
            if word1 == word2:
                continue
            pair_tuple = tuple(sorted([word1.lower(), word2.lower()]))
            if pair_tuple not in tried_combinations and pair_tuple not in existing_recipes:
                tried_combinations.add(pair_tuple) 
                print(f"Attempting combination ({attempt_for_new_pair}/{max_attempts_per_iteration} for this iter): {word1} + {word2}")
                api_response = send_combination_request(word1, word2, driver)
                if api_response:
                    if process_result(api_response):
                        processed_in_session_count +=1
                        processed_new_in_this_iteration = True 
                        data = load_json(json_file_path)
                        words = list(set(get_initial_words(data)))
                        current_words_pool_for_iteration = list(set(words)) 
        if not processed_new_in_this_iteration: 
            print(f"Could not find and process a new, untried combination after {attempt_for_new_pair} attempts for iteration {i+1}.")
    print(f"\nTotal new elements/recipes processed in this session: {processed_in_session_count}")
try:
    run_iterations_sequentially()
except Exception as e:
    print(f"An unexpected error occurred during the main iteration process: {type(e).__name__} - {e}")
    input("Press Enter to acknowledge and exit...")
finally:
    if driver:
        try:
            driver.quit()
            print("Chrome driver quit successfully.")
        except Exception as e:
            print(f"Error quitting driver: {type(e).__name__} - {e}")
            input("Press Enter to acknowledge...")
    print("\nScript finished.")
    input("Press Enter to close this window...")