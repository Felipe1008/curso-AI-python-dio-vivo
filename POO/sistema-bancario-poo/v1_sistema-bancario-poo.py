from abc import ABC, abstractmethod
from datetime import datetime
import textwrap
from colorama import Fore, Back, Style


#posteriormente posso deixar Cliente abstrata e separar em PF e PJ
class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    @property
    def contas(self):
        return self._contas
    
    @property
    def endereco(self):
        return self._endereco

    def adicionar_conta(self, conta):
        self.contas.append(conta)
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def cpf(self):
        return self._cpf

    @property
    def nome(self):
        return self._nome

    @property
    def data_nascimento(self):
        return self._data_nascimento
    
class Conta:
    def __init__(self, numero, agencia, cliente):
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()
        self._saldo = 0

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero

    @property   
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)

    def sacar(self, valor):
        if valor < self._saldo and valor > 0:
            self._saldo -= valor
            print(Fore.GREEN + "≡≡≡ Saque efetuado com sucesso! ≡≡≡")
            return True
        else:
            print(Fore.RED + "@@@ Saldo insuficiente! @@@ ")
            return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(Fore.GREEN + "≡≡≡ Depósito efetuado com sucesso! ≡≡≡ ")
            return True
        else:
            print(Fore.RED + "@@@ Valor inválido! @@@")
            return False

class ContaCorrente(Conta):
    def __init__(self, numero, agencia, cliente, limite=500, limite_saques=3):
        super().__init__(numero, agencia, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._qtdade_saques = 0
        
    def contar_qtdade_saques(self):
        self._qtdade_saques = 0
        for transacao in self.historico.transacoes:
                if transacao['tipo'] == "Saque":
                    self._qtdade_saques += 1

    def sacar(self, valor):
        self.contar_qtdade_saques()

        if valor > self._limite:
            print(Fore.RED + "@@@ Operação inconcluída! Limite insuficiente. @@@")
            return False

        elif self._qtdade_saques >= self._limite_saques:
            print(Fore.RED + "@@@ Operação inconcluída! Quantidade máxima de saques atingida. @@@")
            return False

        return super().sacar(valor)
 
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao_info):
        self._transacoes.append(transacao_info)

    def exibir_historico(self):
        print(f"{Fore.YELLOW + 'Data':<30}{Fore.BLUE + 'Tipo':<20}{Fore.GREEN + 'Valor (R$)':>25}")
        print(Fore.WHITE + "-" * 60)

        if self.transacoes:
            for transacao in self._transacoes:
                valor = transacao['valor']
                print(f"{Fore.YELLOW + transacao['data']:<30}{Fore.BLUE + transacao['tipo']:<20}{Fore.GREEN + f'{valor:>20.2f}'}")
                print(Fore.WHITE + "-" * 60)
        else:
            print(Fore.WHITE + "Não há transações!")

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    def registrar(self, conta):
        if conta.depositar(self._valor):
            transacao_info = {
                "tipo": "Deposito",
                "valor": self._valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }

            conta.historico.adicionar_transacao(transacao_info)
        
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    def registrar(self, conta):
        if conta.sacar(self._valor):
            transacao_info = {
                "tipo": "Saque",
                "valor": self._valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
            
            conta.historico.adicionar_transacao(transacao_info)
            
class Banco:
    def __init__(self, endereco, nome):
        self._endereco = endereco
        self._nome = nome
        self._clientes = []
        self._contas = []

    @property
    def endereco(self):
        return self._endereco
    
    @property
    def nome(self):
        return self._nome

    @property
    def clientes(self):
        return self._clientes
    
    @property
    def contas(self):
        return self._contas

    def menu(self):
        menu = Fore.WHITE + """\n
        ========= MENU ==========
        [d]\t Depositar
        [s]\t Sacar
        [e]\t Extrato
        [nc]\t Nova Conta
        [lc]\t Listar Contas
        [nu]\t Novo Cliente
        [q]\t Sair
        """
        return input(textwrap.dedent(menu))
    
    def filtrar_clientes(self, cpf, clientes):
        clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
        return clientes_filtrados[0] if clientes_filtrados else None
    
    def recuperar_conta_cliente(self, cliente):
        if not cliente.contas:
            print(Fore.RED + "@@@ Cliente não possui conta! @@@")
            return None

        agencia_conta = input(Fore.WHITE + "Digite a agência: ")
        numero_conta = input(Fore.WHITE + "Digite o número da conta: ")
        for conta in cliente.contas:
            if conta.agencia == agencia_conta and conta.numero == numero_conta:
                return conta
        
        return None

    def depositar(self, clientes):
        cpf = input("Digite o CPF do cliente: ")
        cliente = self.filtrar_clientes(cpf, clientes)

        if not cliente:
            print(Fore.RED + "@@@ Cliente não encontrado!  Não foi possível realizar o depósito @@@")
            return

        valor = float(input(Fore.WHITE + "Informe o valor do depósito: "))
        transacao = Deposito(valor)

        conta = self.recuperar_conta_cliente(cliente)
        if not conta:
            print(Fore.RED + "@@@ Conta não encontrada! Não foi possível realizar o depósito @@@")
            return
            
        cliente.realizar_transacao(conta, transacao)

    def sacar(self, clientes):
        cpf = input("Digite o CPF do cliente: ")
        cliente = self.filtrar_clientes(cpf, clientes)

        if not cliente:
            print(Fore.RED + "@@@ Cliente não encontrado! Não foi possível realizar o saque @@@")
            return
        
        valor = float(input("Informe o valor do saque: "))
        transacao = Saque(valor)

        conta = self.recuperar_conta_cliente(cliente)
        if not conta:
            print(Fore.RED + "@@@ Conta não encontrada! Não foi possível realizar o saque @@@")
            return
        
        cliente.realizar_transacao(conta, transacao)
    
    def exibir_extrato(self, clientes):
        cpf = input("Digite o CPF do cliente: ")
        cliente = self.filtrar_clientes(cpf, clientes)

        if not cliente:
            print(Fore.RED + "@@@ Cliente não encontrado! @@@")
            return
        
        conta = self.recuperar_conta_cliente(cliente)

        if not conta:
            print(Fore.RED + "@@@ Cliente sem conta cadastrada! Não foi possível exibir o extrato @@@")
            return

        print(Fore.WHITE + f"\n{'='*25} EXTRATO {'='*25}")
        print(Fore.WHITE + f"Cliente: {cliente.nome}")
        print(Fore.WHITE + f"Agência: {conta.agencia} | Conta: {conta.numero}")
        print(Fore.WHITE + "="*60)

        conta.historico.exibir_historico()
        print(Fore.GREEN + f"{'Saldo atual:':<40}{conta.saldo:>20.2f}")
        print(Fore.WHITE + "="*60)
    
    def criar_cliente(self, clientes):
        tipo_cliente = int(input(Fore.WHITE + """
        [1] para PF
        [2] para Cliente genérico
        """))
        endereco = input(Fore.WHITE + "Digite o endereço: ")
        if tipo_cliente == 1:
            nome = input("Digite o Nome: ")
            cpf = input("Digite o CPF: ")
            data_nascimento = input("Digite a data de nascimento: ")
            cliente = PessoaFisica(endereco=endereco, cpf=cpf, nome=nome, data_nascimento=data_nascimento)
        elif tipo_cliente == 2: 
            cliente = Cliente(endereco=endereco)
        else:
            print(Fore.RED + "@@@ Escolha inválida! @@@")
            return

        clientes.append(cliente)

    def criar_conta(self, clientes):
        cpf = input(Fore.WHITE + "Digite o CPF do cliente: ")
        cliente = self.filtrar_clientes(cpf, clientes)
        if not cliente:
            print(Fore.RED + "@@@ Cliente não encontrado! Não foi possível criar a conta @@@")
            return
        tipo_conta = int(input(Fore.WHITE + """
        [1] Conta Corrente
        [2] Conta genérica
        """))
        numero = input(Fore.WHITE + "Digite o número da conta: ")
        agencia = input(Fore.WHITE + "Digite a agência: ")

        if tipo_conta == 1:
            conta = ContaCorrente(numero, agencia, cliente)
        elif tipo_conta == 2:
            conta = Conta(numero, agencia, cliente)
        else:
            print(Fore.RED + "@@@ Escolha inválida! @@@")
            return

        self.contas.append(conta)
        cliente.adicionar_conta(conta)
        print(Fore.GREEN + "≡≡≡ Conta criada com sucesso! ≡≡≡")
        
    def listar_contas(self, clientes):
        cpf = input("Digite o CPF do cliente: ")
        cliente = self.filtrar_clientes(cpf, clientes)

        if not cliente:
            print(Fore.RED + "@@@ Cliente não encontrado! @@@")
            return

        print(Fore.WHITE + "="*20)
        print(Fore.WHITE + f"Usuário: {cliente.nome}")
        print(Fore.WHITE + "====== CONTAS ======")
        for conta in cliente.contas:
            print(Fore.WHITE + f"Agência: {conta.agencia}")
            print(Fore.WHITE + f"Número: {conta.numero}")
            print(Fore.WHITE + "="*20)


def main():
    clientes = []

    banco = Banco("Rua WYZ, 347", "JPM")
    
    while True:
        opcao = banco.menu()
        if opcao == "d":
            banco.depositar(clientes)
        elif opcao == "s":
            banco.sacar(clientes)
        elif opcao == "e":
            banco.exibir_extrato(clientes)
        elif opcao == "nc":
            banco.criar_conta(clientes)
        elif opcao == "lc":
            banco.listar_contas(clientes)
        elif opcao == "nu":
            banco.criar_cliente(clientes)
        elif opcao == "q":
            print(Fore.LIGHTGREEN_EX + "Finalizando sessão...")
            break
        else:
            print(Fore.RED + "@@@ Opção Inválida! @@@")
    
    print(Fore.GREEN + "≡≡≡ Sessão finalizada! ≡≡≡")

main()


    





    

