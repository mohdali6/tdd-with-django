from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def check_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	def test_can_start_list_and_retrieve_later(self):
		print self
		self.browser.get(self.live_server_url)

		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)
		
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

		inputbox.send_keys('Buy Apple Watch')
		
		inputbox.send_keys(Keys.ENTER)
		list_url = self.browser.current_url
		self.assertRegexpMatches(list_url, '/lists/.+')
		self.check_row_in_list_table('1: Buy Apple Watch')

		# New text box to enter new to-do item.
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use Apple Watch')
		inputbox.send_keys(Keys.ENTER)

		# The page updates, and now shows both to-do items
		self.check_row_in_list_table('1: Buy Apple Watch')
		self.check_row_in_list_table('2: Use Apple Watch')

		#New user
		self.browser.quit()
		self.browser = webdriver.Firefox()

		#New user visits site
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy Apple Watch', page_text)
		self.assertNotIn('Use Apple Watch', page_text)

		#New user starts new list
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Clean room')
		inputbox.send_keys(Keys.ENTER)

		#New user unique url
		new_user_list_url = self.browser.current_url
		self.assertRegexpMatches(new_user_list_url, '/lists/.+')
		self.assertNotEqual(new_user_list_url, list_url)

		#Again test for old user list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy Apple Watch', page_text)
		self.assertIn('Clean room', page_text)

		self.fail('Finish the test!')

		#Define further