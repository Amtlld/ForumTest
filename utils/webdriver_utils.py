from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os

class WebDriverFactory:
    """WebDriver工厂类，用于创建和管理WebDriver实例"""
    
    @staticmethod
    def create_chrome_driver(headless=False):
        """创建Chrome WebDriver"""
        options = ChromeOptions()
        
        if headless:
            options.add_argument("--headless")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        # options.add_argument("--window-size=1920,1080")

        # 关闭HTTPS安全警告
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--allow-insecure-localhost')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # 关闭密码泄露提示
        options.add_experimental_option("prefs", {"profile.password_manager_leak_detection": False})

        # 使用webdriver_manager自动下载和管理ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # 设置隐式等待时间
        driver.implicitly_wait(10)
        
        return driver
    
    @staticmethod
    def create_firefox_driver(headless=False):
        """创建Firefox WebDriver"""
        options = FirefoxOptions()
        
        if headless:
            options.add_argument("--headless")
        
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        
        # 使用webdriver_manager自动下载和管理GeckoDriver
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        
        # 设置隐式等待时间
        driver.implicitly_wait(10)
        
        return driver
    
    @classmethod
    def create_driver(cls, browser_name="chrome", headless=False):
        """根据浏览器名称创建WebDriver"""
        browser_name = browser_name.lower()
        
        if browser_name == "chrome":
            return cls.create_chrome_driver(headless)
        elif browser_name == "firefox":
            return cls.create_firefox_driver(headless)
        else:
            raise ValueError(f"不支持的浏览器类型: {browser_name}")
    
    @staticmethod
    def quit_driver(driver):
        """关闭WebDriver"""
        if driver:
            driver.quit() 