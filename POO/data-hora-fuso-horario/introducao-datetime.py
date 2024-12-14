# O módulo 'datetime' em Python é usado para lidar com datas e horas.
# Ele possui várias classes úteis como date, time e timedelta.

import datetime  # importando o módulo datetime

# Objetos Aware ou Naive
## Um objeto é aware se ele possui fuso horário. Por outro lado, um objeto é naive se ele não possui fuso horário.

# Objetos Date
## Uma data ingênua(naive) idealizada, presumindo que o atual calendário Gregoriano sempre foi, e sempre estará em vigor. Atributos: year, month e day.
## Objetos do tipo date sempre serão naive, isto é, não possuem a opção de usar fuso horário
## Exemplo de código usando date:
print("EXEMPLO DO USO DE DATE")
data = datetime.date(2024, 11, 7) # usando a classe date do módulo datetime
print(f"Data: {data}") # 2024-11-07
## Métodos da classe Date:
### classmethod date.today()
#### Retorna a data local atual.
print(f"Data atual: {datetime.date.today()}")
## Métodos de instância:
### date.replace(year=self.year, month=self.month, day=self.day)
#### Retorna uma data com o mesmo valor, exceto por aqueles parâmetros que receberam novos valores, por quaisquer argumentos nomeados especificados.
#### Exemplo de uso:
print("EXEMPLO DO USO DE REPLACE()")
d1 = datetime.date(2022, 12, 31)
d1.replace(day=20)
print(f"Data após uso do replace(): {d1}")
### date.weekday()
#### Retorna o dia da semana como um inteiro, onde Segunda é 0 e Domingo é 6.
print("EXEMPLO DO USO DE WEEKDAY()")
d2 = datetime.date(2022, 12, 31)
print(f"Dia da semana: {d2.weekday()}")
### date.isoweekday()
#### Retorna o dia da semana como um inteiro, onde Segunda é 1 e Domingo é 7.
print("EXEMPLO DO USO DE ISOWEEKDAY()")
d3 = datetime.date(2023, 12, 31)
print(f"Dia da semana: {d3.isoweekday()}")
### date.ctime()
#### Retorna uma string representando a data, exemplo:
print("EXEMPLO DO USO DE CTIME()")
print(f"Data com ctime(): {datetime.date(2023, 12, 31).ctime()}")
### date.strftime(format)
#### Retorna uma string representando a data, controlado por uma string explícita de formatação. 
#### Códigos de formatação referenciando horas, minutos ou segundos irão ver valores 0.
#### Mais informações em: https://docs.python.org/pt-br/3/library/datetime.html#strftime-strptime-behavior
print("EXEMPLO DO USO DE STRFTIME()")
d4 = datetime.datetime.today()
d5 = d4.strftime("%A, %d %B %Y") # mais opções de formatação no link acima
d6 = d4.strftime("%A, %d %B %Y, %I:%M:%S%p")
print(f"Data com uso de strftime(): {d5}")
print(f"Data e hora com uso de strftime(): {d6}")

# Objetos Time
## Um horário ideal, independente de qualquer dia em particular, presumindo que todos os dias tenham exatamente 24*60*60 segundos.
## Atributos: hour, minute, second, microsecond e tzinfo.
## Um objeto do tipo time pode ser naive ou aware.
## O objeto time t é aware, se os seguintes itens são verdadeiros:
### 1. t.tzinfo não é None
### 2. t.tzinfo.utcoffset(None) não retorna None.
## Caso contrário, t é naive.
## Exemplo de código usando time:
print("EXEMPLO DO USO DE TIME")
hora = datetime.time(15, 8, 20) # Isso é uma hora naive, pois não possui fuso horário 
print(f"Hora: {hora}")

# Objetos Datetime
## Uma combinação de uma data e uma hora. Atributos: year, month, day, hour, minute, second, microsecond e tzinfo.
## O objeto datetime d é consciente se ambos os seguintes itens forem verdadeiros:
### 1. d.tzinfo não é None;
### 2. d.tzinfo.utcoffset(d) não retorna None;
## Caso contrário, d é naive.
## Exemplo de código usando Datetime:
print("EXEMPLO DO USO DE DATETIME")
dataHora = datetime.datetime(2024, 11, 7, 15, 8, 20)
print(f"Data e hora: {dataHora}")

# Objetos Timedelta
## O objeto timedelta representa uma duração, a diferença entre duas instâncias datetime ou date.
## A distinção entre consciente(aware) e ingênuo(naive) não se aplica a objetos timedelta.
## class datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0).
### Todos os argumentos são opcionais e o padrão é 0. 
### Os argumentos podem ser números inteiros ou ponto flutuantes, e podem ser positivos ou negativos.
## Exemplo de uso da classe timedelta:
print("EXEMPLO DO USO DE TIMEDELTA")
dateTimeBrasilia = datetime.datetime(2024, 11, 7, 15, 28, 37) # Exemplo de datetime com fuso horário de Brasília
dateTimeSydney = dateTimeBrasilia + datetime.timedelta(0, 0, 0, 0, 0, 13) # Convertendo horário de Brasília para de Syney (13 horas de diferença)
print(f"Data e hora de Sydney: {dateTimeSydney}")

## Exemplo de uso timedelta e total_seconds():
ano = datetime.timedelta(days=365) # 365 dias em um ano
print(f"Total de segundos no ano: {ano.total_seconds()} segundos") # usando a função total_seconds() para retornar quantos segundos tem no ano

## Exemplo de uso de aritmética com timedelta:
year = datetime.timedelta(days=365)
ten_years = 10 * year # retorna dez anos no formato datetime.timedelta(days=3650)
print(f"timedelta 10 anos: {ten_years}")
print(f"Quantidade de dias em 10 anos: {ten_years.days} dias") # retorna quantos dias tem em 10 anos
nine_years = ten_years - year
print(f"timedelta 9 anos: {nine_years}")
print(f"Quantidade de dias em 9 anos: {nine_years.days} dias")
