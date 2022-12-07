"""Orange HRM test suite"""
import time
import unittest
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


DRIVER_WAIT_TIME = 6
STABILITY_SLEEP_TIME = 7
URL = 'https://opensource-demo.orangehrmlive.com/web/index.php/auth/login'
DRIVER_SERVICE = Service(executable_path=ChromeDriverManager().install())
ADMIN_PASSWORD = 'admin123'
ADMIN_LOGIN = 'Admin'
TEST_USER_NAME = 'Petr'
TEST_USER_LASTNAME = 'Ivanoff'
TEST_JOB_TITLE = 'QA Engineer'
NO_SEARCH_RESULTS = "No Records Found"


class BCSelWebDriver(unittest.TestCase):
    """User manipulations test cases"""

    def setUp(self) -> None:
        self.driver = webdriver.Chrome(service=DRIVER_SERVICE)
        self.driver.implicitly_wait(DRIVER_WAIT_TIME)
        self.driver.get(url=URL)
        self.driver.find_element(By.XPATH, '//input[@name="username"]').send_keys(ADMIN_LOGIN)
        self.driver.find_element(By.XPATH, '//input[@name="password"]').send_keys(ADMIN_PASSWORD)
        self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        self.assertTrue(self.driver.find_element(By.XPATH, '//h6[text()="Dashboard"]'))

    def tearDown(self) -> None:
        header_profile_picture_element = '//img[@alt="profile picture" and @class="oxd-userdropdown-img"]'
        self.driver.find_element(By.XPATH, header_profile_picture_element).click()
        self.driver.find_element(By.XPATH, '//a[text()="Logout"]').click()
        self.assertTrue(self.driver.find_element(By.XPATH, '//h5[text()="Login"]'))
        self.driver.quit()

    def test_add_new_user(self) -> None:
        """Adding a new user in PIM tab """
        self.driver.find_element(By.XPATH, '//span[text()="PIM"]').click()
        self.driver.find_element(By.XPATH, '//button[text()=" Add "]').click()
        self.driver.find_element(By.XPATH, '//input[@name="firstName"]') \
            .send_keys(TEST_USER_NAME)
        self.driver.find_element(By.XPATH, '//input[@name="lastName"]') \
            .send_keys(TEST_USER_LASTNAME)
        self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()

        self.assertTrue(self.driver.find_element(By.XPATH, '//h6[text() = "Personal Details"]'))

        self.driver.find_element(By.XPATH, '//span[text()="PIM"]').click()
        self.driver.find_element(By.XPATH, '//input[@placeholder = "Type for hints..."]') \
            .send_keys(f'{TEST_USER_NAME} {TEST_USER_LASTNAME}')
        self.driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
        time.sleep(STABILITY_SLEEP_TIME)
        self.assertEqual(TEST_USER_NAME,
                         self.driver.find_element(By.XPATH, '//div[@role="cell"][3]').text)
        self.assertEqual(TEST_USER_LASTNAME,
                         self.driver.find_element(By.XPATH, '//div[@role="cell"][4]').text)

    def test_add_user_job_title(self) -> None:
        """Add missing user information in Job Details"""
        job_title_dropdown_btn_element = '//label[text()="Job Title"]/..//following-sibling::div//i'

        self.driver.find_element(By.XPATH, '//span[text()="PIM"]').click()
        self.driver.find_element(By.XPATH, '//input[@placeholder = "Type for hints..."]') \
            .send_keys(f'{TEST_USER_NAME} {TEST_USER_LASTNAME}')
        self.driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
        time.sleep(STABILITY_SLEEP_TIME)
        job_title_ext = self.driver.find_element(By.XPATH, '//div[@role="cell"][5]').text
        self.assertEqual('', job_title_ext)

        self.driver.find_element(By.XPATH, '//i[@class="oxd-icon bi-pencil-fill"]').click()

        self.assertTrue(self.driver.find_element(By.XPATH, '//h6[text() = "Personal Details"]'))

        self.driver.find_element(By.XPATH, '//a[text()= "Job"]').click()
        self.driver.find_element(By.XPATH, job_title_dropdown_btn_element).click()
        self.driver.find_element(By.XPATH,
                                 '//div[@role="option"]//span[text()="QA Engineer"]').click()
        self.driver.find_element(By.XPATH, '//input[@placeholder="yyyy-mm-dd"]').click()
        self.driver.find_element(By.XPATH, '//div[text()="Today"]').click()
        self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()

        self.driver.find_element(By.XPATH, '//span[text()="PIM"]').click()
        self.driver.find_element(By.XPATH, '//input[@placeholder = "Type for hints..."]') \
            .send_keys(f'{TEST_USER_NAME} {TEST_USER_LASTNAME}')
        self.driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
        time.sleep(STABILITY_SLEEP_TIME)
        job_title_ext = self.driver.find_element(By.XPATH, '//div[@role="cell"][5]').text
        self.assertEqual(TEST_JOB_TITLE, job_title_ext)

    def test_delete_user(self) -> None:
        """ Delete User """
        employee_name_autosuggest_list_element = \
            f'//div[@role="listbox"]//span[normalize-space()="{TEST_USER_NAME} {TEST_USER_LASTNAME}"]'
        self.driver.find_element(By.XPATH, '//span[text()="PIM"]').click()

        self.driver.find_element(By.XPATH, '//input[@placeholder = "Type for hints..."]') \
            .send_keys(f'{TEST_USER_NAME}'[:3])
        time.sleep(STABILITY_SLEEP_TIME)

        self.driver.find_element(By.XPATH, employee_name_autosuggest_list_element).click()
        self.driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
        self.assertTrue(self.driver.find_element(By.XPATH, '//span[text() = "(1) Record Found"]'))

        self.driver.find_element(By.XPATH, '//i[@class = "oxd-icon bi-trash"]').click()
        self.driver.find_element(By.XPATH, '//button[text() = " Yes, Delete "]').click()
        time.sleep(STABILITY_SLEEP_TIME)

        self.driver.find_element(By.XPATH, '//span[text()="PIM"]').click()
        self.driver.find_element(By.XPATH, '//input[@placeholder = "Type for hints..."]') \
            .send_keys(f'{TEST_USER_NAME} {TEST_USER_LASTNAME}')
        time.sleep(STABILITY_SLEEP_TIME)

        self.driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
        time.sleep(STABILITY_SLEEP_TIME)

        text_element_is_present = True
        try:
            self.driver.find_element(By.XPATH,
                                                  '//span[text() = "No Records Found"]')
        except NoSuchElementException:
            text_element_is_present = False
        self.assertTrue(text_element_is_present)

if __name__ == '__main__':
    unittest.main()
