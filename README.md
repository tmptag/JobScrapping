### jobscrapping

this is the django-based python project for scrapping, witht the help of selenium and beautifulshop.


### Table of Contents

- [Project Name](#project-name)
- [Introduction](#introduction)
- [Requirements](#Configuration)
- [Configuration](#Configuration)

## Introduction

aim is to fetch the job/skills/position related data of given job-post.


## Requirements

- you will required python3 on your local machine, to set up the enviroment for the project.
- then, you will have other requirements(related to the packages) are available, in this repo as a file named "requirements.txt".
- you should have installed one webdriver for doing the scrapping job(as we are using selenium for the login purposes, and i am using chrom). command for mac: "brew install --cask chromedriver"
- next step is you as you run this brew install command, it will install the chrom driver in your local machine, and return the installed path in your terminal as something like this
Linking Binary 'chromedriver' to '/usr/local/bin/chromedriver', copy this path this path have further usage in set-up.

## Configuration
step:1)download the project's repo as a zip.

step:2)unzip the folder, and place it properly where you want to setup the project.

step:3) now you will have folder like jobScrapping-main, for mac right click on this folder and select "new terminal at folder" .

step:4) type followings.
  - "python3 -m venv env" (for creating env)
  - "source env/bin/activate" (for activing env)
  - "pip install -r requirements.txt" (for installing requirements)
  - "code ." (open the code in terminal)

step: 5) add the DRIVER_PATH = "/usr/local/bin/chromedriver", change this path with the path that you got while installing driver by this command "brew install --cask chromedriver".

-Location of path: this path place at the datascrapper.py module available in the apk folder, and then job_scrapper in this function's try block's starting you will find the DRIVER_PATH, just change it's value with your path.

step:6) now after all this process you need to set up the .env file in the same folder where we have opened the termial: so you will find the folder name in the vs code as a  "JobScrapping-main", preciesly create one .env file in the same directory.

- to create .env just click on explorer pane of vs code, then find the name as"JobScrapping-main" in this tab you will have -- minus type checkbox to set all directory, and sub directory in one manner, now click on the empty at the bottom that is available in explorer pane. now just go in the JobScrappin-main, select first option +new file, and name it as .env

  - Note:- still if your .env goes into any other subdirectory of the project then drag and drop it in the main directory manually.

step:7) give credentials in this file,
.env file looks like this
- USERNAME=examplemail@21.com
- PWORD=exapmlepassword
 - Note:- change exaples with the actual credentials to login into the linked in.

step: 8) now, finally press this command in terminal
- "python manage.py runserver 9000"
	- Note:- you can run this server on any port you want, just change in the url accordingly.

- url:- "http://127.0.0.1:9000/job_scrapping/get_jd/"
- req: {"job_url": "https://www.linkedin.com/jobs/view/3819954068/"}
