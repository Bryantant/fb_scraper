from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep

def find_element_by_css_selector(driver, selector):
    try:
        return driver.find_element(By.CSS_SELECTOR, selector)
    except Exception as e:
        print(f"Error finding element by CSS selector '{selector}'")
        return None
    
def find_elements_by_css_selector_from_an_element(element, selector):  
    try:
        return element.find_element(By.CSS_SELECTOR, selector)
    except Exception as e:
        print(f"Error finding element by CSS selector '{selector}'")
        return None

def scrape(url):

    options = Options()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    is_story_or_post = "story.php" in url or "post" in url
    if(not is_story_or_post):
        close_button = find_element_by_css_selector(driver, "[aria-label='Close']")
        close_button.click()


    driver.execute_script("window.scrollTo(0, 200);")
    sleep(3)


    if not is_story_or_post:
        while True:
            try:
                view_more_button = driver.find_element(By.CSS_SELECTOR, ".html-div .html-div [role='button'][tabindex='0']:not([aria-label='Identity badges']):not([aria-label='1 reaction; see who reacted to this'])")
                view_more_button.click()
                print("Clicked 'View more comments' button.")
                sleep(1.5)
            except NoSuchElementException as e:
                print(f"Error clicking 'View more comments' button: {e}")
                break

    result = []
    if not is_story_or_post:
        comments = driver.find_elements(By.CSS_SELECTOR, "[role='article']")
        print(len(comments))
        for comment in comments:
            username = 'unknown'
            timestamp = '00:00'
            comment_text = '-'
            reaction_element = find_elements_by_css_selector_from_an_element(comment, "img[height='18'][width='18'][role='presentation']")
            if reaction_element is None:
                continue

            username_element = find_elements_by_css_selector_from_an_element(comment, "div span span[dir='auto']")
            if username_element is not None:
                username = username_element.get_attribute("textContent")

            timestamp_element = find_elements_by_css_selector_from_an_element(comment, "span div[role='button']")
            if timestamp_element is not None:
                timestamp = timestamp_element.get_attribute("textContent")

            comment_text_element = find_elements_by_css_selector_from_an_element(comment, "div[dir='auto']")
            if comment_text_element is not None:
                comment_text = comment_text_element.get_attribute("textContent")

            result.append({
                "username": username,
                "timestamp": timestamp,
                "comment_text": comment_text
            })
    else:
        handled_comments = []
        last_total_comments = 0
        while True:
            comments = driver.find_elements(By.CSS_SELECTOR, "[data-visualcompletion='ignore-dynamic']  [role='article']")
            if (last_total_comments > 0 and len(comments) == last_total_comments):
                print("No new comments found, breaking the loop.")
                break
            last_total_comments = len(comments)
            last_comment = len(comments) - 1
            current_comment = 0
            for comment in comments:
                if current_comment == last_comment:
                    print("Last comment reached, scrolling to it.")
                    driver.execute_script("arguments[0].scrollIntoView();", comment)
                    sleep(3)


                current_comment += 1

                username = 'unknown'
                timestamp = '00:00'
                comment_text = '-'
                reaction_element = find_elements_by_css_selector_from_an_element(comment, "img[height='18'][width='18'][role='presentation']")
                if reaction_element is None:
                    continue

                username_element = find_elements_by_css_selector_from_an_element(comment, "div span span[dir='auto']")
                if username_element is not None:
                    username = username_element.get_attribute("textContent")

                timestamp_element = find_elements_by_css_selector_from_an_element(comment, "span div[role='button']")
                if timestamp_element is not None:
                    timestamp = timestamp_element.get_attribute("textContent")

                comment_text_element = find_elements_by_css_selector_from_an_element(comment, "div[dir='auto']")
                if comment_text_element is not None:
                    comment_text = comment_text_element.get_attribute("textContent")
    

                keys = f"{username} {timestamp} {comment_text}"
                if keys in handled_comments:
                    print(f"Already handled comment: {keys}")
                    continue

                result.append({
                    "username": username,
                    "timestamp": timestamp,
                    "comment_text": comment_text
                })

                handled_comments.append(keys)

    driver.quit()
    return result

