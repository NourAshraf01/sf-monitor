from playwright.sync_api import sync_playwright
import time
import yagmail
from re import sub
from decimal import Decimal
import telegram_send
yag = yagmail.SMTP('nourashraf225@gmail.com', 'llcalsqrernmkogw')
browser = None
def scrap():
    
    with sync_playwright() as p:
        global browser
        def send_simple_message(value):
            global yag
            #yag.send(['nourashrafde@gmail.com','ramyamr900@yahoo.com','ramyamr200@yahoo.com','aeldash99@gmail.com'],subject= 'El7a2 flosak',contents= value)
            telegram_send.send(messages=[value])
        browser = p.webkit.launch()
        page = browser.new_page()
        page.goto("https://polygon.poocoin.app/tokens/0xdf9b4b57865b403e08c85568442f95c26b7896b0")
        def refresh():
            nonlocal page
            page.close()
            page = browser.new_page()
            page.goto("https://polygon.poocoin.app/tokens/0xdf9b4b57865b403e08c85568442f95c26b7896b0")
        startValue = None
        refreshTime = time.time()
        startTime = time.time()
        while True:
            if time.time() - startTime >= 60:
                refresh()
                startTime = time.time()
            try:
                val = page.query_selector('.mb-1.d-flex.flex-column.lh-1 span.text-success')
                val = val.inner_text()
                decimalVal = float(Decimal(sub(r'[^\d.]', '', val)))
                if startValue == None:
                    startValue = decimalVal
                if abs(startValue - decimalVal) >= 0.15 :
                    print('sending',startValue,decimalVal)
                    startValue = decimalVal
                    send_simple_message(val)
                print(val)
                refreshTime=time.time()
                page.reload()
            except:
                if (time.time()- refreshTime) > 2:
                    refreshTime=time.time()
                    page.reload()
                continue
            time.sleep(1)
while True:
    try: 
        scrap()
    except:
        continue