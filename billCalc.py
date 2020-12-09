import requests,bs4, re, os
from selenium import webdriver
import time
from venmo_api import Client,PaymentPrivacy
#Bill info holds - roommates venmos, path to the chrome driver, rent price and urls
from billInfo import *

priceRegex = re.compile(r'([0-9]+[\.]*[0-9]*)')

username = os.environ.get('USERNAME')
access_token = os.environ.get('VENMO_ACCESS_TOKEN')
password = os.environ.get('PASS')

driver =  webdriver.Chrome(CHROME_DRIVER_PATH)
driver.get(electricUrl)
userElem = driver.find_element_by_css_selector('#user-id')
passElem = driver.find_element_by_css_selector('#password')
userElem.send_keys(username)
passElem.send_keys(password)

driver.find_element_by_css_selector('#loginBtn').click()
time.sleep(5)
amerenPriceElem = driver.find_element_by_css_selector('#billing > div.c-billing-and-payments-overview.col-md-6 > p.currency-amount')
amerenPriceWCurr = amerenPriceElem.text.strip()
mo = priceRegex.search(amerenPriceWCurr)
amerenPrice = mo.group()
driver.quit()
print("Electric Bill: "+amerenPrice)

driver = webdriver.Chrome(CHROME_DRIVER_PATH)
driver.get(gasUrl)
userElem = driver.find_element_by_css_selector('#loginEmail')
passElem = driver.find_element_by_css_selector('#loginPassword')
userElem.send_keys(username+'@gmail.com')
passElem.send_keys(password)
driver.find_element_by_css_selector('#sign-in > form > section.buttons > button').click()
time.sleep(20)
spirePriceElem = driver.find_element_by_css_selector('#account-summary-left > account-details-payment-tile > div > div.tile-body > div.tile-body-amount-details.ng-tns-c6-3.ng-trigger.ng-trigger-fadeIn.ng-star-inserted > div.amount-due')
spirePriceWCurr = spirePriceElem.text.strip()
mo = priceRegex.search(spirePriceWCurr)
spirePrice = mo.group()
print("Gas Bill:" + spirePrice)
driver.quit()

totalBill =  rentPrice + float(spirePrice) + float(amerenPrice)
print("Total Price:" + str(totalBill))
pricePerPerson = round(totalBill/3,2)
print("Price Per Person: "+ str(pricePerPerson))
message = "Electric Bill: "+amerenPrice + "\n" + "Gas Bill: " + spirePrice + "\n" +"Rent:" + str(rentPrice) + "\n" + "Total Price: " + str(totalBill) + "\n" + "Price Per Person: "+ str(pricePerPerson)
message = message + "\n *BEEP BOOP* \n🤖 This request was sent by Will's  PayBOT 🤖"
print(message)
# access_token = Client.get_access_token(username=,password=)
venmo = Client(access_token=access_token)
#Get the roommates user objects
users = venmo.user.search_for_users(query=roommate1Venmo,page=1)
roommate1 = users[0]
users = venmo.user.search_for_users(query=roommate2Venmo,page=1)
#Room mate 2 pays for internet
roommate2 = users[0]
roommate2Price = pricePerPerson - 16.67
#Request the amounts
venmo.payment.request_money(pricePerPerson, message,int(roommate1.id), PaymentPrivacy.PRIVATE,roommate1) 
venmo.payment.request_money(roommate2Price, message,int(roommate2.id), PaymentPrivacy.PRIVATE,roommate2) 

print("Payment requests sent")


