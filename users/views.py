from django.shortcuts import render, redirect
from django.contrib import messages
from .utils import validating_new_user
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


def user_index(request):
    return render(request, 'users/user_register.html')


def user_register(request):
    # Recebe todos os dados da request como post
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        # Função que verifica os dados para criar a conta, caso tudo esteja válido retorna True, se não retorna uma msg de info.
        msg_info = validating_new_user(first_name, last_name, username, password1, password2, email)
        if msg_info == True:
            # Se tudo tiver válido, cria a conta, loga o usuário e redireciona para a página principal dos posts.
            create_user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, password=password1, email=email)
            create_user.save()
            messages.success(request, 'Usuário cadastrado com sucesso')
            user = authenticate(request, username=username, password=password1)
            if user is not None:
                login(request, user)
                return redirect('post_index')
        # Se nao, insere a msg de error para informar o usuario o que está inválido
        messages.warning(request, msg_info)
        return redirect('user_register')
    return redirect('user_index')


def user_login(request):
    # Apenas loga o usuário pela pagina de login normal kkk
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('post_index')
        else:
            messages.error(request, 'Usuário ou senha incorreto.')
            return redirect('user_login')
    return render(request, 'users/user_login.html')


def user_logout(request):
    logout(request)
    return redirect('post_index')


def user_update(request, user_id):
    # View basicona só para alterar nome e sobrenome
    if request.method == 'POST':
        new_first_name = request.POST['new_first_name']
        new_last_name = request.POST['new_last_name']
        update = User.objects.get(pk=user_id)
        update.first_name = new_first_name
        update.last_name = new_last_name
        update.save()
        messages.info(request, 'Dados alterados com sucesso')
        return redirect('user_profile', user_id)
    return render(request, 'users/user_update.html')


def user_profile(request, user_id):
    return render(request, 'users/user_profile.html')


def user_delete(request, user_id):
    # Verifica se a senha confere com a do DB e deleta a conta do usuário
    if request.method == 'POST':
        user = User.objects.get(pk=user_id)
        password = request.POST.get('password')
        password_verification = check_password(password, user.password)
        if password_verification:
            user.delete()
            messages.info(request, 'Usuário deletado com sucesso')
            return redirect('post_index')
        messages.info(request, 'A senha informada está incorreta')
        return redirect('user_delete', user_id)
    return render(request, 'users/user_delete.html')


def user_update_email(request, user_id):
    # Verifica se o novo email enviado ja existe e altera o mesmo, se não retorna uma msg informando que ja existe
    if request.method == 'POST':
        new_email = request.POST.get('new_email')
        try:
            email_verification = User.objects.get(email=new_email)
            messages.info(request, 'Este e-mail ja está sendo usado.')
            return redirect('user_profile', user_id)
        except:
            user = User.objects.get(pk=user_id)
            user.email = new_email
            user.save()
            messages.info(request, 'E-mail alterado com sucesso.')
            return redirect('user_profile', user_id)
    return render(request, 'users/user_update_email.html')


def user_update_password(request, user_id):
    # Confere se a antiga senha é a do usuário, e se as 2 novas senhas informadas conferem, se sim, altera a senha.
    if request.method == 'POST':
        user = User.objects.get(pk=user_id)
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']
        password_verification = check_password(old_password, user.password)
        if password_verification:
            if confirm_new_password == new_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Senha alterada com sucesso')
                user = authenticate(request, username=user.username, password=new_password)
                if user is not None:
                    login(request, user)
                    return redirect('user_profile', user_id)
            messages.success(request, 'Senhas não coincidem')
            return redirect('user_update_password', user_id)
        messages.success(request, 'Sua senha antiga é inválida')
        return redirect('user_update_password', user_id)

    return render(request, 'users/user_update_password.html')
