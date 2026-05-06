# cadastro\views.py

from django.shortcuts import get_object_or_404, redirect, render
from cadastro.forms import PessoaForm, TelefoneFormSet, ContatoForm
from cadastro.models import Pessoa
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required  # ← NOVO
from django.contrib.auth.forms import UserCreationForm                    # ← NOVO
from django.contrib.auth import login                                     # ← NOVO
from django.contrib import messages


def index(request):
    pessoas = Pessoa.objects.order_by('nome')
    total = Pessoa.objects.count()
    context = {
        'pessoas': pessoas,
        'total': total,
    }
    return render(request, 'cadastro/index.html', context)


def contato(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contato enviado com sucesso!')
            return redirect('contato')
    else:
        form = ContatoForm()
    return render(request, 'cadastro/contato.html', {'form': form})


@staff_member_required  # ← TROCADO
def adicionar(request):
    if request.method == 'POST':
        form = PessoaForm(request.POST)
        formset = TelefoneFormSet(request.POST, instance=Pessoa())

        if form.is_valid() and formset.is_valid():
            pessoa = form.save()
            formset.instance = pessoa
            formset.save()
            messages.success(request, 'Pessoa adicionada com sucesso!')
            return redirect('index')
    else:
        form = PessoaForm()
        formset = TelefoneFormSet(instance=Pessoa())

    return render(request, 'cadastro/adicionar.html', {
        'form': form,
        'formset': formset,
    })


def detalhe(request, id):
    pessoa = get_object_or_404(Pessoa, id=id)
    return render(request, 'cadastro/detalhe.html', {'pessoa': pessoa})


@staff_member_required  # ← TROCADO
def editar(request, id):
    pessoa = get_object_or_404(Pessoa, id=id)

    if request.method == 'POST':
        form = PessoaForm(request.POST, instance=pessoa)
        formset = TelefoneFormSet(request.POST, instance=pessoa)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, f'{pessoa.nome} atualizada com sucesso!')
            return redirect('detalhe', id=id)
    else:
        form = PessoaForm(instance=pessoa)
        formset = TelefoneFormSet(instance=pessoa)

    return render(request, 'cadastro/editar.html', {
        'form': form,
        'formset': formset,
        'pessoa': pessoa,
    })


@staff_member_required  # ← TROCADO
def deletar(request, id):
    pessoa = get_object_or_404(Pessoa, id=id)
    if request.method == 'POST':
        pessoa.delete()
        messages.success(request, 'Pessoa apagada com sucesso!')
        return redirect('index')
    return render(request, 'cadastro/deletar.html', {'pessoa': pessoa})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def perfil(request):
    return render(request, 'cadastro/perfil.html')