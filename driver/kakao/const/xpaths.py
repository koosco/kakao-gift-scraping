#  CATEGORY
XPATH_CATEGORY_BUTTON = '//*[@id="kakaoWrap"]/sc-gift-header/header/lib-container-pc/div[1]/div/div[1]/button'
XPATH_CATEGORY_NAME = '/html/body/cu-popup-container2[1]/cu-popup-wrapper2/app-pc-category-tab/div/div/div[2]/div/div[1]/app-pc-category-l-category/ul/li[{i}]/a/span'
XPATH_SUB_CATEGORY_NAME = '//*[@id="tabpan-{i}"]/ul/li[{j}]/gc-link/a/span'
XPATH_CATEGORY_LIST = '/html/body/cu-popup-container2[1]/cu-popup-wrapper2/app-pc-category-tab/div/div/div[2]/div/div[1]/app-pc-category-l-category/ul'
XPATH_CATEGORY_ELEMENT = '/html/body/cu-popup-container2[1]/cu-popup-wrapper2/app-pc-category-tab/div/div/div[2]/div/div[1]/app-pc-category-l-category/ul/li[{i}]/a'
XPATH_SUB_LIST = '//*[@id="tabpan-{i}"]/ul'  # i는 1부터 시작
XPATH_SUB_CATEGORY_ELEMENT = '//*[@id="tabpan-{i}"]/ul/li[{j}]/gc-link/a'  # i, j는 1부터 시작
XPATH_CATEGORY_CANCEL_BUTTON = '/html/body/cu-popup-container2[1]/cu-popup-wrapper2/app-pc-category-tab/div/div/button'

#  ITEM

XPATH_SUB_CATEGORY_SELECTOR = '//*[@id="mArticle"]/app-pw-home/app-category-list/div/div/ul/li[{i}]/gc-link/a'
XPATH_ITEM_ELEMENT = '//*[@id="mArticle"]/app-pw-home/div/app-category-product-list/cu-infinite-scroll/div/app-category-product-wrapper/div/app-view-grid/div/ul/li[{i}]/app-product/div'
XPATH_ITEM_BUTTON = '//*[@id="mArticle"]/app-pw-home/div/app-product-brand-tab/div/ul/li[2]/a'
