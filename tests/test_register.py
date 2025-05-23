import pytest
import allure
import time
from retrying import retry

# 定义重试装饰器，最多尝试3次，每次间隔2秒
@retry(stop_max_attempt_number=3, wait_fixed=2000)
def check_toast_with_retry(page, expected_message):
    """带重试机制的toast检查
    
    Args:
        page: 包含check_toast_message方法的页面对象
        expected_message: 预期的toast消息
        
    Returns:
        tuple: (是否匹配, 实际toast文本)
        
    Raises:
        AssertionError: 如果三次尝试后仍未找到toast或toast不匹配预期
    """
    is_matched, actual_toast = page.check_toast_message(expected_message)
    if not is_matched:
        raise AssertionError(f"Toast消息不匹配。预期: {expected_message}, 实际: {actual_toast or '无toast消息'}")
    return is_matched, actual_toast

@allure.epic("论坛测试")
@allure.feature("注册功能")
class TestRegister:
    
    @allure.story("有效注册")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("case_id", ["register_valid_1", "register_valid_2", "register_valid_3"])
    def test_valid_register(self, register_page, home_page, database, register_test_data, case_id):
        """测试有效注册"""
        # 获取测试数据
        test_cases = {case["case_id"]: case for case in register_test_data}
        test_case = test_cases[case_id]
        
        # 测试数据
        username = test_case["input"]["username"]
        password = test_case["input"]["password"]
        repeat_password = test_case["input"]["repeat_password"]
        nickname = test_case["input"]["nickname"]
        
        # 预期结果
        expected_success = test_case["expected"]["success"]
        expected_toast = test_case["expected"]["toast_message"]
        expected_redirect = test_case["expected"]["redirect_to_home"]
        
        with allure.step(f"打开注册页面"):
            register_page.open_register_page()
        
        with allure.step(f"输入用户名: {username}"):
            register_page.input_username(username)
        
        with allure.step(f"输入密码: {password}"):
            register_page.input_password(password)
        
        with allure.step(f"输入重复密码: {repeat_password}"):
            register_page.input_repeat_password(repeat_password)
        
        with allure.step(f"输入昵称: {nickname}"):
            register_page.input_nickname(nickname)
        
        with allure.step("点击注册按钮"):
            register_page.click_register()
        
        with allure.step(f"检查toast提示消息"):
            try:
                is_matched, actual_toast = check_toast_with_retry(register_page, expected_toast)
                allure.attach(f"预期toast: {expected_toast}\n实际toast: {actual_toast or '无toast消息'}", 
                             name="Toast提示比较", 
                             attachment_type=allure.attachment_type.TEXT)
                assert is_matched == expected_success
            except AssertionError as e:
                allure.attach(str(e), name="Toast检查失败", attachment_type=allure.attachment_type.TEXT)
                raise
        
        if expected_redirect:
            with allure.step("等待重定向到主页"):
                # 等待toast消失
                time.sleep(2)
                assert register_page.is_redirect_to_home()
                
                with allure.step("退出登录"):
                    home_page.click_logout()
                
                with allure.step(f"从数据库中删除注册的用户: {username}"):
                    database.delete_user(username=username)
    
    @allure.story("用户名无效")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case_id", ["register_invalid_username_too_long", "register_invalid_username_exists"])
    def test_invalid_username(self, register_page, register_test_data, case_id):
        """测试无效用户名"""
        # 获取测试数据
        test_cases = {case["case_id"]: case for case in register_test_data}
        test_case = test_cases[case_id]
        
        # 测试数据
        username = test_case["input"]["username"]
        password = test_case["input"]["password"]
        repeat_password = test_case["input"]["repeat_password"]
        nickname = test_case["input"]["nickname"]
        
        # 预期结果
        expected_toast = test_case["expected"]["toast_message"]
        
        with allure.step(f"打开注册页面"):
            register_page.open_register_page()
        
        with allure.step(f"输入用户名: {username}"):
            register_page.input_username(username)
        
        with allure.step(f"输入密码: {password}"):
            register_page.input_password(password)
        
        with allure.step(f"输入重复密码: {repeat_password}"):
            register_page.input_repeat_password(repeat_password)
        
        with allure.step(f"输入昵称: {nickname}"):
            register_page.input_nickname(nickname)
        
        with allure.step("点击注册按钮"):
            register_page.click_register()
        
        with allure.step(f"检查toast提示消息"):
            try:
                is_matched, actual_toast = check_toast_with_retry(register_page, expected_toast)
                allure.attach(f"预期toast: {expected_toast}\n实际toast: {actual_toast or '无toast消息'}", 
                             name="Toast提示比较", 
                             attachment_type=allure.attachment_type.TEXT)
                assert is_matched
            except AssertionError as e:
                allure.attach(str(e), name="Toast检查失败", attachment_type=allure.attachment_type.TEXT)
                raise
    
    @allure.story("密码无效")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case_id", ["register_invalid_password_no_digit", 
                                         "register_invalid_password_too_short", 
                                         "register_invalid_password_too_long"])
    def test_invalid_password(self, register_page, register_test_data, case_id):
        """测试无效密码"""
        # 获取测试数据
        test_cases = {case["case_id"]: case for case in register_test_data}
        test_case = test_cases[case_id]
        
        # 测试数据
        username = test_case["input"]["username"]
        password = test_case["input"]["password"]
        repeat_password = test_case["input"]["repeat_password"]
        nickname = test_case["input"]["nickname"]
        
        # 预期结果
        expected_toast = test_case["expected"]["toast_message"]
        
        with allure.step(f"打开注册页面"):
            register_page.open_register_page()
        
        with allure.step(f"输入用户名: {username}"):
            register_page.input_username(username)
        
        with allure.step(f"输入密码: {password}"):
            register_page.input_password(password)
        
        with allure.step(f"输入重复密码: {repeat_password}"):
            register_page.input_repeat_password(repeat_password)
        
        with allure.step(f"输入昵称: {nickname}"):
            register_page.input_nickname(nickname)
        
        with allure.step("点击注册按钮"):
            register_page.click_register()
        
        with allure.step(f"检查toast提示消息"):
            try:
                is_matched, actual_toast = check_toast_with_retry(register_page, expected_toast)
                allure.attach(f"预期toast: {expected_toast}\n实际toast: {actual_toast or '无toast消息'}", 
                             name="Toast提示比较", 
                             attachment_type=allure.attachment_type.TEXT)
                assert is_matched
            except AssertionError as e:
                allure.attach(str(e), name="Toast检查失败", attachment_type=allure.attachment_type.TEXT)
                raise
    
    @allure.story("密码不一致")
    @allure.severity(allure.severity_level.NORMAL)
    def test_password_mismatch(self, register_page, register_test_data):
        """测试密码不一致"""
        # 获取测试数据
        test_cases = {case["case_id"]: case for case in register_test_data}
        test_case = test_cases["register_invalid_passwords_mismatch"]
        
        # 测试数据
        username = test_case["input"]["username"]
        password = test_case["input"]["password"]
        repeat_password = test_case["input"]["repeat_password"]
        nickname = test_case["input"]["nickname"]
        
        # 预期结果
        expected_toast = test_case["expected"]["toast_message"]
        
        with allure.step(f"打开注册页面"):
            register_page.open_register_page()
        
        with allure.step(f"输入用户名: {username}"):
            register_page.input_username(username)
        
        with allure.step(f"输入密码: {password}"):
            register_page.input_password(password)
        
        with allure.step(f"输入重复密码: {repeat_password}"):
            register_page.input_repeat_password(repeat_password)
        
        with allure.step(f"输入昵称: {nickname}"):
            register_page.input_nickname(nickname)
        
        with allure.step("点击注册按钮"):
            register_page.click_register()
        
        with allure.step(f"检查toast提示消息"):
            try:
                is_matched, actual_toast = check_toast_with_retry(register_page, expected_toast)
                allure.attach(f"预期toast: {expected_toast}\n实际toast: {actual_toast or '无toast消息'}", 
                             name="Toast提示比较", 
                             attachment_type=allure.attachment_type.TEXT)
                assert is_matched
            except AssertionError as e:
                allure.attach(str(e), name="Toast检查失败", attachment_type=allure.attachment_type.TEXT)
                raise
    
    @allure.story("昵称无效")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case_id", ["register_invalid_nickname_too_long", "register_invalid_nickname_exists"])
    def test_invalid_nickname(self, register_page, register_test_data, case_id):
        """测试无效昵称"""
        # 获取测试数据
        test_cases = {case["case_id"]: case for case in register_test_data}
        test_case = test_cases[case_id]
        
        # 测试数据
        username = test_case["input"]["username"]
        password = test_case["input"]["password"]
        repeat_password = test_case["input"]["repeat_password"]
        nickname = test_case["input"]["nickname"]
        
        # 预期结果
        expected_toast = test_case["expected"]["toast_message"]
        
        with allure.step(f"打开注册页面"):
            register_page.open_register_page()
        
        with allure.step(f"输入用户名: {username}"):
            register_page.input_username(username)
        
        with allure.step(f"输入密码: {password}"):
            register_page.input_password(password)
        
        with allure.step(f"输入重复密码: {repeat_password}"):
            register_page.input_repeat_password(repeat_password)
        
        with allure.step(f"输入昵称: {nickname}"):
            register_page.input_nickname(nickname)
        
        with allure.step("点击注册按钮"):
            register_page.click_register()
        
        with allure.step(f"检查toast提示消息"):
            try:
                is_matched, actual_toast = check_toast_with_retry(register_page, expected_toast)
                allure.attach(f"预期toast: {expected_toast}\n实际toast: {actual_toast or '无toast消息'}", 
                             name="Toast提示比较", 
                             attachment_type=allure.attachment_type.TEXT)
                assert is_matched
            except AssertionError as e:
                allure.attach(str(e), name="Toast检查失败", attachment_type=allure.attachment_type.TEXT)
                raise
    
    @allure.story("表单验证")
    @allure.severity(allure.severity_level.MINOR)
    def test_empty_form_validation(self, register_page):
        """测试空表单验证"""
        with allure.step("打开注册页面"):
            register_page.open_register_page()
        
        with allure.step("检查注册按钮是否禁用"):
            assert not register_page.is_register_button_enabled()
        
        with allure.step("输入用户名"):
            register_page.input_username("test_user")
            assert not register_page.is_register_button_enabled()
        
        with allure.step("输入密码"):
            register_page.input_password("test123")
            assert not register_page.is_register_button_enabled()
        
        with allure.step("输入重复密码"):
            register_page.input_repeat_password("test123")
            assert not register_page.is_register_button_enabled()
        
        with allure.step("输入昵称"):
            register_page.input_nickname("test_nick")
            assert register_page.is_register_button_enabled()