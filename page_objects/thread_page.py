from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage
import time

class ThreadPage(BasePage):
    """帖子页面类，包含帖子页面特有的元素和方法"""
    
    # 定位器
    LIKE_BUTTON = (By.XPATH, "//span[contains(text(),'赞')]/..")
    LIKED_BUTTON_CLASS = "_32k6KpwFJXU4ufhoOTLCa_"
    COMMENT_TEXTAREA = (
        By.CSS_SELECTOR,
        "#__next > div > div > div > div > div > div > div > div:nth-child(1) > div> div > div:nth-child(2) > div > div> div > textarea"
    )
    COMMENT_SUBMIT_BUTTON = (
        By.CSS_SELECTOR,
        "#__next > div > div > div > div > div > div > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div > button"
    )
    COMMENT_LIST = (
        By.CSS_SELECTOR,
        "#__next > div > div > div> div> div> div > div> div:nth-child(1) > div > div > div> div > div > div > div> div > a"
    )
    AUTHOR_AVATAR = (
        By.CSS_SELECTOR,
        "#__next > div > div > div> div > div > div > div> div:nth-child(1) > div> div> div> div > div> div > div.dzq-avatar"
    )
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def open_thread_page(self, thread_id):
        """打开帖子页面"""
        self.open(f"thread/{thread_id}")
        return self
    
    def click_like_button(self):
        """点击赞按钮"""
        self.click(self.LIKE_BUTTON)
        return self

    def is_thread_liked(self):
        """判断帖子是否已点赞"""
        time.sleep(3)  # 等待脚本响应
        like_button = self.find_element(self.LIKE_BUTTON)
        return self.LIKED_BUTTON_CLASS in like_button.get_attribute("class")

    def input_comment(self, comment):
        """输入评论"""
        self.input_text(self.COMMENT_TEXTAREA, comment)
        return self
    
    def submit_comment(self):
        """提交评论"""
        self.click(self.COMMENT_SUBMIT_BUTTON)
        return self
    
    def create_comment(self, comment):
        """评论流程"""
        self.input_comment(comment)
        self.submit_comment()
        return self
    
    def get_comments(self):
        """获取评论列表"""
        return self.find_elements(self.COMMENT_LIST)
    
    def is_comment_present(self, comment):
        """判断评论是否存在"""
        comments = self.get_comments()
        if not comments:
            return False
            
        comment_text = comment[:20] if len(comment) > 20 else comment
        
        for comment_element in comments:
            title = comment_element.get_attribute("title")
            if title == comment_text:
                return True
        
        return False
    
    def check_toast_message(self, expected_message):
        """检查toast提示信息"""
        return self.wait_for_toast(expected_message)
    
    def click_author_avatar(self):
        """点击楼主头像"""
        self.click(self.AUTHOR_AVATAR)
        return self 