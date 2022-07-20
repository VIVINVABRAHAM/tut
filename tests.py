from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Hosttest(LiveServerTestCase):
	def testform(self):
		selenium = webdriver.Chrome()
		#Choose your url to visit
		selenium.get('http://127.0.0.1:8000/account/signin')
		#find the elements you need to submit form
		player_name = selenium.find_element_by_name('email')
		player_pass = selenium.find_element_by_name('pass')


		submit = selenium.find_element_by_name('button')

		#populate the form with data
		player_name.send_keys('anu123@gmail.com')
		player_pass.send_keys('Anu@123456')


		#submit form
		submit.send_keys(Keys.RETURN)

		#check result; page source looks at entire html document
		assert 'Anu' in selenium.page_source