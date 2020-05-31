from django.shortcuts import render, redirect
from .models import Post
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from coments.models import Comment
from django.contrib.auth import get_user


def post_index(request):
    # Pega todos os posts e retorna eles paginados.
    posts = Post.objects.all()
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts/posts_index.html', {'posts': page_obj})


def post_details(request, post_id):
    # Abre da página de detalhe do post especificado, exibindo numeros de comentarios do mesmo.
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        # Se o usuário tentar enviar um comentário sem estar logado, é redirecionado para a página de login.
        if not request.user.is_authenticated:
            messages.error(request, 'Para comentar você precisa estar logado.')
            return redirect('user_login')
        # Criando o comentário
        user_comment = request.POST['coment']
        author_comment = get_user(request)
        Comment.objects.create(comment_content=user_comment, comment_author=author_comment, comment_post=post)
        messages.success(request, 'Seu comentário foi enviado com sucesso.')
        return redirect('post_details', post_id)
    try:
        # Pega todos os comentarios vinculados ao post e retorna como contexto para ser apresentado no html
        comments = Comment.objects.filter(comment_post=post_id)
        return render(request, 'posts/posts_detail.html', {'post': post, 'comments': comments})
    except:
        pass
    return render(request, 'posts/posts_detail.html', {'post': post})


def posts_filter(request, search):
    # Filtra se veio python ou django dos links da navbar, e retorna os posts relacionados ao assunto.
    posts = Post.objects.filter(Q(post_name__icontains=search) | Q(post_introduction__icontains=search))
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts/posts_index.html', {'posts': page_obj})

def posts_search(request):
    # Recebe o que veio da caixa "Pesquisar", e retorna os posts relacionados ao assunto caso ele exista, se não pagina com msg de erro.
    search = request.GET.get('search')
    posts = Post.objects.filter(Q(post_name__icontains=search) | Q(post_introduction__icontains=search) | Q(post_content__icontains=search))
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts/posts_index.html', {'posts': page_obj})


