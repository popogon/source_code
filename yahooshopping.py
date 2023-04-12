# ヤフーショッピングの自分の注文履歴から情報を取得します
# 古いコードなので動かないかもしれません
from time import sleep
from turtle import onclick
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re

# chromedriverのパス
chrome_pass = r''

def purchase_history():
    options = Options()
    options.add_argument("--incognito")
    crawl_list = []

    try:
        driver = webdriver.Chrome(chrome_pass,options=options)
        sleep(2)
        url = "https://shopping.yahoo.co.jp/?sc_i=shp_pc_top_MhdLogo"

        driver.get(url)
        sleep(5)
        #ログイン画面へ遷移
        element = driver.find_element_by_link_text("ログイン")
        element.click()
        sleep(2)
        #自分のYahooアドレス
        yahoo_mail = ""
        id_box = driver.find_element_by_name("login")
        id_box.send_keys(yahoo_mail)
        button = driver.find_element_by_id("btnNext")
        button.click()
        sleep(3)
        #確認コードは手動
        code = input("コードを入力してください")
        sleep(3)
        pass_box = driver.find_element_by_id("code")
        pass_box.send_keys(code)
        code_button = driver.find_element_by_id("btnSubmit")
        code_button.click()
        sleep(3)
        history = driver.find_element_by_link_text("注文履歴")
        history.click()
        

        sleep(4)
        
   
        a = driver.find_elements_by_class_name("elButton")
        elements = []
        for j in range(10):
            a = driver.find_elements_by_class_name("elButton")
            button = a[j].find_element_by_class_name("elDetail")
           
            button.click()
        


            sleep(5)
    
            soup = BeautifulSoup(driver.page_source, "html.parser")
            date = soup.find("dd",class_="elDetail").text
            date=re.sub('\n',"",date) 

            title_content = soup.find("dd",class_="elName").text
            title_content=re.sub('\n',"",title_content) 

            price_content = soup.find("div",id="total")
            price = price_content.find("dd").text
            price=re.sub('\n',"",price) 

            store_content = soup.find("p",class_="elStore").text
            store_content=re.sub('\n',"",store_content) 
                    
            d = {
                "購入日":date,
                "商品名":title_content,
                "金額":price,
                "販売店":store_content
            }

            crawl_list.append(d)

            driver.back()
            sleep(5)
            


        print(crawl_list)
        
        driver.quit()
        print("chromedriverを閉じました")

    finally:    
        driver.quit()
        print("chromedriverを閉じました")

purchase_history()


