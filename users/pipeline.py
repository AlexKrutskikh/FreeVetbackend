"""Pipeline for creating a user profile in the database"""


from .models import Profile


def save_profile(backend, user, response, *args, **kwargs):

    profile, created = Profile.objects.get_or_create(user=user)

    if backend.name == 'facebook':
        profile.auth_provider = 'Facebook'
        profile.name = response.get('first_name', '')
        profile.last_name = response.get('last_name', '')
        profile.email = response.get('email', '')
    elif backend.name == 'google-oauth2':
        profile.auth_provider = 'Google'
        profile.name = response.get('given_name', '')
        profile.last_name = response.get('family_name', '')
        profile.email = response.get('email', '')
    elif backend.name == 'apple':
        profile.auth_provider = 'Apple'
        profile.name = response.get('name', {}).get('firstName', '')
        profile.last_name = response.get('name', {}).get('lastName', '')
        profile.email = response.get('email', '')

    profile.last_login_time = user.last_login  # Время последнего входа
    profile.registration_time = user.date_joined  # Время регистрации

    profile.save()



    if created:

        kwargs['request'].session['redirect_url'] = f'https://free-vet-app.vercel.app/verification/role?user_id={user.id}'
    else:
        kwargs['request'].session['redirect_url'] = f'https://free-vet-app.vercel.app/main?user_id={user.id}'