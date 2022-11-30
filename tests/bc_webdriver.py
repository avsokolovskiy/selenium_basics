"""Orange HRM test suite"""
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

TIME_TO_WAIT = 5000

URL = 'https://opensource-demo.orangehrmlive.com/web/index.php/auth/login'
DRIVER_SERVICE = Service(executable_path=ChromeDriverManager().install())
ADMIN_PASSWORD = 'admin123'
ADMIN_LOGIN = 'Admin'
NEW_USER_NAME = 'Petr'
NEW_USER_LASTNAME = 'Ivanoff'
NEW_JOB_TITLE = 'QA Engineer'
NO_SEARCH_RERSULTS = "No Records Found"


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
        self.driver.find_element(By.XPATH, '//img[@alt="profile picture" and @class="oxd-userdropdown-img"]').click()
        self.driver.find_element(By.XPATH, '//a[text()="Logout"]').click()
        self.assertTrue(self.driver.find_element(By.XPATH, '//h5[text()="Login"]'))
        self.driver.quit()

    def test_add_new_user(self) -> None:
        """Adding a new user in PIM tab """

        self.find_xp('//span[text()="PIM"]').click()
        # self.driver.find_element(By.XPATH, '//span[text()="PIM"]').click()
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
        time.sleep(5)
        self.assertEqual(NEW_USER_NAME, self.driver.find_element(By.XPATH, '//div[@role="cell"][3]').text)
        self.assertEqual(NEW_USER_LASTNAME, self.driver.find_element(By.XPATH, '//div[@role="cell"][4]').text)


    def test_add_user_job_title(self) -> None:
        """Add missing user information in Job Details"""
        self.driver.find_element(By.XPATH, '//span[text()="PIM"]').click()
        self.driver.find_element(By.XPATH, '//input[@placeholder = "Type for hints..."]') \
            .send_keys(f'{NEW_USER_NAME} {NEW_USER_LASTNAME}')
        self.driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
        time.sleep(5)
        job_title_ext = self.driver.find_element(By.XPATH, '//div[@role="cell"][5]').text
        self.assertEqual('', job_title_ext)

        self.driver.find_element(By.XPATH, '//i[@class="oxd-icon bi-pencil-fill"]').click()

        self.assertTrue(self.driver.find_element(By.XPATH, '//h6[text() = "Personal Details"]'))

        self.driver.find_element(By.XPATH, '//a[text()= "Job"]').click()
        self.driver.find_element(By.XPATH,
                                 '//label[text()="Job Title"]/..//following-sibling::div//i').click()
        self.driver.find_element(By.XPATH, '//div[@role="option"]//span[text()="QA Engineer"]').click()
        self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()

        self.driver.find_element(By.XPATH, '//span[text()="PIM"]').click()
        self.driver.find_element(By.XPATH, '//input[@placeholder = "Type for hints..."]') \
            .send_keys(f'{NEW_USER_NAME} {NEW_USER_LASTNAME}')
        self.driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
        time.sleep(5)
        job_title_ext = self.driver.find_element(By.XPATH, '//div[@role="cell"][5]').text
        self.assertEqual(NEW_JOB_TITLE, job_title_ext)

    def test_delete_user(self) -> None:
        """
        Scenario Delete User
            When I go to “PIM” tab
            And I start typing employee name in [Employee Name] field
            Then 5 suggestions in displayed in dropdown
            When I select user name from dropdown
            And I click [Search] button
            Then Row with user is presented in [Records Found]
            When I delete the user from list of employees
            Then Row with user is not presented in [Records Found]
        """
        self.driver.find_element(By.XPATH, '//span[text()="PIM"]').click()

        self.driver.find_element(By.XPATH, '//input[@placeholder = "Type for hints..."]') \
            .send_keys(f'{NEW_USER_NAME}'[:1])
        time.sleep(5)

        # self.driver.find_element(By.XPATH,
        #self.driver.find_element(By.XPATH, '//div[@role="listbox"]//span[.="Petr Ivanoff"]').click()
        #self.driver.find_element(By.XPATH, '//span[contains(text(),"Petr Ivanoff")]').click()
        #ActionChains(driver=self.driver)\
        #    .move_to_element(self.driver.find_element(By.XPATH,'//div[@role="listbox"]')).perform()
        ActionChains(driver=self.driver) \
            .move_to_element(self.driver.find_element(By.XPATH, '//div[@role="option"]//span[text()="Petr Ivanoff"]')).click().perform()
        #self.driver.find_element(By.XPATH, '//div[@role="listbox"]').
        #self.driver.find_element(By.XPATH, '//span[.="Petr Ivanoff"]').click()
        
        self.driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
        self.assertTrue(self.driver.find_element(By.XPATH, '//span[text() = "(1) Record Found"]'))

        self.driver.find_element(By.XPATH, '//i[@class = "oxd-icon bi-trash"]').click()
        self.driver.find_element(By.XPATH, '//button[text() = " Yes, Delete "]').click()

        self.driver.find_element(By.XPATH, '//span[text()="PIM"]').click()
        self.driver.find_element(By.XPATH, '//input[@placeholder = "Type for hints..."]') \
            .send_keys(f'{NEW_USER_NAME} {NEW_USER_LASTNAME}')
        self.driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
        time.sleep(5)
        test_txt_value = self.driver.find_element(By.XPATH, '//span[text() = "No Records Found"]').text
        self.assertEqual(NO_SEARCH_RERSULTS, test_txt_value)

    def find_xp(self, xpath):
        """Exception handler"""
        return self.driver.find_element(By.XPATH, xpath)


if __name__ == '__main__':
    unittest.main()
