
import time
import random
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
from fake_useragent import UserAgent

#define function
def choose(command):
    if command == "1":
        return options[0]
    elif command == "2":
        return options[1]
    elif command == "3":
        return options[2]
    elif command == "4":
        return random.choice(options)

#initialize variables
choice = ""
options = ["Vote 1", "Vote 2", "Vote 3"]
vote1_votes = 0
vote2_votes = 0
vote3_votes = 0
start_time = 0
end_time = 0
chrome_options = Options()
chrome_options.add_argument('--log-level=3')
ua = UserAgent()
userAgent = ua.random
chrome_options.add_argument(f'user-agent={userAgent}')

while True:
    #print instructions
    print("\n     Website Vote Bot\n")
    print("Enter 1 to vote for Vote 1")
    print("Enter 2 to vote for Vote 2")
    print("Enter 3 to vote for Vote 3")
    print("Enter 4 to vote for random")
    print("Enter \"Quit\" to exit\n")

    #what to do
    command = input("1, 2, 3, 4 or Quit? ")

    #check input
    if command == "Quit":
        exit()
    elif command not in {"1", "2", "3", "4"}:
        print("Try again...")
        continue

    #how many times to run the script
    number_of_votes = input("Vote how many times? ")

    #check input
    try:
        int(number_of_votes)
    except ValueError:
        print("Enter a number...")
        continue

    #show browser option, no check needed
    headless = input("Show browser (y/n)? ")

    if headless != "y":
        chrome_options.add_argument('headless')

    #begin automation----------------------------------

    #open browser and begin timer
    start_time = time.time()

    driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", options=chrome_options)

    #tqdm() progress bar
    for _ in tqdm(range(int(number_of_votes))):

        click_try = 0
        
        try:
            #interpret input with choose funtion
            choice = choose(command) #must be in loop for random to function correctly
            #navigate to website and find buttons
            driver.get("URL DA VOTAÇÃO")
            driver.execute_script("window.scrollTo(0, 2000)") #avoids spam detection in headless
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "309")))
            
            try:
                btnCookies = driver.find_element_by_xpath("//button[@class='banner-lgpd-consent__accept']")
                btnCookies.click()
            except:
                pass
            vote = driver.find_element_by_xpath("//button[@class='poll_question--vote']")
            test = driver.find_elements_by_xpath(".//span[@class='text']")
            for x in test:
                if(x.text == choice):
                    spanVote = x
            #make sure button is selected, try one more time to switch to frame and select choice before breaking on error
            while click_try < 1:
                time.sleep(1)
                spanVote.click()
                click_try += 1
                
            #time delays avoid spam detection
            time.sleep(1)
            vote.click()
            time.sleep(2)
            
            #count vote (only if successful)
            if choice == "Vote 1":
                vote1_votes += 1
            elif choice == "Vote 2":
                vote2_votes += 1
            elif choice == "Vote 3":
                vote3_votes += 1
                
        except NoSuchElementException as e: #if there is an error...
            error_message = str(e)
            stack_trace = str(traceback.format_exc())
            write_logs(error_message, stack_trace)
            driver.close()
            exit("Not able to reach url")

    #close browser and stop timer
    driver.quit()
    end_time = time.time()
    break

    #end automation------------------------------------

#final report and exit
print("\nProcess complete in " + str(round(end_time - start_time, 2)) + " seconds.")
print("Times voted for Vote 1: " + str(vote1_votes))
print("Times voted for Vote 2: " + str(vote2_votes))
print("Times voted for Vote 3: " + str(vote3_votes))
print("Errors: " + str(int(number_of_votes) - (vote1_votes + vote2_votes + vote3_votes)))
exit()
