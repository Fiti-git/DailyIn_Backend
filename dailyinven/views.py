from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

# Login endpoint using JWT
class CustomTokenObtainPairView(TokenObtainPairView):
    # You can customize the token response here if needed
    pass

# Optional: For user logout (You can implement JWT blacklisting)
@api_view(['POST'])
def logout_view(request):
    try:
        # To logout, you can delete the user's token or blacklist it (for JWT)
        token = request.data.get('token')
        refresh_token = RefreshToken(token)
        refresh_token.blacklist()  # This will blacklist the refresh token
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
