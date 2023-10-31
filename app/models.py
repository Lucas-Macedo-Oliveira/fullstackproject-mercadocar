from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.forms import ModelForm


class Cliente(models.Model):
    nome_completo = models.CharField(max_length=50, null=True)
    endereco = models.CharField(max_length=50, null=True)
    telefone = models.CharField(max_length=11, null=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome_completo







class Produto(models.Model):
    nome_produto = models.CharField(max_length=255, null=True)
    marca = models.CharField(max_length=20, null=True)
    tipo = models.CharField(max_length=20, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(unique=True)
    estoque = models.DecimalField(max_digits=10, decimal_places=0)
    produto_id = models.CharField(max_length=255, null=True)

    def save(self, *args, **kwargs):
        if not self.id or not self.slug:
            self.slug = slugify(self.nome_produto)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('editar_produto', args=[str(self.slug)])

    def __str__(self):
        return self.nome_produto



class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data = models.DateField(auto_now_add=True)
    produtos = models.ManyToManyField(Produto)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total(self):
        total = sum(produto.preco for produto in self.produtos.all())
        return round(total, 2)  # Arredonda o valor total para 2 casas decimais
    
    def __str__(self):
        return f"Pedido #{self.pk} - {self.cliente.nome_completo}"

    def adicionar_produto(self, produto):
        self.produtos.add(produto)

    def remover_produto(self, produto):
        self.produtos.remove(produto)

class Contato(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    mensagem = models.TextField()

    arquivado = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

from django.db import models
from django.contrib.auth.models import User

class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mensagem = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentário de {self.usuario.username}'









