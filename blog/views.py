from django.core.paginator import Paginator, EmptyPage
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
#from django.http import Http404
from .models import Post
from .forms import EmailPostForm


# Create your views here.
class PostListView(ListView): #una vista basada en clases que hereda de ListView, lo que significa que se utiliza para mostrar una lista de objetos. En este caso, se muestra una lista de objetos Post.
        
        queryset = Post.published.all() #se especifica el conjunto de consultas (queryset) que se utilizará para obtener los objetos Post publicados. Esto se hace utilizando el administrador personalizado published que se definió en el modelo Post.
        context_object_name = 'posts' #se establece el nombre del contexto que se utilizará en la plantilla para acceder a la lista de objetos Post. En este caso, se establece como 'posts'.
        paginate_by = 3 #se especifica el número de objetos Post que se mostrarán por página. En este caso, se establece en 3, lo que significa que se mostrarán 3 posts por página.
        template_name = 'blog/post/list.html' #se especifica el nombre de la plantilla que se utilizará para renderizar la vista. En este caso, se establece como 'blog/post/list.html', lo que significa que se buscará una plantilla con ese nombre en la carpeta de plantillas del blog.


def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(posts, 3) #3 posts por página
    page_number = request.GET.get('page', 1) #obtener el número de página de la consulta GET, con un valor predeterminado de 1 si no se proporciona
    try:
        posts = paginator.get_page(page_number) #obtener los objetos Post correspondientes a la página solicitada utilizando el método get_page del paginador, que maneja automáticamente los casos en los que el número de página no es válido (por ejemplo, si es un número negativo o si excede el número total de páginas).
    except EmptyPage:
        posts = paginator.get_page(paginator.num_pages) #si la página solicitada no existe, se devuelve la última página válida del paginador.
    return render(request, 'blog/post/list.html', {'posts': posts})

# def post_detail(request, id):
#     try:
#         post = Post.published.get(id=id)
#     except Post.DoesNotExist:
#         raise Http404('No existe el post')
#     return render(request, 'blog/post/detail.html', {'post': post})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post, publish__year=year, publish__month=month, publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    
    sent=False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cd['name']} ({cd['email']}) "
                f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html',{'post': post,'form': form, 'sent': sent}
    )