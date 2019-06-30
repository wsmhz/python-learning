from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import time
import json
import os

LG_URL_Login = "https://passport.lagou.com/login/login.html"
# LG_URL_Login = "https://passport.lagou.com/login/login.html?signature=92BCC9986EC45D302B12500FDCDE27FD&service=http%253A%252F%252Fwww.lagou.com%252Flogin&action=login&serviceId=lagou&ts=1561705661816"
cookies_path = "./cookies.json"


class MyException(Exception):
    def __init__(self, status, msg):
        self.status = status
        self.msg = msg


class LaGou:
    def __init__(self):
        self.login_status = False
        self.browser = None
        self.__init_browser()

    def __init_browser(self):
        '''初始化浏览器配置'''
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        self.browser = webdriver.Chrome('D:\\chromedriver\\chromedriver.exe')
        # self.browser = webdriver.Chrome(options=options)
        self.browser.maximize_window()
        self.browser.implicitly_wait(3)
        self.wait = WebDriverWait(self.browser, 10)
        self.ac = ActionChains(self.browser)
        self.browser.get(LG_URL_Login)

    def __choose_login_mode(self):
        '''通过用户名，密码去登录'''
        # 虽然默认是用户名密码登录去，确保无误，仍是本人点击一下
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@data-lg-tj-id='1Us0']")))
        self.browser.find_element_by_xpath("//*[@data-lg-tj-id='1Us0']").click()

    def __input_user_pwd(self, username, password):
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="请输入密码"]')))
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="请输入常用手机号/邮箱"]')))
        if not username:
            username = input("请输入常用手机号/邮箱>>:").strip()
        if not password:
            password = input("请输入密码>>:").strip()
        phone_ele = self.browser.find_element_by_xpath('//input[@placeholder="请输入常用手机号/邮箱"]')
        pwd_ele = self.browser.find_element_by_xpath('//input[@placeholder="请输入密码"]')
        # 输入账号
        phone_ele.clear()
        phone_ele.send_keys(username)
        # 输入密码
        pwd_ele.clear()
        pwd_ele.send_keys(password)

    def __chick_submit(self):
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@data-lg-tj-id='1j90']")))
        self.browser.find_element_by_xpath("//*[@data-lg-tj-id='1j90']").click()

    def __judge_login_successful(self):
        '''判断能否登录成功'''
        # 判断class属性 user_dropdown
        try:
            self.browser.find_element_by_xpath("//*[@class='user_dropdown']")
            return True
        except NoSuchElementException:
            return False

    def __pull_down_page(self):
        '''起首拉钩它是没有懒加载的，所以我们只需要下拉一次就好了，所以while轮回能够正文掉'''
        height = self.browser.execute_script("return document.body.scrollHeight;")
        js = "window.scrollTo(0, {});".format(height)
        self.browser.execute_script(js)
        return self.browser.page_source
        # while True:
        #     now_height = self.browser.execute_script("return document.body.scrollHeight;")
        #     if height == now_height:
        #         return self.browser.page_source
        #     js = "window.scrollTo({}, {});".format(height, now_height)
        #     self.browser.execute_script(js)
        #     height = now_height

    def __judge_ele_exist_by_xpath(self, xpath):
        '''通过xpath，判断能否具有这个元素'''
        try:
            self.browser.find_element_by_xpath(xpath)
            return True
        except NoSuchElementException:
            return False

    def __click_next_page(self):
        '''点击下一页'''
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='pager_next ']")))
        self.browser.find_element_by_xpath("//span[@class='pager_next ']").click()

    def __search_job(self, job_name):
        '''输入查询的job消息'''

        # 起首在搜刮职位之前呢，会弹回一个框框，默认选择全国站，
        # 之所以会有这个框框，那是由于你不是在登录形态下拜候这个url，若是是登录的，那么不会呈现
        try:
            self.browser.find_element_by_link_text("全国站").click()
        except NoSuchElementException:
            pass

        # 搜刮职位
        try:
            # self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='search_input']")))
            search_ele = self.browser.find_element_by_xpath("//*[@id='search_input']")
        except NoSuchElementException:
            search_ele = self.browser.find_element_by_xpath("//*[@id='keyword']")
        search_ele.click()
        search_ele.clear()
        search_ele.send_keys(job_name, Keys.ENTER)

    def __del__(self):
        # 10秒之后，封闭一些资本
        self.browser.close()

    def login(self, username: str = None, password: str = None, load_cookies: bool = True):

        # if load_cookies and os.path.exists(cookies_path):
        #     # 利用保留再文件中的cookies去拜候页面
        #     with open(cookies_path, "r", encoding="utf-8") as f:
        #         cookies = json.loads(f.read())
        #
        #     # 将cookies添加进去
        #     for cookie in cookies:
        #         self.browser.add_cookie(cookie)
        #
        #     # 拜候登录页面，若是是登录页面暗示cookie失效了，cookies没有的失效的环境就是重定向到首页
        #     self.browser.get(LG_URL_Login)
        #     if self.__judge_login_successful():
        #         print("登录成功....")
        #         return True
        #     else:
        #         print("cookies曾经失效....")
        #         # 删除方才添加的cookies
        #         self.browser.delete_all_cookies()
        self.browser.refresh()
        self.__choose_login_mode()
        self.__input_user_pwd(username, password)
        self.__chick_submit()

        # 判断能否有极验验证码
        # 若是你多试几回，你会发觉某次登录不需要滑动验证码，所以说我们就操纵这个，虽然并没有完全处理破解，可是目标最终仍是达到了
        while True:
            time.sleep(720)
            if self.__judge_ele_exist_by_xpath("//p[@class='geetest_panel_box geetest_panelshowslide']"):
                self.browser.find_element_by_xpath("//a[@class='geetest_close']").click()
                time.sleep(2)
                self.browser.find_element_by_xpath("//*[@data-lg-tj-id='1j90']").click()
                continue
            else:
                break

        if self.__judge_login_successful():
            self.login_status = True
            # 登录成功，将cookies保留起来
            with open("./cookies.json", "w", encoding="utf-8") as f:
                f.write(json.dumps(self.browser.get_cookies()))
            print("登录成功")
            return True
        else:
            print("登录失败，请查抄你的用户名或密码")
            return False

    def get_job_info(self, job_name: str = None, is_filter: bool = False):
        '''用于获取到查询的job'''
        if not self.login_status:
            self.browser.get("https://www.lagou.com/")
        if not job_name:
            job_name = input("请输入查询job的名称>>:").strip()

        self.__search_job(job_name)

        if is_filter:
            # 过滤这个功能不忙实现
            pass
        # 这里起头就是进行翻页操作了，以及对数据的处置
        page = 1
        while True:
            print("爬取工作职位为>>{}   第{}页数据".format(job_name, page))
            # 获取到完毕的页面源码，然后进行提取消息的操作
            page_source = self.__pull_down_page()
            print(page_source)
            # 消息提取完毕，进行翻页把持
            if not self.__judge_ele_exist_by_xpath("//span[@class='pager_next ']"):
                print("{} 工作职位爬取完毕...".format(job_name))
                break
            self.__click_next_page()
            time.sleep(2)

            # 点击完毕下一页，可能碰到一些反扒办法
            if self.browser.current_url == "https://passport.lagou.com/login/login.html":
                self.login()

            page += 1


if __name__ == '__main__':
    lagou = LaGou()

    username = ""
    password = ""
    lagou.login(username, password)