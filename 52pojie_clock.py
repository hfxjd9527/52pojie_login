# -*- coding: utf-8 -*-
# @AuThor  : frank_lee

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
import time
from aip import AipOcr
import base64


class CrackSlider:
    def __init__(self):
        super(CrackSlider, self).__init__()
        self.url = 'https://www.52pojie.cn/member.php?mod=logging&action=login'
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 30)  # 设置超时时间
        self.zoom = 1

    def open(self):
        self.driver.get(self.url)
        self.driver.maximize_window()

    def recognize_image(self):
        captcha_image = self.driver.find_element_by_xpath('//div[@class="imgCaptcha_img"]/img')
        captcha = captcha_image.get_attribute('src')
        # 下载图片
        fh = open("captcha.jpg", "wb")
        fh.write(base64.b64decode(captcha.split(',')[1]))
        fh.close()
        APP_ID = '你的 App ID'
        API_KEY = '你的 Api Key'
        SECRET_KEY = '你的 Secret Key'
        with open('./captcha.jpg', 'rb') as bin_data:
            image_data = bin_data.read()
        options = {}
        # options["language_type"] = "ENG"
        options["detect_direction"] = "true"
        options["detect_language"] = "false"
        options["probability"] = "true"
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        result = client.basicAccurate(image_data, options)
        print(result['words_result'][0]['words'])
        return result['words_result'][0]['words'].strip()

    def input_captcha(self, captcha):
        self.driver.find_element_by_xpath('//input[@id="nc_1_captcha_input"]').send_keys(captcha)
        time.sleep(5)
        self.driver.find_element_by_xpath('// *[ @ id = "nc_1_scale_submit"] / span').click()
        time.sleep(10)

        if '验证通过' in self.driver.page_source:
            self.driver.find_element_by_xpath('//*[@name="loginsubmit"]').click()
            time.sleep(10)
            print("你已成功登录，可以开始你的骚操作了")
            time.sleep(2)
            print("等一哈，我要打个卡")
            self.driver.find_element_by_css_selector("#um > p:nth-child(3) > a:nth-child(1)").click()
            print("卡都打了，你还想干什么？")
        # 如果验证码输入错误，将会执行下面的代码，下面的代码意思是不断地刷新验证码，然后填进去
        if '_errorTEXT' in self.driver.page_source:
            self.driver.find_element_by_xpath('//*[@id="nc_1__btn_1"]').click()
            time.sleep(5)
            secondcap = self.recognize_image()
            self.input_captcha(secondcap)
            time.sleep(10)
        # 如果验证码老是错误，将会执行下面的代码
        elif '_errorTooMuch' in self.driver.page_source:
            self.driver.find_element_by_xpath('//*[@id="nc_1__btn_1"]').click()
            time.sleep(10)
            secondcap = self.recognize_image()
            self.input_captcha(secondcap)
            time.sleep(10)

    def crack_slider(self):
        try:
            self.open()
            time.sleep(3)
            self.driver.find_element_by_xpath('//input[@name="username"]').send_keys('你的吾爱破解论坛账号')
            time.sleep(1)
            self.driver.find_element_by_xpath('//input[@name="password"]').send_keys('你的论坛密码')
            time.sleep(2)
            slider = self.driver.find_element_by_xpath("//*[@id='nc_1_n1z']")
            time.sleep(1)
            ActionChains(self.driver).click_and_hold(slider).perform()
            ActionChains(self.driver).move_by_offset(xoffset=300, yoffset=0).perform()  # xoffset，X轴偏移量，不固定，小于300也无妨
            time.sleep(10)  # 给网页足够的时间让它完成加载
        except Exception as e:
            print(e)
            exit(0)


if __name__ == '__main__':
    c = CrackSlider()
    c.crack_slider()
    captcha = c.recognize_image()
    c.input_captcha(captcha)
