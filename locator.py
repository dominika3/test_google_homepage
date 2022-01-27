from selenium.webdriver.common.by import By


class MainPageLocators(object):
    SEARCH_BOX_ELEMENT = (By.NAME, 'q')


class SearchPageLocators(object):
    LINK_LOCATOR = (By.XPATH, '/html/body/div[8]/div/div[10]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/a/div/cite')
    PERSONALIZE_SEARCH_DISABLE_BUTTON = (By.XPATH, '/html/body/c-wiz/div/div/div/div[2]/div[3]/div[2]/div/div[2]/div[1]/div/button')
    PERSONALIZE_YOUTUBE_DISABLE_BUTTON = (By.XPATH, '/html/body/c-wiz/div/div/div/div[2]/div[4]/div[2]/div/div[2]/div[1]/div/button')
    PERSONALIZE_ADVERTS_DISABLE_BUTTON = (By.XPATH, '/html/body/c-wiz/div/div/div/div[2]/div[5]/div[2]/div[2]/div/div[2]/div[1]/div/button')
    PERSONAL_SETTINGS_CONFIRM_BUTTON = (By.XPATH, '/html/body/c-wiz/div/div/div/div[2]/form/div/button')
    ADJUST_COOKIES_BUTTON = (By.ID, 'VnjCcb')

