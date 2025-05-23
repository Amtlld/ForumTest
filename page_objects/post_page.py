from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage

class PostPage(BasePage):
    """发帖页面类，包含发帖页面特有的元素和方法"""
    
    # 定位器
    TITLE_INPUT = (By.CSS_SELECTOR, 'input[placeholder="标题（可选）"]')
    CONTENT_TEXTAREA = (By.CSS_SELECTOR, 'pre[placeholder="请填写您的发布内容…"]')
    DEFAULT_CATEGORY = (By.CSS_SELECTOR, "#__next > div > div > div> div> div> div> button:nth-child(1)")
    OTHER_CATEGORY = (By.CSS_SELECTOR, "#__next > div > div > div> div> div> div> button:nth-child(2)")
    POST_BUTTON = (By.CSS_SELECTOR, "#__next > div > div > div> div> div> button:nth-child(2)")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def open_post_page(self):
        """打开发帖页面"""
        self.open("thread/post")
        return self
    
    def input_title(self, title):
        """输入标题"""
        self.input_text(self.TITLE_INPUT, title)
        return self
    
    def input_content(self, content):
        """输入内容"""
        self.input_text(self.CONTENT_TEXTAREA, content)
        return self
    
    def select_category(self, category_name):
        """选择分类"""
        
        if category_name == "默认分类":
            self.click(self.DEFAULT_CATEGORY)
        elif category_name == "其他分类":
            self.click(self.OTHER_CATEGORY)
        
        return self
    
    def click_post_button(self):
        """点击发布按钮"""
        self.click(self.POST_BUTTON)
        return self
    
    def create_post(self, title, content, category="默认分类"):
        """发帖流程"""
        self.input_title(title)
        self.input_content(content)
        self.select_category(category)
        self.click_post_button()
        return self
    
    def check_toast_message(self, expected_message):
        """检查toast提示信息"""
        return self.wait_for_toast(expected_message)
    
    def is_post_button_enabled(self):
        """判断发布按钮是否可点击"""
        button = self.find_element(self.POST_BUTTON)
        return "is-disabled" not in button.get_attribute("class")
    
    def is_redirect_to_thread(self, timeout=5):
        """检查是否重定向到帖子页面"""
        return self.wait_for_url_contains("thread", timeout) 