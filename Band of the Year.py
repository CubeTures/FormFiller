from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
loops = 1000000

def restart():
    print("Restarting...")
    loop(loops)

def click(xpath, message=''):
    driver.execute_script("arguments[0].click();", WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath))))
    if message != '':
        print(message)
def click_if_there(xpath):
    try:
        driver.execute_script("window.scrollTo(0, 2000)")
        driver.execute_script("arguments[0].click();", WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, xpath))))
    except:
        #print('Results not already on screen')
        pass

def captcha(xpath):
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    return driver.find_element(By.XPATH, xpath).text
def solve(prob):
    problem = prob.split(' ')
    for x in range(len(problem)):
        if problem[x].isdigit():
            problem[x] = int(problem[x])
    if problem[1] == '+':
        return str(problem[0] + problem[2])
    elif problem[1] == '-':
        return str(problem[0] - problem[2])
    elif problem[1] == '*':
        return str(problem[0] * problem[2])
    elif problem[1] == '/':
        return str(problem[0] / problem[2])
def fill(xpath, response):
    form = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    form.send_keys(response)
def try_captcha():
    try:
        problem = captcha('//*[@id="captcha_11224424"]/span')
        answer = solve(problem)
        print(problem + " " + answer)
        fill('//*[@id="answer_11224424"]', answer)
        click('//*[@id="pd-vote-button11224424"]')
    except:
        print('No Captcha to Solve')

def read(xpath, message):
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    print(message + driver.find_element(By.XPATH, xpath).text)
    return driver.find_element(By.XPATH, xpath).text[1:-1]
def compare(val1, val2):
    diff = float(val2) - float(val1)
    print(str(diff) + "% difference")
    if diff <= -1:
        return -1

def main_loop():
    click_if_there('//*[@id="PDI_container11224424"]/div/div/div/div/div[5]/div/span[1]/a')
    try:
        click('//*[@id="PDI_answer51302151"]')  # Selecting Seven Lakes
        click('//*[@id="pd-vote-button11224424"]')  # Entering Captcha
        try_captcha()
        sl = read('//*[@id="pds-results"]/li[5]/label/span[2]/span[1]', 'Seven Lakes:')
        f = read('//*[@id="pds-results"]/li[1]/label/span[2]/span[1]', 'Foster: ')
        if compare(sl, f) == -1:
            return -1
        click('//*[@id="PDI_container11224424"]/div/div/div/div/div[5]/div/span[1]/a')  # Back to Voting
    except:
        restart()
def loop(times):
    driver.get('https://www.vype.com/Texas/Houston/vype-hou-public-school-band-of-the-year-fan-poll-presented-by-sun-and-ski-sports')
    driver.execute_script("window.scrollTo(0, 200)")
    click('//*[@id="col-center"]/div[3]/div[3]/div/div[4]/span[1]')  # Read More
    for x in range(times):
        if main_loop() == -1:
            break
        print("Form Completed " + str(x + 1) + " Times")


loop(loops)
