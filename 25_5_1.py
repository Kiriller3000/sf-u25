import pytest, time
from selenium import webdriver #подключение библиотеки
driver = webdriver.Chrome('chdrv.exe')
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



@pytest.fixture(scope='class', autouse=True)
def initialize_tests():
    driver.implicitly_wait(10)
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')
    assert driver.find_element(By.CSS_SELECTOR, 'div.text-center').text == "Социальная сеть для любителей животных"

    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('dwfcw@ewwfwefdc.com')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('access12')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Переходим на страницу пользователя
    driver.implicitly_wait(10)
    driver.get('https://petfriends.skillfactory.ru/my_pets')
    # Проверяем, что мы оказались на странице пользователя
    assert driver.find_element(By.CSS_SELECTOR, 'th').text == "Фото"

    yield
    driver.quit()



@pytest.fixture()
def calc_total():
    """Вычленяем кол-во животных из профиля пользователя total"""
    # Ожидаем загрузки нужного элемента
    # try:
    # WebDriverWait(driver, 10).until(
    #     EC.text_to_be_present_in_element((By.CSS_SELECTOR, "div.\\.col-sm-4.left > h2"), 'Питомцев:'))
    # except:
    #     pass

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(By.CSS_SELECTOR, "div.\\.col-sm-4.left > h2"))

    # Берем текст из трех строк в профиле
    total_in_text = driver.find_element(By.CSS_SELECTOR, 'div.task3 div').text
    # Получаем первый и последний индекс вхождения числа в статистику
    start_index_total = total_in_text.find(':') + 2
    end_index_total = total_in_text.find('\n', start_index_total)
    # Получаем число из строки статистики
    pytest.total = int (total_in_text [ start_index_total : end_index_total ] )
    return pytest.total


class TestPetFriendsSelenium:

    def test_total_equal_all_pets(self, calc_total):
        """Проверяем, что кол-во total питомцев из профиля пользователя равно количеству из списка на странице"""
        total = pytest.total
        allpets = len (driver.find_elements(By.CSS_SELECTOR, '#all_my_pets tbody tr'))
        assert total == allpets


    def test_half_of_total_have_image(self, calc_total):
        """Проверяем, что у половины питомцев есть фото"""
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(By.CSS_SELECTOR, "#all_my_pets img"))
        except:
            driver.quit()
        # Получаем все элементы с тегом img
        images = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets img')
        # Считаем питомцев с фото
        quantity = 0
        for image in images:
            if image.get_attribute('src') != '':
                quantity +=1
        # У половины питомцев должно быть фото
        total = pytest.total
        htotal = int (total // 2)
        if total % 2 == 0:
            assert quantity >= htotal
        else:
            assert quantity >= htotal + 1


    def test_all_fields_is_filled(self, calc_total):
        """Проверяем - у всех питомцев есть имя, возраст и порода"""
        # implicity-wait находиься в фикстуре
        # Получаем список имен, в том числе ''
        names = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets td:nth-child(2)')
        # Избавляемся от пустых имен в новом списке
        tnames = []
        for name in names:
           if name.text != '':
               tnames.append(name.text)
        # Сравниваем два списка по количеству имен
        assert len(tnames) == pytest.total, 'Не у всех есть имя'

        # Получаем список возрастов, в том числе ''
        ages = driver.find_elements(By.CSS_SELECTOR, "tbody td:nth-child(4)")
        # Избавляемся от пустых значений в новом списке
        tages = []
        for age in ages:
           if age.text != '':
              tages.append(age.text)
        # Сравниваем два списка по размеру
        assert len(tages) == pytest.total, 'Не у всех есть возраст'

        # Получаем список всех пород, в том числе ''
        animal_types = driver.find_elements(By.CSS_SELECTOR, "#all_my_pets tbody td:nth-child(3)")
        # Избавляемся от пустых значений в новом списке
        tanimal_types = []
        for animal_type in animal_types:
           if animal_type.text != '':
              tanimal_types.append(animal_type.text)
        # Сравниваем два списка по размеру
        assert len(tanimal_types) == pytest.total, 'Не у всех есть порода'


    def test_unique_names(self):
        """Проверяем на уникальность имен"""
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(By.CSS_SELECTOR, "#all_my_pets tbody td:nth-child(2)"))
        except:
            driver.quit()
        #Получаем все имена
        names = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets td:nth-child(2)')
        names = [name.text for name in names]
        # Получаем множество неповторяющихся имен
        unames = set(names)
        # Если объекты равны, значит имена не повторяються
        assert len(names) == len(unames)


    def test_unique_pets(self):
        """Проверка на неповторяемость питомцев"""
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(By.CSS_SELECTOR, "#all_my_pets tbody td:nth-child(2)"))
        except:
            driver.quit()
        # Получаем все записи питомцев
        records = driver.find_elements(By.CSS_SELECTOR, "#all_my_pets tbody tr")
        # Получаем список кортежей, где кортеж - (имя, порода, возраст)
        records = [ tuple(record.text.split(' ')) for record in records ]
        # Проверяем на совпадения, сравнивая кортежи
        N = len(records)
        for i in range(N-1):
            for j in range(i+1, N):
                assert records[i] != records[j], 'Есть одинаковые карточки питомцев!'

