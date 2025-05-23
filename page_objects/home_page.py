from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage

class HomePage(BasePage):
    """主页类，包含主页特有的元素和方法"""
    
    # 定位器
    LOGIN_BUTTON = (
        By.CSS_SELECTOR,
        "#__next > div > div > div > div > div > div> div > button:nth-child(1)"
    )
    REGISTER_BUTTON = (
        By.CSS_SELECTOR,
        "#__next > div > div > div > div > div > div> div > button:nth-child(2)"
    )
    USER_TRIGGER = (
        By.CSS_SELECTOR,
        "#__next > div > div > div > div > div > div > div.dzq-dropdown"
    )
    USER_CENTER = (
        By.CSS_SELECTOR,
        "#__next > div > div > div> div > div > div> div > ul > li:nth-child(1)"
    )
    LOGOUT_BUTTON = (
        By.CSS_SELECTOR,
        "#__next > div > div > div> div > div > div> div > ul > li:nth-child(2)"
    )
    POST_BUTTON = (
        By.CSS_SELECTOR,
        "#__next > div > div > div > div > div > div > div > div > div > div > button"
    )
    THREAD_LIST = (
        By.CSS_SELECTOR,
        "#__next > div > div > div > div > div.list > div > div > div > div > div > div > div > h1"
    )
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def open_home(self):
        """打开主页"""
        self.open("")
        return self
    
    def click_login(self):
        """点击登录按钮"""
        self.click(self.LOGIN_BUTTON)
        return self
    
    def click_register(self):
        """点击注册按钮"""
        self.click(self.REGISTER_BUTTON)
        return self
    
    def hover_user_trigger(self):
        """鼠标悬停在用户触发器上"""
        self.hover_element(self.USER_TRIGGER)
        return self
    
    def click_user_center(self):
        """点击个人中心"""
        self.hover_user_trigger()
        self.click(self.USER_CENTER)
        return self
    
    def click_logout(self):
        """点击退出登录"""
        self.hover_user_trigger()
        self.click(self.LOGOUT_BUTTON)
        return self
    
    def click_post_button(self):
        """点击发布按钮"""
        self.click(self.POST_BUTTON)
        return self
    
    def click_thread(self, index=0):
        """点击帖子，默认点击第一个"""
        threads = self.find_elements(self.THREAD_LIST)
        if threads and len(threads) > index:
            threads[index].click()
        return self
    
    def is_logged_in(self):
        """判断是否已登录"""
        return self.is_element_present(self.USER_TRIGGER, timeout=3)
    
    def is_thread_list_loaded(self):
        """判断帖子列表是否加载完成"""
        return len(self.find_elements(self.THREAD_LIST)) > 0 