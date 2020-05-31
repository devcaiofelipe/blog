from django.contrib.auth.models import User


def validating_new_user(first_name, last_name, username, password1, password2, email):
    if not first_name or not last_name or not username or not password1 or not password2 or not email:
        return 'Existem campos em branco'
    try:
        username_exist = User.objects.filter(username=username).exists()
        if username_exist:
            return 'Esse nome de usuário ja está sendo usado.'
    except:
        pass

    try:
        email_exist = User.objects.filter(email=email).exists()
        if email_exist:
            return 'Esse e-mail ja está sendo usado.'
    except:
        pass

    if len(username) < 6:
        return 'O nome de usuário precisa ter mais de 6 caracteres.'
    if len(password1) < 4:
        return 'A senha precisa ter mais de 4 caracteres.'
    if len(password1) > 8:
        return 'A senha precisa ter 8 caracteres ou menos.'
    if password1 != password2:
        return 'As senhas nao coincidem.'

    return True

