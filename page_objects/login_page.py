from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage

class LoginPage(BasePage):
    """登录页面类，包含登录页面特有的元素和方法"""
    
    # 定位器
    USERNAME_INPUT = (By.CSS_SELECTOR, 'input[placeholder="输入您的用户名"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, 'input[placeholder="输入您的登录密码"]')
    LOGIN_BUTTON = (By.CSS_SELECTOR, '#__next > div > div > div> div > div > div > div > div> div > button')
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def open_login_page(self):
        """打开登录页面"""
        self.open("user/username-login")
        return self
    
    def input_username(self, username):
        """输入用户名"""
        self.input_text(self.USERNAME_INPUT, username)
        return self
    
    def input_password(self, password):
        """输入密码"""
        self.input_text(self.PASSWORD_INPUT, password)
        return self
    
    def click_login(self):
        """点击登录按钮"""
        self.click(self.LOGIN_BUTTON)
        return self
    
    def login(self, username, password):
        """登录流程"""
        self.input_username(username)
        self.input_password(password)
        self.click_login()
        return self
    
    def is_login_button_enabled(self):
        """判断登录按钮是否可点击"""
        button = self.find_element(self.LOGIN_BUTTON)
        return "is-disabled" not in button.get_attribute("class")
    
    def is_redirect_to_home(self, timeout=5):
        """检查是否重定向到主页"""
        return self.wait_for_url_contains("https://localhost/", timeout) 