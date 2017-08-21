import uuid
import os

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from .models import Company, Funding
from .serializer import CompanySerializer
from .exception import GenericException
from .constants import LOGO_DIRECTORY
from .validations import *


def create_company(params, request):
    """
    method to create a new company
    :param params: name, logo, description, website, founded_on
                   social_info: {'email':'a@b.com'} , markets: ['ecommerce'],
                   fundings: [{"amount": '100000', 'investor': 'ASD'}]
    :param request:
    :return:
    """
    try:
        validate_data(params)
        profile_id = str(uuid.uuid4())
        logo = upload_logo(profile_id, request)
        fundings = params.pop('fundings', [])
        company = Company.objects.create(name=params['name'], logo=logo, website=params.get('website', ''),
                                        markets=params.get('markets', []), description=params.get('description', ''),
                                        founded_on=params['founded_on'], social_info=params.get('social_info', {}),
                                        profile_id=profile_id)
        create_funds(company, fundings)
        return {"message": "Company created successfully with profile id: " + profile_id}
    except GenericException as e:
        raise GenericException(detail=e.detail)
    except Exception as e:
        raise GenericException(detail=repr(e))


def create_funds(company, funds):
    """
    method to create company funding records
    :param params:
    :param request:
    :return:
    """
    try:
        if not funds:
            return
        fundings = []
        for fund in funds:
            funding = Funding(company=company, amount=float(fund['amount']), date=fund.get('date', ''),
                              stage=fund.get('stage', '') ,investor=fund['investor'])
            fundings.append(funding)
        Funding.objects.bulk_create(fundings)
        return
    except Exception as e:
        raise GenericException(detail=repr(e))


def get_company_data(profile_id):
    """
    method to get company data
    :param params:
    :param request:
    :return:
    """
    try:
        company = Company.objects.get(profile_id=profile_id)
        company_data = CompanySerializer(company)
        return company_data.data
    except ObjectDoesNotExist:
        raise GenericException(detail="Company not found")
    except Exception as e:
        raise GenericException(detail=repr(e))


def add_logo(params, request):
    """
    method to add logo
    :param params: profile_id
    :param request:
    :return:
    """
    try:
        profile_id = params.get('profile_id', '')
        company = Company.objects.get(profile_id=profile_id)
        logo = upload_logo(profile_id, request)
        if not logo:
            raise GenericException(detail="Logo not found")
        company.logo = logo
        company.save()
        return {"message": "Logo uploaded"}
    except ObjectDoesNotExist:
        raise GenericException(detail="Company not found")
    except GenericException as e:
        raise GenericException(detail=e.detail)
    except Exception as e:
        raise GenericException(detail=repr(e))
    

def upload_logo(profile_id, request):
    """
    method to upload logo
    :param profile_id:
    :param request:
    :return:
    """
    try:
        logo = request.FILES.get('logo')
        if not logo:
            return ""
        file_name, file_extension = os.path.splitext(logo.name)
        destination_directory = settings.MEDIA_ROOT + LOGO_DIRECTORY
        destination_url = settings.MEDIA_URL + LOGO_DIRECTORY
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)
        file_path = destination_directory + profile_id + file_extension
        logo_url = settings.HOST_DOMAIN + "/" + destination_url + profile_id + file_extension

        with open(file_path, 'wb+') as destination:
            for chunk in logo.chunks():
                destination.write(chunk)
        return logo_url
    except TypeError as e:
        raise GenericException(detail=repr(e))
    except FileNotFoundError as e:
        raise GenericException(detail="File not found")
    except IOError as e:
        raise GenericException(detail=repr(e))
    except OSError as e:
        raise GenericException(detail=repr(e.filename))
    except KeyError as e:
        raise GenericException(detail=repr(e))
    except Exception as e:
        raise GenericException(detail=repr(e))
