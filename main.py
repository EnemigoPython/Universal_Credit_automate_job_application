from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date, datetime


class InvalidFileError(Exception):
    pass


def wait(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "body")))


def submit(driver):
    driver.find_element_by_id('id-submit-button').click()


def main():
    try:
        with open('login.txt', 'r') as login:
            content = login.readlines()
            if len(content) == 3:
                user = content[0][:-1]
                password = content[1][:-1]
                security = content[2]
            else:
                raise InvalidFileError("The file 'login.txt' does not meet the requirements of the program.")
    except FileNotFoundError:
        print('No existing login details found, creating new txt:')
        user = input('Type username: ')
        password = input('Type password: ')
        security = input('Type answer to security question: ')
        with open('login.txt', 'w') as login:
            login.write(user + "\n")
            login.write(password + "\n")
            login.write(security)

    number_of_submits = input('How many submissions would you like to make? ')
    job_title = []
    company = []
    notes = []
    if number_of_submits.isnumeric() and int(number_of_submits) > 1:
        number_of_submits = int(number_of_submits)
    else:
        print('Singular submission.')
        number_of_submits = 1
    for i in range(number_of_submits):
        job_title.append(input('Enter job title: '))
        company.append(input('Enter company or agency: '))
        notes.append(input('Enter notes (optional): '))
    
    # insert the path/driver type of your browser here
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)

    driver.get("https://www.universal-credit.service.gov.uk/sign-in")
    driver.find_element_by_id('id-userName').send_keys(user)
    driver.find_element_by_id('id-password').send_keys(password)
    submit(driver)

    wait(driver)

    driver.find_element_by_id('id-answer').send_keys(security)
    submit(driver)

    wait(driver)

    driver.find_element_by_xpath("//a[@href='/journal']").click()
    driver.find_element_by_id('id-add-a-journal-entry-link').click()

    wait(driver)

    driver.find_element_by_id('clickable-WORK_SEARCH_JOB_APPLICATIONS').click()
    submit(driver)

    wait(driver)

    for i in range(number_of_submits):
        driver.find_element_by_id('add-job').click()

        wait(driver)

        driver.find_element_by_id('id-jobTitle').send_keys(job_title[i])
        driver.find_element_by_id('id-employer').send_keys(company[i])
        driver.find_element_by_id('clickable-APPLIED').click()
        if notes != "":
            driver.find_element_by_id('id-notes').send_keys(notes[i])
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "id-applicationDate.day")))
        driver.find_element_by_id("id-applicationDate.day").send_keys(date.today().strftime("%d"))
        driver.find_element_by_id("id-applicationDate.month").send_keys(date.today().strftime("%m"))
        driver.find_element_by_id("id-applicationDate.year").send_keys(datetime.now().year)
        submit(driver)

        wait(driver)
    print("Finished")
    input('Any key to exit')
    driver.quit()

if __name__ == '__main__':
    main()
