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
            print('A categoria que deseja remover não existe')
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
                    
        estoque = DaoEstoque.ler()
        estoque = list(map(lambda x: Estoque(Produtos(x.produto.nome, x.produto.preco, "Sem categoria"), x.quantidade)
                           if(x.produto.categoria == categoriaRemover) else (x), estoque))
        with open('estoque.txt', 'w') as arq:
            for i in estoque:
                arq.writelines(i.produto.nome + "|" + i.produto.preco + "|" + i.produto.categoria + "|" + str(i.quantidade))
                arq.writelines("\n")

    def alterarCategoria(self, categoriaAlterada, novaCategoria):
        x = DaoCategoria.ler()

        cat = list(filter(lambda y: y.categoria == categoriaAlterada, x))

        if len(cat) > 0:
            cat1 = list(filter(lambda y: y.categoria == novaCategoria, x))
            if len(cat1) == 0:
                x = list(map(lambda y: Categoria(novaCategoria) if (y.categoria == categoriaAlterada) else y, x))
                print('A alteração foi efetuada com sucesso')
                estoque = DaoEstoque.ler()
                estoque = list(map(lambda x: Estoque(Produtos(x.produto.nome, x.produto.preco, novaCategoria), x.quantidade)
                                   if(x.produto.categoria == categoriaAlterada) else (x), estoque))
                with open('estoque.txt', 'w') as arq:
                    for i in estoque:
                        arq.writelines(i.produto.nome + "|" + i.produto.preco + "|" + i.produto.categoria + "|" + str(i.quantidade))
                        arq.writelines("\n")
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

from datetime import datetime

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
            if not existe:
                if i.produto.nome == nomeProduto:
                    existe = True
                    if i.quantidade >= quantidadeVendida:
                        quantidade = True
                        i.quantidade = int(i.quantidade) - int(quantidadeVendida)

                        vendido = Venda(Produtos(i.produto.nome, i.produto.preco, i.produto.categoria), vendedor, comprador, quantidadeVendida)
                        valorCompra = int(quantidadeVendida) * int(i.produto.preco)
                        
                        DaoVenda.salvar(vendido)
            temp.append([Produtos(i.produto.nome, i.produto.preco, i.produto.categoria), i.quantidade])
        
        arq = open('estoque.txt', 'w')
        arq.write("")
        arq.close()

        for i in temp:
            with open('estoque.txt', 'a') as arq:
                arq.writelines(i[0].nome + "|" + i[0].preco + "|" + i[0].categoria + "|" + str(i[1]))
                arq.writelines('\n')
                    
        if not existe:
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
            nome = i.itensVendido.nome
            quantidade = i.quantidadeVendida
            tamanho = list(filter(lambda x: x['produto'] == nome, produtos))
            if len(tamanho) > 0:
                produtos = list(map(lambda x: {'produto': nome, 'quantidade': int(x['quantidade']) + int(quantidade)}
                                    if (x['produto'] == nome) else x, produtos))
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

    def parse_date(self, date_str):
        for fmt in ('%d/%m/%Y', '%d-%m-%Y'):
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"Formato de data não suportado: {date_str}")

    def mostrarVenda(self, dataInicio, dataTermino):
        vendas = DaoVenda.ler()
        dataInicio1 = self.parse_date(dataInicio)
        dataTermino1 = self.parse_date(dataTermino)
        
        vendasSelecionadas = list(filter(lambda x: self.parse_date(x.data) >= dataInicio1 and self.parse_date(x.data) <= dataTermino1, vendas))

        cont = 1
        total = 0
        for i in vendasSelecionadas:
            print(f"=========Venda [{cont}]======")
            print(f"Nome: {i.itensVendido.nome}\n"
                  f"Categoria: {i.itensVendido.categoria}\n"
                  f"Data: {i.data}\n"
                  f"Quantidade: {i.quantidadeVendida}\n"
                  f"Cliente: {i.comprador}\n"
                  f"Vendedor: {i.vendedor}\n")
            total += int(i.itensVendido.preco) * int(i.quantidadeVendida)
            cont += 1
        print(f"Total vendido: {total}")


class controllerFornecedor:
    def cadastrarFornecedor(self, nome, cnpj, telefone, categoria):
        x = DaoFornecedor.ler()
        listaCnpj = list(filter(lambda x: x.cnpj == cnpj, x))
        listaTelefone = list(filter(lambda x: x.cnpj == cnpj, x))
        if len(listaCnpj) > 0:
            print("O cnpj já existe")
        elif len(listaTelefone) > 0:
            print("O telefone já existe")
        else:
            if len(cnpj) == 14 and len(telefone) <= 11 and len(telefone) == 10:
                DaoFornecedor.salvar(Fornecedor(nome, cnpj, telefone, categoria))
            else:
                print("Digite um cnpj ou telefone válido")    
                
        def alterarFornecedor(self, nomeAlterar, novoNome, novoCnpj, novoTelefone, novoCategoria):
            x = DaoFornecedor.ler()
            
            est = list(filter(lambda x: x.nome == nomeAlterar, x))
            if len(est) > 0:
                est = list(filter(lambda x: x.cnpj == novoCnpj, x))
                if len(est) == 0:
                    x = list(map(lambda x: Fornecedor(novoNome, novoCnpj, novoTelefone, novoCategoria) if x.nome == nomeAlterar else x, x))
                else:
                    print("Cnpj já existe")
            else:
                print("O Fornecedor que você deseja alterar não existe")
            with open('fornecedores.txt', 'w') as arq:
                for i in x:
                    arq.writelines(i.nome + "|" + i.cnpj + "|" + i.telefone + "|" + str(i.categoria))
                    arq.writelines('\n')
                    print("Fornecedor alterado com sucesso")
                    
        def removerFornecedor(self, nome):
            x = DaoFornecedor.ler()
            
            est = list(filter(lambda x: x.nome == nome, x))
            if len(est) > 0:
                for i in tange(len(x)):
                    if x[i].nome == nome:
                        del x[i]
                        break
            else:
                 print("O Fornecedor que deseja remover não existe")
                 return None
            with open('fornecedores.txt', 'w') as arq:
                for i in x:
                    arq.writelines(i.nome + "|" + i.cnpj + "|" + i.telefone + "|" + str(i.categoria))
                    arq.writelines('\n')
                    print("O Fornecedor foi removido com sucesso")
                    
        def mostrarFornecedor(self):
            fornecedores = DaoFornecedor.ler()
            if len(fornecedores) == 0:
                    print("Lista de fornecedores vazia")
                    
            for i in fornecedores:
                print("=======Fornecedores========")
                print(f"Categoria fornecida: {i.categoria}\n"
                      f"Nome: {i.nome}\n"
                      f"Telefone: {i.telefone}\n"
                      f"Cnpj: {i.cnpj}")
                
class ControllerCliente:
     def cadastrarCliente(self, nome, telefone, cpf, email, endereço):
         x = DaoPessoa.ler()

         listaCpf = list(filter(lambda x: x.cpf == cpf, x))
         if len(listaCpf) > 0:
             print(" Cpf já existente")
         else:
             if len(cpf) == 11 and len(telefone) >= 10 and len(telefone) <=11:
                 DaoPessoa.salvar(Pessoa(nome, telefone, cpf, email, endereco))
                 print(" Cliente cadastrado com sucesso")
             else:
                  print(" Digite um cpf ou telefone válido")
     def alterarCliente(self, nomeAlterar, novoNome, novoTelefone, novoCpf, novoEmail, novoEndereco):
         x = DaoPessoa.ler()

         est = list(filter(lambda x: x.nome == nomeAlterar, x))
         if len(est) > 0:
             x = list(map(lambda x: Pessoa(novoNome, novoTelefone, novoCpf, novoEmail, novoEndereço) if (x.nome == nomeAlterar) else (x), x))
         else:
             print(" O cliente que deseja alterar não existe")
         with open('cliente.txt', 'w') as arq:
             for i in x:
                 arq.writelines(i.nome + "|" + i.telefone + "|" + i.cpf + "|" + i.email + "|" + i.endereço)
                 arq.writelines('\n')
                 print(" O cliente alterado com sucesso")
def removerCliente(self, nome):
    x =DaoPessoa.ler()
    
    est = list(filter(lambda x: x.nome == nome, x))
    if len(est) > 0:
        for i in range(len(x)):
            if x[i].nome == nome:
                del x[i]
                break
    else:
        print("O cliente que deseja remover não existe")
        return None
    with open('clientes.txt', 'w') as arq:
        for i in x:
            arq.writelines(i.nome + "|" + i.telefone + "|" + i.cpf + "|" + i.email + "|" + i.endereco)
            arq.writelines('\n')
            print("Cliente removido com sucesso")
            
def mostrarCliente(self):
    clientes = DaoPessoa.ler()
    
    if len(clientes) == 0:
        print("Lista de clientes vazia")
        
        for i in clientes:
            print("========Cliente=========")
            print(f"Nome: {i.nome}\n"
                  f"Telefone: {i.telefone}\n"
                  f"Endereco: {i.endereco}\n"
                  f"Email:{i.email}\n"
                  f"Cpf:{i.cpf}\n")
            
class ControllerFuncionario:
    def cadastrarFuncionario(self, clt, nome, telefone, cpf, email, endereco):
        x = DaoFuncionario.ler()
        listaCpf = list(filter(lambda x: x.cpf == cpf, x))
        listaClt = list(filter(lambda x: x.clt == clt, x))
        if len(listaCpf) > 0:
            print(" CPF já existente")
        elif len(listaClt) > 0:
            print(" Já existe funcionário com esta clt")
        else:
            if len(cpf) == 11 and len(telefone) >= 10 and len(telefone) <= 11:
                DaoFuncionario.salvar(Funcionario(clt, nome, telefone, cpf, email, endereco))
                print(" Funcionário cadastrado com sucesso")
            else:
                print(" Digite um cpf ou telefone válido")
    def alterarFuncionario(self, nomeAlterar, novoClt, novoNome, novoTelefone, novoCpf, novoEmail, novoEndereco):
        x = DaoFuncionario.ler()
        
        est = list(filter (lambda x: x.nome == nomeAlterar, x))
        if len(est) > 0:
            x = list(map(lambda x: Funcionario(novoClt, novoNome, novoTelefone, novoCpf, novoEmail, novoEndereco) if x.nome == nomeAlterar else x, x))

        else:
            print(" O Funcionario que deseja alterar não existe")
            
            with open('funcionarios.txt', 'w') as arq:
                for i in x:
                    arq.writelines(i.clt + "|" + i.nome + "|" + i.telefone + "|" + i.cpf + "|" + i.email + "|" + i.endereco)
                    arq.writelines('\n')

                    print('Funcionário alterado com sucesso')
                
def removerFuncionario(self, nome):
    x = DaoFuncionario.ler()

    est = list(filter(lambda x: x.nome == nome, x))
    if len(est) > 0:
        for i in range(len(x)):
            if x[i].nome == nome:
                del x[i]
                break
        with open('funcionarios.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.nome + "|" + i.telefone + "|" + i.cpf + "|" + i.email + "|" + i.endereco)
                arq.writelines('\n')
        print("Funcionário removido com sucesso")
    else:
        print("O funcionário que deseja remover não existe")


            
def mostrarFuncionarios(self):
        funcionario = DaoFuncionario.ler()
        
        if len(funcionario) == 0:
            print("Lista de funcionários vazia")
            
        for i in funcionario:
            print("========Funcionario=========")
            print(f"Nome: {i.nome}\n"
                  f"Telefone: {i.telefone}\n"
                  f"Email: {i.email}\n"
                  f"Endereço: {i.endereco}\n"
                  f"CPF: {i.cpf}\n"
                  f"Clt: {i.clt}\n")
            
                
        


#a = ControllerCategoria()
#a.alterarCategoria("Verduras", "Frios")
#a.removerCategoria("Legumes")
#a = ControllerVenda()
#a.mostrarVenda("09/04/2024", "10/04/2024")

#a.relatorioProdutos()
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
