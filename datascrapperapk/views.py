from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .serializers import MySerializer
import traceback
from .datascrapper import job_scrapper
import json
import time


@api_view(["POST"])
def job_description(req):
    try:
        data = req.data
        ser = MySerializer(data=data)
        ser.is_valid(raise_exception=True)

        final_dict = job_scrapper(data["job_url"])

        if len(final_dict["job-title"]) <= 0:
            return Response(
                {
                    "error": True,
                    "msg": "no job exists or captcha validation",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(final_dict, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": True, "msg": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )
