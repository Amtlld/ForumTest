# Discuz! Q论坛测试项目

## 项目概述

本项目是对Discuz! Q论坛系统的自动化测试项目，主要测试两个功能模块：
1. 用户注册功能
2. 基本论坛功能：发帖、点赞、评论、用户关注/取消关注、屏蔽/取消屏蔽、发私信

项目使用Pytest+Selenium实现自动化测试，并使用Allure自动生成测试报告。

## 项目结构

```
ForumTest/
├── conftest.py                    # Pytest配置文件，包含固定装置(fixtures)和配置
├── data/                          # 测试数据目录
│   ├── register_test_data.json    # 注册功能测试数据
│   └── forum_test_data.json       # 论坛功能测试数据
├── data_generators/               # 测试数据生成器
│   ├── register_data_generator.py # 注册功能测试数据生成器
│   └── forum_data_generator.py    # 论坛功能测试数据生成器
├── page_objects/                  # 页面对象模式实现
│   ├── base_page.py               # 基础页面类
│   ├── home_page.py               # 主页
│   ├── register_page.py           # 注册页面
│   ├── login_page.py              # 登录页面
│   ├── post_page.py               # 发帖页面
│   ├── thread_page.py             # 帖子页面
│   ├── user_page.py               # 用户主页
│   └── message_page.py            # 私信页面
├── tests/                         # 测试用例
│   ├── test_register.py           # 注册功能测试
│   └── test_forum.py              # 论坛功能测试
├── utils/                         # 工具函数
│   ├── db_utils.py                # 数据库操作工具
│   ├── mail_utils.py              # 邮件发送工具
│   └── webdriver_utils.py         # WebDriver相关工具
├── requirements.txt               # 项目依赖
└── README.md                      # 项目说明
```

## 使用方法

### 1. 环境准备

```bash
# 安装依赖
pip install -r requirements.txt
```

### 2. 生成测试数据

```bash
# 生成注册功能测试数据
python data_generators/register_data_generator.py

# 生成论坛功能测试数据
python data_generators/forum_data_generator.py
```

### 3. 运行测试

```bash
# 运行所有测试
pytest

# 运行注册功能测试
pytest tests/test_register.py

# 运行论坛功能测试
pytest tests/test_forum.py

# 生成Allure报告
pytest --alluredir=./allure-results
allure serve ./allure-results

# 使用无头模式运行并发送报告
pytest --headless --send-report
```

## 测试设计思路

本项目采用等价类划分方法设计测试用例，针对不同功能模块的输入参数进行有效等价类和无效等价类的划分，确保测试覆盖各种场景。

### 注册功能测试

针对用户名、密码、重复密码和昵称等字段进行等价类划分：
- 用户名：长度限制、唯一性约束
- 密码：包含数字、长度限制
- 重复密码：一致性检查
- 昵称：长度限制、唯一性约束

### 论坛功能测试

- 发帖功能：标题和内容的长度限制、分类选择
- 点赞功能：点赞/取消点赞
- 评论功能：评论内容长度限制、空评论检查
- 用户关注/屏蔽：关注/取消关注、屏蔽/取消屏蔽
- 私信功能：私信内容长度限制

## 实现细节

### 1. Page Object模式

项目采用Page Object设计模式，将页面元素和操作封装在对应的页面类中：

- BasePage: 封装基础操作，如元素查找、点击、输入文本等
- 各功能页面: 封装特定页面的元素和操作，如注册、登录、发帖等

### 2. 测试数据生成

采用程序化生成测试数据，确保测试数据的多样性和全面性：

- 根据等价类划分原则生成有效和无效的测试数据
- 生成JSON格式的测试数据文件，便于测试用例使用

### 3. 数据库操作

提供数据库操作工具，用于测试前后的数据准备和清理：

- 删除测试过程中创建的用户
- 查询用户ID和帖子ID等信息

### 4. 测试报告

使用Allure生成丰富的测试报告，并通过邮件发送：

- 记录测试步骤和结果
- 捕获测试失败的截图
- 通过邮件发送测试报告

### 5. 命令行选项

提供丰富的命令行选项，支持灵活的测试配置：

- 选择浏览器类型
- 启用无头模式
- 发送测试报告

## 注意事项

1. 需要确保Discuz! Q论坛系统已经部署在localhost，并且数据库可以正常连接
2. 测试前需要在数据库中准备一个已存在的测试用户，用于登录测试
3. 请确保locator和邮件发送配置正确

## License

本项目采用 [MIT License](LICENSE) 开源协议。