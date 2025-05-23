import pytest
import json
import allure
from utils.webdriver_utils import WebDriverFactory
from utils.db_utils import db_utils
from utils.mail_utils import email_utils
from page_objects.home_page import HomePage
from page_objects.register_page import RegisterPage
from page_objects.login_page import LoginPage
from page_objects.post_page import PostPage
from page_objects.thread_page import ThreadPage
from page_objects.user_page import UserPage
from page_objects.message_page import MessagePage

# 读取测试数据
@pytest.fixture(scope="session")
def register_test_data():
    """读取注册功能测试数据"""
    with open("data/register_test_data.json", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture(scope="session")
def forum_test_data():
    """读取论坛功能测试数据"""
    with open("data/forum_test_data.json", encoding="utf-8") as f:
        return json.load(f)

# WebDriver相关fixtures
@pytest.fixture(scope="session")
def browser_name(request):
    """获取浏览器名称，默认为chrome"""
    return request.config.getoption("--browser", default="chrome")

@pytest.fixture(scope="session")
def headless(request):
    """获取是否使用无头模式，默认为False"""
    return request.config.getoption("--headless", default=False)

@pytest.fixture(scope="function")
def driver(browser_name, headless, request):
    """创建WebDriver实例"""
    driver = WebDriverFactory.create_driver(browser_name, headless)
    
    # 设置窗口大小
    # driver.maximize_window()
    
    # 将driver添加到allure报告
    allure.attach(
        driver.get_screenshot_as_png(),
        name="启动浏览器",
        attachment_type=allure.attachment_type.PNG
    )
    
    # 返回driver实例
    yield driver
    
    # 捕获测试失败的截图
    if request.node.rep_call.failed:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="测试失败截图",
            attachment_type=allure.attachment_type.PNG
        )
    
    # 关闭driver
    WebDriverFactory.quit_driver(driver)

# 添加测试结果处理
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

# 页面对象fixtures
@pytest.fixture(scope="function")
def home_page(driver):
    """主页对象"""
    return HomePage(driver)

@pytest.fixture(scope="function")
def register_page(driver):
    """注册页面对象"""
    return RegisterPage(driver)

@pytest.fixture(scope="function")
def login_page(driver):
    """登录页面对象"""
    return LoginPage(driver)

@pytest.fixture(scope="function")
def post_page(driver):
    """发帖页面对象"""
    return PostPage(driver)

@pytest.fixture(scope="function")
def thread_page(driver):
    """帖子页面对象"""
    return ThreadPage(driver)

@pytest.fixture(scope="function")
def user_page(driver):
    """用户主页对象"""
    return UserPage(driver)

@pytest.fixture(scope="function")
def message_page(driver):
    """私信页面对象"""
    return MessagePage(driver)

# 数据库工具fixture
@pytest.fixture(scope="session")
def database():
    """数据库工具对象"""
    yield db_utils
    db_utils.close()

# 登录用户fixture
@pytest.fixture(scope="function")
def logged_in_user(login_page, home_page):
    """创建一个已登录的用户会话"""
    login_page.open_login_page()
    login_page.login("test01", "test01")  # 使用测试用户名和密码
    
    # 确认登录成功
    assert home_page.is_logged_in()
    
    yield
    
    # 退出登录
    home_page.open_home()
    home_page.click_logout()

# 测试完成后发送Allure报告
@pytest.fixture(scope="session", autouse=True)
def send_report_after_tests(request):
    """测试完成后发送Allure报告"""
    yield
    if request.config.getoption("--send-report", default=False):
        email_utils.send_allure_report()

# 注册命令行选项
def pytest_addoption(parser):
    """添加命令行选项"""
    parser.addoption("--browser", action="store", default="chrome", help="指定浏览器: chrome 或 firefox")
    parser.addoption("--headless", action="store_true", default=False, help="是否使用无头模式")
    parser.addoption("--send-report", action="store_true", default=False, help="是否发送Allure报告") 