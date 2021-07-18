from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    ''' Тест от лица нового посетителя '''

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_can_stat_a_list_and_retrieve_it_later(self):
        '''Тест: можно создать список и получить его позже'''
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)
        self.fail('Закончить тест!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
