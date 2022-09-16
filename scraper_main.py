

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep 
from multiprocessing import freeze_support,set_start_method,get_context



def driver_wait(driver,element, time=5, wait_type=EC.element_to_be_clickable):
        try:
                element = WebDriverWait(driver, timeout=time).until(wait_type(element))
                return element
        except Exception as ex:
            pass
def thrift_book(test_isbns,order_number):
   print('thrift')
   
   sleep(order_number*50)
   driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


   driver.get('https://www.thriftbooks.com/')
   list_of_results=[]
   for isbn in test_isbns:
       try:
         search_box=driver.find_element(By.CSS_SELECTOR,'input.Search-input')
       except Exception as c:
         if 'selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element:' in str(c):
             driver.quit()
             sleep(60)
             driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
             driver.get('https://www.thriftbooks.com/')
             try:
                 search_box=driver.find_element(By.XPATH,'input.Search-input.is-empty')
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
              list_of_results.append(str(f'{isbn},{name_of_book},{avai},{price_book},{Quant.split(" ")[0]},{link}\n'))
              try_=1
       except Exception as ex:
           pass
       if try_==0:
           try:
             name_of_book=driver.find_element(By.XPATH,'/html/body/div[4]/div/div[3]/div[1]/div[1]/div/div/div/div/div[2]/div[1]/h1').text
             Quant=driver.find_element(By.XPATH,'/html/body/div[4]/div/div[3]/div[1]/div[1]/div/div/div/div/div[3]/div/div/p[1]').text
             link=driver.current_url
             avai='Unavailable'
             price_book='none'
             if Quant!=None:
                 list_of_results.append(str(f'{isbn},{name_of_book},{avai},{price_book},{Quant},{link}\n'))
                 try_=1
           except:
               pass
       elif try_==0 :
           name_of_book='none'
           price_book='none'
           avai='not found'
           Quant='none'
           link='none'
           list_of_results.append(str(f'{isbn},{name_of_book},{avai},{price_book},{Quant},{link}\n'))
   driver.quit()
   return list_of_results 

def devide():
    print('out')

    with open('ISBN-test.csv','r') as file :
       test_isbns=file.readlines()
    
       test_isbns_filtered=[]
       for i in test_isbns:
           i=i.replace(',','')
           i=i.replace('\n','')
           i=i.replace('ISBN','')
           i=i.replace('ï»¿','')
           i=i.replace(' ','')


           if i!='' and i!=None:
               test_isbns_filtered.append(i)
       test_isbns=test_isbns_filtered
    length=int(len(test_isbns)/5)
    final_list=[]
    x=0
    for l in range(5):

     sub_list=[]
     for k in range(x,length+x):
       sub_list.append(test_isbns[k])

     final_list.append(sub_list)
     x=x+length          


    check_len=length*5
    final_list_1=final_list
    for w in range(len(test_isbns)-check_len):
        try:
            c=0
            for p in final_list:
                sub=test_isbns[check_len]
                final_list_1[c].append(sub)
                c=c+1
                check_len=check_len+1
        except:
            pass
    return final_list_1
        
def output(list_1):
  print('out')                 
  x_1=0
  while x_1<1:
   try:
     with open('results.csv','w') as file: 
        file.write('ISBN,Book Title,Result (not found- unavailable- available) ,Price (if available),Quantity (if available),link(available),Buyer (leave blank)\n')          
        file.writelines(list_1)
        x_1=x_1+1
   except:
       sleep(40)
def hyper(list_1,order):
    output(thrift_book(test_isbns=list_1,order_number=order))
if __name__=="__main__":
    set_start_method("spawn")
    freeze_support()
    

    args=devide()
    final_args=[]
    e=0
    for l in args:
        final_args.append([l,e])
        e=e+1

    with get_context("spawn").Pool(processes=5) as pool:
        pool.starmap(hyper,final_args)



 
