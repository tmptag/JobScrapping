from rest_framework import serializers
import re


class MySerializer(serializers.Serializer):
    job_url = serializers.URLField()

    # can also use the validate_job_url, as django custom functionality
    # here you do not need to send whole data packet just send 2args as self, job_url
    # otherwise we can also modify inbuilt functionality of validate function
    #  here, you need to send the whole data packet in args as self, data
    def validate(self, data):
        job_url = data["job_url"]
        linkedin_jobs_regex = (
            r"^(https?:[\\/]{0,2}|https?://)?(www\.)?linkedin\.com/jobs/view/\d+/$"
        )

        # Adding my custom logic here...
        if (isinstance(job_url, str)) and (re.match(linkedin_jobs_regex, job_url)):
            print("url is validated..")
            pass
        else:
            print("......url not validated..")
            raise serializers.ValidationError("The URL must be a LinkedIn job URL.")

        return data
