from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from sys import argv, exit
import signal, re
import random

class spoofPhone:
    def __init__(self, numm, callnumm, userName, passWord):
        self.phoneNumber = numm
        self.callN = callnumm
        self.uN = userName
        self.pN = passWord
        signal.signal(signal.SIGINT, self.signal_handler)
        profile = webdriver.FirefoxProfile()
        profile.set_preference('media.navigator.permission.disabled', True)
        profile.set_preference('dom.webnotifications.enabled', False)
        self.s = webdriver.Firefox(profile)
        self.s.set_window_position(0,0)
        self.s.set_window_size(800, 800)
        self.login()

    def login(self):
        self.s.get("https://phone.firertc.com")
        usern = self.s.find_element_by_id("user_email")
        passn = self.s.find_element_by_id("user_password")
        subb = self.s.find_element_by_xpath('//input[@value="Sign In"]')
        usern.send_keys(self.uN)
        passn.send_keys(self.pN)
        subb.click()
        self.spoofId()

    def spoofId(self):
        self.s.get("https://phone.firertc.com/settings")
        spoofAdd =  self.s.find_element_by_id("address-ua-config-display-name")
        subb = self.s.find_element_by_xpath('//button[@type="submit"]')
        for x in range(20):
            spoofAdd.send_keys(Keys.BACKSPACE)        
        spoofAdd.send_keys('1'+self.phoneNumber)
        subb.click()
        self.callNumber()

    def callNumber(self):
        self.s.get("https://phone.firertc.com/phone")
        sleep(3)
        phoneInput = self.s.find_element_by_xpath('//input[@class="dialer-input form-control dropdown-toggle"]')
        phoneInput.send_keys(self.callN)
        phoneInput.send_keys(Keys.ENTER)
        sleep(2)
        while True:
            sleep(.5)
            try:
                b = self.s.find_element_by_xpath('//button[@data-action="cancel"]')
            except:
                b = self.s.find_element_by_xpath('//button[@data-action="hangup"]')
                b.click()
                self.phoneNumber = "".join([str(random.randint(0, 9)) for _ in range(10)])
                print(self.phoneNumber)
                self.spoofId()
        

        self.die()

    def signal_handler(self, signal, frame):
            self.die()
            exit(0)

    def die(self):
        self.s.close()


def usage():
    print('Usage: phoneSpoofer.py <PhoneToSpoof> <PhoneToCall> <Username for FireRTC> <Password for FireRTC>')
    print('\n')

if __name__ == '__main__':
    s = argv[0]
    c = argv[1]
    u = argv[2]
    p = argv[3]
    try:
        a = spoofPhone(s, c, u, p)
    except:
        a.die()
