import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    """Set up Chrome in headless mode."""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


class TestHomePage:
    """Test home page."""

    def test_home_page_loads(self, driver):
        """Test that home page loads."""
        driver.get('http://localhost:8080')
        assert 'Dice Roller' in driver.title

    def test_home_page_has_login_link(self, driver):
        """Test login link exists."""
        driver.get('http://localhost:8080')
        login_link = driver.find_element(By.LINK_TEXT, 'Login')
        assert login_link is not None


class TestLogin:
    """Test login functionality."""

    def test_login_page_loads(self, driver):
        """Test login page loads."""
        driver.get('http://localhost:8080/login')
        heading = driver.find_element(By.TAG_NAME, 'h1')
        assert 'Login' in heading.text

    def test_login_with_valid_credentials(self, driver):
        """Test successful login."""
        driver.get('http://localhost:8080/login')
        
        # Fill in form
        driver.find_element(By.NAME, 'username').send_keys('user')
        driver.find_element(By.NAME, 'password').send_keys('password')
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        # Wait for redirect
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h1'))
        )
        
        # Verify on dashboard
        assert 'Hello user' in driver.page_source

    def test_login_with_invalid_credentials(self, driver):
        """Test failed login."""
        driver.get('http://localhost:8080/login')
        
        driver.find_element(By.NAME, 'username').send_keys('user')
        driver.find_element(By.NAME, 'password').send_keys('wrongpassword')
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        # Should see error message
        assert 'Invalid username or password' in driver.page_source


class TestDashboard:
    """Test dashboard functionality."""

    def test_roll_dice(self, driver):
        """Test rolling dice."""
        # Login first
        driver.get('http://localhost:8080/login')
        driver.find_element(By.NAME, 'username').send_keys('user')
        driver.find_element(By.NAME, 'password').send_keys('password')
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'num_dice'))
        )
        
        # Roll dice
        driver.find_element(By.NAME, 'num_dice').clear()
        driver.find_element(By.NAME, 'num_dice').send_keys('2')
        driver.find_element(By.NAME, 'sides').clear()
        driver.find_element(By.NAME, 'sides').send_keys('6')
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        # Should see roll result
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'bg-green-100'))
        )
        assert 'Rolled 2d6' in driver.page_source


class TestLogout:
    """Test logout functionality."""

    def test_logout(self, driver):
        """Test logout works."""
        # Login first
        driver.get('http://localhost:8080/login')
        driver.find_element(By.NAME, 'username').send_keys('user')
        driver.find_element(By.NAME, 'password').send_keys('password')
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Logout (user)'))
        )
        
        # Logout
        driver.find_element(By.LINK_TEXT, 'Logout (user)').click()
        
        # Should see logged out message
        assert 'logged out' in driver.page_source.lower()