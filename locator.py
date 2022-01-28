from selenium.webdriver.common.by import By


class MainPageLocators(object):
    ADJUST_COOKIES_BUTTON = (By.ID, 'VnjCcb')
    SEARCH_BOX_ELEMENT = (By.NAME, 'q')
    VOICE_SEARCH_BUTTON = (By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[3]/div[3]')
    VOICE_SEARCH_TOOLTIP = (By.XPATH, '/html/body/div[4]')
    GOOGLE_IMAGE = (By.XPATH, '/html/body/div[1]/div[2]/div/img')
    SEARCH_IN_GOOGLE_BUTTON = (By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]')
    SEARCH_BAR_WITH_PADDING = (By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div')
    PERSONALIZE_SEARCH_DISABLE_BUTTON = (By.XPATH, '/html/body/c-wiz/div/div/div/div[2]/div[3]/div[2]/div/div[2]/'
                                                   'div[1]/div/button')
    PERSONALIZE_YOUTUBE_DISABLE_BUTTON = (By.XPATH, '/html/body/c-wiz/div/div/div/div[2]/div[4]/div[2]/div/div[2]/'
                                                    'div[1]/div/button')
    PERSONALIZE_ADVERTS_DISABLE_BUTTON = (By.XPATH, '/html/body/c-wiz/div/div/div/div[2]/div[5]/div[2]/div[2]/div/'
                                                    'div[2]/div[1]/div/button')


class SearchPageLocators(object):
    LINK_LOCATOR = (By.XPATH, '/html/body/div[8]/div/div[10]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/a/'
                              'div/cite')
    PERSONAL_SETTINGS_CONFIRM_BUTTON = (By.XPATH, '/html/body/c-wiz/div/div/div/div[2]/form/div/button')
    FILETYPE_SEARCH_RESULT_3 = (By.XPATH, '//*[@id="rso"]/div[4]/div/div/div[1]/div/div[2]/span[2]')
    FILETYPE_SEARCH_RESULT_4 = (By.XPATH, '//*[@id="rso"]/div[5]/div/div[1]/div[1]/div/div[2]/span[2]')
    FILETYPE_SEARCH_RESULT_6 = (By.XPATH, '//*[@id="rso"]/div[7]/div/div/div[1]/div/div[2]/span[2]')


