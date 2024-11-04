# Utilizando o Sistema Bancário criado para o projeto de POO, implemente as seguintes funcionalidades:
# - Decorador de log
## Implemente um decorador que seja aplicado a todas as funções de transações. Esse decorador deve 
## registrar (printar) a data e a hora de cada transação, bem como o tipo de transação. 
# - Gerador de relatórios
## Crie um gerador que permita iterar sobre as transações de uma conta e retorne, uma a uma,
## as transações que foram realizadas. Esse gerador deve também ter uma forma de filtrar as
## transações baseado em seu tipo.
# - Iterador personalizado
## Implemente um iterador personalizado que permita iterar sobre todas as contas do banco,
## retornando informações básicas de cada conta (número, saldo atual, etc).

# Projeto Sistema Bancário
from abc import ABC, abstractmethod
from datetime import datetime
import textwrap
from colorama import Fore

# Classe base para Clientes, que pode ser estendida futuramente para Cliente Pessoa Física (PF) ou Pessoa Jurídica (PJ)
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

# Subclasse específica para Cliente do tipo Pessoa Física (CPF)
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

# Classe base para Conta, que pode ser estendida para tipos de contas específicos    
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
        if valor < self._saldo and valor > 0: # Verifica se há saldo suficiente
            self._saldo -= valor # Deduz o valor sacado do saldo
            print(Fore.GREEN + "≡≡≡ Saque efetuado com sucesso! ≡≡≡")
            return True
        else:
            print(Fore.RED + "@@@ Saldo insuficiente! @@@ ")
            return False
    
    def depositar(self, valor):
        if valor > 0: # Verifica se o valor do depósito é válido
            self._saldo += valor # Adiciona o valor depositado ao saldo
            print(Fore.GREEN + "≡≡≡ Depósito efetuado com sucesso! ≡≡≡ ")
            return True
        else:
            print(Fore.RED + "@@@ Valor inválido! @@@")
            return False

# Subclasse específica para Conta Corrente, com regras de saque e limite
class ContaCorrente(Conta):
    # Construtor seta valores padrões para limite e limite de saques
    def __init__(self, numero, agencia, cliente, limite=500, limite_saques=3):
        super().__init__(numero, agencia, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._qtdade_saques = 0

    # Conta quantos saques já foram feitos no dia para determinada conta corrente    
    def contar_qtdade_saques(self):
        self._qtdade_saques = 0
        for transacao in self.historico.transacoes: # Percorre as transações da conta
                if transacao['tipo'] == "Saque":
                    self._qtdade_saques += 1

    # Sobrescreve o método sacar para aplicar limites e restrições adicionais
    def sacar(self, valor):
        self.contar_qtdade_saques()

        if valor > self._limite:
            print(Fore.RED + "@@@ Operação inconcluída! Limite insuficiente. @@@")
            return False

        elif self._qtdade_saques >= self._limite_saques:
            print(Fore.RED + "@@@ Operação inconcluída! Quantidade máxima de saques atingida. @@@")
            return False

        return super().sacar(valor)  # Chama o método sacar da classe base

# Classe abstrata que define a estrutura de uma Transação
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

# Classe que armazena o histórico de transações de uma conta
class Historico:
    def __init__(self):
        self._transacoes = [] # Lista de transações realizadas na conta

    @property
    def transacoes(self):
        return self._transacoes

    # Adiciona uma transação ao histórico
    def adicionar_transacao(self, transacao_info):
        self._transacoes.append(transacao_info)

    # Exibe o histórico completo de transações
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
    
    # Implementação do gerador
    def gerador_gerar_relatorio(self, tipo=None):
        if not tipo:
            for transacao in self.transacoes:
                yield transacao
        else:
            for transacao in self.transacoes:
                if transacao['tipo'].lower() == tipo.lower():
                    yield transacao
        
# Subclasse de Transacao para depósitos
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    # Registra um depósito em uma conta
    def registrar(self, conta):
        if conta.depositar(self._valor):  # Se o depósito na conta for realizado
            transacao_info = {
                "tipo": "Deposito",
                "valor": self._valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }

            conta.historico.adicionar_transacao(transacao_info) # Adiciona a transação ao histórico

# Subclasse de Transacao para saques       
class Saque(Transacao):
    def __init__(self, valor): 
        self._valor = valor

    # Registra um saque em uma conta
    def registrar(self, conta):
        if conta.sacar(self._valor):  # Se o saque na conta for realizado
            transacao_info = {
                "tipo": "Saque",
                "valor": self._valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
            
            conta.historico.adicionar_transacao(transacao_info) # Adiciona a transação ao histórico

# Iterador das contas do banco
class ContasBanco: 
    def __init__(self, contas):
        self._contas = contas
        self._contador = 0
    
    def __iter__(self):
        self._contador = 0
        return self 
        
    def __next__(self):
        if self._contador < len(self._contas):
            conta = self._contas[self._contador]
            self._contador += 1
            return {
                "titular": conta.cliente.nome,
                "numero": conta.numero,
                "agencia": conta.agencia,
                "saldo": conta.saldo
            }

        raise StopIteration
       
# Classe Banco que gerencia clientes, contas e transações           
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

    # Exibe o menu principal e retorna a opção escolhida pelo usuário
    def menu(self):
        menu = Fore.WHITE + """\n
        ========= MENU ==========
        [d]\t Depositar
        [s]\t Sacar
        [e]\t Extrato
        [nc]\t Nova Conta
        [lc]\t Listar Contas
        [nu]\t Novo Cliente
        [gr]\t Gerar Relatório de Transações
        [it]\t Iterar Contas do Banco
        [q]\t Sair
        """
        return input(textwrap.dedent(menu))

    # Encontra um cliente pelo CPF
    def filtrar_clientes(self, cpf, clientes):
        clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
        return clientes_filtrados[0] if clientes_filtrados else None
    
    # Recupera uma conta específica de um cliente pela agência e número da conta
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
        
    # Decorador que registra informações sobre a transação realizada, 
    # incluindo o horário e o tipo da transação
    def decorador_log(transacao_func):
        def log_transacao(self, *args, **kwargs):
            horario_atual = datetime.now()
            horario_formatado = horario_atual.strftime("%Y-%m-%d %H:%M:%S")
            print(Fore.WHITE + "="*41)
            print(Fore.WHITE + f"Horário da transação: {horario_formatado}")
            print(Fore.WHITE + f"Tipo da transação: {transacao_func.__name__.capitalize()}")
            print(Fore.WHITE + "="*41)
            resultado = transacao_func(self, *args, **kwargs)
            print(Fore.GREEN + "Transação realizada com sucesso!" if resultado else Fore.RED + "Falha na transação!")
            return resultado

        return log_transacao
            
    # Realiza um depósito na conta de um cliente
    @decorador_log
    def depositar(self, clientes):
        cpf = input("Digite o CPF do cliente: ")
        cliente = self.filtrar_clientes(cpf, clientes)

        if not cliente:
            print(Fore.RED + "@@@ Cliente não encontrado!  Não foi possível realizar o depósito @@@")
            return False

        valor = float(input(Fore.WHITE + "Informe o valor do depósito: "))
        transacao = Deposito(valor)

        conta = self.recuperar_conta_cliente(cliente)
        if not conta:
            print(Fore.RED + "@@@ Conta não encontrada! Não foi possível realizar o depósito @@@")
            return False
            
        cliente.realizar_transacao(conta, transacao)
        return True

    # Realiza um saque na conta de um cliente
    @decorador_log
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
        return True

    # Implementação do gerador em prática no sistema do Banco
    def gerador_relatorio(self, clientes):
        cpf = input("Digite o CPF do cliente: ")
        cliente = self.filtrar_clientes(cpf, clientes)

        if not cliente:
            print(Fore.RED + "@@@ Cliente não encontrado! @@@")
            return

        conta = self.recuperar_conta_cliente(cliente)

        if not conta:
            print(Fore.RED + "@@@ Conta não encontrada! Não foi possível gerar o relatório @@@")
            return

        tipo_transacao = input(Fore.WHITE + "Digite o tipo de transação (Deposito/Saque) ou deixe em branco para todas: ").strip()
        print(Fore.WHITE + f"\n{'='*25} RELATÓRIO DE TRANSAÇÕES {'='*25}")
        print(Fore.WHITE + f"Cliente: {cliente.nome}")
        print(Fore.WHITE + f"Agência: {conta.agencia} | Conta: {conta.numero}")
        print(Fore.WHITE + "="*60)

        for transacao in conta.historico.gerador_gerar_relatorio(tipo=tipo_transacao):
            valor = transacao['valor']
            print(f"{Fore.YELLOW + transacao['data']:<30}{Fore.BLUE + transacao['tipo']:<20}{Fore.GREEN + f'{valor:>20.2f}'}")
            print(Fore.WHITE + "-" * 60)

        print(Fore.WHITE + "="*75)

    # Exibe o extrato de uma conta específica de um determinado cliente
    @decorador_log
    def exibir_extrato(self, clientes):
        cpf = input("Digite o CPF do cliente: ")
        cliente = self.filtrar_clientes(cpf, clientes) # Encontra o cliente pelo CPF

        # Se o cliente não for encontrado Retorna
        if not cliente:
            print(Fore.RED + "@@@ Cliente não encontrado! @@@")
            return False
        
        conta = self.recuperar_conta_cliente(cliente) # Encontra a conta do cliente

        # Se a conta não for encontrada Retorna
        if not conta:
            print(Fore.RED + "@@@ Cliente sem conta cadastrada! Não foi possível exibir o extrato @@@")
            return False

        print(Fore.WHITE + f"\n{'='*25} EXTRATO {'='*25}")
        print(Fore.WHITE + f"Cliente: {cliente.nome}")
        print(Fore.WHITE + f"Agência: {conta.agencia} | Conta: {conta.numero}")
        print(Fore.WHITE + "="*60)

        conta.historico.exibir_historico() # Exibe o histórico das transações da conta
        print(Fore.GREEN + f"{'Saldo atual:':<40}{conta.saldo:>20.2f}")
        print(Fore.WHITE + "="*60)
        return True

    # Cria e adiciona um novo cliente ao banco
    @decorador_log
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
            return False

        clientes.append(cliente)
        return True

    # Abre uma nova conta e a associa a um cliente
    @decorador_log
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

        self.contas.append(conta) # Adiciona a conta à lista de contas do banco
        cliente.adicionar_conta(conta) # Adiciona a conta ao cliente
        print(Fore.GREEN + "≡≡≡ Conta criada com sucesso! ≡≡≡")
        return True
        
    # Lista as contas de um determinado cliente
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
    
    def iterar_contas_banco(self):
        iterador = iter(ContasBanco(self.contas))
        print("================ Contas ================")
        for conta in iterador:
            print(f"Titular:\t{conta['titular']}")
            print(f"Número:\t\t{conta['numero']}")  
            print(f"Agência:\t{conta['agencia']}")
            print(f"Saldo:\t\t{conta['saldo']:.2f}")
            print("=" * 40)

# Função principal que inicia o sistema do banco
def main():
    clientes = []

    banco = Banco("Rua WYZ, 347", "JPM") # Criação de uma instância do banco
    
    # Opções de escolha do menu para o usuário
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
        elif opcao == "gr":
            banco.gerador_relatorio(clientes)
        elif opcao == "it":
            banco.iterar_contas_banco()
        elif opcao == "q":
            print(Fore.LIGHTGREEN_EX + "Finalizando sessão...")
            break
        else:
            print(Fore.RED + "@@@ Opção Inválida! @@@")
    
    print(Fore.GREEN + "≡≡≡ Sessão finalizada! ≡≡≡")

main() # Inicia o programa