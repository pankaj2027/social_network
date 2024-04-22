import requests
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication


class MyAuthenticationClass(TokenAuthentication):
    """
    Custom token-based authentication class.

    This class extends TokenAuthentication and adds additional logic for authentication
    based on the request path and user roles obtained from an external service.
    """

    def authenticate(self, request):
        """
        Authenticate the incoming request.

        This method checks if the request path starts with '/download-logs/'.
        If it does, it bypasses authentication. Otherwise, it verifies the token
        sent in the request headers and checks the user's business role.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - tuple: A tuple containing the authenticated user and token, or None if authentication fails.
        """
        if request.path.startswith("/download-logs/"):
            return None

        auth = request.headers.get("Authorization")
        if not auth:
            raise exceptions.AuthenticationFailed(
                {"status": 401, "message": "Unauthorised access.", "data": ""}
            )

        url = settings.USER_AUTHENTICATE_URL
        headers = {"Authorization": auth}
        response = requests.request("GET", url, headers=headers)

        if response.status_code != 200:
            raise exceptions.AuthenticationFailed(
                {"status": 401, "message": "Unauthorised access.", "data": ""}
            )
        result = response.json()
        business_role = result.get("data", {}).get("business_role")
        id = result.get("data", {}).get("id")
        username = result.get("data", {}).get("username")
        request.business_role = business_role
        request.username = username
        request.first_name = result.get("data", {}).get("firstname")
        request.last_name = result.get("data", {}).get("lastname")
        request.id = id
        business_role = "fdms_maker"
        #business_role = "fdms_enricher"
        #business_role = "fdms_approver"
        id = 1
        username = "Pankaj"
        request.business_role = business_role
        request.username = username
        request.first_name = "yy"
        request.last_name = "kkk"
        request.id = id
