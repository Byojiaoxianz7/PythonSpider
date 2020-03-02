from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

print("自动完成教务网评教，解放你的双手哈哈哈哈\n 制作: 计算机部 - FatTig3R")
print("注意：目前仅支持Chrome")
print("-"*30)
username = input(" 学号: ")
password = input(" 密码: ")
print("-"*30)
print("开始自动化工作，该程序正在后台运行，请耐心等待")
browser = webdriver.Chrome()
browser.get('http://222.30.63.15/NKEMIS/SystemLogin.aspx')
print("正在访问NKEMIS...")
login_username = browser.find_element_by_id('txtUserID')
login_password = browser.find_element_by_id('txtPasswd')
browser.implicitly_wait(30)
login_button = browser.find_element_by_id('ImageButton1')
login_username.send_keys(username)
login_password.send_keys(password)
login_button.click()
time.sleep(2)
# 处理 alert
browser.switch_to.alert.accept()
print("开始处理...")

for k in range(2, 12):
    # 选择 "Enter"
    """
    //*[@id="dgrdCourse"]/tbody/tr[2]/td[5]/a
    //*[@id="dgrdCourse"]/tbody/tr[3]/td[5]/a
    //*[@id="dgrdCourse"]/tbody/tr[9]/td[5]/a
    """
    browser.implicitly_wait(3)
    enter = browser.find_element_by_xpath('//*[@id="dgrdCourse"]/tbody/tr[{}]/td[5]/a'.format(k))
    enter.click()
    # 选择 "优"
    for i in range(3,30):
        try:
            Select(browser.find_element_by_id("dgrdVoteItem__ctl{}_StuVoteScore".format(i))).select_by_visible_text("优")
        except:
            pass

    # 点击 "提交"
    browser.implicitly_wait(30)
    vote_post_button = browser.find_element_by_id('imgbtnSubmit')
    vote_post_button.click()
    time.sleep(3)
    try:
        # 处理 alert
        browser.switch_to.alert.accept()
    except:
        pass
    time.sleep(1)

    # 点击 "返回"
    vote_return_button = browser.find_element_by_id('ImageButton1')
    vote_return_button.click()
    print("完成第{}个".format(k-1))
    time.sleep(2)
print("已经全部完成, 登陆教务网查看成果")
browser.close()