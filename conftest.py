import pytest
from selenium import webdriver #подключение библиотеки
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



@pytest.fixture(scope='class', autouse=True)
def initialize_tests():
    pytest.driver = webdriver.Chrome('chdrv.exe')
    pytest.driver.implicitly_wait(10)
    pytest.driver.get('https://petfriends.skillfactory.ru/login')
    assert pytest.driver.find_element(By.CSS_SELECTOR, 'div.text-center').text == "Социальная сеть для любителей животных"

    pytest.driver.find_element(By.ID, 'email').send_keys('*******')
    pytest.driver.find_element(By.ID, 'pass').send_keys('******')
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    pytest.driver.implicitly_wait(10)
    pytest.driver.get('https://petfriends.skillfactory.ru/my_pets')
    assert pytest.driver.find_element(By.CSS_SELECTOR, 'th').text == "Фото"

    yield
    pytest.driver.quit()




@pytest.fixture()
def calc_total():
    """Вычленяем кол-во животных из профиля пользователя total"""
    # Ожидаем загрузки нужного элемента
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.task2.fill div.\\.col-sm-4.left > h2")))
    # Берем текст из трех строк в профиле
    total_in_text = pytest.driver.find_element(By.CSS_SELECTOR, 'div.task3 div').text
    # Получаем пеервый и последний индекс вхождения числа в статистику
    start_index_total = total_in_text.find(':') + 2
    end_index_total = total_in_text.find('\n', start_index_total)
    # Получаем число из строки статистики
    pytest.total = int (total_in_text [ start_index_total : end_index_total ] )
    return pytest.total
