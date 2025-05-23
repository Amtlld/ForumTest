import json
import os
import random
import string

THREAD_ID = "2"
USER_ID = "2"
NICKNAME = "a"

def generate_random_string(length):
    """生成指定长度的随机字符串"""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def generate_random_title(length=20):
    """生成随机标题"""
    return f"测试标题_{generate_random_string(length-5)}"

def generate_random_content(length=100):
    """生成随机内容"""
    return f"测试内容_{generate_random_string(length-5)}"

def generate_post_test_data():
    """生成发帖功能测试数据"""
    test_cases = []

    # 1. 有效等价类 - 正常发帖
    # 1.1 标题和内容正常长度，默认分类
    test_cases.append({
        "case_id": "post_valid_default_category",
        "description": "正常发帖，默认分类",
        "input": {
            "title": generate_random_title(20),
            "content": generate_random_content(200),
            "category": "默认分类"
        },
        "expected": {
            "success": True,
            "toast_message": None,
            "redirect_to_thread": True
        }
    })

    # 1.2 标题和内容正常长度，选择其他分类
    test_cases.append({
        "case_id": "post_valid_other_category",
        "description": "正常发帖，选择其他分类",
        "input": {
            "title": generate_random_title(20),
            "content": generate_random_content(200),
            "category": "其他分类"
        },
        "expected": {
            "success": True,
            "toast_message": None,
            "redirect_to_thread": True
        }
    })

    # 1.3 标题接近最大长度，内容正常
    title_max = generate_random_title(99)  # 标题最大100字符
    test_cases.append({
        "case_id": "post_valid_max_title",
        "description": "标题接近最大长度发帖测试",
        "input": {
            "title": title_max,
            "content": generate_random_content(200),
            "category": "默认分类"
        },
        "expected": {
            "success": True,
            "toast_message": None,
            "redirect_to_thread": True
        }
    })

    # 2. 无效等价类 - 发帖失败
    # 2.1 内容超过50000字符
    content_too_long = generate_random_content(50001)
    test_cases.append({
        "case_id": "post_invalid_content_too_long",
        "description": "内容超长发帖测试",
        "input": {
            "title": generate_random_title(20),
            "content": content_too_long,
            "category": "默认分类"
        },
        "expected": {
            "success": False,
            "toast_message": "不能超过50000字",
            "redirect_to_thread": False
        }
    })

    return test_cases

def generate_like_test_data():
    """生成点赞功能测试数据"""
    test_cases = []

    # 1. 点赞测试
    test_cases.append({
        "case_id": "like_post",
        "description": "点赞帖子测试",
        "input": {
            "thread_id": THREAD_ID,
            "action": "like"
        },
        "expected": {
            "success": True,
            "like_status": True
        }
    })

    # 2. 取消点赞测试
    test_cases.append({
        "case_id": "unlike_post",
        "description": "取消点赞帖子测试",
        "input": {
            "thread_id": THREAD_ID,
            "action": "unlike"
        },
        "expected": {
            "success": True,
            "like_status": False
        }
    })

    return test_cases

def generate_comment_test_data():
    """生成评论功能测试数据"""
    test_cases = []

    # 1. 有效等价类 - 正常评论
    # 1.1 正常长度的评论
    test_cases.append({
        "case_id": "comment_valid_normal",
        "description": "正常评论测试",
        "input": {
            "thread_id": THREAD_ID,
            "content": generate_random_content(100)
        },
        "expected": {
            "success": True,
            "toast_message": None,
            "comment_appears": True
        }
    })

    # 1.2 接近最大长度的评论
    test_cases.append({
        "case_id": "comment_valid_max_length",
        "description": "最大长度评论测试",
        "input": {
            "thread_id": THREAD_ID,
            "content": generate_random_content(4999)  # 评论最大5000字符
        },
        "expected": {
            "success": True,
            "toast_message": None,
            "comment_appears": True
        }
    })

    # 2. 无效等价类 - 评论失败
    # 2.1 空评论
    test_cases.append({
        "case_id": "comment_invalid_empty",
        "description": "空评论测试",
        "input": {
            "thread_id": THREAD_ID,
            "content": ""
        },
        "expected": {
            "success": False,
            "toast_message": "请输入内容",
            "comment_appears": False
        }
    })

    return test_cases

def generate_follow_test_data():
    """生成用户关注功能测试数据"""
    test_cases = []

    # 1. 关注用户测试
    test_cases.append({
        "case_id": "follow_user",
        "description": "关注用户测试",
        "input": {
            "user_id": USER_ID,
            "action": "follow"
        },
        "expected": {
            "success": True,
            "button_text": "已关注"
        }
    })

    # 2. 取消关注用户测试
    test_cases.append({
        "case_id": "unfollow_user",
        "description": "取消关注用户测试",
        "input": {
            "user_id": USER_ID,
            "action": "unfollow"
        },
        "expected": {
            "success": True,
            "button_text": "关注"
        }
    })

    return test_cases

def generate_block_test_data():
    """生成用户屏蔽功能测试数据"""
    test_cases = []

    # 1. 屏蔽用户测试
    test_cases.append({
        "case_id": "block_user",
        "description": "屏蔽用户测试",
        "input": {
            "user_id": USER_ID,
            "action": "block"
        },
        "expected": {
            "success": True,
            "button_text": "解除屏蔽"
        }
    })

    # 2. 取消屏蔽用户测试
    test_cases.append({
        "case_id": "unblock_user",
        "description": "取消屏蔽用户测试",
        "input": {
            "user_id": USER_ID,
            "action": "unblock"
        },
        "expected": {
            "success": True,
            "button_text": "屏蔽"
        }
    })

    return test_cases

def generate_message_test_data():
    """生成私信功能测试数据"""
    test_cases = []

    # 1. 有效等价类 - 正常发送私信
    # 1.1 正常长度的私信
    test_cases.append({
        "case_id": "message_valid_normal",
        "description": "正常私信测试",
        "input": {
            "user_id": USER_ID,
            "nickname": NICKNAME,
            "content": generate_random_content(100)
        },
        "expected": {
            "success": True,
            "toast_message": None,
            "message_appears": True
        }
    })

    # 1.2 接近最大有效长度的私信
    test_cases.append({
        "case_id": "message_valid_max_length",
        "description": "最大有效长度私信测试",
        "input": {
            "user_id": USER_ID,
            "nickname": NICKNAME,
            "content": generate_random_content(450)  # 私信最大有效450字符
        },
        "expected": {
            "success": True,
            "toast_message": None,
            "message_appears": True
        }
    })

    # 2. 无效等价类 - 私信失败
    # 2.1 私信超过450字符
    test_cases.append({
        "case_id": "message_invalid_too_long",
        "description": "私信超长测试",
        "input": {
            "user_id": USER_ID,
            "nickname": NICKNAME,
            "content": generate_random_content(451)  # 超过450字符
        },
        "expected": {
            "success": False,
            "toast_message": "message text 不能大于 450 个字符。",
            "message_appears": False
        }
    })

    return test_cases

def generate_forum_test_data():
    """生成所有论坛功能的测试数据"""
    forum_test_data = {
        "post_tests": generate_post_test_data(),
        "like_tests": generate_like_test_data(),
        "comment_tests": generate_comment_test_data(),
        "follow_tests": generate_follow_test_data(),
        "block_tests": generate_block_test_data(),
        "message_tests": generate_message_test_data()
    }
    return forum_test_data

def save_test_data_to_json(test_data, output_file='../data/forum_test_data.json'):
    """将测试数据保存为JSON文件"""
    # 确保目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=4)
    
    # 计算所有测试用例总数
    total_tests = sum(len(test_data[key]) for key in test_data)
    print(f"已生成 {total_tests} 个论坛功能测试用例，保存到 {output_file}")

if __name__ == '__main__':
    test_data = generate_forum_test_data()
    save_test_data_to_json(test_data) 