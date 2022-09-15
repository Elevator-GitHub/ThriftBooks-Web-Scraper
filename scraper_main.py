
from unittest import result
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep 



driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
def driver_wait(driver,element, time=5, wait_type=EC.element_to_be_clickable):
        try:
                element = WebDriverWait(driver, timeout=time).until(wait_type(element))
                return element
        except Exception as ex:
            pass
def thrift_book(driver):
   with open('ISBN-test-input-file.csv','r') as file :
       test_isbns=file.readlines()
    
       test_isbns_filtered=[]
       for i in test_isbns:
           i=i.replace(',','')
           i=i.replace('\n','')
           i=i.replace('ISBN','')
           if i!='' and i!=None:
               test_isbns_filtered.append(i)
       test_isbns=test_isbns_filtered
   driver.get('https://www.thriftbooks.com/')
   list_of_results=[]
   for isbn in test_isbns:
       try:
         search_box=driver.find_element(By.XPATH,'/html/body/div[3]/div/div[2]/div[2]/div[1]/div/div/input')
       except Exception as c:
         if 'selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element:' in str(c):
             driver.quit()
             sleep(60)
             driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
             driver.get('https://www.thriftbooks.com/')
             try:
                 search_box=driver.find_element(By.XPATH,'/html/body/div[3]/div/div[2]/div[2]/div[1]/div/div/input')
             except:
                 pass

         search_box=driver.find_element(By.XPATH,'/html/body/div[4]/div/div[2]/div[2]/div[1]/div/div/input')
       
       search_box.clear()
       search_box.send_keys(isbn)
       search_box.send_keys(Keys.RETURN)
       try_=0
       try:
           sleep(3)
           price_book=driver.find_element(By.XPATH,'/html/body/div[3]/div/div[3]/div[1]/div[2]/div/div/div[1]/div/div[3]/div/div[2]/span[2]').text
           link=str(driver.current_url)
           Quant=driver.find_element(By.XPATH,'/html/body/div[3]/div/div[3]/div[1]/div[2]/div/div/div[1]/div/div[3]/div/p[2]').text
           name_of_book=driver.find_element(By.XPATH,'/html/body/div[3]/div/div[3]/div[1]/div[2]/div/div/div[1]/div/div[2]/div[1]/h1').text
           avai='available'
           if price_book != None :
              list_of_results.append(str(f'{isbn},{name_of_book},{avai},{price_book},{Quant.split(" ")[0]},{link}'))
           try_=1
       except Exception as ex:
           pass
       if try_==0:
           try:
             name_of_book=driver.find_element(By.XPATH,'/html/body/div[4]/div/div[3]/div[1]/div[1]/div/div/div/div/div[2]/div[1]/h1').text
             Quant=driver.find_element(By.XPATH,'/html/body/div[4]/div/div[3]/div[1]/div[1]/div/div/div/div/div[3]/div/div/p[1]').text
             link=driver.current_url
             avai='Unavailable'
             price_book=''
             if Quant!=None:
                 list_of_results.append(str(f'{isbn},{name_of_book},{avai},{price_book},{Quant},{link}'))
                 try_=1
           except:
               pass
       elif try_==0 :
           name_of_book=''
           price_book=''
           avai='not found'
           Quant=''
           link=''
           list_of_results.append(str(f'{isbn},{name_of_book},{avai},{price_book},{Quant},{link}'))
   return list_of_results 


def output(list_1):
    with open('results.csv','w') as file:           
        file.writelines(list_1)


output(thrift_book(driver))

sleep(150)

