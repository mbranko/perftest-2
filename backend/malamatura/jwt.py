from pitanja.models import Ucenik


def jwt_response_payload_handler(token, user=None, request=None):
    try:
        ucenik = Ucenik.objects.get(user_id__exact=user.id)
        user_data = {
            'id': ucenik.id,
            'email': ucenik.user.email,
            'firstName': ucenik.user.first_name,
            'lastName': ucenik.user.last_name,
            'token': token
        }
    except Ucenik.DoesNotExist:
        user_data = {
            'id': user.id,
            'token': token
        }
    return user_data
