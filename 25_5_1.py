import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestPetFriendsSelenium:

    def test_total_equal_all_pets(self, calc_total):
        """Проверяем, что кол-во total питомцев из профиля пользователя равно количеству из списка на странице"""
        total = pytest.total
        allpets = len (pytest.driver.find_elements(By.CSS_SELECTOR, '#all_my_pets tbody tr'))
        assert total == allpets


    def test_half_of_total_have_image(self, calc_total):
        """Проверяем, что у половины питомцев есть фото"""

        WebDriverWait(pytest.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#all_my_pets img")))

        # Получаем все элементы с тегом img
        images = pytest.driver.find_elements(By.CSS_SELECTOR, '#all_my_pets img')
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
        names = pytest.driver.find_elements(By.CSS_SELECTOR, '#all_my_pets td:nth-child(2)')
        # Избавляемся от пустых имен в новом списке
        tnames = []
        for name in names:
           if name.text != '':
               tnames.append(name.text)
        # Сравниваем два списка по количеству имен
        assert len(tnames) == pytest.total, 'Не у всех есть имя'

        # Получаем список возрастов, в том числе ''
        ages = pytest.driver.find_elements(By.CSS_SELECTOR, "tbody td:nth-child(4)")
        # Избавляемся от пустых значений в новом списке
        tages = []
        for age in ages:
           if age.text != '':
              tages.append(age.text)
        # Сравниваем два списка по размеру
        assert len(tages) == pytest.total, 'Не у всех есть возраст'

        # Получаем список всех пород, в том числе ''
        animal_types = pytest.driver.find_elements(By.CSS_SELECTOR, "#all_my_pets tbody td:nth-child(3)")
        # Избавляемся от пустых значений в новом списке
        tanimal_types = []
        for animal_type in animal_types:
           if animal_type.text != '':
              tanimal_types.append(animal_type.text)
        # Сравниваем два списка по размеру
        assert len(tanimal_types) == pytest.total, 'Не у всех есть порода'


    def test_unique_names(self):
        """Проверяем на уникальность имен"""

        WebDriverWait(pytest.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#all_my_pets tbody td:nth-child(2)")))

        #Получаем все имена
        names = pytest.driver.find_elements(By.CSS_SELECTOR, '#all_my_pets td:nth-child(2)')
        names = [name.text for name in names]
        # Получаем множество неповторяющихся имен
        unames = set(names)
        # Если объекты равны, значит имена не повторяються
        assert len(names) == len(unames)


    def test_unique_pets(self):
        """Проверка на неповторяемость питомцев"""

        WebDriverWait(pytest.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#all_my_pets tbody td:nth-child(2)")))

        # Получаем все записи питомцев
        records = pytest.driver.find_elements(By.CSS_SELECTOR, "#all_my_pets tbody tr")
        # Получаем список кортежей, где кортеж - (имя, порода, возраст)
        records = [ tuple(record.text.split(' ')) for record in records ]
        # Проверяем на совпадения, сравнивая кортежи
        N = len(records)
        for i in range(N-1):
            for j in range(i+1, N):
                assert records[i] != records[j], 'Есть одинаковые карточки питомцев!'

