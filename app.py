import os
import time

try:
  import playwright
except ImportError:
  os.system('python -m pip install playwright')
  os.system('playwright install')
# -- above lines try to install requests module if not present
# -- if all went well, import required module again ( for global access)

from playwright.sync_api import sync_playwright
import time
from re import sub
from decimal import Decimal
browser = None
def scrap():
    
    with sync_playwright() as p:
        global browser
        def send_simple_message(value):
            os.system('curl -X POST "https://api.telegram.org/bot5043944167:AAFgFh4oLtg5yMOa7qnjMD1ufZYkp_xImYc/sendMessage" -d "chat_id=-770598851&text='+value+'"')
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
        send_simple_message('Monitoring..')
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
