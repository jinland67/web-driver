import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


class WebDriverError(Exception):
    # -----------------------------------------------
    # 생성할 때 value 값을 입력 받은다.
    # -----------------------------------------------
    def __init__(self, value):
        self.value = value

    # -----------------------------------------------
    # 생성할 때 받은 value 값을 확인 한다.
    # -----------------------------------------------
    def __str__(self):
        return self.value


# ================================================================
#   [Dependancy]
#       - pip install selenium <version 4.0.0 이상>
#
#   [Useage]
#       broswer = WebDriver(remote_url='http://localhost:4444')
#       driver = broswer.connect()
#               :
#       driver.quit() 또는 browser.disconnect()
# 	[주의]
#       반드시 사용 후 종료를 하지 않으면 메모리의 누수가 발생한다.
#       if broswer is not None:
#           broswer.quit()
# ================================================================
class WebDriver:
    def __init__(self,connect_type, **kwargs):
        try:
            self.__type = connect_type
            self.__driver = None
            self.__version = kwargs.get('version', '89.0.4389.23')
            self.__visible = kwargs.get('visible', False)
            self.__remote_url = kwargs.get('remote_url', None)
            self.__driver_path = kwargs.get('driver_path', None)
            self.__page_load_time_out = kwargs.get('page_load_time_out', 10)
            self.__implicitly_wait = kwargs.get('implicitly_wait', 1)
            self.__explicitly_wait = kwargs.get('explicitly_wait', 10)
            self.__maximize_window = kwargs.get('maximize_window', True)
            self.__user_agent = f"Mozilla/5.0 (Windows NT 10.0; Win64;x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{self.__version} Safari/537.36"
            # 접속방식 체크
            if self.__type == 'grid-hub' and self.__remote_url is None:
                msg = 'If the connection method is grid-hub, the grid-hub address is required.'
                raise WebDriverError(msg)
            if self.__type == 'chromedriver' and self.__driver_path is None:
                msg = 'If the connection method is chrome, the path to chromedriver is required.'
                raise WebDriverError(msg)
            if self.__type == 'geckodriver' and self.__driver_path is None:
                msg = 'If the connection method is firefox, the path to geckodriver is required.'
                raise WebDriverError(msg)
            # chrome 옵션 설정
            self.__options = webdriver.ChromeOptions()
            if not self.__visible and self.__driver_path is not None:
                # Run in headless mode, i.e., without a UI or display server dependencies.
                self.__options.add_argument('--headless')
                # Disables sandbox mode for all processes
                self.__options.add_argument("--no-sandbox")
                # Disables GPU hardware acceleration.
                self.__options.add_argument("--disable-gpu")
            self.__options.add_argument(f'user-agent={self.__user_agent}')
            # The /dev/shm partition is too small in certain VM environments,
            # causing Chrome to fail or crash (see http://crbug.com/715363).
            # Use this flag to work-around this issue (a temporary directory will always be used to create
            # anonymous shared memory files).
            self.__options.add_argument("--disable-dev-shm-usage")
            # set windows size to the specified values
            self.__options.add_argument('--window-size=1920,1080')
            # Disable crash reporter for headless. It is enabled by default in official builds.
            self.__options.add_argument('--disable-crash-reporter')
            # Disables the in-process stack traces.
            self.__options.add_argument('--disable-in-process-stack-traces')
            # Quite clear what it does
            self.__options.add_argument('--disable-extensions')
            # logging should be already disabled in production builds, but better to double disable.
            self.__options.add_argument('--disable-logging')
            # Sets the minimum log level. Valid values are from 0 to 3:
            # INFO = 0, WARNING = 1, LOG_ERROR = 2, LOG_FATAL = 3
            self.__options.add_argument('--log-level=3')
        except Exception as e:
            msg = 'WebDriver exception occured in __init__(). Message: %s' % str(e)
            raise WebDriverError(msg)

    #------------------------------------------------
    # __wait_element()
    # -----------------------------------------------
    def __wait_element(self, **kwargs):
        try:
            id_name = kwargs.get('id', None)
            tag_name = kwargs.get('tag', None)
            class_name = kwargs.get('class', None)
            xpath_name = kwargs.get('xpath', None)
            wait_time = kwargs.get('wait_time', 0.1)
            if id_name is not None:
                WebDriverWait(self.__driver, self.__explicitly_wait).until(
                              EC.presence_of_element_located((By.ID, id_name)))
            elif tag_name is not None:
                WebDriverWait(self.__driver, self.__explicitly_wait).until(
                              EC.presence_of_element_located((By.TAG_NAME, tag_name)))
            elif class_name is not None:
                WebDriverWait(self.__driver, self.__explicitly_wait).until(
                              EC.presence_of_element_located((By.CLASS_NAME, class_name)))
            elif xpath_name is not None:
                WebDriverWait(self.__driver, self.__explicitly_wait).until(
                              EC.presence_of_element_located((By.XPATH, xpath_name)))
            else:
                time.sleep(wait_time)
        except Exception as e:
            msg = 'WebDriver exception occured in __wait_element(). Message: %s' % str(e)
            raise WebDriverError(msg)

    #------------------------------------------------
    # set_config(self)
    # [설명]
    #   WebDriver의 환경설정
    # -----------------------------------------------
    def set_config(self, connect_type, **kwargs):
        try:
            self.__type = connect_type
            self.__driver = None
            self.__version = kwargs.get('version', '89.0.4389.23')
            self.__visible = kwargs.get('visible', False)
            self.__page_load_time_out = kwargs.get('page_load_time_out', 10)
            self.__remote_url = kwargs.get('remote_url', None)
            self.__driver_path = kwargs.get('driver_path', None)
            self.__implicitly_wait = kwargs.get('implicitly_wait', 1)
            self.__explicitly_wait = kwargs.get('explicitly_wait', 10)
            self.__maximize_window = kwargs.get('maximize_window', True)
            self.__user_agent = f"Mozilla/5.0 (Windows NT 10.0; Win64;x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{self.__version} Safari/537.36"
            # 접속방식 체크
            if self.__type == 'grid-hub' and self.__remote_url is None:
                msg = 'If the connection method is grid-hub, the grid-hub address is required.'
                raise WebDriverError(msg)
            if self.__type == 'chromedriver' and self.__driver_path is None:
                msg = 'If the connection method is chrome, the path to chromedriver is required.'
                raise WebDriverError(msg)
            if self.__type == 'geckodriver' and self.__driver_path is None:
                msg = 'If the connection method is firefox, the path to geckodriver is required.'
                raise WebDriverError(msg)
            # chrome 옵션 설정
            self.__options = webdriver.ChromeOptions()
            if not self.__visible and self.__driver_path is not None:
                # Run in headless mode, i.e., without a UI or display server dependencies.
                self.__options.add_argument('--headless')
                # Disables sandbox mode for all processes
                self.__options.add_argument("--no-sandbox")
                # Disables GPU hardware acceleration.
                self.__options.add_argument("--disable-gpu")
            self.__options.add_argument(f'user-agent={self.__user_agent}')
            # The /dev/shm partition is too small in certain VM environments,
            # causing Chrome to fail or crash (see http://crbug.com/715363).
            # Use this flag to work-around this issue (a temporary directory will always be used to create
            # anonymous shared memory files).
            self.__options.add_argument("--disable-dev-shm-usage")
            # set windows size to the specified values
            self.__options.add_argument('--window-size=1920,1080')
            # Disable crash reporter for headless. It is enabled by default in official builds.
            self.__options.add_argument('--disable-crash-reporter')
            # Disables the in-process stack traces.
            self.__options.add_argument('--disable-in-process-stack-traces')
            # Quite clear what it does
            self.__options.add_argument('--disable-extensions')
            # logging should be already disabled in production builds, but better to double disable.
            self.__options.add_argument('--disable-logging')
            # Sets the minimum log level. Valid values are from 0 to 3:
            # INFO = 0, WARNING = 1, LOG_ERROR = 2, LOG_FATAL = 3
            self.__options.add_argument('--log-level=3')
            # set chromedriver path or remote_url
            if self.__driver_path is not None and self.__remote_url is not None:
                msg = 'There must be only one "driver_path" or "remote_url" value among the transfer arguments.'
                raise WebDriverError(msg)
        except Exception as e:
            msg = 'WebDriver exception occured in set_config(). Message: %s' % str(e)
            raise WebDriverError(msg)

    #------------------------------------------------
    # connect(self)
    # [설명]
    #   예) connect()
    # [반환값]
    #   WebDriver를 리턴
    # -----------------------------------------------
    def connect(self):
        try:
            if self.__type == 'grid-hub':
                # grid 접속을 위한 web driver remote 설정
                self.__driver = webdriver.Remote(
                        command_executor=self.__remote_url,
                        # selenium version 4에서는 권장하지 않는다.
                        # desired_capabilities=DesiredCapabilities.CHROME,
                        options=self.__options)
            elif self.__type == 'chromedriver':
                self.__driver = webdriver.Chrome(
                         executable_path=self.__driver_path,
                        # selenium version 4에서는 권장하지 않는다.
                        # desired_capabilities=DesiredCapabilities.CHROME,
                         options=self.__options)
            elif self.__type == 'geckodriver':
                self.__driver = webdriver.Firefox(
                         executable_path=self.__driver_path,
                        # selenium version 4에서는 권장하지 않는다.
                        # desired_capabilities=DesiredCapabilities.CHROME,
                         options=self.__options)
            else:
                msg = 'A value for which the connection method is not defined. Please check again.'
                raise WebDriverError(msg)
            if self.__driver is not None:
                # page load time out 설정
                self.__driver.set_page_load_timeout(self.__page_load_time_out)
                # 브라우저 윈도우 사이즈를 설정
                if self.__maximize_window:
                    self.__driver.maximize_window()
                # Implicitly Wait
                self.__driver.implicitly_wait(self.__implicitly_wait)
                # return web driver
                return self.__driver
            else:
                return None
        except Exception as e:
            self.__driver = None
            msg = 'WebDriver exception occured in connect(). Message: %s' % str(e)
            raise WebDriverError(msg)

    #------------------------------------------------
    # disconnect(self)
    # [설명]
    #   WebDriver를 리턴
    # -----------------------------------------------
    def disconnect(self):
        try:
            if self.__driver is not None:
                self.__driver.quit()
                self.__driver = None
        except Exception as e:
            msg = 'WebDriver exception occured in reconnect(). Message: %s' % str(e)
            raise WebDriverError(msg)

    #------------------------------------------------
    # get()
    # [설명]
    # 	주어진 url로 페이지를 로딩.
    #   만일, id, tag, css, class, xpath의 option 값이 설정되면
    # 	해당 값이 loading 될 때까지 최소 __explicitly_wait 만큼 기다린다.
    #	별도로 페이지 로딩에 필요한 time.sleep()이 필요 없다.
    # -----------------------------------------------
    def get(self, url, **kwargs):
        try:
            # url page loading
            self.__driver.get(url)
            self.__wait_element(**kwargs)
        except Exception as e:
            msg = 'WebDriver exception occured in get(). Message: %s' % str(e)
            raise WebDriverError(msg)

    #------------------------------------------------
    # quit()
    # [설명]
    # 	드라이버를 종료할 때 사용한다.
    # 	close() method에 비해 memory에서 완전히 제거된다.
    # -----------------------------------------------
    def quit(self):
        try:
            if self.__driver is not None:
                self.__driver.quit()
                self.__driver = None
        except Exception as e:
            msg = 'WebDriver exception occured in quit(). Message: %s' % str(e)
            raise WebDriverError(msg)

    #------------------------------------------------
    # get_driver()
    # [설명]
    #   WebDriver를 리턴
    # -----------------------------------------------
    def get_driver(self):
        try:
            return self.__driver
        except Exception as e:
            msg = 'WebDriver exception occured in get_driver(). Message: %s' % str(e)
            raise WebDriverError(msg)

    #------------------------------------------------
    # page_source()
    # [설명]
    # 	현재 로딩되어 있는 페이지의 source를 리턴한다.
    #	보통의 경우 beautifulsoup과 연동해서 사용한다.
    # 	soup = BeautifulSoup(self.__driver.page_source(), 'lxml')
    # -----------------------------------------------
    def page_source(self):
        try:
            return self.__driver.page_source
        except Exception as e:
            msg = 'WebDriver exception occured in page_source(). Message: %s' % str(e)
            raise WebDriverError(msg)

    #------------------------------------------------
    # click(element, **kwargs)
    # [설명]
    # 	주어진 element에 click 이벤트를 발생 시킨다.
    #   만일, 그 결과가 display 될 때 까지 기다리고자 한다면
    #   id, class,... xpath등의 값을 추가로 설정한다.
    # -----------------------------------------------
    def click(self, element, **kwargs):
        try:
            ActionChains(self.__driver).click(element).perform()
            self.__wait_element(**kwargs)
        except Exception as e:
            msg = 'WebDriver exception occured in click(). Message: %s' % str(e)
            raise WebDriverError(msg)

    #------------------------------------------------
    # input(element, value)
    # [설명]
    # 	주어진 element에 값을 입력하기 위해 사용한다.
    # -----------------------------------------------
    def input(self, element, value):
        try:
            element.clear()
            element.send_keys(value)
        except Exception as e:
            msg = 'WebDriver exception occured in input(). Message: %s' % str(e)
            raise WebDriverError(msg)

    #------------------------------------------------
    # enter(element, value, **kwargs)
    # [설명]
    # 	주어진 element에 value 값을 입력하고 enter event를 발생하기 위해 사용한다.
    #	만일 enter event에 의해 변화된 페이지가 완료될 때 까지 기다리고자 한다면,
    #   id, class, xpath 등의 값을 추가로 설정한다.
    # -----------------------------------------------
    def enter(self, element, value, **kwargs):
        try:
            wait_time = kwargs.get('wait_time', 0.1)
            element.clear()
            element.send_keys(value)
            time.sleep(wait_time)
            element.send_keys(Keys.RETURN)
            self.__wait_element(**kwargs)
        except Exception as e:
            msg = 'WebDriver exception occured in enter(). Message: %s' % str(e)
            raise WebDriverError(msg)

    #------------------------------------------------
    # scroll(**kwargs)
    # [설명]
    # 	페이지의 특정 위치까지 스크롤하는 기능을 함.
    #	height 값을 이용하여 원하는 위치까지 스크롤
    #   wait_time은 스크롤 후 대기시간을 설정
    # -----------------------------------------------
    def scroll(self, **kwargs):
        try:
            height = kwargs.get('height', 1080)
            wait_time = kwargs.get('wait_time', 0.5)
            self.__driver.execute_script('window.scrollTo(0, %s);' % height)
            time.sleep(wait_time)
        except Exception as e:
            msg = 'WebDriver exception occured in scroll(). Message: %s' % str(e)
            raise WebDriverError(msg)

    #------------------------------------------------
    # page_down()
    # [설명]
    # 	PAGE_DOWN event를 발생시킨다.
    #   count: page_down event 발생회수
    #   wait_time: event 발생 후 대기시간 설정
    # -----------------------------------------------
    def page_down(self, **kwargs):
        try:
            count = kwargs.get('count', 6)
            wait_time = kwargs.get('wait_time', 0.5)
            element = WebDriverWait(self.__driver, self.__explicitly_wait).until(
                                    EC.presence_of_element_located((By.TAG_NAME, 'body')))
            for i in range(count):
                element.send_keys(Keys.PAGE_DOWN)
                time.sleep(wait_time)
        except Exception as e:
            msg = 'WebDriver exception occured in page_down(). Message: %s' % str(e)
            raise WebDriverError(msg)

    #------------------------------------------------
    # page_end()
    # [설명]
    # 	PAGE_DOWN event를 통해 페이지의 끝까지 이동시킬 때 사용
    # -----------------------------------------------
    def page_end(self, **kwargs):
        try:
            count = kwargs.get('count', 3)
            wait_time = kwargs.get('wait_time', 0.5)
            # 크롤링을 위해 화면 맨 아래까지 스크롤 내리기
            while True:
                # 현재 화면의 길이를 리턴 받아 last_height에 넣음
                last_height = self.__driver.execute_script('return document.documentElement.scrollHeight')
                for i in range(count):
                    # body 본문에 END키를 입력(스크롤내림)
                    element = WebDriverWait(self.__driver, self.__explicitly_wait).until(
                                EC.presence_of_element_located((By.TAG_NAME, 'body')))
                    element.send_keys(Keys.END)
                    time.sleep(wait_time)
                new_height = self.__driver.execute_script('return document.documentElement.scrollHeight')
                if new_height == last_height:
                    break
        except Exception as e:
            msg = 'WebDriver exception occured in end(). Message: %s' % str(e)
            raise WebDriverError(msg)

    #------------------------------------------------
    # back()
    # [설명]
    # 	이전 url page로 돌아가기 위해 사용
    # -----------------------------------------------
    def back(self):
        try:
            self.__driver.back()
        except Exception as e:
            msg = 'WebDriver exception occured in back(). Message: %s' % str(e)
            raise WebDriverError(msg)

    #------------------------------------------------
    # alert()
    # [설명]
    # 	alert가 발생했을 때 사용, 무조건 확인 버튼을 클릭한 효과를 갖는다.
    # -----------------------------------------------
    def alert(self):
        try:
            WebDriverWait(self.__driver, self.__explicitly_wait).until(
                            EC.alert_is_present(), 'Timed out waiting for alerts to appear')
            obj = self.__driver.switch_to.alert
            obj.accept()
        except Exception as e:
            msg = 'WebDriver exception occured in alert(). Message: %s' % str(e)
            raise WebDriverError(msg)

    #------------------------------------------------
    # switch_to_frame()
    # [설명]
    # 	주어진 iframe으로 context를 변경 하고자 할 때 사용
    # -----------------------------------------------
    def switch_to_frame(self, element):
        try:
            self.__driver.switch_to.frame(element)
        except Exception as e:
            msg = 'WebDriver exception occured in switch_to_frame(). Message: %s' % str(e)
            raise WebDriverError(msg)

    #------------------------------------------------
    # switch_to_default_content()
    # [설명]
    # 	iframe에서 이전 context로 변경 하고자 할 때 사용
    # -----------------------------------------------
    def switch_to_default_content(self):
        try:
            self.__driver.switch_to.default_content()
        except Exception as e:
            msg = 'WebDriver exception occured in switch_to_default_content(). Message: %s' % str(e)
            raise WebDriverError(msg)