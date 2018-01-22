import unittest
import time

from app import app

from flask import Flask
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from flask_testing import TestCase


class FlaskTest(TestCase):
    
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        self.baseURL = "http://localhost:5000"
        return app
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.get(self.baseURL)

    def tearDown(self):
        self.browser.quit()

    def test_server_is_running(self):
        self.assertEqual(self.browser.title, 'Store Locator')

    def test_displays_correct_template(self):
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertEqual(header_text, 'Find Nearest Store')

        label_text = self.browser.find_element_by_tag_name('label').text
        self.assertEqual(label_text, 'Enter your postcode:')        

    def test_page_displays_stores_and_maps(self):
        stores = self.browser.find_elements_by_class_name('store')
        maps = self.browser.find_elements_by_class_name('map')
        names = [store.text for store in stores]
        self.assertIn('Alton', names)
        self.assertIn('Worthing', names)
        self.assertIn('Friern Barnet', names)
        self.assertEqual(len(names), 95)
        self.assertEqual(len(maps), 95)

    def test_raise_error_on_invalid_postcode(self):
        field = self.browser.find_element_by_id('postcode')
        field.send_keys('dm')
        field.send_keys(Keys.ENTER)
        time.sleep(1)
        error = self.browser.find_element_by_id('error').text
        self.assertEqual(error, 'Invalid Postcode!')

    def test_find_nearby_store(self):
        field = self.browser.find_element_by_id('postcode')
        self.assertEqual(field.get_attribute('name'), 'postcode')
        field.send_keys('br5 4mu')
        field.send_keys(Keys.ENTER)
        time.sleep(1)
        store = self.browser.find_element_by_tag_name('h3').text
        store_map = self.browser.find_element_by_tag_name('img')
        self.assertEqual(store, 'Orpington')
        self.assertTrue(store_map)

    def test_displaying_2_nearby_stores(self):
        field = self.browser.find_element_by_id('postcode')
        self.assertEqual(field.get_attribute('name'), 'postcode')
        field.send_keys('rg40 8wo')
        field.send_keys(Keys.ENTER)
        time.sleep(1)
        stores = self.browser.find_elements_by_class_name('store')
        names = [store.text for store in stores]
        self.assertEqual('Wokingham', names[0])
        self.assertEqual('Winnersh', names[1])
        self.assertEqual(len(names), 2)

    def test_no_nearby_stores(self):
        field = self.browser.find_element_by_id('postcode')
        self.assertEqual(field.get_attribute('name'), 'postcode')
        field.send_keys('w12 0pr')
        field.send_keys(Keys.ENTER)
        time.sleep(1)
        empty = self.browser.find_element_by_id('no-result').text
        self.assertEqual(empty, 'No stores nearby.')

if __name__ == '__main__':
    unittest.main()
