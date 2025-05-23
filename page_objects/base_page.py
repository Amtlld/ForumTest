from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time

class BasePage:
    """基础页面类，包含所有页面共有的方法"""

    TOAST = (By.CSS_SELECTOR, '#dzq-toast-root > div > span')
    
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://localhost"
        self.timeout = 10
    
    def open(self, url=""):
        """打开页面"""
        self.driver.get(f"{self.base_url}/{url}")
    
    def find_element(self, locator, timeout=None):
        """查找元素"""
        if timeout is None:
            timeout = self.timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            raise NoSuchElementException(f"找不到元素：{locator}")
    
    def find_elements(self, locator, timeout=None):
        """查找多个元素"""
        if timeout is None:
            timeout = self.timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException:
            return []
    
    def click(self, locator, timeout=None):
        """点击元素"""
        element = self.find_element(locator, timeout)
        element.click()
        return element
    
    def input_text(self, locator, text, timeout=None):
        """输入文本"""
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)
        return element
    
    def is_element_present(self, locator, timeout=None):
        """判断元素是否存在"""
        try:
            self.find_element(locator, timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False
    
    def wait_for_element(self, locator, timeout=None):
        """等待元素出现"""
        return self.find_element(locator, timeout)
    
    def wait_for_element_to_be_clickable(self, locator, timeout=None):
        """等待元素可点击"""
        if timeout is None:
            timeout = self.timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException:
            raise NoSuchElementException(f"元素不可点击：{locator}")
    
    def wait_for_url_contains(self, url_part, timeout=None):
        """等待URL包含特定字符串"""
        if timeout is None:
            timeout = self.timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.url_contains(url_part)
            )
        except TimeoutException:
            return False
    
    def wait_for_toast(self, expected_text=None, timeout=5):
        """等待toast提示出现并返回其文本内容，使用轮询机制提高可靠性
        
        Args:
            expected_text: 预期toast文本，为None时只返回实际文本
            timeout: 等待超时时间
            
        Returns:
            tuple: (是否匹配预期, 实际toast文本)，如果toast未出现则返回(False, None)
        """
        # 由于toast可能出现和消失很快，使用轮询方式检查
        max_attempts = 10
        poll_interval = min(timeout / max_attempts, 0.5)  # 最大0.5秒一次轮询
        start_time = time.time()
        end_time = start_time + timeout
        
        for attempt in range(max_attempts):
            try:
                # 使用可见性条件等待toast
                toast = WebDriverWait(self.driver, poll_interval).until(
                    EC.visibility_of_element_located(self.TOAST)
                )
                
                actual_text = toast.text
                if actual_text:  # 确保toast有文本内容
                    # 截图记录toast出现
                    self.driver.save_screenshot(f"toast_found_{attempt}.png")
                    
                    if expected_text is None:
                        return (True, actual_text)
                    return (expected_text in actual_text, actual_text)
                
            except (TimeoutException, NoSuchElementException, StaleElementReferenceException):
                # 如果超出总超时时间，退出循环
                if time.time() > end_time:
                    break
                # 否则继续尝试
                time.sleep(poll_interval)
                continue
        
        # 如果到这里仍然没有找到toast或toast没有文本，尝试最后一次直接查找
        try:
            elements = self.driver.find_elements(*self.TOAST)
            if elements:
                for element in elements:
                    try:
                        text = element.text
                        if text:
                            if expected_text is None:
                                return (True, text)
                            return (expected_text in text, text)
                    except:
                        pass
        except:
            pass
            
        # 截图记录未找到toast的状态
        self.driver.save_screenshot("toast_not_found.png")
        return (False, None)
    
    def get_current_url(self):
        """获取当前URL"""
        return self.driver.current_url
    
    def hover_element(self, locator, timeout=None):
        """鼠标悬停在元素上"""
        from selenium.webdriver.common.action_chains import ActionChains
        element = self.find_element(locator, timeout)
        ActionChains(self.driver).move_to_element(element).perform()
        return element