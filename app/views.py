from typing import Any, Dict, Optional
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, Group
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from .models import Cliente, Produto, Pedido
#from braces.views import GroupRequiredMixin
from django.views.generic.edit import UpdateView
from django.utils.text import slugify
from django import forms
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db import transaction
from .models import Pedido, Produto
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout



# Import statements organized and deduplicated

# Rest of the code...


# Create your views here.


def home(request):
    return render(request, 'home.html')

def comprar(request):
    return render(request, 'comprar.html')

#CADASTRO DO USUARIO
def create(request):
    return render(request, 'create.html')

            
#INSERÇÃO DOS DADOS DE USUARIO NO BANCO
from django.contrib.auth.models import Group

def store(request):
    data = {}
    if not all([request.POST['user'], request.POST['email'], request.POST['password'], request.POST['endereco'], request.POST['telefone'], request.POST['nome_completo']]):
        data['msg'] = 'Por favor, preencha todos os campos obrigatórios!'
        data['class'] = 'alert-danger'
        return HttpResponse("Por favor, preencha todos os campos obrigatórios!")
    elif(request.POST['password'] != request.POST['password-conf']):
        data['msg'] = 'Senha e confirmação de senhas estão diferentes!'
        data['class'] = 'alert-danger'
        return HttpResponse("Erro: senhas diferentes!")
    else:
        # Verifica se o e-mail já está cadastrado
        existing_users = User.objects.filter(email=request.POST['email'])
        if existing_users.exists():
            data['msg'] = 'Já existe um usuário com este endereço de e-mail'
            data['class'] = 'alert-danger'
            return HttpResponse("Já existe um usuário com este endereço de e-mail")

        # Verifica se o telefone já está cadastrado
        existing_clientes = Cliente.objects.filter(telefone=request.POST['telefone'])
        if existing_clientes.exists():
            data['msg'] = 'Já existe um usuário com este número de telefone'
            data['class'] = 'alert-danger'
            return HttpResponse("Já existe um usuário com este número de telefone")

        try:
            new_user = User.objects.create_user(request.POST['user'], request.POST['email'], request.POST['password'])
            new_cliente = Cliente.objects.create(
                nome_completo=request.POST['nome_completo'],
                endereco=request.POST['endereco'],
                telefone=request.POST['telefone'],
                usuario=new_user
            )
            # Adiciona o usuário ao grupo Cliente
            grupo_cliente = Group.objects.get(name='Cliente')
            new_user.groups.add(grupo_cliente)

            data['msg'] = 'Usuário cadastrado com sucesso'
            data['class'] = 'alert-success'
        except IntegrityError:
            data['msg'] = 'Já existe um usuário com este nome de usuário ou telefone'
            data['class'] = 'alert-danger'
            return HttpResponse("Já existe um usuário com este nome de usuário ou telefone")

    return render(request, 'home.html', data)
def verificar_username(request):
    username = request.GET.get('username')
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})

def verificar_email(request):
    email = request.GET.get('email')
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({'exists': exists})

#FORMULARIO DE LOGIN DO USUARIO
def painel(request):
    return render(request, 'painel.html')

#processar o login
def loginuser(request):
    data = {}
    user = authenticate(username=request.POST['user'], password=request.POST['password'])
    if user is not None:
        login(request, user)
        return redirect('/dashboard/')
    else:
        data['msg'] = 'Usuario ou senha invalidos!'
        data['class'] = 'alert-danger'
        return render(request, 'painel.html', data)

#CADASTRO PRODUTO
def create_produto(request):
    return render(request, 'create_produto.html')
                  
def store_produto(request):
    data = {}
    if not all([request.POST['nome_produto'], request.POST['marca'], request.POST['tipo'], request.POST['preco'], request.POST['produto_id'], request.POST['estoque']]):
        data['msg'] = 'Por favor, preencha todos os campos obrigatórios!'
        data['class'] = 'alert-danger'
        return JsonResponse(data, status=400)
    else:
        produto_id = request.POST.get('produto_id')
        slug = slugify(request.POST['nome_produto'])
        if produto_id and Produto.objects.filter(produto_id=produto_id).exists():
            data['msg'] = f"O produto com o ID {produto_id} já está cadastrado. Por favor, insira um ID válido."
            data['class'] = 'alert-danger'
            return JsonResponse(data, status=400)
        elif Produto.objects.filter(slug=slug).exists():
            data['msg'] = f"O produto com o slug {slug} já está cadastrado. Por favor, insira um nome de produto diferente."
            data['class'] = 'alert-danger'
            return JsonResponse(data, status=400)
        else:
            new_produto = Produto.objects.create(
                nome_produto=request.POST['nome_produto'],
                marca=request.POST['marca'],
                tipo=request.POST['tipo'],
                preco=request.POST['preco'],
                produto_id=request.POST['produto_id'],
                estoque=request.POST['estoque'],
                slug=slug
            )
            if produto_id:
                new_produto.produto_id = produto_id
            new_produto.save() # salvando o produto no banco de dados
            data['msg'] = 'Produto cadastrado com sucesso!'
            data['class'] = 'alert-success'
            return JsonResponse(data)

def verificar_produto_id(request):
    produto_id = request.GET.get('produto_id')
    exists = Produto.objects.filter(produto_id=produto_id).exists()
    return JsonResponse({'exists': exists})

#PAGINA INICIAL DO DASHBOARD
def dashboard(request):
    produtos = Produto.objects.all()
    return render(request, 'dashboard/home.html', {'produtos': produtos})


class editar_produto(UpdateView):
    model = Produto
    fields = ['nome_produto', 'marca', 'tipo', 'preco', 'produto_id', 'estoque']#'imagem_produto'
    template_name = 'editar_produto.html'
    success_url = '/dashboard/'

    def form_valid(self, form):
        produto = form.save(commit=False)
        produto.save()
        return super().form_valid(form)
    

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username']

class CustomUsernameWidget(forms.TextInput):
    def format_value(self, value):
        return value

class PerfilUpdateForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        widget=CustomUsernameWidget(attrs={'placeholder': 'Username'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].error_messages = {'required': ''}

    class Meta:
        model = Cliente
        fields = ['nome_completo', 'endereco', 'telefone']

class PerfilUpdate(UpdateView):
    template_name = "editar_perfil.html"
    model = Cliente
    form_class = PerfilUpdateForm
    success_url = '/dashboard/'

    def get_object(self, queryset=None):
        self.object = get_object_or_404(Cliente, usuario=self.request.user)
        return self.object

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields.update(UserForm(instance=self.request.user).fields)
        return form

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial['username'] = user.username
        initial['email'] = user.email
        return initial

    def form_valid(self, form):
        user_form = UserForm(self.request.POST, instance=self.request.user)
        if user_form.is_valid():
            user_form.save()
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Meus dados"
        context["botao"] = "atualizar"
        return context

def selecionar_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'selecionar_produtos.html', {'produtos': produtos})


def detalhes_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id, cliente=request.user.cliente)
    context = {'pedido': pedido}
    return render(request, 'detalhes_pedido.html', context)


@transaction.atomic
def criar_pedido(request):
    if request.method == 'POST':
        # Retrieve the selected product IDs from the form
        produtos_ids = request.POST.getlist('produtos')

        # Calculate the total value
        valor_total = 0
        for produto_id in produtos_ids:
            produto = Produto.objects.get(id=produto_id)
            valor_total += produto.preco

            # Deduct 1 from the stock of each selected product
            produto.estoque -= 1
            produto.save()

        # Retrieve the associated Cliente instance for the current user
        if not request.user.is_authenticated:
            raise LoginRequired('Para criar um pedido, você precisa estar logado')
        cliente = request.user.cliente

        # Create the new pedido entry
        pedido = Pedido(cliente=cliente, valor_total=valor_total)
        pedido.save()

        # Assign the selected products to the pedido
        pedido.produtos.set(produtos_ids)

        # Perform any additional operations or redirects as needed
        return redirect('detalhes_pedido', pedido_id=pedido.id)

    else:
        # Retrieve the available products for display in the template
        produtos = Produto.objects.all()
        return render(request, 'criar_pedido.html', {'produtos': produtos})







@login_required
def visualizar_pedido(request, pk):
 pedido = get_object_or_404(Pedido, pk=pk)
 return render(request, 'visualizar_pedido.html', {'pedido': pedido})




def pedido_confirmado(request, pedido_pk, total):
    pedido = Pedido.objects.get(pk=pedido_pk)
    return render(request, 'pedido_confirmado.html', {'pedido': pedido, 'total': total})

from django.contrib.auth.decorators import login_required

@login_required
def meus_pedidos(request):
 cliente = request.user.cliente
 pedidos = Pedido.objects.filter(cliente=cliente)
 return render(request, 'meus_pedidos.html', {'pedidos': pedidos})





def logout(request):
    """Desloga o usuário atual."""
    request.session.flush()
    # Não chame a função logout recursivamente.

    return redirect('/')


from django.shortcuts import render, redirect
from .forms import ContatoForm

def contato(request):
  form = ContatoForm(request.POST or None)
  if form.is_valid():
    contato = form.save()
    return render(request, 'contato_sucesso.html', {'contato': contato})
  return render(request, 'contato.html', {'form': form})




from django.shortcuts import render
from django.http import HttpResponse
from .models import Contato

def tickets(request):
    contatos = Contato.objects.all()
    return render(request, 'tickets.html', {'contatos': contatos})


from django.shortcuts import get_object_or_404

def marcar_como_arquivado(request, contato_id):
    contato = get_object_or_404(Contato, pk=contato_id)
    contato.arquivado = True
    contato.save()
    return redirect('/tickets/')  # Substitua 'nome_da_url' pelo nome da URL que você quer redirecionar após a atualização

def tickets_arquivados(request):
    contatos_arquivados = Contato.objects.filter(arquivado=True)
    return render(request, 'tickets_arquivados.html', {'contatos': contatos_arquivados})

def avaliacao(request):
    return render(request, 'avaliacao.html')

from django.shortcuts import render, redirect
from .models import Comentario
from .forms import ComentarioForm

from django.shortcuts import render
from datetime import datetime

def comentarios(request):
    comentarios = Comentario.objects.all()
    
    # Convertendo a data para o formato desejado
    for comentario in comentarios:
        comentario.data_formatada = comentario.data.strftime('%d/%m/%Y %H:%M')

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.save()
            return redirect('comentarios')  # Redireciona após enviar o comentário
    else:
        form = ComentarioForm()

    return render(request, 'comentarios.html', {'form': form, 'comentarios': comentarios})
    
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout, authenticate
from django.contrib import messages

@method_decorator(login_required, name='dispatch')
class DeleteAccountView(View):
    template_name = 'delete_account.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # Verifique se a senha fornecida está correta
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)

        if user is not None:
            # Senha correta, proceda com a exclusão
            user.delete()
            logout(request)
            messages.success(request, 'Sua conta foi excluída com sucesso. Agradecemos por utilizar nossos serviços.')
            return redirect('exlucsao_concluida.html')
        else:
            # Senha incorreta, exiba uma mensagem de erro
            messages.error(request, 'Senha incorreta. Tente novamente.')
            return redirect('delete_account')


from django.shortcuts import render

class exlucsao_concluida(View):
    template_name = 'exlucsao_concluida.html'

    def get(self, request):
        return render(request, self.template_name)

