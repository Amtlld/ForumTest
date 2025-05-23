import pytest
import allure
import time

@allure.epic("论坛测试")
@allure.feature("论坛功能")
class TestForum:
    
    @allure.story("发帖功能")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("case_id", ["post_valid_default_category", "post_valid_other_category", "post_valid_max_title"])
    def test_valid_post(self, logged_in_user, post_page, forum_test_data, case_id):
        """测试有效发帖"""
        # 获取测试数据
        test_cases = {case["case_id"]: case for case in forum_test_data["post_tests"]}
        test_case = test_cases[case_id]
        
        # 测试数据
        title = test_case["input"]["title"]
        content = test_case["input"]["content"]
        category = test_case["input"]["category"]
        
        # 预期结果
        expected_success = test_case["expected"]["success"]
        expected_redirect = test_case["expected"]["redirect_to_thread"]
        
        with allure.step(f"打开发帖页面"):
            post_page.open_post_page()
        
        with allure.step(f"输入标题: {title}"):
            post_page.input_title(title)
        
        with allure.step(f"输入内容: {content[:100]}..."):
            post_page.input_content(content)
        
        with allure.step(f"选择分类: {category}"):
            post_page.select_category(category)
        
        with allure.step("点击发布按钮"):
            post_page.click_post_button()
        
        if expected_redirect:
            with allure.step("等待重定向到帖子页面"):
                assert post_page.is_redirect_to_thread() == expected_success
    
    '''@allure.story("发帖失败")
    @allure.severity(allure.severity_level.NORMAL)
    def test_invalid_post(self, logged_in_user, post_page, forum_test_data):
        """测试无效发帖 - 内容超长"""
        # 获取测试数据
        test_cases = {case["case_id"]: case for case in forum_test_data["post_tests"]}
        test_case = test_cases["post_invalid_content_too_long"]
        
        # 测试数据
        title = test_case["input"]["title"]
        content = test_case["input"]["content"]
        category = test_case["input"]["category"]
        
        # 预期结果
        expected_toast = test_case["expected"]["toast_message"]
        
        with allure.step(f"打开发帖页面"):
            post_page.open_post_page()
        
        with allure.step(f"输入标题: {title}"):
            post_page.input_title(title)
        
        with allure.step(f"输入内容: {content[:100]}..."):
            post_page.input_content(content)
        
        with allure.step(f"选择分类: {category}"):
            post_page.select_category(category)
        
        with allure.step("点击发布按钮"):
            post_page.click_post_button()
        
        with allure.step(f"检查toast提示消息: {expected_toast}"):
            assert post_page.check_toast_message(expected_toast)'''
    
    @allure.story("点赞、取消点赞功能")
    @allure.severity(allure.severity_level.NORMAL)
    def test_unlike_post(self, logged_in_user, thread_page, forum_test_data):
        """测试取消点赞帖子"""
        # 获取测试数据
        test_cases = {case["case_id"]: case for case in forum_test_data["like_tests"]}
        test_case = test_cases["unlike_post"]
        
        # 测试数据
        thread_id = test_case["input"]["thread_id"]
        
        # 预期结果
        expected_like_status = test_case["expected"]["like_status"]
        
        with allure.step(f"打开帖子页面: {thread_id}"):
            thread_page.open_thread_page(thread_id)
        
        # 先点赞
        with allure.step("先点赞"):
            thread_page.click_like_button()
            assert thread_page.is_thread_liked()

        # 再取消点赞
        with allure.step("再取消点赞"):
            thread_page.click_like_button()
        
        with allure.step("检查点赞状态"):
            assert thread_page.is_thread_liked() == expected_like_status
    
    @allure.story("评论功能")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case_id", ["comment_valid_normal", "comment_valid_max_length"])
    def test_valid_comment(self, logged_in_user, thread_page, forum_test_data, case_id):
        """测试有效评论"""
        # 获取测试数据
        test_cases = {case["case_id"]: case for case in forum_test_data["comment_tests"]}
        test_case = test_cases[case_id]
        
        # 测试数据
        thread_id = test_case["input"]["thread_id"]
        content = test_case["input"]["content"]
        
        # 预期结果
        expected_success = test_case["expected"]["success"]
        
        with allure.step(f"打开帖子页面: {thread_id}"):
            thread_page.open_thread_page(thread_id)
        
        with allure.step(f"输入评论: {content[:50]}..."):
            thread_page.input_comment(content)
        
        with allure.step("提交评论"):
            thread_page.submit_comment()
            # 等待评论显示
            time.sleep(2)
        
        with allure.step("检查评论是否显示"):
            assert thread_page.is_comment_present(content) == expected_success
    
    @allure.story("评论失败")
    @allure.severity(allure.severity_level.NORMAL)
    def test_invalid_comment(self, logged_in_user, thread_page, forum_test_data):
        """测试无效评论 - 空评论"""
        # 获取测试数据
        test_cases = {case["case_id"]: case for case in forum_test_data["comment_tests"]}
        test_case = test_cases["comment_invalid_empty"]
        
        # 测试数据
        thread_id = test_case["input"]["thread_id"]
        content = test_case["input"]["content"]
        
        # 预期结果
        expected_toast = test_case["expected"]["toast_message"]
        
        with allure.step(f"打开帖子页面: {thread_id}"):
            thread_page.open_thread_page(thread_id)
        
        with allure.step("输入空评论"):
            thread_page.input_comment(content)
        
        with allure.step("提交评论"):
            thread_page.submit_comment()
        
        with allure.step(f"检查toast提示消息: {expected_toast}"):
            assert thread_page.check_toast_message(expected_toast)
    
    @allure.story("关注用户")
    @allure.severity(allure.severity_level.NORMAL)
    def test_follow_user(self, logged_in_user, user_page, forum_test_data):
        """测试关注用户"""
        # 获取测试数据
        test_cases = {case["case_id"]: case for case in forum_test_data["follow_tests"]}
        test_case = test_cases["follow_user"]
        
        # 测试数据
        user_id = test_case["input"]["user_id"]
        
        # 预期结果
        expected_button_text = test_case["expected"]["button_text"]
        
        with allure.step(f"打开用户主页: {user_id}"):
            user_page.open_user_page(user_id)
        
        # 如果已经关注，先取消关注
        if user_page.is_following():
            with allure.step("已关注状态，先取消关注"):
                user_page.click_follow_button()
                time.sleep(3)
        
        with allure.step("点击关注按钮"):
            user_page.click_follow_button()
            time.sleep(3)
        
        with allure.step(f"检查关注按钮文本: {expected_button_text}"):
            assert user_page.get_follow_button_text() == expected_button_text
        
        # 取消关注，恢复初始状态
        with allure.step("取消关注"):
            user_page.click_follow_button()
    
    @allure.story("取消关注用户")
    @allure.severity(allure.severity_level.NORMAL)
    def test_unfollow_user(self, logged_in_user, user_page, forum_test_data):
        """测试取消关注用户"""
        # 获取测试数据
        test_cases = {case["case_id"]: case for case in forum_test_data["follow_tests"]}
        test_case = test_cases["unfollow_user"]
        
        # 测试数据
        user_id = test_case["input"]["user_id"]
        
        # 预期结果
        expected_button_text = test_case["expected"]["button_text"]
        
        with allure.step(f"打开用户主页: {user_id}"):
            user_page.open_user_page(user_id)
        
        # 如果未关注，先关注
        if not user_page.is_following():
            with allure.step("未关注状态，先关注"):
                user_page.click_follow_button()
                time.sleep(3)
        
        with allure.step("点击取消关注按钮"):
            user_page.click_follow_button()
            time.sleep(3)
        
        with allure.step(f"检查关注按钮文本: {expected_button_text}"):
            assert user_page.get_follow_button_text() == expected_button_text
    
    @allure.story("屏蔽用户")
    @allure.severity(allure.severity_level.NORMAL)
    def test_block_user(self, logged_in_user, user_page, forum_test_data):
        """测试屏蔽用户"""
        # 获取测试数据
        test_cases = {case["case_id"]: case for case in forum_test_data["block_tests"]}
        test_case = test_cases["block_user"]
        
        # 测试数据
        user_id = test_case["input"]["user_id"]
        
        # 预期结果
        expected_button_text = test_case["expected"]["button_text"]
        
        with allure.step(f"打开用户主页: {user_id}"):
            user_page.open_user_page(user_id)
        
        # 如果已经屏蔽，先取消屏蔽
        if user_page.is_blocking():
            with allure.step("已屏蔽状态，先取消屏蔽"):
                user_page.click_block_button()
                time.sleep(3)
        
        with allure.step("点击屏蔽按钮"):
            user_page.click_block_button()
            time.sleep(3)
        
        with allure.step(f"检查屏蔽按钮文本: {expected_button_text}"):
            assert user_page.get_block_button_text() == expected_button_text
        
        # 取消屏蔽，恢复初始状态
        with allure.step("取消屏蔽"):
            user_page.click_block_button()
    
    @allure.story("取消屏蔽用户")
    @allure.severity(allure.severity_level.NORMAL)
    def test_unblock_user(self, logged_in_user, user_page, forum_test_data):
        """测试取消屏蔽用户"""
        # 获取测试数据
        test_cases = {case["case_id"]: case for case in forum_test_data["block_tests"]}
        test_case = test_cases["unblock_user"]
        
        # 测试数据
        user_id = test_case["input"]["user_id"]
        
        # 预期结果
        expected_button_text = test_case["expected"]["button_text"]
        
        with allure.step(f"打开用户主页: {user_id}"):
            user_page.open_user_page(user_id)
        
        # 如果未屏蔽，先屏蔽
        if not user_page.is_blocking():
            with allure.step("未屏蔽状态，先屏蔽"):
                user_page.click_block_button()
                time.sleep(3)
        
        with allure.step("点击取消屏蔽按钮"):
            user_page.click_block_button()
            time.sleep(3)
        
        with allure.step(f"检查屏蔽按钮文本: {expected_button_text}"):
            assert user_page.get_block_button_text() == expected_button_text
    
    @allure.story("发送私信")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case_id", ["message_valid_normal", "message_valid_max_length"])
    def test_valid_message(self, logged_in_user, message_page, forum_test_data, case_id):
        """测试有效私信"""
        # 获取测试数据
        test_cases = {case["case_id"]: case for case in forum_test_data["message_tests"]}
        test_case = test_cases[case_id]
        
        # 测试数据
        user_id = test_case["input"]["user_id"]
        nickname = test_case["input"]["nickname"]
        content = test_case["input"]["content"]
        
        # 预期结果
        expected_success = test_case["expected"]["success"]
        
        with allure.step(f"打开私信页面: {user_id}, {nickname}"):
            message_page.open_message_page(user_id, nickname)
        
        with allure.step(f"输入私信: {content[:50]}..."):
            message_page.input_message(content)
        
        with allure.step("发送私信"):
            message_page.click_send_button()
            # 等待私信显示
            time.sleep(2)
        
        with allure.step("检查私信是否发送成功"):
            assert message_page.is_message_sent(content) == expected_success
    
    @allure.story("发送私信失败")
    @allure.severity(allure.severity_level.NORMAL)
    def test_invalid_message(self, logged_in_user, message_page, forum_test_data):
        """测试无效私信 - 超长私信"""
        # 获取测试数据
        test_cases = {case["case_id"]: case for case in forum_test_data["message_tests"]}
        test_case = test_cases["message_invalid_too_long"]
        
        # 测试数据
        user_id = test_case["input"]["user_id"]
        nickname = test_case["input"]["nickname"]
        content = test_case["input"]["content"]
        
        # 预期结果
        expected_toast = test_case["expected"]["toast_message"]
        
        with allure.step(f"打开私信页面: {user_id}, {nickname}"):
            message_page.open_message_page(user_id, nickname)
        
        with allure.step(f"输入超长私信: {content[:50]}..."):
            message_page.input_message(content)
        
        with allure.step("发送私信"):
            message_page.click_send_button()
        
        with allure.step(f"检查toast提示消息: {expected_toast}"):
            assert message_page.check_toast_message(expected_toast) 