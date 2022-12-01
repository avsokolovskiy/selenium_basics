"""Orange HRM test suite"""
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


TIME_TO_WAIT = 6
SLEEP_INT = 7
URL = 'https://opensource-demo.orangehrmlive.com/web/index.php/auth/login'
DRIVER_SERVICE = Service(executable_path=ChromeDriverManager().install())
ADMIN_PASSWORD = 'admin123'
ADMIN_LOGIN = 'Admin'
NEW_USER_NAME = 'Petr'
NEW_USER_LASTNAME = 'Ivanoff'
NEW_JOB_TITLE = 'QA Engineer'
NO_SEARCH_RESULTS = "No Records Found"


class BCSelWebDriver(unittest.TestCase):
    """User manipulations test cases"""

    def setUp(self) -> None:
        self.driver = webdriver.Chrome(service=DRIVER_SERVICE)
        self.driver.implicitly_wait(TIME_TO_WAIT)
        self.driver.get(url=URL)
        self.driver.find_element(By.XPATH, '//input[@name="username"]') \
            .send_keys(ADMIN_LOGIN)
        self.driver.find_element(By.XPATH, '//input[@name="password"]') \
            .send_keys(ADMIN_PASSWORD)
        self.driver.find_element(By.XPATH, '//button[@type="submit"]') \
            .click()
        self.assertTrue(self.driver.find_element(By.XPATH, '//h6[text()="Dashboard"]'))

    def tearDown(self) -> None:
        p_picture = '//img[@alt="profile picture" and @class="oxd-userdropdown-img"]'
        self.driver.find_element(By.XPATH, p_picture).click()
        self.driver.find_element(By.XPATH, '//a[text()="Logout"]').click()
        self.assertTrue(self.driver.find_element(By.XPATH, '//h5[text()="Login"]'))
        self.driver.quit()

    def test_add_new_user(self) -> None:
        """Adding a new user in PIM tab """
        self.driver.find_element(By.XPATH, '//span[text()="PIM"]').click()
        self.driver.find_element(By.XPATH, '//button[text()=" Add "]').click()
        self.driver.find_element(By.XPATH, '//input[@name="firstName"]') \
            .send_keys(NEW_USER_NAME)
        self.driver.find_element(By.XPATH, '//input[@name="lastName"]') \
            .send_keys(NEW_USER_LASTNAME)
        self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()

        self.assertTrue(self.driver.find_element(By.XPATH, '//h6[text() = "Personal Details"]'))

        self.driver.find_element(By.XPATH, '//span[text()="PIM"]').click()
        self.driver.find_element(By.XPATH, '//input[@placeholder = "Type for hints..."]') \
            .send_keys(f'{NEW_USER_NAME} {NEW_USER_LASTNAME}')
        self.driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
        time.sleep(SLEEP_INT)
        self.assertEqual(NEW_USER_NAME,
                         self.driver.find_element(By.XPATH, '//div[@role="cell"][3]').text)
        self.assertEqual(NEW_USER_LASTNAME,
                         self.driver.find_element(By.XPATH, '//div[@role="cell"][4]').text)

    def test_add_user_job_title(self) -> None:
        """Add missing user information in Job Details"""
        job_title_col = '//label[text()="Job Title"]/..//following-sibling::div//i'

        self.driver.find_element(By.XPATH, '//span[text()="PIM"]').click()
        self.driver.find_element(By.XPATH, '//input[@placeholder = "Type for hints..."]') \
            .send_keys(f'{NEW_USER_NAME} {NEW_USER_LASTNAME}')
        self.driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
        time.sleep(SLEEP_INT)
        job_title_ext = self.driver.find_element(By.XPATH, '//div[@role="cell"][5]').text
        self.assertEqual('', job_title_ext)

        self.driver.find_element(By.XPATH, '//i[@class="oxd-icon bi-pencil-fill"]').click()

        self.assertTrue(self.driver.find_element(By.XPATH, '//h6[text() = "Personal Details"]'))

        self.driver.find_element(By.XPATH, '//a[text()= "Job"]').click()
        self.driver.find_element(By.XPATH,job_title_col).click()
        self.driver.find_element(By.XPATH,
                                 '//div[@role="option"]//span[text()="QA Engineer"]').click()
        self.driver.find_element(By.XPATH, '//input[@placeholder="yyyy-mm-dd"]').click()
        self.driver.find_element(By.XPATH, '//div[text()="Today"]').click()
        self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()

        self.driver.find_element(By.XPATH, '//span[text()="PIM"]').click()
        self.driver.find_element(By.XPATH, '//input[@placeholder = "Type for hints..."]') \
            .send_keys(f'{NEW_USER_NAME} {NEW_USER_LASTNAME}')
        self.driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
        time.sleep(SLEEP_INT)
        job_title_ext = self.driver.find_element(By.XPATH, '//div[@role="cell"][5]').text
        self.assertEqual(NEW_JOB_TITLE, job_title_ext)

    def test_delete_user(self) -> None:
        """ Delete User """
        dd_xpath = \
            f'//div[@role="listbox"]//span[normalize-space()="{NEW_USER_NAME} {NEW_USER_LASTNAME}"]'
        self.driver.find_element(By.XPATH, '//span[text()="PIM"]').click()

        self.driver.find_element(By.XPATH, '//input[@placeholder = "Type for hints..."]') \
            .send_keys(f'{NEW_USER_NAME}'[:3])
        time.sleep(SLEEP_INT)

        self.driver.find_element(By.XPATH, dd_xpath).click()
        self.driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
        self.assertTrue(self.driver.find_element(By.XPATH, '//span[text() = "(1) Record Found"]'))

        self.driver.find_element(By.XPATH, '//i[@class = "oxd-icon bi-trash"]').click()
        self.driver.find_element(By.XPATH, '//button[text() = " Yes, Delete "]').click()

        self.driver.find_element(By.XPATH, '//span[text()="PIM"]').click()
        self.driver.find_element(By.XPATH, '//input[@placeholder = "Type for hints..."]') \
            .send_keys(f'{NEW_USER_NAME} {NEW_USER_LASTNAME}')
        self.driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
        time.sleep(SLEEP_INT)
        test_txt_value = self.driver.find_element(By.XPATH,
                                                  '//span[text() = "No Records Found"]').text
        self.assertEqual(NO_SEARCH_RESULTS, test_txt_value)


if __name__ == '__main__':
    unittest.main()
