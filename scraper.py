import csv
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Firefox
from random import randint


# Use Firefox browser and navigate to Twitter explore page
driver = Firefox()
driver.maximize_window()
wait = WebDriverWait(driver, 30)
driver.get('https://www.twitter.com/explore')

# Search for KU-related tweets during 2022-23 basketball season
searchBox = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Search query"]')))
searchBox.send_keys('(Jayhawks OR "University of Kansas" OR #RockChalk OR #KUbball OR #PayHeed) until:2023-04-01 since:2022-12-01 lang:en')
searchBox.send_keys(Keys.RETURN)
sleep(5)

# Initial tweet collection
# Only records contents
content = []
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"]')))
tweets = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
for tweet in tweets:
  content.append(tweet.find_element(By.CSS_SELECTOR, 'div[lang]').text)

# Collect tweets until end of search results
noNewTweets = 0
Y = 1080
while noNewTweets < 3:

# Scroll down
  driver.execute_script("window.scrollTo(0," + str(Y) + ")")
  Y += 1080

# Check if page has loaded
  state = ""
  while state != "complete":
    sleep(randint(3, 5))
    state = driver.execute_script("return document.readyState")

# Tweet collection
  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"]')))
  tweets = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
  new = 0
  for tweet in tweets:
# Only add contents that have not yet been collected    
    c = tweet.find_element(By.CSS_SELECTOR, 'div[lang]').text
    if c not in content:
      new += 1
      content.append(c)
  print ("Number of new tweets", temp)
  if new == 0:
    noNewTweets += 1

# Put results into .csv file
with open('tweets.csv','w', newline='') as csvfile:
  tweetWriter = csv.writer(csvfile, delimiter=' ')
  for c in content:
    tweetWriter.writerow([c])


print(content)

