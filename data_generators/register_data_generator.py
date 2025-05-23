import json
import os
import random
import string

def generate_random_string(length):
    """生成指定长度的随机字符串"""
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def generate_random_username(length=8):
    """生成指定长度的随机用户名"""
    return 'user_' + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def generate_random_nickname(length=8):
    """生成指定长度的随机昵称"""
    return 'nick_' + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def generate_valid_password(length=10):
    """生成有效的密码（包含数字且长度符合要求）"""
    # 确保至少有一个数字
    pwd = random.choice(string.digits)
    # 添加剩余字符
    pwd += ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length-1))
    return pwd

def generate_register_test_data():
    """生成注册功能的测试数据"""
    test_cases = []
    
    # 1. 有效等价类 - 成功注册
    for i in range(3):
        username = generate_random_username()
        password = generate_valid_password()
        nickname = generate_random_nickname()
        
        test_cases.append({
            "case_id": f"register_valid_{i+1}",
            "description": "有效注册测试",
            "input": {
                "username": username,
                "password": password,
                "repeat_password": password,
                "nickname": nickname
            },
            "expected": {
                "success": True,
                "toast_message": "注册成功",
                "redirect_to_home": True
            }
        })

    # 2. 无效等价类 - 用户名测试
    # 2.1 用户名超过15个字符
    username_too_long = generate_random_string(16)
    password = generate_valid_password()
    test_cases.append({
        "case_id": "register_invalid_username_too_long",
        "description": "用户名超长测试",
        "input": {
            "username": username_too_long,
            "password": password,
            "repeat_password": password,
            "nickname": generate_random_nickname()
        },
        "expected": {
            "success": False,
            "toast_message": "用户名 不能大于 15 个字符。",
            "redirect_to_home": False
        }
    })
    
    # 2.2 用户名已存在
    password = generate_valid_password()
    test_cases.append({
        "case_id": "register_invalid_username_exists",
        "description": "用户名已存在测试",
        "input": {
            "username": "test01",  # 这个用户名已存在
            "password": password,
            "repeat_password": password,
            "nickname": generate_random_nickname()
        },
        "expected": {
            "success": False,
            "toast_message": "用户名 已经存在。",
            "redirect_to_home": False
        }
    })
    
    # 3. 无效等价类 - 密码测试
    # 3.1 密码不包含数字
    password_no_digit = ''.join(random.choice(string.ascii_letters) for _ in range(10))
    test_cases.append({
        "case_id": "register_invalid_password_no_digit",
        "description": "密码不包含数字测试",
        "input": {
            "username": generate_random_username(),
            "password": password_no_digit,
            "repeat_password": password_no_digit,
            "nickname": generate_random_nickname()
        },
        "expected": {
            "success": False,
            "toast_message": "密码格式不正确，必须包含数字。",
            "redirect_to_home": False
        }
    })
    
    # 3.2 密码长度小于6个字符
    password_too_short = random.choice(string.digits) + ''.join(random.choice(string.ascii_letters) for _ in range(4))
    test_cases.append({
        "case_id": "register_invalid_password_too_short",
        "description": "密码过短测试",
        "input": {
            "username": generate_random_username(),
            "password": password_too_short,
            "repeat_password": password_too_short,
            "nickname": generate_random_nickname()
        },
        "expected": {
            "success": False,
            "toast_message": "密码 至少为 6 个字符。",
            "redirect_to_home": False
        }
    })
    
    # 3.3 密码长度大于50个字符
    password_too_long = random.choice(string.digits) + ''.join(random.choice(string.ascii_letters) for _ in range(50))
    test_cases.append({
        "case_id": "register_invalid_password_too_long",
        "description": "密码过长测试",
        "input": {
            "username": generate_random_username(),
            "password": password_too_long,
            "repeat_password": password_too_long,
            "nickname": generate_random_nickname()
        },
        "expected": {
            "success": False,
            "toast_message": "密码 不能大于 50 个字符。",
            "redirect_to_home": False
        }
    })
    
    # 4. 无效等价类 - 重复密码测试
    # 4.1 重复密码与密码不一致
    password_valid = generate_valid_password()
    password_mismatch = generate_valid_password() + "mismatch"
    test_cases.append({
        "case_id": "register_invalid_passwords_mismatch",
        "description": "密码不一致测试",
        "input": {
            "username": generate_random_username(),
            "password": password_valid,
            "repeat_password": password_mismatch,
            "nickname": generate_random_nickname()
        },
        "expected": {
            "success": False,
            "toast_message": "两次输入的密码不一致",
            "redirect_to_home": False
        }
    })
    
    # 5. 无效等价类 - 昵称测试
    # 5.1 昵称超过15个字符
    password = generate_valid_password()
    nickname_too_long = generate_random_string(16)
    test_cases.append({
        "case_id": "register_invalid_nickname_too_long",
        "description": "昵称超长测试",
        "input": {
            "username": generate_random_username(),
            "password": password,
            "repeat_password": password,
            "nickname": nickname_too_long
        },
        "expected": {
            "success": False,
            "toast_message": "昵称长度超过15个字符",
            "redirect_to_home": False
        }
    })
    
    # 5.2 昵称已存在
    password = generate_valid_password()
    test_cases.append({
        "case_id": "register_invalid_nickname_exists",
        "description": "昵称已存在测试",
        "input": {
            "username": generate_random_username(),
            "password": password,
            "repeat_password": password,
            "nickname": "test01"  # 这个昵称已存在
        },
        "expected": {
            "success": False,
            "toast_message": "昵称已经存在",
            "redirect_to_home": False
        }
    })
    
    return test_cases

def save_test_data_to_json(test_cases, output_file='../data/register_test_data.json'):
    """将测试数据保存为JSON文件"""
    # 确保目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(test_cases, f, ensure_ascii=False, indent=4)
    
    print(f"已生成 {len(test_cases)} 个注册功能测试用例，保存到 {output_file}")

if __name__ == '__main__':
    test_cases = generate_register_test_data()
    save_test_data_to_json(test_cases) 