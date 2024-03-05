# JobScrapping
2packages are used for job done (selenium, beautifulshop)

==============================================================================
Job Scrapping: this is based on python data scrapping
            gitignore: env, and .env(for credential purpose.)
==============================================================================
Flow: 1) firstly, make the Request(POST) on this api,
        "http://127.0.0.1:9000/job_scrapping/get_jd/"
        with the "job_post's url" in Json data.
        Json Data-packet: {
                            "job_url": "https://www.linkedin.com/jobs/view/3819954068/"
                                }

      2) the api have end point of get_jd, so via routing from project(jobscrapping) to apk(datascrappingapk)'s 
        view function,
    
      3) in this view function we will fetch the data from the req and then we will varify it with the
         serializers.py, if validated than okay or else we will raise exception by raise_exception=True

      4) we have made the custom serializer where we have added validated functionality and regex matching with the url
         ex:  def validate(self, data):
                job_url = data["job_url"]
                linkedin_jobs_regex = (
                    r"^(https?:[\\/]{0,2}|https?://)?(www\.)?linkedin\.com/jobs/view/\d+/$"
                )

                # Adding my custom logic here...
                if (isinstance(job_url, str)) and (re.match(linkedin_jobs_regex, job_url)):
                    print("url is validated..")
        
      5) so if url is validated then we will fatch the data, from the another module that is made mannually named 
         "datascrapper.py" (currently it is function-based), this module have functions one of them will be called from the views.py, and in return it will get the output result.

      6) data scrapping flow
        -> login headless mode as of now,
        -> for username and password, i have created one env variables
        -> from that env i will load my credentials to the os to the script,
        -> now after login we will search for the url(url is already varified from the ser.), 
        -> now we will get on the job page where we wait for certain seconds and scroll down to the bottom in order to 
           load the whole html containt
        -> now we have made some functions in datascrapping.py module(same module), from where we will gonna have the
           job_related overview or skill related etc etc....
        -> at the end we will have the final output in dict that will be returned to views.py to user who have hitted the api.

        
     