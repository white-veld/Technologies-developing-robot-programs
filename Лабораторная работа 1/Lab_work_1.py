from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


class BasePage:
    def __init__(self, driver):
        self.driver = driver


class LoginPage(BasePage):
    def authorization(self, login, password):
        username = self.driver.find_element(By.ID, "user-name")
        password_field = self.driver.find_element(By.ID, "password")
        submit_button = self.driver.find_element(By.ID, "login-button")
        username.clear()
        password_field.clear()
        username.send_keys(login)
        password_field.send_keys(password)
        submit_button.click()

    def has_error(self):
        try:
            self.driver.find_element(by=By.CLASS_NAME, value="error-message-container")
            return True
        except:
            return False

class InventoryPage(BasePage):
    def sort(self, value):
        select_element = self.driver.find_element(By.CLASS_NAME, 'product_sort_container')
        select = Select(select_element)
        select.select_by_value(value)

    def get_items(self):
        return self.driver.find_elements(By.CLASS_NAME, "inventory_item")

    @staticmethod
    def get_price(item):
        price = item.find_element(By.CLASS_NAME, "inventory_item_price").text[1:]
        return float(price)

    @staticmethod
    def add_to_cart(item):
        need_item = item.find_element(By.CLASS_NAME, "btn")
        need_item.click()

if __name__ == "__main__":
    driver = webdriver.Firefox()
    try:
        driver.get("https://www.saucedemo.com/")

        login_page = LoginPage(driver)
        login_page.authorization("locked_out_user", "secret_sauce")
        if login_page.has_error():
            login_page.authorization("standard_user", "secret_sauce")

        inventory_page = InventoryPage(driver)
        inventory_page.sort('za')
        inventory_list = inventory_page.get_items()
        most_expensive_item = max(inventory_list, key=inventory_page.get_price)
        inventory_page.add_to_cart(most_expensive_item)
    finally:
        driver.quit()