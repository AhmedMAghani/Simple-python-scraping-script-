from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def click_news_button(web_driver):
    news_page_button_x_path = """//*[@href="/news/1/"]"""
    news_button = web_driver.find_element_by_xpath(news_page_button_x_path)
    news_button.click()


def next_page(web_driver):
    next_page_button_x_path = """//div[@class='text-center pagination-navi text-gray-900 dark:text-gray-50']//descendant::a[2] """
    next_page_button = web_driver.find_element_by_xpath(next_page_button_x_path)
    temp_url = web_driver.current_url
    next_page_button.click()
    return web_driver.current_url == temp_url


def get_news(web_driver, news_obj_list):
    news_div_x_path = """pr-4"""
    title_x_path = """//h5[@class='mb-2 font-semibold leading-5']"""
    desc_x_path = """//p[@class='text-sm text-gray-500 pb-2']"""
    news_list = web_driver.find_elements_by_class_name(news_div_x_path)
    for news in news_list:
        title = news.find_element_by_xpath(title_x_path)
        desc = news.find_elements_by_xpath(desc_x_path)[1]
        date = news.find_elements_by_xpath(desc_x_path)[0]
        news_obj_list[title.text] = News(title.text, desc.text, date.text)
    return news_obj_list


def get_news_page(web_driver, delay):
    global main_news_div
    news_div_x_path = """//div[@class='px-4']"""
    try:
        main_news_div = WebDriverWait(web_driver, delay).until(EC.presence_of_element_located((By.XPATH,news_div_x_path)))
    except TimeoutException:
        print("loading took too much time")
    finally:
        return main_news_div


class News():
    def __init__(self, title, description, publish_date):
        self.title = title
        self.description = description
        self.publish_date = publish_date


if __name__ == "__main__":
    news_obj_list = {}
    with webdriver.Edge("resources/msedgedriver.exe") as edgeBrowser:
        edgeBrowser.get("https://rockylinux.org")
        click_news_button(edgeBrowser)
        main_news_div = get_news_page(edgeBrowser, delay=500)
        if main_news_div is not None:
            while True:
                news_obj_list = get_news(edgeBrowser, news_obj_list)
                end = next_page(edgeBrowser)
                if end:
                    break
    print(news_obj_list)
