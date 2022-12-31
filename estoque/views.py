from django.shortcuts import render
from .models import Categoria,Produto,Imagem
from django.http import HttpResponse
from PIL import Image, ImageDraw
from datetime import date
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from rolepermissions.decorators import has_permission_decorator
from .forms import ProdutoForm


@has_permission_decorator('cadastra_produto')
def add_produto(request):
    if request.method == "GET":
        categorias = Categoria.objects.all()
        produtos = Produto.objects.all()
        return render(request, 'add_produto.html', {'categorias': categorias, 'produtos' : produtos})
    elif request.method == "POST":
        nome = request.POST.get('nome')
        categoria = request.POST.get('categoria')
        quantidade = request.POST.get('quantidade')
        preco_compra = request.POST.get('preco_compra')
        preco_venda = request.POST.get('preco_venda')


        produto = Produto(nome=nome,categoria_id=categoria,quantidade=quantidade, preco_compra=preco_compra,preco_venda=preco_venda)

        produto.save()
        
        for f in request.FILES.getlist('imagens'):
            name= f'{date.today()}--{produto.id}.jpg'

            img= Image.open(f)
            img = img.convert('RGB')
            img=img.resize((300,300))
            draw = ImageDraw.Draw(img)
            draw.text((20,280),f"LOBBY {date.today()}", (255,255,255))
            output= BytesIO()
            img.save(output, format="JPEG", quality=100)
            output.seek(0)
            img_final = InMemoryUploadedFile(
                output, "imageField",name,"image/jpeg",sys.getsizeof(output),None
            )




            img_dj= Imagem(imagem = img_final , produto=produto)
            img_dj.save()
            messages.add_message(request, messages.SUCCESS, 'Produto adicionado com sucesso')
        return redirect(reverse('add_produto'))
def produto(request, slug):
    if request.method =="GET":
        produto = Produto.objects.get(slug=slug)
        data = produto.__dict__
        data['categoria']= produto.categoria.id
        form = ProdutoForm(initial=data)
        return render(request, 'produto.html', {'form': form})
