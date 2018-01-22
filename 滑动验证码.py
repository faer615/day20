#!/bin/env python
# -*- coding: utf-8 -*-
import random
import time
from io import BytesIO

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


class HackGeetest():
    def __init__(self):
        self.browser = webdriver.PhantomJS('./phantomjs')
        # self.browser=webdriver.Chrome('./chromedriver')
        self.browser.maximize_window()
        self.browser.implicitly_wait(10)
        self.action = ActionChains(self.browser)
        self.threshold = 10

    def get_captcha_img(self):
        slider_element = self.browser.find_element_by_class_name('gt_slider_knob')
        item = self.browser.find_element_by_class_name('gt_box')
        self.action.click_and_hold(on_element=slider_element).perform()
        time.sleep(0.3)
        screenshot = self.browser.get_screenshot_as_png()
        left = item.location['x']
        right = left + item.size['width']
        top = item.location['y']
        bottom = top + item.size['height']
        img = Image.open(BytesIO(screenshot))
        captcha = img.crop((left, top, right, bottom))
        return captcha

    def cal_slider_offset(self):
        captcha = self.get_captcha_img()
        captcha.show()
        image = captcha.convert('L')
        flag = 0
        for x in range(60, image.size[0]):
            sum_pix = 0
            for y in range(image.size[1]):
                pix = image.getpixel((x, y))
                if pix < 55:
                    sum_pix += 1
            print(x, sum_pix)
            if sum_pix > self.threshold:
                return x - flag
            if sum_pix == 0:
                flag = 0
            else:
                flag += 1
            if flag > 4:
                return x - flag
        return -1

    def load_page(self, url):
        self.browser.get(url)

    def get_track(self, offset):
        line = []
        while offset > 5:
            num = random.randint(1, 5)
            line.append(num)
            offset -= num
        for i in range(offset):
            line.append(1)
        return line

    def drag_and_drop_by_offset(self, offset):
        element = self.browser.find_element_by_class_name('gt_slider_knob')
        line = self.get_track(offset)
        for x in line:
            self.action.move_by_offset(x, random.randint(1, 20)).perform()
            self.action.reset_actions()
            time.sleep(random.randint(50, 200) / 1000)
        self.action.release().perform()
        time.sleep(2)
        screenshot = self.browser.get_screenshot_as_png()
        # 结果
        img = Image.open(BytesIO(screenshot))
        img.show()

    def quit(self):
        self.browser.quit()


if __name__ == '__main__':
    geetest = HackGeetest()
    geetest.load_page('https://pt.whu.edu.cn/portal.php')
    time.sleep(2)
    offset = geetest.cal_slider_offset()
    if offset != -1:
        geetest.drag_and_drop_by_offset(offset - 5)
        time.sleep(20)
        geetest.quit()
