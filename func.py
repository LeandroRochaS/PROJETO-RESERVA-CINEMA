from time import sleep

clientes = {}
reservas = {}
cadeiras_canceladas = {}

class Cinema():
    def __init__(self):
        self.matriz = [] 

    def atualiza_matriz(self):
        global reservas
        for reserva in reservas.values(): #EX: reserva = [[1,2],[1,3],...]
            for cadeira in reserva:    #Ex: cadeira = [1,2]
                print(cadeira)
                self.matriz[int(cadeira[0])-1][int(cadeira[1])-1] = True 
    
    def formatar_dados(self,reserva):
        #Formata de  '[1,2]'(string)  par   [1,2], sendo 1 e 2 inteiros positivos
        return [int(reserva[1]),int(reserva[4])]
        
    def ler_relatorio_reserva(self):
        global clientes, reservas     
        with open('Relatorio_reservas.txt','r') as file:  
            
            aux = []  #lista auxiliar
            auxFile = file.readlines() #auxiliar que recebe TODAS as linhas do arquivo
            
            for linha in auxFile:
                aux = [] #limpa o auxiliar
                if  linha == '\n': #final do arquivo
                    break
                
                nome = linha.split('|')[0].split(':')[1]  #pega o nome escrito na linha
                cpf = linha.split('|')[1].split(':')[1]   #pega o cpf escrito na linha
    
                #Caso o cpf já possua alguma reserva
                if cpf in reservas:
                    for reserva in reservas[cpf]:
                        #Aux recebe reservas antigas
                        aux.append(reserva)  
                        #receber as reservas novas
                        aux.append(self.formatar_dados(linha.split('|')[2].split(':')[1].split('\n')[0]))
                        #Atualiza o dict reservas
                        reservas.update({cpf:aux})
                        
                #Caso base, inicial
                else:
                    aux.append(self.formatar_dados(linha.split('|')[2].split(':')[1].split('\n')[0]))
                    reservas[cpf]=aux
                #Cpf recebe um nome
                clientes[cpf] = nome 
        self.atualiza_matriz()         
        file.close()

    def gerar_relatorio_reserva(self, cpf):
        if cpf not in clientes:
            print(f'O {cpf} Não esta cadastrado.')
            return
        if cpf not in reservas:
            print(f'Nome:{clientes[cpf]}\nReservas: Não tem registro de reserva para esse cliente.')
            return
        with open('Relatorio_reservas.txt', 'a') as file:
            for cadeira in reservas[cpf]:
                file.write(f'O cliente de Nome:{clientes[cpf]}| CPF:{cpf}| Reservou a cadeira:{cadeira}\n')

    def gerar_relatorio_cancelamento_reserva(self, cpf):
        global cadeiras_canceladas
        with open('Relatorio_cancelamento_reservas.txt', 'a') as file:
            file.write(f'O cliente de Nome:{clientes[cpf]} e com o CPF:{cpf} cancelou a cadeira:{cadeiras_canceladas[cpf]}')
            file.write('\n')

    def gerar_relatorio_cadeirasLivres(self):
        cont = 0
        with open('Relatorio_cadeiraslivres.txt', 'a') as file:
            for i in self.matriz:
                for j in i:
                    if j == False:
                        cont += 1
            file.write(f'No total restaram {cont} cadeiras vazias.')
            file.write('\n')

    def criar_matriz(self):
        for i in range(8):
            linha = []
            for j in range(12):
                linha.append(False)
            self.matriz.append(linha)
        return self.matriz

    def imprimi_matriz(self):
        #Indices de coluna
        print("\n 1  2  3  4  5  6  7  8  9  10 11 12")
        for i in range(len(self.matriz)):
            for j in range(12):
                if not self.matriz[i][j]:
                    #Se False = o verde
                    print('\033[0;32m o \033[m', end="")
                else:
                    #Se True  = x vermelho
                    print('\033[0;31m x \033[m', end="")
            #Imprime os indices de linha
            print(' ' + str(i + 1) + ' ')
        print('\n')
        print('\033[0;32m o \033[m - Disponível\n', end="")
        print('\033[0;31m x \033[m - Reservado\n', end="")
        
        
    def consulta_reserva_cadeira(self, fila, cadeira):
        if self.matriz[cadeira - 1][fila - 1]:
            return True  # Ocupada
        else:
            return False  # Livre

    def reserva_cadeira(self, cpf: str, fila: int, cadeira: int):
        aux = []  # Lista Auxiliar
        pos = 0  # Contador auxiliar para armazenar as posições da lista auxiliar

        # verfica se o cpf já está cadastrado
        if cpf not in clientes:
            print('-> CPF não cadastrado.')
            return False

        # verificar se a cadeira que quer reservar ja está reservada!!
        if self.matriz[cadeira - 1][fila - 1] == True:
            print('-> Cadeira não disponível.')
            return False

        # Verifica se o dict reservas já possui registros com o cpf
        # Caso sim (true):
        if cpf in reservas:
            aux = []
            for reserva in reservas[cpf]:
                # Armazena uma por uma das reservas antigas do cliente
                aux.insert(pos, reserva) 
                pos += 1
            # Armazera a reserva nova do cliente junto às antigas
            aux.insert(pos, [cadeira, fila])
            # Atualiza o dict reservas com todas as novas reservas do cliente
            reservas.update({cpf: aux})

        # Caso nao (Caso inicial: false):
        else:
            # Faz uma inserção
            aux.append([cadeira, fila])
            reservas[cpf] = aux

        # Limpa a lista auxiliar
        aux = []
        # Atualiza a matriz, inserindo a reserva
        self.matriz[cadeira - 1][fila - 1] = True

        print('Reserva realizada com sucesso!\n')
        sleep(1)
        return True

    def cancelar_cadeira(self, cpf):
        global cadeiras_canceladas
        lista_cadeiras_canceladas =[]
        auxReservas = []  # Lista auxiliar
        opcaoDeRemocao: int = -1  # Armazena a posicao da lista de reservas que usuario deseja remover
        if cpf not in clientes:
            print(f'O {cpf} Não esta cadastrado.')
            return
        auxReservas = reservas[cpf]
        # Menu de pergunta para saber qual reserva o cliente deseja remover
        print('Qual reserva deseja remover?\n')
        for i in range(len(auxReservas)):
            print(str(i + 1) + ' - ' + str(auxReservas[i]))
        opcaoDeRemocao = int(input('>'))
        
        #EX:  auxReservas = [[1,2],[1,3],[1,4]]      
        #   Menu:
        #       1-[1,2]
        #       2-[1,3]
        #   OpcaoDeRemocao = 1 -> [1,2] -> [linha,coluna]
        #linha= 1
        #coluna= 2
        
        linha = auxReservas[opcaoDeRemocao - 1][0]
        coluna = auxReservas[opcaoDeRemocao - 1][1]
        
        #Caso o cpf ja possua alguma cadeira cancelada
        if cpf in cadeiras_canceladas:
            #auxCadeiras recebe todas as cadeiras canceladas anteriores
            auxCadeiras = cadeiras_canceladas[cpf]
            for i in range(len(cadeiras_canceladas[cpf])):
                #inserindo de um em um dentro de lista_cadeiras_canceladas
                lista_cadeiras_canceladas.insert(i,auxCadeiras[i])
                
            #Insere a nova cadeira cancelada na lista_cadeiras_canceladas    
            lista_cadeiras_canceladas.append([linha,coluna])
            #Atualiza o dict cadeiras_canceladas com todas as cadeiras canceladas
            cadeiras_canceladas.update({cpf:lista_cadeiras_canceladas})
        #Caso base:
        else:   
            lista_cadeiras_canceladas.append([linha,coluna])
            cadeiras_canceladas.update({cpf:lista_cadeiras_canceladas})
           
        # Atualiza a matriz, removendo a reserva
        self.matriz[linha - 1][coluna - 1] = False
        
        #Remove a reserva informada pelo menu
        #Menu:
        #       1-[1,2]
        #       2-[1,3]
        #   OpcaoDeRemocao = 1 -> [1,2] -> [linha,coluna]
        del (auxReservas[opcaoDeRemocao - 1])
        #Atualiza as reservas, removendo a reserva selecionada anteriormente
        reservas.update({cpf: auxReservas})
        #Gera o novo relatorio de reservas
        with open('Relatorio_reservas.txt', 'w+') as file:
            for cpf_reservas in reservas.keys():
                for cadeiras_reservas in reservas[cpf_reservas]:
                    file.write(f'O cliente de Nome:{clientes[cpf_reservas]}| CPF:{cpf_reservas}| Reservou a cadeira:{cadeiras_reservas}\n')
        print('Reserva removida com sucesso!\n')
        return


    def valida_cpf(self,cpf):
        novo_cpf = cpf[:-2]                 # Elimina os dois últimos digitos do CPF
        reverso = 10                        # Contador reverso
        total = 0

        # Loop do CPF
        for index in range(19):
            if index > 8:                   # Primeiro índice vai de 0 a 9,
                index -= 9                  # São os 9 primeiros digitos do CPF

            total += int(novo_cpf[index]) * reverso  # Valor total da multiplicação

            reverso -= 1                    # Decrementa o contador reverso
            if reverso < 2:
                reverso = 11
                d = 11 - (total % 11)

                if d > 9:                   # Se o digito for > que 9 o valor é 0
                    d = 0
                total = 0                   # Zera o total
                novo_cpf += str(d)          # Concatena o digito gerado no novo cpf

        # Evita sequencias. Ex.: 11111111111, 00000000000...
        sequencia = novo_cpf == str(novo_cpf[0]) * len(cpf)

        # Descobri que sequências avaliavam como verdadeiro, então também
        # adicionei essa checagem aqui
        if cpf == novo_cpf and not sequencia:
            return True
        else:
            return False
    
    def cadastrar_cliente(self, cpf, nome):
        global clientes
        #CPF que exista
        if self.valida_cpf(cpf):
            if cpf in clientes:
                print('Cliente já tem cadastro.')
                return
            clientes[cpf] = nome
            print('Cliente cadastrado com sucesso!')
            sleep(1)
        else: 
            print('Cpf Invalido!\n')
            return
        return clientes

    def consultar_cliente(self, cpf):
        global clientes, reservas
        print('***** Informações do cliente *****')
        if cpf not in clientes:
            print(f'O {cpf} Não esta cadastrado.')
            return
        if cpf not in reservas:
            print(f'Nome:{clientes[cpf]}\nReservas: Não tem registro de reserva para esse cliente.')
            return
        print(f'Nome:{clientes[cpf]}\nReservas:{reservas[cpf]}')
        return