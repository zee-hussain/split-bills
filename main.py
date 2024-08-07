import datetime
import os
import parasitesplitwise as parasitesplitwise
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import chromedriver_autoinstaller
from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 800))  
display.start()

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

chrome_options = webdriver.ChromeOptions()    
options = [
  # Define window size here
   "--window-size=1200,1200",
    "--ignore-certificate-errors"
]

for option in options:
    chrome_options.add_argument(option)

driver = webdriver.Chrome(options = chrome_options)


class Utility(object):
    def __init__(self, name):
        self.name = name
        self.price = "1"
        self.notes = ""

    def getGas(self):
        ## Login to CoA
        driver.get("https://www.texasgasservice.com/account")
        driver.implicitly_wait(30)
        reject_cookies = driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div/div[1]/div/div[2]/div/button[2]")
        reject_cookies.click()
        username = driver.find_element(By.XPATH, "/html/body/div[2]/app-root/ogs-login-page/section/div/ogs-login-form/fieldset/form/div[1]/input")
        username.send_keys("zeehussain")
        password = driver.find_element(By.XPATH,"/html/body/div[2]/app-root/ogs-login-page/section/div/ogs-login-form/fieldset/form/div[2]/input")
        password.send_keys(os.environ['GAS_PASS'])
        login = driver.find_element(By.XPATH,"/html/body/div[2]/app-root/ogs-login-page/section/div/ogs-login-form/fieldset/form/ogs-busy-button/button")
        login.click()
        time.sleep(30)

        ## Get bill post date
        dueDate = driver.find_element(By.XPATH,"/html/body/div[2]/app-root/ogs-account-page/div/ogs-account-profile-card/section/div/div[2]/div[1]/span[2]")
        dueDate = str(dueDate.text)
        dueDate = dueDate[5:]

        ## Get bill amount
        totalAmt = driver.find_element(By.XPATH,"/html/body/div[2]/app-root/ogs-account-page/div/ogs-account-profile-card/section/div/div[2]/div[1]/span[1]")
        totalAmt = str(totalAmt.text)
        totalAmt = totalAmt[1:]

        ## Generate utility notes
        gasNotes = "Gas - " + dueDate + ". Posted by ParasiteBot"

        return totalAmt, gasNotes

    def getElectric(self):
        ## Login to CoA
        driver.get("https://dss-coa.opower.com/dss/billing/view")
        driver.implicitly_wait(30)
        username = driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div/div[1]/div/form/input[1]")
        username.send_keys("zeehussain")
        password = driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div/div[1]/div/form/input[2]")
        password.send_keys(os.environ['ELEC_PASS'])
        login = driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div/div[1]/div/form/button")
        login.click()
        time.sleep(15)

        ## Get bill due date
        dueDate = driver.find_element(By.XPATH,"/html/body/div/div/div/main/div[2]/section/div/div[1]/opower-widget-bill-summary/div/div/div/div/div/div/div[4]/div[2]/div/div")
        dueDate = str(dueDate.text)
        dueDate = dueDate[5:]

        ## Get bill amount
        totalAmt = driver.find_element(By.XPATH,"/html/body/div/div/div/main/div[2]/section/div/div[1]/opower-widget-bill-summary/div/div/div/div/div/div/div[3]/div[2]")
        totalAmt = str(totalAmt.text)
        totalAmt = totalAmt[1:]

        ## Generate utility notes
        electricNotes = "Electric - " + dueDate + ". Posted by ParasiteBot"

        return totalAmt, electricNotes

        
    
    def set_data(self,price,notes):
        if self.name == "gas":
            data = self.getGas()
            self.price = data[0]
            self.notes = data[1]
        elif self.name == "electric":
            data = self.getElectric()
            self.price = data[0]
            self.notes = data[1]
        elif self.name == "internet":
            self.price = "70"
            self.notes = "Internet - " + str(datetime.date.today()) + ". Posted by CocoaBot"



def main():
    ## Get current list of expenses
    expenses = parasitesplitwise.getParasiteExpenses()

    ## Get internet data
    internet = Utility("internet")
    internet.set_data(internet.price, internet.notes)
    
    # Get electric data
    electric = Utility("electric")
    electric.set_data(electric.price, electric.notes)
    
    ## Get Gas Data
    gas = Utility("gas")
    gas.set_data(gas.price, gas.notes)


    # If bill has not been posted, post it.
    if electric.notes not in expenses and float(electric.price) != 0.00:
        parasitesplitwise.createParasiteExpense(electric.price, "Electricity", electric.notes)

    if gas.notes not in expenses and float(gas.price) != 0.00:
        parasitesplitwise.createParasiteExpense(gas.price, "Gas", gas.notes)

    ## If today is the 13th of the month, post internet
    if str(datetime.date.today().day) == "13" and int(internet.price) != 0:
        parasitesplitwise.createParasiteExpense(internet.price, "Internet", internet.notes)
    

main()
