import time
from func import *
from menu import menu
from time import sleep

'''Limpa tela do terminal'''
def limpartela():
    return print('\n' * 100)


'''Controla o programa baseado na escolha da entrada'''
# Parâmetros: cinema(Instância de Cinema), entrada(valor escolhido pelo usuário no Menu)
def controlador(cinema: Cinema, entrada):
    limpartela()
    match entrada:
        case 1:
            print('\n******* Cadastrar Cliente ******\n')
            nome = input('informe o Nome: ')
            cpf = str(input('informe o CPF(11): '))
            cinema.cadastrar_cliente(cpf, nome)

        case 2:
            print('\n******* Pesquisar Cliente ******\n')
            cpf = str(input('informe o CPF(11): '))
            cinema.consultar_cliente(cpf)

        case 3:
            flag = False
            print('\n\n******* Cadastrar Reserva ******\n')
            cpf = str(input('informe o CPF(11):'))
            # While que loopa as entradas de fila e cadeira e cria a reserva
            # enquanto o usuário continuar inserindo
            while (not flag):
                while True:
                    cinema.imprimi_matriz()
                    fila = int(input('Fila: '))
                    cadeira = int(input('Cadeira: '))
                    if 0<=fila<=8 and 0<=cadeira<=12: 
                        confirmaReserva = cinema.reserva_cadeira(cpf, fila, cadeira)
                        break
                    else:
                        print('\n** Valor inválido. Tente novamente! **\n')
                # While que loopa se o usuário quer inserir mais reservas
                # até que seja informado um valor válido (1 ou 2)
                # IF verifica se a reserva foi realizada ou não
                if confirmaReserva:
                    cinema.imprimi_matriz()
                    while (True):
                        print('\n->Deseja reservar mais cadeiras?\n1 - sim\n2 - não')
                        resposta = int(input('> '))
                        match resposta:
                            case 1:
                                break
                            case 2:
                                # Condição de parada do While mais EXTERNO
                                flag = True
                                # Break irá para o While mais INTERNO
                                break
                            case _:
                                print('** Valor inválido **')
                                sleep(1)
                else:
                    print('-> Não foi possível realizar a reserva!\n')
                    break

        case 4:
            print('\n******* Cancelar Reserva ******\n')
            cpf = input('CPF: ')
            cinema.cancelar_cadeira(cpf)
            
        case 5:
            print('\n******* Relatório De Reservas Do Cliente ******\n')
            cpf = input('CPF: ')
            cinema.gerar_relatorio_reserva(cpf)
            print('Relatório de Reserva Gerado com exito.')
            sleep(2)

        case 6:
            print('\n******* Relatório cadeiras livres ******\n')
            cinema.gerar_relatorio_cadeirasLivres()
            print('Relatório gerado com sucesso!')

        case 7:
            print('\n******* Relatório Cancelamento de cadeiras ******\n')
            cpf = input('CPF: ')
            cinema.gerar_relatorio_cancelamento_reserva(cpf)
            time.sleep(2)
            print('Relatório gerado com sucesso!')

        case 8:
            cinema.imprimi_matriz()

        case 9:
            limpartela()
            print('.salvando')
            sleep(1)
            limpartela()
            print('..salvando')
            sleep(1)
            limpartela()
            print('...salvando')
            sleep(1)
            limpartela()
            print('Salvo com exito!')
            sleep(1)
            print('  Saindo! \n')
    return


def main():
    
    # Cria uma instacia de Cinema
    cinema = Cinema()
    
    #Inicia a matriz
    cinema.criar_matriz()
    
    #Lê o arquivo e, caso tenha dados, atualiza as variáveis
    with open('Relatorio_reservas.txt', 'a') as file:
        pass
    cinema.ler_relatorio_reserva()

    # Armazena a opção do Menu. Condição inicial: 0(nulo)
    entrada = 0

    # Função responsável por "limpar" a tela do terminal
    limpartela()

    # While:
    # Condição de parada -> entrada == 9
    while entrada != 9:
        # Funcao responsável por imprimir o Menu para o usuário
        menu()
        entrada = int(input('>'))

        # Controlador do programa.
        # Responsável por controlar as funções baseado no valor da entrada
        controlador(cinema, entrada)


if __name__ == '__main__':
    main() 