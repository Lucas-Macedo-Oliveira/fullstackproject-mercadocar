from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from app.views import (
    contato, home, create, store, painel, loginuser, dashboard, login, create_produto,
    store_produto, PerfilUpdate, comprar, selecionar_produtos, criar_pedido,
    detalhes_pedido, pedido_confirmado, visualizar_pedido, editar_produto,
    verificar_username, verificar_email, verificar_produto_id, visualizar_pedido, meus_pedidos, logout, tickets, marcar_como_arquivado, tickets_arquivados, avaliacao, comentarios, ComentarioForm, DeleteAccountView, exlucsao_concluida
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('create/', create),
    path('store/', store),
    path('painel/', painel),
    path('loginuser/', loginuser),
    path('dashboard/', dashboard),
    path('store_produto/', store_produto),
    path('create_produto/', create_produto, name='create'),
    path('editar_produto/<slug:slug>/', editar_produto.as_view(), name='editar_produto'),
    path('editar_perfil/', PerfilUpdate.as_view(), name='editar_perfil'),
    path('verificar_username/', verificar_username, name='verificar_username'),
    path('verificar_email/', verificar_email, name='verificar_email'),
    path('api/verificar_produto_id/', verificar_produto_id, name='verificar_produto_id'),
    path('comprar/', comprar),
    path('selecionar-produtos/', selecionar_produtos, name='selecionar_produtos'),
    path('criar-pedido/', criar_pedido, name='criar_pedido'),
    path('detalhes-pedido/<int:pedido_id>/', detalhes_pedido, name='detalhes_pedido'),
    path('pedido/confirmado/<int:pedido_pk>/<str:total>/', pedido_confirmado, name='pedido_confirmado'),
    path('visualizar-pedido/<int:pk>/', visualizar_pedido, name='visualizar_pedido'),
    path('meus-pedidos/', meus_pedidos, name='meus_pedidos'),
    path('logout/', logout, name='logout'),
    path('contato/', contato, name='contato'),
    path('contato_sucesso/', contato, name='contato_sucesso'),
    path('tickets/', tickets, name='tickets'),
    path('marcar_como_arquivado/<int:contato_id>/', marcar_como_arquivado, name='marcar_como_arquivado'),
    path('tickets_arquivados/', tickets_arquivados, name='tickets_arquivados'),
    path('avaliacao/', avaliacao, name='avaliacao'),
    path('comentarios/', comentarios, name='comentarios'),
    path('delete_account/', DeleteAccountView.as_view(), name='delete_account'),
    path('exlucsao_concluida.html/', exlucsao_concluida.as_view(), name='exlucsao_concluida.html'),

    



]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 