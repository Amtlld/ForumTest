from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage

class UserPage(BasePage):
    """用户主页类，包含用户主页特有的元素和方法"""
    
    # 定位器
    FOLLOW_BUTTON = (
        By.CSS_SELECTOR,
        "#__next > div > div > div > div > div > div > div:nth-child(1) > div > div > div > div > div > div> div > div> div> div> button:nth-child(1)"
    )
    BLOCK_BUTTON = (
        By.XPATH,
        "//span[contains(text(),'屏蔽')]/.."
    )
    SEND_MESSAGE_BUTTON = (
        By.CSS_SELECTOR,
        "#__next > div > div > div > div > div > div > div:nth-child(1) > div > div > div > div > div > div> div > div> div> div> button:nth-child(2)"
    )
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def open_user_page(self, user_id):
        """打开用户主页"""
        self.open(f"user/{user_id}")
        return self
    
    def click_follow_button(self):
        """点击关注按钮"""
        self.click(self.FOLLOW_BUTTON)
        return self
    
    def click_block_button(self):
        """点击屏蔽按钮"""
        self.click(self.BLOCK_BUTTON)
        return self
    
    def click_send_message_button(self):
        """点击发私信按钮"""
        self.click(self.SEND_MESSAGE_BUTTON)
        return self
    
    def get_follow_button_text(self):
        """获取关注按钮文本"""
        button = self.find_element(self.FOLLOW_BUTTON)
        span = button.find_element(By.TAG_NAME, "span")
        return span.text
    
    def get_block_button_text(self):
        """获取屏蔽按钮文本"""
        button = self.find_element(self.BLOCK_BUTTON)
        span = button.find_element(By.TAG_NAME, "span")
        return span.text
    
    def is_following(self):
        """判断是否已关注"""
        return self.get_follow_button_text() == "已关注"
    
    def is_blocking(self):
        """判断是否已屏蔽"""
        return self.get_block_button_text() == "解除屏蔽" 