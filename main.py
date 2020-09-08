from selenium import webdriver
import os,argparse
import pandas as pd
from time import sleep



# Parameters
name = 'laureatta_2020'
psw = 'TTw^PnyRSQsr'
# dilettaleotta, chiaraferragni, selenagomez, kyliejenner, kendalljenner
# realdonaldtrump, jayalvarrez, kingjames, shawnmendes, therock
target = 'jayalvarrez'
time_wait = 20
time_sleep = 5
n_swipe = 1000

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def open_chrome():
    from webdriver_manager.chrome import ChromeDriverManager
    driver = webdriver.Chrome(ChromeDriverManager().install())
    #driver = webdriver.Chrome()
    driver.get('https://www.instagram.com')
    return driver

def login(name, psw):
    # name
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(name)
    # psw
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(psw)
    # accedi
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()
    # salva
    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/section/div/button').click()
    # non ora
    driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
    
def open_profile(target):
    # cerca
    driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input').send_keys(target)
    # risultato
    driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div[2]/div/a[1]/div/div[2]/span').click()
    
def get_description():
    try:
        descrizione = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span').text
    except:
        descrizione = ''
    return descrizione
        
def get_image_url():
    body = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/div/div/div[1]')
    bodyHTML = body.get_attribute('innerHTML')
    url = bodyHTML.split('src="')[-1].split('" style=')[0].split('"')[0].replace("amp;", "")
    if len(url) == 0:
        body = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div[1]')
        bodyHTML = body.get_attribute('innerHTML')
        url = bodyHTML.split('src="')[-1].split('" style=')[0].split('"')[0].replace("amp;", "")
    return url

def swipe(n_post, target, time_sleep, APP_ROOT):
    dict_data = {}
    for i in range(n_post):
        if i == 0:
            try:
                driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[3]/article/div/div/div[1]/div[1]/a/div').click()
            except:
                driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[2]/article/div[1]/div/div[1]/div[1]/a/div').click()
            descrizione = get_description()
            url = get_image_url()
            driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div/a').click()
        else:
            descrizione = get_description()
            url = get_image_url()
            driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div/a[2]').click()
        
        dict_data[i+1] = [url, descrizione]
        df_data = pd.DataFrame(dict_data)
        df_data = df_data.T
        df_data.rename(columns={0: "url", 1: "txt"}, inplace=True)
        # sovrascrivo file
        old_destination = os.path.join(APP_ROOT, 'output', os.path.basename(target + '-' + str(i) + '.pkl'))
        if os.path.exists(old_destination):
            os.remove(old_destination)
        new_destination = os.path.join(APP_ROOT, 'output', os.path.basename(target + '-' + str(i+1) + '.pkl'))
        df_data.to_pickle(new_destination)
        
        print(i+1, 'su', n_post)
        sleep(time_sleep)
    

# Processi
driver = open_chrome()
driver.implicitly_wait(time_wait)
login(name, psw)
open_profile(target)
swipe(n_swipe, target, time_sleep, APP_ROOT)

# open 
path = './output/' + target + '-' + str(n_swipe) + '.pkl'
data = pd.read_pickle(path)
# data.iloc[:,:].txt.apply(lambda x: len(x.split(' '))).mean()

