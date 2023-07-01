from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd

#firefox option browser
firefox_option = Options()
firefox_option.add_argument('--headless')
firefox_option.add_argument('--window_size=1600, 900')
firefox_option.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')
# firefox_option.add_argument('--disable-popup-blocking')


#path of browser
browser = Service(executable_path='geckodriver')

#calling firefox driver
driver = webdriver.Firefox(service=browser)
# driver = webdriver.Firefox(service=browser, options=firefox_option)


#url tokopedia yang akan di scrap
# url = 'https://www.tokopedia.com/p/fashion-pria/batik-pria/kemeja-batik-pria?page=1'
url = input('input url address: ')

isi_data = False
while not isi_data:
    #banyak halaman produk yang discrap (masukkan "0" jika semua atau tidak tau)
    max_page = int(input('banyak halaman diambil: '))

    #banyak data yang ingin didapatkan:
    data_scrap = int(input('banyak data didapatkan: '))

    if data_scrap != 0:
        max_page = 0
    
    if max_page == 0 and data_scrap == 0:
        print("Error, data didapatkan salah!")
    else:
        isi_data= True

#nama file hasil data scrap format .csv
name_file = input('input nama filemu: ')


print('please wait, sedang mengambil data...')


def search_link_kategori(indeks):
    link = driver.find_element(
        by=By.XPATH,
        value=f'//*[@id="zeus-root"]/div/div[2]/div/div[2]/div/div[2]/div[3]/div[2]/div[3]/div[{indeks}]/a'
    ).get_attribute('href')                                    
    return link

def search_link_by_column(indeks):
    link = driver.find_element(
        by=By.XPATH,
        value=f'(//div[@class="css-llwpbs"]/div//div/div/div/div/div[2]/a)[{indeks}]'
    ).get_attribute('href')                                    
    return link

def search_link_by_toko(indeks):
    link = driver.find_element(
        by=By.XPATH,
        value=f'(//div[@class="css-1sn1xa2"]/div/div/div/div/div/div[2]/a)[{indeks}]'
    ).get_attribute('href')                                    
    return link

etalase =[]
driver.get(url)

page = 1
if max_page == 0:
    page = 0

while page <= max_page:    
    driver.implicitly_wait(30)
    driver.delete_all_cookies()
    driver.maximize_window()        

    if max_page == 0 and data_scrap == 0:
        break
    
    for x in range(3):
        for y in range (0,10):
            ordinat = y*900
            driver.execute_script(f'window.scrollTo(0,{ordinat})')
            time.sleep(1)

    #search direct kategori tokped
    products = driver.find_elements(
            by=By.XPATH, 
            value='//div[@class="css-bk6tzz e1nlzfl2"]'
        )        
    search_ = 0
    #product direct kategori
    #len(products) ==75
    filter = [1,8,15]       

    #search by kolom search
    if search_ == 0:
        if not products:
            products = driver.find_elements(
                by=By.XPATH, 
                value='//div[@class="css-llwpbs"]'
            )
            search_ = 1  
            #product by kolom search product
            # len(products)  == 80
            filter =[1,4,7,16]  
    
    #search by produk toko
    if search_ == 1:
        if not products:
            products = driver.find_elements(
                by= By.XPATH,
                value='//div[@class="css-1sn1xa2"]'
            )
            search_ =2
            filter =[]


    # print(products)
    # print(len(products))
    time.sleep(5)
    
    for product in range(1, int((len(products)/5))+1):
        if data_scrap !=0:
            if len(etalase) >= data_scrap:
                break          

        for loop in range(1,6):                                      
            if product in filter:
                pass
            else:
                factor = 5-loop
                indeks = (product*5)-factor

                if search_ == 0:
                    link= search_link_kategori(indeks)
                elif search_ == 1:
                    link= search_link_by_column(indeks)
                elif search_ == 2:
                    link = search_link_by_toko(indeks)                                

                etalase.append(link)
                driver.delete_all_cookies() 

            if data_scrap !=0:
                if len(etalase) >= data_scrap:
                    break                
          
    if data_scrap !=0:
        if len(etalase) >= data_scrap:
            page = max_page+1       

    iframe_list = driver.find_elements(
        by=By.TAG_NAME,
        value="iframe"
    )
    size = len(iframe_list)
    # print(size)
    # print(iframe_list)
    
    driver.switch_to.frame(iframe_list[0])
    try:
        close_pop = driver.find_element(
            by=By.XPATH,
            value='//div[@aria-label="Tutup"]'
        )
    except NoSuchElementException:
        close_pop = False

    if close_pop:
        close_pop.click()    
        
    driver.switch_to.default_content()
    driver.implicitly_wait(10)
    time.sleep(5)    
    # next = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Laman berikutnya"]'))
    # )
    next = driver.find_element(
        by=By.XPATH,
        value='//button[@aria-label="Laman berikutnya"]'
    )
    if next:
        next.click()
        if max_page != 0:
            page = page + 1                       
    

data_produk=[]
for x in etalase:
    # print(x)
    driver.get(x)
    driver.delete_all_cookies()
    driver.implicitly_wait(30)    

    time.sleep(1)
    for a in range(3):
        for b in range (0,5):
            ordinat = b*900
            driver.execute_script(f'window.scrollTo(0,{ordinat})')
            time.sleep(0.5)    
    
    name_product = driver.find_element(
        by=By.XPATH, 
        value='//*[@id="pdp_comp-product_content"]/div/h1'
    ).text    
    harga = driver.find_element(
        by=By.XPATH,
        value='//*[@id="pdp_comp-product_content"]/div/div[2]/div[@data-testid="lblPDPDetailProductPrice"]'
    ).text
    try:
        terjual = driver.find_element(
            by=By.XPATH,
            value='//*[@id="pdp_comp-product_content"]/div/div[1]/div/p[@data-testid="lblPDPDetailProductSoldCounter"]'
        ).text
    except NoSuchElementException:
        terjual = 'tidak ada data'
    try:
        rating = driver.find_element(
            by=By.XPATH,
            value='//span[@class="score"]'
        ).text
    except NoSuchElementException:
        rating = 'belum dirating'

    #konversi harga
    price = harga.split('Rp')
    harga = ''.join(price)
    price  = harga.split('.')
    harga = ''.join(price) 

    #konversi terjual
    if terjual != 'tidak ada data':
        order = terjual.split('Terjual ')
        terjual = ''.join(order)
        order = terjual.split('barang berhasil terjual')
        terjual = ''.join(order)
        if '+' in terjual:
            order = terjual.split('+')
            terjual = ''.join(order)
            if 'rb' in terjual:
                order = terjual.split('rb')
                terjual = ''.join(order)
                terjual = float(terjual) * 1000
                terjual = int(terjual)

    # print(name_product)
    lis_jual = {
        'nama produk' : name_product,
        'harga (Rp)' : harga,
        'terjual' : terjual,
        'rating' : rating,
        'link' : x,
    }
    data_produk.append(lis_jual)
    print(lis_jual)
    time.sleep(1)
    driver.delete_all_cookies()


driver.quit()
# detail_data = pd.DataFrame(batik)

detail_data = pd.DataFrame(data_produk)

detail_data.to_csv(f'{name_file}.csv')
print(detail_data)
print('\n')
print('finished..!')



