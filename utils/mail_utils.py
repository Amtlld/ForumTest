import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import zipfile
import glob

class EmailUtils:
    """邮件工具类，用于发送邮件和Allure报告"""
    
    def __init__(self, smtp_server, smtp_port, sender, password, receiver):
        """初始化邮件参数"""
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender = sender
        self.password = password
        self.receiver = receiver
    
    def zip_allure_report(self, report_dir="./allure-results", zip_name="allure-report.zip"):
        """压缩Allure报告"""
        if not os.path.exists(report_dir):
            raise FileNotFoundError(f"Allure报告目录不存在: {report_dir}")
        
        # 确保输出的zip文件名有zip扩展名
        if not zip_name.endswith('.zip'):
            zip_name += '.zip'
        
        # 获取报告目录下的所有文件
        report_files = glob.glob(os.path.join(report_dir, "*"))
        
        # 创建zip文件
        with zipfile.ZipFile(zip_name, 'w') as zipf:
            for file in report_files:
                if os.path.isfile(file):
                    zipf.write(file, os.path.basename(file))
        
        return zip_name
    
    def send_email(self, subject, body, attachment_path=None):
        """发送邮件"""
        # 创建邮件对象
        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = self.receiver
        msg['Subject'] = subject
        
        # 添加邮件正文
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # 添加附件
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as f:
                attachment = MIMEApplication(f.read())
                attachment.add_header('Content-Disposition', 'attachment', 
                                      filename=os.path.basename(attachment_path))
                msg.attach(attachment)
        
        # 发送邮件
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.login(self.sender, self.password)
            server.sendmail(self.sender, self.receiver, msg.as_string())
            server.quit()
            return True
        except Exception as e:
            print(f"发送邮件失败: {str(e)}")
            return False
    
    def send_allure_report(self, report_dir="./allure-results", subject="测试报告"):
        """打包并发送Allure报告"""
        try:
            # 压缩Allure报告
            zip_file = self.zip_allure_report(report_dir)
            
            # 发送邮件
            body = "请查收附件中的Allure测试报告。\n\n此邮件由自动化测试系统发送，请勿回复。"
            result = self.send_email(subject, body, zip_file)
            
            # 清理临时文件
            if os.path.exists(zip_file):
                os.remove(zip_file)
            
            return result
        except Exception as e:
            print(f"发送Allure报告失败: {str(e)}")
            return False

email_info = {
    "smtp_server": "smtp.example.com",
    "smtp_port": 80,
    "sender": "sender_email@example.com",
    "password": "your_password",
    "receiver": "receiver_email@foxmail.com"
}

# 创建邮件工具类实例
email_utils = EmailUtils(**email_info)

if __name__ == '__main__':
    email_utils.send_allure_report()