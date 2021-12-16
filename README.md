# web driver
selenium webdriver를 사용하기 위한 라이브러리

    * 의존성:
        - python 3.8.10 이상
        - selenium 4.0.0 이상
    * 브라우저:
        - selenium grid 사용 시
          . Chrome
          . Firefox
          . Edge
        - chromedriver 사용 시
          . Chrome
          . Firefox

------------------
### 사용법
```
    # install
        $  pip install git+https://github.com/jinland67/web-driver.git

    # chromedriver 사용 시
        from web_driver import WebDriver, WebDriverError
                :
                :
        browser = WebDriver(
            "connect_type",
            driver_path="chromedriver "./driver/chromedriver",
                :
        )
                :
        # chrome 접속
        driver = browser.connect()
        if driver is not None:
            browser.get(url)
                :
                :
        # chrome 접속 해제
        browser.disconnect() 또는 browser.quit()

    # selenium grid hub 사용 시
        from web_driver import WebDriver, WebDriverError
                :
                :
        browser = WebDriver(
            "connect_type",
            session_url="<ip-address or dns>:4444"
        )
                :

        # selenium grid hub 접속
        driver = browser.connect()
        if driver is not None:
            browser.get(url)
                :
                :
        # selenium grid 접속 해제
        browser.disconnect() 또는 browser.quit()

    # selenium web driver 요청
    driver = browser.get_driver()

    # page 요청
    browser.get(url)

    # page source 요청
    html = browser.page_source()

    [참고]
    driver = browser.get_driver()를 통해서 driver를 획득했을 경우 driver는 selenium의 webdriver의 모든 메소드를 사용할 수 있다.

    [주의]
    web driver 종료 시 반드시 browser.quit() 또는 browser.disconnect()를 해야한다. 만일 connect()를 통해 할당된 변수값 즉 driver.quit()으로 종료할 경우 cloass에서 종료에 대한 정보를 처리할 수 없어 오류를 발생한다.

```

------------------
### ARG 정의
```
    # connect_type
        - 형식: string
        - 설명: 접속방식을 grid-hub, chromedriver, geckodriver를 선택
    # remote_url
        - 형식: string
        - 설명: selenium grid 사용 시 grid hub의 주소를 표시한다. 예) WebDriver(remote_url='http://localhost:4444')
    # driver_path
        - 형식: string
        - 설명: chromedriver의 경로를 표시한다. 예) WebDriver(driver_path='./chromedriver')
    # version
        - 형식: string
        - 설명: chrome 버전을 입력한다. 예) 95.0
        - 참고: 버전 확인 방법은 chrome -> 옵션 -> 도움말 -> 크롬정보 또는 grid 사용 시 selenium grid Overview 참조
    # visible
        - 형식: Boolean
        - 설명: 브라우저를 화면에 보이게 실행할 것인가 선택. 기본값은 False
    # implicitly_wait
        - 형식: int
        - 설명: selenium driver가 명시적으로 기다리는 시간. 단위는 초, 기본값은 1
    # __explicitly_wait
        - 형식: int
        - 설명: selenium driver가 묵시적으로 기다리는 시간. 단위는 초, 기본값은 10
    # maximize_window
        - 형식: Boolean
        - 설명: 브라우저 윈도우를 최대 사이즈로 할 것인가 선택. 기본값은 False
```

------------------
### method 정의
```
    # set_config(**kwargs)
      드라이브 설정을 다시 하고자 할 때 사용. arg는 클라스 선언 시 ARG와 동일
    # connect()
      grid hub 또는 chrome에 접속하고자 할 때 사용. 리턴값은 selenium webdriver object
      [주의]
      반드시 return 값이 None인지를 체크해야 한다.
    # disconnect()
      grid hub 또는 chrome으로 부터 접속을 해제할 때 사용.
    # get(url)
      페이지를 요청할 때 사용
    # get_driver()
      selenium webdriver를 요청할 때 사용
    # page_source()
      현재 드라이버가 가지고 있는 페이지의 소스를 리턴. 형식: html
```

------------------
### chromedriver 사용 시 주의점
```
    # chrome의 버전을 확인한 후 chromedriver를 사용해야 한다.
        - chrome 버전 확인 방법
            $ google-chrome --version
    # chromedriver download
        - Linux일 경우
            $ wget https://chromedriver.storage.googleapis.com/"chromedriver version"/chromedriver_linux64.zip
            $ unzip chromedriver_linux64.zip
        - Windows 또는 Mac 사용 시
          다음 사이트(https://chromedriver.chromium.org/downloads)에서 OS에 맞는 드라이버를 다운로드 후 사용한다.
    # Mac os 사용 시
        - 해당 시스템의 CPU 칩셋의 종류(mac64 또는 mac64_m1)에 따라 chromedriver를 구분해서 다운로는 해야한다.
        - "개발자를 확인할 수 없기 때문에 'chromedriver'을(를) 열 수 없습니다." 오류 메시지 발생 시
            $ cd "chromedriver path"
            $ xattr -d com.apple.quarantine chromedriver
```