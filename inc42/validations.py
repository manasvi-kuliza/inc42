import datetime

from .constants import FUNDING_STAGES
from .exception import GenericException

def validate_data(params):
    """
    method to validate company's data
    :param params:
    :param request:
    :return:
    """
    if not params.get('name'): raise GenericException(detail="Company name is mandatory field")
    if not params.get('founded_on'): raise GenericException(detail="Company found date is mandatory")
    validate_date(params['founded_on'])
    for funds in params.get('fundings', []):
        if not funds.get('amount'): raise GenericException(detail="Funding amount is mandatory")
        if not funds.get('investor'): raise GenericException(detail="Funding Investor is mandatory")
        if not funds.get('date'): raise GenericException(detail="Funding Date is mandatory")
        if not str(funds.get('amount')).isdigit(): raise GenericException(detail="Funding amount must be numerical")
        if funds.get('stage'):
            if funds['stage'].lower() not in FUNDING_STAGES: raise GenericException(detail="Funding Stage is incorrect")
        validate_date(funds.get('date'))

def validate_date(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise GenericException(detail="Incorrect date format, should be YYYY-MM-DD")
