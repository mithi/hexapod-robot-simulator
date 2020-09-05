import random
from selenium import webdriver

# Install the web drivers for selenium to your path if they do not already exist
import chromedriver_binary
import geckodriver_autoinstaller

import unittest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from widgets import leg_patterns_ui, dimensions_ui, ik_ui

# This class tests the UI for the web application.
# Index.py needs to be run first to start the server before the tests can be conducted.
class WidgetTests(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.server = 'http://127.0.0.1:8050/'
        self.timeout = 10

    # Helper function - wait until the webpage is loaded completely before starting tests
    def load_webpage_completely(self):
        self.browser.get(self.server)
        try:
            title_loaded = EC.title_contains("Hexapod")
            body_loaded = EC.presence_of_element_located((By.TAG_NAME, "h6"))
            WebDriverWait(self.browser, self.timeout).until(title_loaded)
            WebDriverWait(self.browser, self.timeout).until(body_loaded)
        except TimeoutException:
            print
            "Timed out waiting for the webpage to load"

    # Test all hyperlinks for all pages are available and working
    def test_all_links_working(self):
        self.load_webpage_completely()
        links = ['/leg-patterns',
                 '/kinematics',
                 '/inverse-kinematics',
                 '/',
                 'https://github.com/mithi/hexapod-robot-simulator',
                 'https://github.com/mithi/hexapod-robot-simulator',
                 'https://ko-fi.com/minimithi']
        for link in links:
            element = self.browser.find_element_by_xpath("//a[@href='"+link+"']")
            self.assertEqual(element.size!=0,True,"Web app has no link to "+ link)

    # Tests the UI for changing robot dimensions
    def test_dimensions_ui(self):
        self.load_webpage_completely()
        self.browser.find_element_by_xpath("//a[@href='/leg-patterns']").click()
        leg_dimension_names = dimensions_ui.WIDGET_NAMES

        for name in leg_dimension_names:
            widget = self.browser.find_element_by_id('widget-dimension-'+name)
            widget.clear()
            widget.send_keys(random.randint(90, 110))

    # Tests the UI for changing leg patterns
    def test_leg_patterns_ui(self):
        self.load_webpage_completely()
        self.browser.find_element_by_xpath("//a[@href='/leg-patterns']").click()
        widget_names = leg_patterns_ui.WIDGET_NAMES

        for name in widget_names:
            slider = WebDriverWait(self.browser,self.timeout).until(
            EC.element_to_be_clickable((By.ID,"widget-"+name)))
            random_slide = random.randint(-10,10)
            action = webdriver.ActionChains(self.browser)
            action.move_to_element(slider)
            action.click_and_hold(slider)
            action.move_by_offset(random_slide, 0)
            action.release()
            action.perform()

    # Tests the UI for changing inverse kinematics settings
    def test_inverse_kinematics_ui(self):
        self.load_webpage_completely()
        self.browser.find_element_by_xpath("//a[@href='/inverse-kinematics']").click()
        widget_ids = ik_ui.IK_WIDGETS_IDS
        for widget_id in widget_ids:
            slider = WebDriverWait(self.browser,self.timeout).until(
            EC.element_to_be_clickable((By.ID,widget_id)))
            random_slide = random.randint(-10,10)
            action = webdriver.ActionChains(self.browser)
            action.move_to_element(slider)
            action.click_and_hold(slider)
            action.move_by_offset(0,random_slide)
            action.release()
            action.perform()

    # Close the web application test
    def tearDown(self):
       self.browser.quit()


if __name__ =='__main__':
    unittest.main(warnings='ignore')
