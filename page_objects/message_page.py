from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage

class MessagePage(BasePage):
    """私信页面类，包含私信页面特有的元素和方法"""
    
    # 定位器
    MESSAGE_TEXTAREA = (
        By.CSS_SELECTOR,
        "div > textarea"
    )
    SEND_BUTTON = (
        By.CSS_SELECTOR,
        "#__next > div > div > div> div > div > div> div > div> div> button"
    )
    MESSAGES = (
        By.CSS_SELECTOR,
        "#__next > div > div > div._1AABQTkjs60yLerksyv0Lm._2Ma7oHEHm1xrBV92mrcdqI.mymessage-page > div > div > div._3ZZfB0N5_Sh035AFamfsrk > div > div.tztHKVAjDfSwFtjiTjboS > div > div > div.rqymFR5ufbMmkwvt7hBVT"
    )
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def open_message_page(self, user_id, nickname):
        """打开私信页面"""
        self.open(f"message?page=chat&userId={user_id}&nickname={nickname}")
        return self
    
    def input_message(self, message):
        """输入私信"""
        self.input_text(self.MESSAGE_TEXTAREA, message)
        return self
    
    def click_send_button(self):
        """点击发送按钮"""
        self.click(self.SEND_BUTTON)
        return self
    
    def send_message(self, message):
        """发送私信流程"""
        self.input_message(message)
        self.click_send_button()
        return self
    
    def get_messages(self):
        """获取所有私信"""
        return self.find_elements(self.MESSAGES)
    
    def get_last_message(self):
        """获取最新的私信"""
        messages = self.get_messages()
        if messages:
            return messages[-1].text
        return None
    
    def is_message_sent(self, message):
        """判断私信是否发送成功"""
        last_message = self.get_last_message()
        return message in last_message
    
    def check_toast_message(self, expected_message):
        """检查toast提示信息"""
        return self.wait_for_toast(expected_message)