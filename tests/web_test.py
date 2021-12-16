import sys
from web_driver import WebDriver, WebDriverError


def main(connect_type):
    try:
        driver = None
        browser = None
        if connect_type == 'chromedriver':
            browser = WebDriver(connect_type, driver_path='./chromedriver')
        elif connect_type == 'grid-hub':
            browser = WebDriver(connect_type, remote_url='http://localhost:4444')
        for idx in range(10):
            try:
                driver = browser.connect()
                if driver is not None:
                    driver.get('http://www.naver.com')
                    print('idx %s web site title is %s' % (idx, driver.title))
                    browser.quit()
            except WebDriverError:
                continue
    except Exception as e:
        print(type(e), str(e))
        if browser is not None:
            browser.quit()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print('option: chromedriver or remote')