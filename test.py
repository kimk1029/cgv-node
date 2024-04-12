import smtplib
from email.mime.text import MIMEText
import threading
import time
import gc
from selenium.webdriver.common.alert import Alert
import pyperclip
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import getopt
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import telegram

telegram_token = '5657392155:AAE980y3EqAYJHdF3ZzsVJv-3zf4V28ViRU'
telegram_id = '1416605644'

driverlist=[]

# -----------------------------------------------------------------------------
# - Name : send_telegram_msg
# - Desc : 텔레그램 메세지 전송
# - Input
#   1) message : 메세지
# -----------------------------------------------------------------------------
def send_telegram_message(message):
    # 5413864535:AAHmzU-DyeU31EeTBPpSlxVnlOTLr9U77SE
    # https://api.telegram.org/5413864535:AAHmzU-DyeU31EeTBPpSlxVnlOTLr9U77SE/getUpdates
    try:
        # 텔레그램 메세지 발송
        bot = telegram.Bot(telegram_token)
        print("########--->>")
        print(bot)
        res = bot.sendMessage(chat_id=telegram_id, text=message)

        return res

    # ----------------------------------------
    # 모든 함수의 공통 부분(Exception 처리)
    # ----------------------------------------
    except Exception:
        raise


# import seleniumwire
# from seleniumwire.webdriver.common.alert import Alert
# import algoseats
# 5413864535:AAHmzU-DyeU31EeTBPpSlxVnlOTLr9U77SE

BGmode = False
# BGmode=True
# INPUTmode = False
INPUTmode = False

load0_lock = threading.Lock()


def arg(argv):
    FILE_NAME = argv[0]
    global MOVIE_NAME
    global CGVID
    global CGVPW
    global START_DAY
    global END_DAY
    global FIRST_T
    global LAST_T

    if INPUTmode == True:
        MOVIE_NAME = input("영화 이름 입력(단어만 입력)ex)\"신비한 동물사전\" 일경우 \"신비한\" 혹은 \"동물사전\"만 입력 :")
        # MOVIE_NAME = "모비" #부분만 입력가능
        CGVID = input("CGV 아이디 입력:")  # id
        CGVPW = input("CGV 비번 입력:")  # 비번
        print("예시 4월 2일 부터 4월 3일의 15시부터 19시 사이에 \"시작\"하는 영화 모두 다 열어서 자리찾기")
        START_DAY = input("시작 날짜 입력ex)20220402:")
        END_DAY = input("종료 날짜 입력ex)20220403:")
        FIRST_T = input("시작 시간 입력ex)1500:")
        LAST_T = input("종료 시간 입력ex)1900:")

    else:
        MOVIE_NAME = "와칸다"  # 부분만 입력가능
        CGVID = "kimk1029"
        CGVPW = "aormsja!4"
        print("예시 4월 2일 부터 4월 3일의 15시부터 19시 사이에 \"시작\"하는 영화 모두 다 열어서 자리찾기")

        START_DAY = 20221126
        END_DAY = 20221126
        FIRST_T = 1600
        LAST_T = 2000

    try:
        opts, etc_args = getopt.getopt(argv[1:], \
                                       "hm:i:p:s:e:f:l:",
                                       ["help", "name=", "id=", "pw=", "start=", "end=", "first=", "last="])

    except getopt.GetoptError:  # 옵션지정이 올바르지 않은 경우
        print(FILE_NAME, '-m -i -p -s -e -f -l')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(FILE_NAME, '-m -i -p -s -e -f -l')
            sys.exit()

        elif opt in ("-m", "--name"):  #
            MOVIE_NAME = str(arg)

        elif opt in ("-i", "--id"):
            CGVID = str(arg)

        elif opt in ("-p", "--pw"):
            CGVPW = str(arg)

        elif opt in ("-s", "--start"):
            START_DAY = int(arg)

        elif opt in ("-e", "--end"):
            END_DAY = int(arg)

        elif opt in ("-f", "--first"):
            FIRST_T = int(arg)

        elif opt in ("-l", "--last"):
            LAST_T = int(arg)


def loginBG(driver):
    # send_telegram_message("로그인")
    url = "https://www.cgv.co.kr/user/login/?returnURL=https%3a%2f%2fwww.cgv.co.kr%2fdefault.aspx"
    driver.get(url)

    tag_id = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id=\"txtUserId\"][@name=\"txtUserId\"]")))
    tag_id.send_keys(CGVID)

    tag_pw = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id=\"txtPassword\"][@name=\"txtPassword\"]"))
    )
    tag_pw.send_keys(CGVPW)

    driver.find_element(By.XPATH, "//button[@id=\"submit\"][@title=\"로그인\"]").click()
    print("로그인 접속")

    try:
        driver.find_element(By.XPATH, "//a[@id=\"ctl00_PlaceHolderContent_btn_pw_chag_later\"]").click()
        print("나중에 변경하기 클릭")
    except:
        print("비번변경스킵")


def login(driver):
    send_telegram_message("로그인")
    url = "https://www.cgv.co.kr/user/login/?returnURL=https%3a%2f%2fwww.cgv.co.kr%2fdefault.aspx"
    driver.get(url)
    for i in range(1, 10):
        try:
            tag_id = driver.find_element(By.XPATH, "//input[@id=\"txtUserId\"][@name=\"txtUserId\"]")
            tag_pw = driver.find_element(By.XPATH, "//input[@id=\"txtPassword\"][@name=\"txtPassword\"]")
            load0_lock.acquire()
            # pyperclip.copy('')
            pyperclip.copy(CGVID)
            tag_id.send_keys(Keys.CONTROL, 'v')
            load0_lock.release()

            load0_lock.acquire()
            # pyperclip.copy('')
            pyperclip.copy(CGVPW)
            tag_pw.send_keys(Keys.CONTROL, 'v')
            pyperclip.copy("1")
            load0_lock.release()

            driver.find_element(By.XPATH, "//button[@id=\"submit\"][@title=\"로그인\"]").click()
            print("로그인 접속")
            break
        except:
            print("로그인 건너뜀")

    # driver.find_element(By.XPATH,"//a[@id=\"ctl00_PlaceHolderContent_btn_pw_chag_later\"]")
    try:
        driver.find_element(By.XPATH, "//a[@id=\"ctl00_PlaceHolderContent_btn_pw_chag_later\"]").click()
        print("나중에 변경하기 클릭")
    except:
        print("비번변경스킵")


def find_movie(driver, name):
    url = "http://www.cgv.co.kr/ticket/"
    driver.get(url)
    iframe = driver.find_element(By.XPATH, "//iframe[@title=\"CGV 빠른예매\"]")
    driver.switch_to.frame(iframe)
    passvalue = False
    mlist = []
    while True:
        try:
            mlist = driver.find_elements(By.XPATH,
                                         "//div[@class=\"movie-list nano has-scrollbar has-scrollbar-y\"]/ul/li")
            if len(mlist) > 0:
                # print(theater.get_attribute("theater_cd"))
                break
            # movie=driver.find_element(By.XPATH,"//a[@title=\"" + name + "\"]")
            # delayclick(movie,"영화")
            # driver.find_element(By.XPATH,"//div[@class=\"selectbox-movie-type checkedBD\"]")
            # passvalue=True
            # break
        except:
            print("로딩중,")

    for mov in mlist:
        if name in mov.text:
            if "[" not in mov.text:
                thatmov = mov
                mov1 = mov.find_element(By.XPATH, "a")
                delayclick(mov1, "영화")
                passvalue = True
                break

    if passvalue == False:
        return passvalue

    # delayclick(thatmov, "영화확실")

    while True:
        if "press" in thatmov.get_attribute("class"):
            break

    while True:
        try:
            checkbox = driver.find_element(By.XPATH, "//div[@class=\"selectbox-movie-type checkedBD\"]")
            print("트라이")
            print(checkbox.get_attribute("style"))
            break
            # driver.find_element(By.XPATH,"//a[@data-type=\"ALL\"]")
        except:
            print("로딩중")

    try:
        imax = driver.find_element(By.XPATH, "//a[@data-type=\"IMAX\"]")
        delayclick(imax, "IMAX")
        passvalue = True
    except:
        passvalue = False

    if passvalue == False:
        return passvalue

    # theater=None
    passvalue = False
    # time.sleep(3)
    for i in range(1, 500):
        try:
            theater = driver.find_element(By.XPATH, "//li[@theater_cd=\"0013\"]")
            theater.click()
            list = driver.find_elements(By.XPATH, "//ul[@class=\"content scroll-y\"]/div/li")
            if len(list) > 0:
                passvalue = True
                print(theater.get_attribute("theater_cd"))
                break
        except:
            print("로딩중")

    return passvalue


def get_option(driver):
    list = driver.find_elements(By.XPATH, "//ul[@class=\"content scroll-y\"]/div/li")
    daylist = []
    for day in list:
        if (day.get_attribute("class") != "month dimmed"):
            if (day.get_attribute("class") != "day dimmed") and (
                    day.get_attribute("class") != "day day-sat dimmed") and (
                    day.get_attribute("class") != "day day-sun dimmed"):
                daylist.append(day)
    print("::daylist::")
    return daylist


def select_day_time(driver, name, day, time):
    loginBG(driver)
    movie_ready = False
    while movie_ready == False:
        find_movie(driver, name)
        # time.sleep(0.5)
        daylist = get_option(driver)
        theday = []
        for yymmdd in daylist:
            if yymmdd.get_attribute("date") == day:
                theday.append(yymmdd)

        delayclick(theday[0], "날짜")

        list = driver.find_elements(By.XPATH, "//div[@class=\"theater\"]/ul/li")
        while len(list) < 1:
            list = driver.find_elements(By.XPATH, "//div[@class=\"theater\"]/ul/li")
        for i in range(1, 20):
            list = driver.find_elements(By.XPATH, "//div[@class=\"theater\"]/ul/li")

        for thetime in list:
            if thetime.get_attribute("play_start_tm") == time:
                if thetime.find_element(By.XPATH, "./a/span[@class=\"count\"]").text != "준비중":
                    movie_ready = True
                    delayclick(thetime, "시간")

    # time.sleep(1)
    select = driver.find_element(By.XPATH, "//a[@class=\"btn-right on\"]")
    delayclick(select, "좌석선택")


def seatselect(driver):
    # popup1=driver.find_elements(By.XPATH,"//div[@class=\"ft_layer_popup popup_alert w450 ko\"]/div[@class=\"ft\"]")
    # if len(popup1)>0:
    #     popup1[0].click()
    # popup2 = driver.find_elements(By.XPATH,"//div[@class=\"ft_layer_popup popup_alert ko\"]/div[@class=\"ft\"]")
    # if len(popup2)>0:
    #     popup2[0].click()
    # time.sleep(0.5)
    # while True:
    #     try:
    #         popup1 = driver.find_element(By.XPATH,
    #             "//div[@class=\"ft_layer_popup popup_alert w450 ko\"]/div[@class=\"ft\"]")
    #         popup1.click()
    #         popup2 = driver.find_element(By.XPATH,"//div[@class=\"ft_layer_popup popup_alert ko\"]/div[@class=\"ft\"]")
    #         break
    #     except:
    #         print("로딩중")

    # time.sleep(1)
    # while True:
    #     try:
    #         popup2 = driver.find_element(By.XPATH,"//div[@class=\"ft_layer_popup popup_alert ko\"]/div[@class=\"ft\"]")
    #         popup2.click()
    #         break
    #     except:
    #         print("로딩중")
    #         popup1 = driver.find_element(By.XPATH,
    #             "//div[@class=\"ft_layer_popup popup_alert w450 ko\"]/div[@class=\"ft\"]")
    #         popup1.click()
    #
    # try:
    #     popup2 = driver.find_element(By.XPATH,"//div[@class=\"ft_layer_popup popup_alert ko\"]/div[@class=\"ft\"]")
    #     popup2.click()
    # except:
    #     print("로딩중")

    #############12세 관람########
    time.sleep(1)
    try:
        popup2 = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@class=\"ft_layer_popup popup_alert w450 ko\"]/div[@class=\"ft\"]"))
        )
        popup2.click()
        popup2.click()
        popup2.click()
        print("관람등급 클릭완료")
    except:
        print("관람등급 패스33")
        try:
            popup2 = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@class=\"ft_layer_popup popup_alert ko\"]/div[@class=\"ft\"]"))
            )
            popup2.click()
            popup2.click()
            print("관람등급 클릭완료22")
        except:
            print("관람등급 패스44")

    passvalue = False
    while passvalue == False:
        while True:
            twoselect = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//li[@data-count=\"2\"][@type=\"adult\"]"))
            )
            if twoselect.get_attribute("class") != "selected":
                # twoselect.click()
                element = driver.find_element(By.XPATH, "//li[@data-count=\"2\"][@type=\"adult\"]")
                driver.execute_script("arguments[0].click();", element)
            else:
                break
            break
        # print("2연좌석선택")

        row = "I"
        # row = "C"
        row = ord(row)
        for i in range(5):
            value = checkseat_byline(driver, chr(row))
            if value == "reset":
                break
            if value == True:
                passvalue = value

                # pay_public(driver)
                break
            row += 1

        gc.collect()
        if passvalue == False:
            # driver.find_element(By.XPATH,"//a[@class=\"btn-refresh\"]").click()
            refresh = driver.find_element(By.XPATH, "//a[@class=\"btn-refresh\"]")
            driver.execute_script("arguments[0].click();", refresh)


def pay_public(driver):
    # 계좌이체
    time.sleep(2)
    while True:
        try:
            driver.find_element(By.XPATH, "//input[@name=\"last_pay_radio\"][@value=\"4\"]").click()
            break
        except:
            print("wait a")

    time.sleep(2)

    gopay = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@title=\"결제하기\"]")))
    gopay.click()
    # driver.find_element(By.XPATH,"//a[@title=\"결제하기\"]").click()
    time.sleep(2)
    while True:
        try:
            driver.find_element(By.XPATH, "//input[@id=\"agreementAll\"]").click()
            break
        except:
            print("wait b")

    time.sleep(2)
    while True:
        try:
            driver.find_element(By.XPATH, "//input[@id=\"resvConfirm\"]").click()
            break
        except:
            print("wait c")

    time.sleep(2)
    driver.find_element(By.XPATH, "//a[@title=\"예매 결제하기\"]").click()

    time.sleep(2)
    driver.switch_to.window(driver.window_handles[1])
    # phonenum = driver.find_element(By.XPATH,"//input[@name=\"cphoneNo\"]")

    phonenum = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@name=\"cphoneNo\"]"))
    )
    phonenum.send_keys(MYPHONE)

    driver.find_element(By.XPATH, "//button[@id=\"send\"]").click()
    # driver.save_screenshot("D://screenshot.png")
    # 63*6=378, 63*3=189, 63*9=567
    time.sleep(5)

    num1 = driver.find_element(By.XPATH, "//div[@data-pos-x=\"0\"][@data-pos-y=\"205\"]")
    num2 = driver.find_element(By.XPATH, "//div[@data-pos-x=\"63\"][@data-pos-y=\"205\"]")
    num3 = driver.find_element(By.XPATH, "//div[@data-pos-x=\"126\"][@data-pos-y=\"205\"]")
    num4 = driver.find_element(By.XPATH, "//div[@data-pos-x=\"189\"][@data-pos-y=\"205\"]")
    num5 = driver.find_element(By.XPATH, "//div[@data-pos-x=\"252\"][@data-pos-y=\"205\"]")
    num6 = driver.find_element(By.XPATH, "//div[@data-pos-x=\"315\"][@data-pos-y=\"205\"]")
    num7 = driver.find_element(By.XPATH, "//div[@data-pos-x=\"378\"][@data-pos-y=\"205\"]")
    num8 = driver.find_element(By.XPATH, "//div[@data-pos-x=\"441\"][@data-pos-y=\"205\"]")
    num9 = driver.find_element(By.XPATH, "//div[@data-pos-x=\"504\"][@data-pos-y=\"205\"]")
    num0 = driver.find_element(By.XPATH, "//div[@data-pos-x=\"567\"][@data-pos-y=\"205\"]")

    for i in str(PAY_PW):
        if i == "1":
            num1.click()
            time.sleep(0.5)
        elif i == "2":
            num2.click()
            time.sleep(0.5)
        elif i == "3":
            num3.click()
            time.sleep(0.5)
        elif i == "4":
            num4.click()
            time.sleep(0.5)
        elif i == "5":
            num5.click()
            time.sleep(0.5)
        elif i == "6":
            num6.click()
            time.sleep(0.5)
        elif i == "7":
            num7.click()
            time.sleep(0.5)
        elif i == "8":
            num8.click()
            time.sleep(0.5)
        elif i == "9":
            num9.click()
            time.sleep(0.5)
        elif i == "0":
            num0.click()
            time.sleep(0.5)

    time.sleep(2)
    while True:
        try:
            driver.find_element(By.XPATH, "//button[@id=\"send\"][@onclick=\"order();\"]").click()
            break
        except:
            print("lastwait")

    time.sleep(2)
    while True:
        try:
            driver.find_element(By.XPATH,
                                "//button[@id=\"proceed-button\"][@class=\"secondary-button small-link\"]").click()
            break
        except:
            print("lastwait2")
    # 계좌이체 끝


def checkseat_byline(driver, row, ):
    rows = driver.find_elements(By.XPATH, "//div[@class=\"row\"]")
    therow = None
    for row_candidate in rows:
        if row_candidate.find_element(By.CLASS_NAME, "label").text == row:
            therow = row_candidate
            break

    nums = therow.find_elements(By.XPATH, "div[@class=\"seat_group\"]/div[@class=\"group\"]/div/a")

    for num_candidate in nums:
        time.sleep(0.015)
        selectnum = int(num_candidate.text)
        if selectnum >= 18 and selectnum < 26:
            for num_candidate2 in nums:
                if int(num_candidate2.text) == selectnum + 1:
                    num_candidate2.click()
                    while True:
                        try:
                            # driver.find_element(By.XPATH,"//a[@class=\"btn-right on\"][@id=\"tnb_step_btn_right\"]").click()

                            button = WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable((By.XPATH, "//a[@class=\"btn-right on\"]"))
                            )
                            driver.execute_script("arguments[0].click();", button)

                            while True:
                                try:
                                    print(111)
                                    da = Alert(driver)
                                    print(222)
                                    da.accept()
                                    print(333)
                                    driver.find_element(By.XPATH, "//a[@class=\"btn-refresh\"]").click()
                                    print(444)
                                    txt = "간바레차!!!"
                                    print(txt)
                                    # th = threading.Thread(target=sendemail, args=(txt, 1,))
                                    # th.start()
                                    return "reset"
                                except:
                                    try:
                                        send_telegram_message("자리남")
                                        driver.find_element(By.XPATH, "//div[@id=\"lastPayMethod\"]")
                                        txt = "용아맥 오픈 자리 획득!!!!"
                                        print(txt)
                                        time.sleep(100000)
                                        # th = threading.Thread(target=sendemail, args=(txt, 4,))
                                        # th.start()
                                        return True
                                    except:
                                        print("wait22")
                        except:
                            print("wait")
                            # if 만약 자리찬거뜨면
                            # if 팝업==True:
                            # return False
                    return True

    return False


def delayclick(element, comment):
    for i in range(1, 20):
        try:
            element.click()
            print(comment + " 선택")
            break
        except:
            print(str(i) + comment + " 선택 실패")


def do(name, i, j, driver_list):
    if BGmode == True:
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        user_agent = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
        options.add_argument('user-agent=' + user_agent)
        drivertemp = webdriver.Chrome('/Users/kimk1029/chromedriver', options=options)
    if BGmode == False:
        drivertemp = webdriver.Chrome('/Users/kimk1029/chromedriver')

    select_day_time(drivertemp, name, i, j)
    # driver_list.append(drivertemp)

    seatselect(drivertemp)


def sendemail(txt, cycle):
    for i in range(cycle):
        s = smtplib.SMTP('smtp.gmail.com', 587)

        # TLS 보안 시작
        s.starttls()

        senderAddr = ""
        recipientAddr = ""

        # 로그인 인증
        s.login(senderAddr, "")
        text = txt

        msg = MIMEText(text)
        msg['Subject'] = text
        msg['From'] = senderAddr
        msg['To'] = recipientAddr

        s.sendmail(senderAddr, [recipientAddr], msg.as_string())
        s.quit()


# def imax_check_day(driver,day):
#     while True:
#         url = "http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode=0013&screencodes=&screenratingcode=02&regioncode=07"
#         url=url+"&date="+str(day)
#         driver.get(url)
#         selected_day=driver.find_element(By.XPATH,"//a[@title=\"현재 선택\"]")
#         if int(day)%100==int(selected_day.text.split("\n")[2]):
#             return True, url


def imax_check_day(driver, day):
    while True:
        url = "http://www.cgv.co.kr/theaters/special/show-times.aspx?regioncode=07&theatercode=0013"
        driver.get(url)
        iframe = driver.find_element(By.XPATH, "//iframe[@title=\"IMAX 용산아이파크몰 상영시간표\"]")
        driver.switch_to.frame(iframe)

        try:
            btn_prev = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@class=\"sect-schedule\"]/div/button[@class=\"btn-prev\"]")))
        except:
            print("아직 로딩 안됨")
            time.sleep(15)
            continue
        btn_next = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@class=\"sect-schedule\"]/div/button[@class=\"btn-next\"]")))
        driver.execute_script("arguments[0].click();", btn_next)
        driver.execute_script("arguments[0].click();", btn_prev)
        firstwrap = "//div[@class=\"sect-schedule\"]/div/div[@class=\"item-wrap on\"]/ul/li"
        wlist = driver.find_elements(By.XPATH, firstwrap)
        findflag = False
        for date in wlist:
            if int(day) % 100 == int(date.text.split("\n")[2]):
                date.click()
                findflag = True
                return True
                break
        if findflag == False:
            driver.execute_script("arguments[0].click();", btn_next)
            nextwrap = "//div[@class=\"sect-schedule\"]/div/div[@class=\"item-wrap on\"]/ul/li"
            wlist = driver.find_elements(By.XPATH, nextwrap)
            for date in wlist:
                if int(day) % 100 == int(date.text.split("\n")[2]):
                    date.click()
                    findflag = True
                    return True
                    break
        print("찾는영화 아직 없음")
        time.sleep(5)

        #
        # selected_day=driver.find_element(By.XPATH,"//a[@title=\"현재 선택\"]")
        # if int(day)%100==int(selected_day.text.split("\n")[2]):
        #     return True, url


def imax_check_timeopen(driver):
    already_flag = True
    while True:
        movielist = driver.find_elements(By.XPATH, "//div[@class=\"sect-showtimes\"]/ul/li")
        try:
            if "상영하는 영화가 없습니다." in movielist[0].text:
                already_flag = False
                driver.refresh()
            else:
                driver.find_element(By.XPATH, "//div[@class=\"info-timetable\"]")
                if already_flag == False:
                    readytxt = "영화 열렸음!!!!!!!!"
                    # t = threading.Thread(target=sendemail, args=(readytxt, 1,))
                    # t.start()
                return True
        except:
            print("상영하는 영화가 없습니다.의 버그??")


def imax_times_run(driver):
    info_list = []
    movielist = driver.find_elements(By.XPATH, "//div[@class=\"sect-showtimes\"]/ul/li")

    for i in movielist:
        if MOVIE_NAME in i.text.split("\n")[1]:
            print("find")
            links = i.find_elements(By.XPATH, "div/div/div[@class=\"info-timetable\"]/ul/li/a")
            for link in links:
                m_time = int(link.get_attribute("data-playstarttime"))
                if int(FIRST_T) <= m_time and m_time <= int(LAST_T):
                    linkurl = link.get_attribute("href")
                    ymd = int(link.get_attribute("data-playymd"))
                    info_list.append([linkurl, ymd, m_time])
                    print(ymd, m_time)

                    if BGmode == True:
                        options = webdriver.ChromeOptions()
                        options.add_argument("headless")
                        user_agent = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
                        options.add_argument('user-agent=' + user_agent)
                        # background
                        drivertemp = webdriver.Chrome('/Users/kimk1029/chromedriver', options=options)
                    if BGmode == False:
                        # not background
                        drivertemp = webdriver.Chrome('/Users/kimk1029/chromedriver')

                    # do_extrawindow(drivertemp, linkurl)
                    #
                    print(drivertemp)
                    print(linkurl)
                    t = threading.Thread(target=do_extrawindow, args=(drivertemp, linkurl,))
                    t.start()
    return info_list



def do_extrawindow(drivertemp, url):
    #각 창마다 하는일 에러나면 여기 while이나 try문 다시
    stack = 0
    while True:

        try:
            drivertemp.get(url)
            try:
                drivertemp.find_element_by_xpath("//a[@title=\"로그아웃\"]")
            except:
                print("다시로그인")
                loginBG(drivertemp)
                drivertemp.get(url)

            iframe = drivertemp.find_element_by_xpath("//iframe[@title=\"CGV 빠른예매\"]")
            drivertemp.switch_to.frame(iframe)
            # select = driver.find_element_by_xpath("//a[@class=\"btn-right on\"]")
            # select.click()
            # time.sleep(1)
            button = btn_right_on(drivertemp)
            drivertemp.execute_script("arguments[0].click();", button)
            stack=0

            print("날짜시간 고름")
            seatselect(drivertemp)
        except:
            print("{Alert text : 좌석 선택 시간이 초과되어 스케줄로 이동됩니다.}")
            stack+=1
            if stack>20:
                # options = webdriver.ChromeOptions()
                # options.add_argument("headless")
                # user_agent = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
                # options.add_argument('user-agent=' + user_agent)
                # background
                drivertemp = webdriver.Chrome('D:/chromedriver.exe')
                loginBG(drivertemp)

def btn_right_on(driver):
    while True:
        try:
            driver.find_element(By.XPATH, "//a[@class=\"btn-right\"]")
        except:
            try:
                button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@class=\"btn-right on\"]"))
                )

                return button
                break
            except:
                print("로딩 버튼")


def do_parallel(day):
    # driver = webdriver.Chrome('D:/chromedriver.exe')
    if BGmode == True:
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        user_agent = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
        options.add_argument('user-agent=' + user_agent)
        # background
        driver = webdriver.Chrome('/Users/kimk1029/chromedriver', options=options)
    if BGmode == False:
        # not background
        driver = webdriver.Chrome('/Users/kimk1029/chromedriver')
    imax_check_day(driver, day)
    imax_check_timeopen(driver)
    imax_times_run(driver)


def interceptor(request):
    del request.headers['Referer']  # Delete the header first
    request.headers[
        'Referer'] = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?theatercode=0074&screencodes=&screenratingcode=02&regioncode=07'


def find_movie_name(driver, MOVIE_NAME):
    # url = "http://www.cgv.co.kr/ticket/"
    # driver.get(url)
    # iframe = driver.find_element(By.XPATH,"//iframe[@title=\"CGV 빠른예매\"]")
    # driver.switch_to.frame(iframe)
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@class=\"movie-list nano has-scrollbar has-scrollbar-y\"]/ul/li")))
        mlist = driver.find_elements(By.XPATH, "//div[@class=\"movie-list nano has-scrollbar has-scrollbar-y\"]/ul/li")

        findmovie = False
        for mov in mlist:
            if MOVIE_NAME in mov.text:
                if "[" not in mov.text:
                    findmovie = True
                    mov1 = mov.find_element(By.XPATH, "a")
                    driver.execute_script("arguments[0].click();", mov1)
                    thatmov = mov
                    id = thatmov.get_attribute("movie_cd_group")
                    global MOVIE_CD_GROUP
                    MOVIE_CD_GROUP = "MOVIE_CD_GROUP=" + str(id)
                    loadingpass(driver)

        if findmovie == False:
            print("선택한 영화는 아직 개봉안함")
            return False

        imax = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@data-type=\"IMAX\"]")))
        driver.execute_script("arguments[0].click();", imax)

        while True:
            if "selected" in thatmov.get_attribute("class"):
                break
        loadingpass(driver)
        return True
    except:
        print("선택한 영화에 원하시는 상영스케줄이 없습니다.")
        return False


def find_yongsan_theather(driver):
    while True:
        try:
            gangnam = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//li[@theater_cd=\"0056\"]")))
            if "dimmed" in gangnam.get_attribute("class"):
                print("영화관세팅")
                break
        except:
            print()

    try:
        yongsan = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//li[@theater_cd=\"0013\"]")))
        if "dimmed" in yongsan.get_attribute("class"):
            print("용아맥 아직 없음")
            return False

        while True:
            yongsan_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//li[@theater_cd=\"0013\"]/a")))
            driver.execute_script("arguments[0].click();", yongsan_button)

            selected = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//li[@theater_cd=\"0013\"]")))

            if "selected" in selected.get_attribute("class"):
                break
        loadingpass(driver)
        return True
    except:
        print("용아맥 없음")
        return False


def find_day(driver, day):
    try:
        day_obj = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//li[@date=\"" + str(day) + "\"]")))

        if "dimmed" in day_obj.get_attribute("class"):
            print("날짜 아직임")
            return False, False

        while True:
            # send_telegram_message("날짜 풀림!!!!!")
            day_obj_button = day_obj.find_element(By.XPATH, "a")
            driver.execute_script("arguments[0].click();", day_obj_button)

            selected = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//li[@date=\"" + str(day) + "\"]")))

            if "selected" in selected.get_attribute("class"):
                break
        loadingpass(driver)
        return True, day_obj_button
    except:
        print("날짜 에러")
        return False, False


def reset_reservation(driver):
    try:
        reset = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class=\"button button-reservation-restart\"]")))
        loading = driver.find_element(By.XPATH, "//div[@id=\"ticket_loading\"]")
        driver.execute_script("arguments[0].click();", reset)
        loadingpass_for_reset(driver, loading)
    except:
        print("리셋 에러")


def loadingpass_for_reset(driver, loading):
    for i in range(40):
        if "block" in loading.get_attribute("style"):
            break

    while True:
        if "none" in loading.get_attribute("style"):
            break


def loadingpass(driver):
    loading = driver.find_element(By.XPATH, "//div[@id=\"ticket_loading\"]")
    for i in range(40):
        if "block" in loading.get_attribute("style"):
            break

    for i in range(40):
        if "none" in loading.get_attribute("style"):
            break


def find_timelist_ready(driver):
    find_timelist = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[@class=\"section section-time\"]/div/div[@class=\"time-list nano has-scrollbar\"]")))
    print(find_timelist.text)
    if "준비" in find_timelist.text or ":" in find_timelist.text:
        return True
    else:
        return False
    # timelist=find_timelist.find_elements(By.XPATH,"div/div[@class=\"theater\"]/ul/li")
    # for time in timelist:
    #     print(time.get_attribute("play_start_tm"))


def first_reservation(driver, first_day):
    url = "http://www.cgv.co.kr/ticket/"
    driver.get(url)
    iframe = driver.find_element(By.XPATH, "//iframe[@title=\"CGV 빠른예매\"]")
    driver.switch_to.frame(iframe)
    # loading = WebDriverWait(driver, 5).until(
    #     EC.element_to_be_clickable((By.XPATH, "//div[@id=\"ticket_loading\"]")))
    # loading=driver.find_element(By.XPATH,"//div[@id=\"ticket_loading\"]")
    done = False
    while not done:
        pass_bool_2 = False
        pass_bool = find_movie_name(driver, MOVIE_NAME)
        print("pass_bool", pass_bool)
        now = datetime.now()
        print("문자열 변환 : ", now.strftime('%Y-%m-%d %H:%M:%S'))
        if pass_bool:
            pass_bool_2 = find_yongsan_theather(driver)
        print("pass_bool_2", pass_bool_2)

        if pass_bool_2:
            done, day_obj_button = find_day(driver, first_day)
        print("done", done)
        if not done:
            reset_reservation(driver)
            time.sleep(5)

    print("예매 준비 고고")
    # send_telegram_message("예매준비완료")
    return day_obj_button


def full_ready(driver, day_obj_button):
    while True:
        try:
            driver.execute_script("arguments[0].click();", day_obj_button)
            find_timelist = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                     "//div[@class=\"section section-time\"]/div/div[@class=\"time-list nano has-scrollbar\"]")))
            if "석" in find_timelist.text:
                print(":::::::::::::모든 준비완료 좌석 오픈:::::::::::")
                return True
        except:
            print("다시다시")

def get_time_by_day(driver,day):
    if int(day) != int(START_DAY):
        find_day(driver, day)
    find_timelist = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.XPATH,
             "//div[@class=\"section section-time\"]/div/div[@class=\"time-list nano has-scrollbar\"]")))
    rawtext=find_timelist.text
    t = threading.Thread(target=extract_time_from_text, args=(rawtext,day ))
    t.start()


def extract_time_from_text(rawtext,ymd):
    raw_list=rawtext.split('\n')
    condition_on=0
    for candidate in raw_list:
        if ":" in candidate:
            candidate_time=candidate.replace(":","")
            print("candidate",candidate)
            candidate_time=int(candidate_time)
            # if int(FIRST_T) <= candidate_time and candidate_time <= int(LAST_T):
            #범위안에 없을경우 대비 범위 뒤에꺼도 차근차근 넣기
            if int(FIRST_T) <= candidate_time:
                condition_on=condition_on+1
                # linkurl = link.get_attribute("href")
                linkurl=make_url(ymd,candidate_time)
                # ymd = int(link.get_attribute("data-playymd"))
                # info_list.append([linkurl, ymd, candidate])
                print("find", ymd, candidate_time)
                try:
                    drivertemp = driverlist.pop()
                except:
                    break
                # do_extrawindow(drivertemp, linkurl)
                #
                t = threading.Thread(target=do_extrawindow, args=(drivertemp, linkurl,))
                t.start()
                gc.collect()

    if condition_on==0:
        print("time condition_on fail")
        for candidate in raw_list:
            if ":" in candidate:
                candidate_time = candidate.replace(":", "")
                print("candidate", candidate)
                candidate_time = int(candidate_time)
                if int(FIRST_T) <= candidate_time:
                    condition_on = condition_on + 1
                    # linkurl = link.get_attribute("href")
                    linkurl = make_url(ymd, candidate_time)
                    # ymd = int(link.get_attribute("data-playymd"))
                    # info_list.append([linkurl, ymd, candidate])
                    print(ymd, candidate_time)
                    drivertemp = driverlist.pop()
                    # do_extrawindow(drivertemp, linkurl)
                    #
                    t = threading.Thread(target=do_extrawindow, args=(drivertemp, linkurl,))
                    t.start()
                    gc.collect()
                    break

def make_url(ymd, st_tm):
    baseurl = "http://www.cgv.co.kr/ticket/?AREA_CD=13&SCREEN_CD=018&THEATER_CD=0013"
    # MOVIE_CD_GROUP="MOVIE_CD_GROUP"
    # MOVIE_CD=""
    PLAY_YMD = "PLAY_YMD=" + str(ymd)
    PLAY_START_TM = "PLAY_START_TM=" + str(st_tm)
    fullurl = baseurl + "&" + MOVIE_CD_GROUP + "&" + PLAY_YMD + "&" + PLAY_START_TM
    return fullurl

if __name__ == "__main__":
    arg(sys.argv)
    cgv_ready_test = 0

    # if INPUTmode == True:
    #     MYPHONE = input("내통장결제 핸드폰번호 입력:")
    #     PAY_PW = input("내통장결제 비밀번호 입력:")
    # else:
    #     MYPHONE = "01012341234"
    #     PAY_PW = "123456"

    MYPHONE = '01032440103'
    PAY_PW = '135798'

    # BGmode= input("내통장결제 비밀번호 입력:")

    # options = webdriver.ChromeOptions()
    # # options.add_argument("headless")
    # user_agent ='Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    # options.add_argument('user-agent=' + user_agent)
    # referer="http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?theatercode=0074&screencodes=&screenratingcode=02&regioncode=07"
    # options.add_argument('referer=' + referer)
    # #
    # # # background
    # webdriver.Chrome('D:/chromedriver.exe', options=options)
    # driver = webdriver.Chrome('D:/chromedriver.exe', options=options)
    # not background
    # driver = webdriver.Chrome('D:/chromedriver.exe')
    # driver._client.set_header_overrides(
    #     headers={
    #         "User-Agent": "Mozilla/5.0 (test)",
    #         "Referer": "http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?theatercode=0074&screencodes=&screenratingcode=02&regioncode=07",
    #     })
    total_day = int(END_DAY) - int(START_DAY) + 1
    total_time = int(LAST_T) / 100 - int(FIRST_T) / 100

    print(int(END_DAY))
    print(total_day)
    print(total_time)
    divide_time = round(total_time / 2.5)
    print(divide_time)
    tn = total_day * divide_time

    for i in range(tn):
        driver = webdriver.Chrome('/Users/kimk1029/chromedriver')
        loginBG(driver)
        driverlist.append(driver)

    maindriver = webdriver.Chrome('/Users/kimk1029/chromedriver')
    already_flag = True

    day_obj_button = first_reservation(maindriver, START_DAY)
    while not find_timelist_ready(maindriver):
        day_obj_button = first_reservation(maindriver, START_DAY)
    # 준비중이라는 상태

    full_ready(maindriver, day_obj_button)

    for i in range(total_day):
        day=int(START_DAY)+i
        get_time_by_day(maindriver,day)
        print(i,"번 날짜 오픈")

    ending = input("끝?? :")
    while True:
        print("refresh lists")
        time.sleep(100000)


