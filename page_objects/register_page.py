from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage

class RegisterPage(BasePage):
    """注册页面类，包含注册页面特有的元素和方法"""
    
    # 定位器
    USERNAME_INPUT = (
        By.CSS_SELECTOR, 'input[placeholder="输入您的用户名"]'
    )
    PASSWORD_INPUT = (
        By.CSS_SELECTOR, 'input[placeholder="输入您的登录密码"]'
    )
    REPEAT_PASSWORD_INPUT = (
        By.CSS_SELECTOR, 'input[placeholder="确认密码"]'
    )
    NICKNAME_INPUT = (
        By.CSS_SELECTOR, 'input[placeholder="输入您的昵称"]'
    )
    REGISTER_BUTTON = (
        By.CSS_SELECTOR, '#__next > div > div > div:nth-child(2) > div > div > div > div > div > div > button'
    )
    TOAST_MESSAGE = (By.CSS_SELECTOR, '#dzq-toast-root > div > span')
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def open_register_page(self):
        """打开注册页面"""
        self.open("user/register")
        return self
    
    def input_username(self, username):
        """输入用户名"""
        self.input_text(self.USERNAME_INPUT, username)
        return self
    
    def input_password(self, password):
        """输入密码"""
        self.input_text(self.PASSWORD_INPUT, password)
        return self
    
    def input_repeat_password(self, repeat_password):
        """输入重复密码"""
        self.input_text(self.REPEAT_PASSWORD_INPUT, repeat_password)
        return self
    
    def input_nickname(self, nickname):
        """输入昵称"""
        self.input_text(self.NICKNAME_INPUT, nickname)
        return self
    
    def click_register(self):
        """点击注册按钮"""
        self.click(self.REGISTER_BUTTON)
        return self
    
    def register(self, username, password, repeat_password, nickname):
        """注册流程"""
        self.input_username(username)
        self.input_password(password)
        self.input_repeat_password(repeat_password)
        self.input_nickname(nickname)
        self.click_register()
        return self
    
    def is_register_button_enabled(self):
        """判断注册按钮是否可点击"""
        button = self.find_element(self.REGISTER_BUTTON)
        return "is-disabled" not in button.get_attribute("class")
    
    def check_toast_message(self, expected_message):
        """检查toast提示信息
        
        Args:
            expected_message: 预期的toast消息文本
            
        Returns:
            tuple: (是否匹配预期, 实际toast文本)
        """
        return self.wait_for_toast(expected_message)
    
    def is_redirect_to_home(self, timeout=5):
        """检查是否重定向到主页"""
        return self.wait_for_url_contains("https://localhost/", timeout) 