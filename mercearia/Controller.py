from Models import Categoria, Estoque, Produtos, Fornecedor, Pessoa, Funcionario, Venda
from DAO import DaoCategoria, DaoVenda, DaoEstoque, DaoFornecedor, DaoPessoa, DaoFuncionario
from datetime import datetime
import os

class ControllerCategoria:
    def cadastraCategoria(self, novaCategoria):
        existe = False
        x = DaoCategoria.ler()
        for i in x:
            if i.categoria == novaCategoria:
                existe = True
        if not existe:
            DaoCategoria.salvar(novaCategoria)
            print('Categoria cadastrada com sucesso')
        else:
            print('A categoria que deseja cadastrar já existe')

    def removerCategoria(self, categoriaRemover):
        x = DaoCategoria.ler()
        cat = list(filter(lambda y: y.categoria == categoriaRemover, x))

        if len(cat) <= 0:
            print('A categoria que deseja cadastrar não existe')
        else:
            for i in range(len(x)):
                if x[i].categoria == categoriaRemover:
                    del x[i]
                    break
            print('Categoria removida com sucesso')
            # TODO: COLOCAR SEM CATEGORIA NO ESTOQUE

            with open('categoria.txt', 'w') as arq:
                for i in x:
                    arq.writelines(i.categoria)
                    arq.writelines('\n')

    def alterarCategoria(self, categoriaAlterada, novaCategoria):
        x = DaoCategoria.ler()

        cat = list(filter(lambda y: y.categoria == categoriaAlterada, x))

        if len(cat) > 0:
            cat1 = list(filter(lambda y: y.categoria == novaCategoria, x))
            if len(cat1) == 0:
                x = list(map(lambda y: Categoria(novaCategoria) if (y.categoria == categoriaAlterada) else y, x))
                print('A alteração foi efetuada com sucesso')
                # TODO: ALTERAR A CATEGORIA TAMBEM NO ESTOQUE
            else:
                print('A categoria para qual deseja alterar já existe')
        else:
            print('A categoria para alterar não existe')

        with open('categoria.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.categoria)
                arq.writelines('\n')

    def mostrarCategoria(self):
        categorias = DaoCategoria.ler()
        if len(categorias) == 0:
            print('Categoria vazia')
        else:
            for i in categorias:
                print(f'Categoria: {i.categoria}')

class ControllerEstoque:
    def cadastrarProduto(self, nome, preco, categoria, quantidade):
        x = DaoEstoque.ler()
        y = DaoCategoria.ler()
        h = list(filter(lambda c: c.categoria == categoria, y))
        est = list(filter(lambda e: e.produto.nome == nome, x))

        if len(h) > 0:
            if len(est) == 0:
                produto = Produtos(nome, preco, categoria)
                DaoEstoque.salvar(produto, quantidade)
                print('Produto cadastrado com sucesso')
            else:
                print('Produto já existe em Estoque')
        else:
            print('Categoria inexistente')

    def removerProduto(self, nome):
        x = DaoEstoque.ler()
        est = list(filter(lambda x: x.produto.nome == nome, x))
        if len(est) > 0:
            for i in range(len(x)):
                if x[i].produto.nome == nome:  # Corrigido "prooduto" para "produto"
                    del x[i]
                    break
            print('O produto foi removido com sucesso')
        else:
            print('O produto que deseja remover não existe')

        with open('estoque.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.produto.nome + "|" + i.produto.preco + "|" +
                        i.produto.categoria + "|" + str(i.quantidade))
                arq.writelines('\n')

    def alterarProduto(self, nomeAlterar, novoNome, novoPreco, novaCategoria, novaQuantidade):
        x = DaoEstoque.ler()
        y = DaoCategoria.ler()
        h = list(filter(lambda c: c.categoria == novaCategoria, y))
        if len(h) > 0:
            est = list(filter(lambda e: e.produto.nome == nomeAlterar, x))
            if len(est) > 0:
                est = list(filter(lambda e: e.produto.nome == novoNome, x))
                if len(est) == 0:
                    x = list(map(lambda e: Estoque(Produtos(novoNome, novoPreco, novaCategoria), novaQuantidade) if (e.produto.nome == nomeAlterar) else e, x))
                    print('Produto alterado com sucesso')
                else:
                    print('Produto já cadastrado')
            else:
                print('Produto que deseja alterar não existe')

            with open('estoque.txt', 'w') as arq:
                for i in x:
                    arq.writelines(i.produto.nome + "|" + i.produto.preco + "|" +
                            i.produto.categoria + "|" + str(i.quantidade))
                    arq.writelines('\n')
        else:
             print('Categoria informada não existe')

    def mostrarEstoque(self):
        estoque = DaoEstoque.ler()
        if len(estoque) == 0:
            print('Estoque vazio')
        else:
             print("=======Produtos========")
             for i in estoque:
                print(f"Nome: {i.produto.nome}\n"
                      f"Preco: {i.produto.preco}\n"
                      f"Categoria: {i.produto.categoria}\n"
                      f"Quantidade: {i.quantidade}"
                      )
                
                print("-----------------")

class ControllerVenda:
    def cadastrarVenda(self, nomeProduto, vendedor, comprador, quantidadeVendida):
        try:
            x = DaoEstoque.ler()
        except FileNotFoundError:
            print("Arquivo 'estoque.txt' não encontrado. Criando o arquivo...")
            with open('estoque.txt', 'w') as arq:
                print("Arquivo 'estoque.txt' criado com sucesso.")
                return

        temp = []
        existe = False
        quantidade = False
        
        for i in x:
            if existe == False:
                if i.produto.nome == nomeProduto:
                    existe = True
                    if i.quantidade >=  quantidadeVendida:
                        quantidade = True
                        i.quantidade = int(i.quantidade) - int(quantidadeVendida)

                        vendido = Venda(Produtos(i.produto.nome, i.produto.preco, i.produto.categoria), vendedor, comprador, quantidadeVendida)
                        valorCompra = int(quantidadeVendida) * int(i.produto.preco)
                        
                        DaoVenda.salvar(vendido)
            temp.append([Produtos(i.produto.nome, i.produto.preco, i.produto.categoria), i.quantidade])
            
            arq = open('estoque.txt', 'w')
            arq.write("")
            
            for i in temp:
                with open('estoque.txt', 'a') as arq:
                    arq.writelines(i[0].nome + "|" + i[0].preco + "|" + i[0].categoria + "|" + str(i[1]))
                    arq.writelines('\n')
                    
            if existe == False:
                print('O produto não existe')
                return None
            elif not quantidade:
                print('A quantidade vendida não contém em estoque')
                return None
            else:
                print('Venda realizada com sucesso')
                return valorCompra
            
    def relatorioProdutos(self):
        vendas = DaoVenda.ler()
        produtos = []
        for i in vendas:
            nome = i.itensVendidoquantidade = i.quantidadeVendida
            quantidade = i.quantidadeVendida
            tamanho = list(filter(lambda x: x['produto'] == nome, produtos))
            if len(tamanho)>0:
                produtos = list(map(lambda x: {'produto': nome, 'quantidade': int(x['quantidade']) + int(quantidade)}
               if (x['produto'] == nome) else(x), produtos))
            else:
                produtos.append({'produto': nome, 'quantidade': int(quantidade)})
                
            ordenado = sorted(produtos, key=lambda k: k['quantidade'], reverse=True)
            
            print('Esses são os produtos mais vendidos')
            a = 1
            for i in ordenado:
                print(f"========Produto [{a}]=============")
                print(f"Produto: {i['produto']}\n"
                      f"Quantidade: {i['quantidade']}\n")
                a += 1

    
    
a = ControllerVenda()
a.relatorioProdutos()
#a.cadastrarVenda('abacaxi', 'Joao', 'Irene', 2)


#a = ControllerEstoque()
#a.cadastrarProduto('abacaxi', '5', 'Verduras', 20)
#a.mostrarEstoque()
#a.alterarProduto('maça', 'Pera', '5', 'Verduras', '20')

#a.cadastrarProduto('banana', '5', 'Verduras', '20')

#a = ControllerEstoque()
#a.removerProduto('banana')
#a.removerProduto('maca')

#a.cadastrarProduto('banana', '5', 'Verduras', '10')

#a = ControllerCategoria()
#a.mostrarCategoria()  # Correção: corrigido o chamado do método para mostrar as categorias
#a.alterarCategoria('Carnes', 'Verduras')
#a.alterarCategoria('Verduras', 'Carnes')
#a.removerCategoria('Frutas')









#a = ControllerCategoria()
#a.cadastraCategoria('frios')
