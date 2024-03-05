from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as BS
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import traceback
import json
import os
from dotenv import load_dotenv

# loading .env to os
load_dotenv()


def job_related_content(soup, final_dict):
    """
    for scrapping job related things from the html soup,
    and add it into the final_dict, and return it
    """

    try:
        print("here...")
        job_related_content = soup.find(
            "li",
            class_="job-details-jobs-unified-top-card__job-insight job-details-jobs-unified-top-card__job-insight--highlight",
        )

        if job_related_content:
            job_content = job_related_content.get_text()
            job_content = job_content.strip().split()

            if job_content[-1] == "level":
                last_ele = job_content[-2] + " " + job_content[-1]
                job_content.pop()
                job_content.pop()
                job_content.append(last_ele)

            if (len(job_content) >= 1) and (len(job_content) <= 3):
                if len(job_content) == 1:
                    final_dict["WorkPlace"] = job_content[0]
                elif len(job_content) == 2:
                    final_dict["WorkPlace"] = job_content[0]
                    final_dict["emploment_type"] = job_content[1]
                elif len(job_content) == 3:
                    final_dict["WorkPlace"] = job_content[0]
                    final_dict["emploment_type"] = job_content[1]
                    final_dict["seniority_level"] = job_content[2]
    except:
        # code here to log the job_related_containt failure's reason
        pass

    try:
        # Find the h1 tag with the specified class, which contains the job-title tag.
        h1_tag = soup.find(
            "h1", class_="t-24 t-bold job-details-jobs-unified-top-card__job-title"
        )

        # Check if the h1 tag is found
        if h1_tag:
            # Extract the text inside the h1 tag
            text_inside_h1 = h1_tag.get_text(strip=True)
            final_dict["job-title"] = text_inside_h1

    except:
        # code here to log the job_related_containt failure's reason
        pass

    return final_dict


def skills_related_content(soup, final_dict):
    """
    for scrapping skills related things from the html soup,
    and add it into the final_dict, and return it
    """
    try:

        skills_related_content = soup.find(
            "a",
            class_="app-aware-link job-details-how-you-match__skills-item-subtitle t-14 overflow-hidden",
        )
        if skills_related_content:
            skills_content = skills_related_content.get_text(strip=True)
            skills_content = skills_content.split(",")
            skills_content = [skills.strip() for skills in skills_content]

            # if len(lst) > 1, then and only then we will get the last element with ,and xyz format
            # confirm first if last element is started with "and "
            # if this is the case then do followings
            # firstly store last ele in variable
            # then pop last element from the list
            # then manipulate the last_element variable, replace "and " with ""
            # now append this manipulated variable into the lst.

            if len(skills_content) > 1:
                last_element = skills_content[-1]
                if last_element.startswith("and "):
                    skills_content.pop()
                    last_element = last_element.replace("and ", "")
                    skills_content.append(last_element)
                print(skills_content)

            if len(skills_content) >= 1:
                final_dict["skills"] = skills_content

    except:
        # code here to log the skills related containt failure's reason
        pass

    return final_dict


def overview_related_content(soup, final_dict):
    """
    for scrapping overview related things from the html soup,
    and add it into the final_dict, and return it.
    """
    try:
        article_related_content = soup.find(
            "article", class_="jobs-description__container--condensed"
        )

        # Find all paragraphs within the article
        paragraphs = article_related_content.find_all("p")

        # our first strong tag name is overview,
        # and up to second strong tag, we have 1 para or more than 1 para
        # that's why set the flag on the strong tag to reach upto 2, and break.
        strong_tag_counter = 0

        # initializing the paragraph here:
        para = ""

        for paragraph in paragraphs:
            # Check if the paragraph contains a strong tag
            if paragraph.find("strong"):
                strong_tag_counter += 1
                if strong_tag_counter >= 2:
                    break
                continue

            # Extract the text of the paragraph
            paragraph_text = paragraph.get_text(strip=True)
            para += paragraph_text

            final_dict["Overview"] = para
    except:
        # code here to log the overview related containt failure's reason
        pass

    return final_dict


def job_scrapper(url_for_scrape):
    """
    This function is used to fetch the linkedin job's data, which includes followings.
    job related info, position related info, skills related info, and overview.
    we will store the output in json as a output.json in a result directory.
    """

    # ensuring that we have the result dict to store the result,
    # if we do not have we will create one folder, and we will make the result_path as well.

    # use when it is necessary, for eg while making page scroll, after login, etc..
    small_buffer = 1.5
    big_buffer = 4

    # initializing the finadict to store result into.
    final_dict = {
        "job-title": "",
        "WorkPlace": "",
        "seniority_level": "",
        "emploment_type": "",
        "skills": "",
        "Overview": "",
        "scrapping_time": "",
    }

    try:

        options = Options()

        options.headless = True  # False, if uh wanna run in the ui mode.
        options.add_argument("--headless")  # comment this line in case of False

        # Note: defining path where my chromedriver is stored, that can differ in the production
        DRIVER_PATH = "/usr/local/bin/chromedriver"

        # Specify the executable_path using the service argument
        service = Service(DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)

        # Opening linkedIn's login page
        driver.get("https://linkedin.com/")

        # entering username
        # Note: this should come from the environment variable instead of defining it manually.
        try:
            # here, we are fetching USERNAME & PASSWORD from os, os was getting from env via dot_env load_dotenv
            username = driver.find_element(By.ID, "session_key")
            username.send_keys(os.environ.get("USERNAME"))
        except Exception as e:
            print("exception for username", e)

        try:
            pword = driver.find_element(By.ID, "session_password")
            pword.send_keys(os.environ.get("PWORD"))
        except Exception as e:
            print("e for the pass", e)

        # Clicking on the log in button
        # Format (syntax) of writing XPath -->
        # //tagname[@attribute='value']
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        print("login done, now we will scrape the urls")

        # as of now it is one, it can be many handle this from here and make a list via agrs, kwargs
        # urls_list = [
        #     url_for_scrape,
        # ]

        urls_list = [url_for_scrape]

        for profile_url in urls_list:

            time.sleep(small_buffer)
            driver.get(profile_url)
            time.sleep(small_buffer)

            start = time.time()

            # initialScroll,finalScroll will be used in the while loop,
            # it is used to scroll whole page just to make a html content as stable as possible.
            initialScroll = 0
            finalScroll = 1000

            while True:
                driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
                # this command scrolls the window starting from
                # the pixel value stored in the initialScroll
                # variable to the pixel value stored at the
                # finalScroll variable
                initialScroll = finalScroll
                finalScroll += 1000

                # we will stop the script for some seconds so that, data gets loaded.
                time.sleep(big_buffer)
                end = time.time()

                # breaking the code if there is the total time of 20seconds or more is required.
                if round(end - start) > 20:
                    break

            # we can add the time too, if we want to measure how much time is needed to fetch data from page
            scrapping_start_at = time.time()
            try:
                print("started soup making")

                # Get the page source
                page_source = driver.page_source
                # Parse the HTML using Beautiful Soup
                soup = BS(page_source, "html.parser")

                print("soup made will scroll page now.")

            except:
                print("scrapper failure and the reason are as below..")
                print(traceback.format_exc())

            final_dict = job_related_content(soup, final_dict)
            print("job related part scrapped")

            final_dict = skills_related_content(soup, final_dict)
            print("skills related part scrapped")

            final_dict = overview_related_content(soup, final_dict)
            print("overview related part scrapped")

            scrapping_time = time.time() - scrapping_start_at
            scrapping_time = round(scrapping_time, 2)
            final_dict["scrapping_time"] = round(scrapping_time, 2)

            # need to make proper logout functionality here., and then quit
            driver.quit()
            return final_dict

    except:
        json_data = json.dumps(final_dict, indent=2)
        return final_dict
