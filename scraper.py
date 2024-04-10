import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def setup_driver():
    page_url = 'https://www.adamchoi.co.uk/teamgoals/detailed'

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(page_url)

    all_matches_button = driver.find_element(By.XPATH, value='//label[@analytics-event="All matches"]')
    all_matches_button.click()

    time.sleep(0.5)
    football_matches_table = driver.find_element(By.TAG_NAME, value='table')
    football_matches = football_matches_table.find_elements(By.TAG_NAME, value='tr')

    dates = []
    home_teams = []
    scores = []
    away_teams = []

    for football_match in football_matches:
        dates.append(football_match.find_element(By.XPATH, value='./td[1]').text)
        home_teams.append(football_match.find_element(By.XPATH, value='./td[2]').text)
        scores.append(football_match.find_element(By.XPATH, value='./td[3]').text)
        away_teams.append(football_match.find_element(By.XPATH, value='./td[4]').text)

    df = pd.DataFrame({
        'date': dates,
        'home_team': home_teams,
        'score': scores,
        'away_teams': away_teams,
    })

    csv_file_path = 'generated/football_matches.csv'
    json_file_path = 'generated/football_matches.json'

    try:
        df.to_csv(csv_file_path, index=False)
        print(f'Successfully saved data to file "{csv_file_path}"')
    except Exception as e:
        print(f'Error saving data to file "{csv_file_path}": \n> {e}')

    try:
        df.to_json(json_file_path, index=False, indent=2)
        print(f'Successfully saved data to files "{json_file_path}"')
    except Exception as e:
        print(f'Error saving data to file "{json_file_path}": \n> {e}')

    driver.quit()
