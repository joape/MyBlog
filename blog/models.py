from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.
class PublishedManager(models.Manager): #un administrador personalizado que se utiliza para filtrar los objetos Post y devolver solo aquellos que tienen un estado de PUBLISHED. Esto permite obtener fácilmente solo los posts publicados sin tener que escribir la lógica de filtrado cada vez que se consulta el modelo Post.
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        )


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'    
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish') #un campo de texto que se utiliza para crear URLs amigables. El slug es una versión simplificada del título del post, que generalmente se convierte a minúsculas y se reemplazan los espacios por guiones.    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )#un campo de clave foránea que se utiliza para establecer una relación entre el modelo Post y el modelo de usuario de Django (AUTH_USER_MODEL). Esto permite asociar cada post con un autor específico. El argumento on_delete=models.CASCADE indica que si un usuario es eliminado, todos los posts asociados a ese usuario también serán eliminados. El argumento related_name='blog_posts' permite acceder a los posts de un autor utilizando la sintaxis author.blog_posts.
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now) #un campo de fecha y hora que se utiliza para almacenar la fecha y hora de publicación del post. El valor predeterminado se establece en la fecha y hora actual utilizando timezone.now, lo que significa que si no se proporciona un valor para este campo al crear un nuevo post, se asignará automáticamente la fecha y hora actual.
    created = models.DateTimeField(auto_now_add=True) #un campo de fecha y hora que se utiliza para almacenar la fecha y hora de creación del post. El valor se establece automáticamente en la fecha y hora actual cuando se crea un nuevo post, gracias a auto_now_add=True.
    updated = models.DateTimeField(auto_now=True) #un campo de fecha y hora que se utiliza para almacenar la fecha y hora de la última actualización del post. El valor se actualiza automáticamente cada vez que se guarda el post, gracias a auto_now=True.
    status = models.CharField(
        max_length=2, 
        choices=Status.choices, 
        default=Status.DRAFT
    ) #un campo de texto que se utiliza para almacenar el estado del post. El campo tiene un conjunto de opciones definidas por la clase interna Status, que utiliza TextChoices para definir las opciones disponibles (DRAFT y PUBLISHED). El valor predeterminado se establece en DRAFT, lo que significa que si no se proporciona un valor para este campo al crear un nuevo post, se asignará automáticamente el estado de borrador.
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.


    class Meta: #Esta clase se utiliza para definir metadatos adicionales para el modelo Post. En este caso, se especifica el orden predeterminado de los objetos Post cuando se consultan desde la base de datos.
        ordering = ('-publish',) #especifica el orden predeterminado de los objetos Post cuando se consultan desde la base de datos. En este caso, se ordenarán por la fecha de publicación en orden descendente (de más reciente a más antiguo), gracias al signo negativo antes de 'publish'.
        indexes = [
            models.Index(fields=['-publish']), #crea un índice en la base de datos para el campo 'publish' en orden descendente. Esto puede mejorar el rendimiento de las consultas que ordenan por este campo.
        ]

    def __str__(self): #este es el método que se ejecuta cuando se llama a str() sobre una instancia de Post, y devuelve el título del post como representación de texto del objeto.
        return self.title

    def get_absolute_url(self):
        #este método devuelve la URL absoluta del detalle del post. Utiliza la función reverse de Django para generar la URL basada en el nombre de la vista 'blog:post_detail' y el ID del post como argumento.
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

class FavouritePost(models.Model):
    pk = models.CompositePrimaryKey("user", "post") #un campo de clave primaria compuesta que se utiliza para garantizar que cada combinación de usuario y post sea única en la tabla FavouritePost. Esto significa que un usuario no puede marcar el mismo post como favorito más de una vez.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        'blog.Post',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True) 
