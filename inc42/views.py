from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .utils import * 

class Company(APIView):

    def get(self, request):
        """
        API to get company details by profile id
        """
        profile_id = request.GET.get('profile_id')
        response = get_company_data(profile_id)
        return Response(data=response, status=status.HTTP_200_OK)

    def post(self, request):
        """
        API to create a new company
        """
        params = request.data
        response = create_company(params, request)
        return Response(data=response, status=status.HTTP_200_OK)


class UploadCompanyLogo(APIView):

 def post(self, request):
        """
        API to upload company logo
        """
        params = request.data
        response = add_logo(params, request)
        return Response(data=response, status=status.HTTP_200_OK)
