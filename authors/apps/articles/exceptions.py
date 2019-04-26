from rest_framework.exceptions import APIException


class NoResultsMatch(APIException):
    """
    Define error when search is not valid
    """

    status_code = 400
    default_detail = 'results matching search not found'
