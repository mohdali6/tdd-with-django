from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_can_start_list_and_retrieve_later(self):
		self.browser.get('http://localhost:8000')

		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)
		
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

		inputbox.send_keys('Buy Apple Watch')
		
		inputbox.send_keys(Keys.ENTER)
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn('1: Buy Apple Watch', [row.text for row in rows])

		# New text box to enter new to-do item.
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use Apple Watch')
		inputbox.send_keys(Keys.ENTER)

		# The page updates, and now shows both to-do items
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn('1: Buy Apple Watch', [row.text for row in rows])
		self.assertIn('2: Use Apple Watch', [row.text for row in rows])

		self.fail('Fininsh the test!')

		#Define further
		 
if __name__ == '__main__':
	unittest.main()	