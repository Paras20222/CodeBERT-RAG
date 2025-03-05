import os
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def get_problem_data(problem_url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(problem_url)
    time.sleep(2)  # Allow time for page to load
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    
    problem_data = {}
    
    # Extract problem title
    title_tag = soup.find('div', class_='title')
    problem_data['title'] = title_tag.text.strip() if title_tag else 'N/A'
    
    # Extract problem statement
    statement_div = soup.find('div', class_='problem-statement')
    problem_data['statement'] = statement_div.get_text(separator='\n', strip=True) if statement_div else 'N/A'
    
    # Extract input and output specifications
    input_spec = soup.find('div', class_='input-specification')
    problem_data['input_specification'] = input_spec.get_text(separator='\n', strip=True) if input_spec else 'N/A'
    
    output_spec = soup.find('div', class_='output-specification')
    problem_data['output_specification'] = output_spec.get_text(separator='\n', strip=True) if output_spec else 'N/A'
    
    # Extract sample test cases
    sample_tests = []
    sample_blocks = soup.find_all('div', class_='sample-test')
    for sample_block in sample_blocks:
        inputs = sample_block.find_all('div', class_='input')
        outputs = sample_block.find_all('div', class_='output')
        
        for i, o in zip(inputs, outputs):
            input_text = i.find('pre').get_text(separator='\n', strip=True)
            output_text = o.find('pre').get_text(separator='\n', strip=True)
            sample_tests.append({'input': input_text, 'output': output_text})
    
    problem_data['sample_tests'] = sample_tests
    
    return problem_data

def save_problem_data(problem_url, output_folder='problems'):
    problem_data = get_problem_data(problem_url)
    os.makedirs(output_folder, exist_ok=True)
    file_name = os.path.join(output_folder, f"{problem_data['title'].replace(' ', '_')}.json")
    
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(problem_data, f, ensure_ascii=False, indent=4)
    
    print(f"Problem data saved to {file_name}")

if __name__ == '__main__':
    problem_url = input("Enter Codeforces problem URL: ")
    save_problem_data(problem_url)
