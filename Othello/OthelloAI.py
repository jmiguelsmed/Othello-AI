from jogos import *
from jogos import infinity
from othello import *
import copy

#Iolanda Leal 48069
#José Medeiros 58607


def states_to_evaluate_49 (estado, jogador):
    """
    Recebe um estado e um jogador.
    Devolve o estado do jogador e o estado do adversário.
    """
    
    clone = copy.deepcopy(estado)

    if jogador == clone.to_move:
        player_state = clone
        opponent_state = EstadoOthello(to_move = clone.other(), board = clone.board, last_move= clone.last_move)
    elif jogador == clone.other():
        player_state = EstadoOthello(to_move = clone.other(), board = clone.board, last_move= clone.last_move)
        opponent_state = clone
    
    return player_state, opponent_state


def player_moves_49(estado):
    """
    A função player_moves encontra as ações possíveis para 
    um jogador. Devolve uma lista com todos os possíveis movimentos
    do jogador para um especifico estado
    """


    player_moves = []

    clone = copy.deepcopy(estado)

    for x in range(1,9):
        for y in range(1,9):

            if clone.legal_move((x,y)):
                player_moves.append((x,y))
    
    return player_moves


tabela_49 = {(1,1) : 100, (1,2) : -25, (1,3) : 10, (1,4) : 5, (1,5) : 5, (1,6) : 10, (1,7) : -25, (1,8) : 100,
                        (2,1) : -25, (2,2) : -25, (2,3) : 1, (2,4) : 1, (2,5) : 1, (2,6) : 1, (2,7) : -25, (2,8) : -25,
                        (3,1) : 10, (3,2) : 1, (3,3) : 5, (3,4) : 2, (3,5) : 2, (3,6) : 5, (3,7) : 1, (3,8) : 10,
                        (4,1) : 5, (4,2) : 1, (4,3) : 2, (4,4) : 1, (4,5) : 1, (4,6) : 2, (4,7) : 1, (4,8) : 5,
                        (5,1) : 5, (5,2) : 1, (5,3) : 2, (5,4) : 1, (5,5) : 1, (5,6) : 2, (5,7) : 1, (5,8) : 5,
                        (6,1) : 10, (6,2) : 1, (6,3) : 5, (6,4) : 2, (6,5) : 2, (6,6) : 5, (6,7) : 1, (6,8) : 10,
                        (7,1) : -25, (7,2) : -25, (7,3) : 1, (7,4) : 1, (7,5) : 1, (7,6) : 1, (7,7) : -25, (7,8) : -25,
                        (8,1) : 100, (8,2) : -25, (8,3) : 10, (8,4) : 5, (8,5) : 5, (8,6) : 10, (8,7) : -25, (8,8) : 100}
    
def table_vals_49(estado,jogador,tabela) :
    clone = copy.deepcopy(estado)
    if clone.the_end():
        winner=clone.the_winner()
        if winner!=0:
            return infinity if winner==jogador else -infinity
        return 0
    soma = 0
    for p,j in clone.board.items() :
        if j == jogador:
            soma += tabela[p]
        else :
            soma -= tabela[p]
            
    return soma

table_valsfinal_49 = lambda estado, jogador: table_vals_49(estado,jogador,tabela_49)



def coin_numb_49(estado,jogador):
    """
    Compara o número de peças entre os dois jogadores.
    Em estágios mais iniciais do jogo, convém que o oponente tenha mais peças e em estágios finais, que o oponente tenha menos peças.
    """
    clone = copy.deepcopy(estado)

    if clone.the_end():
        winner=clone.the_winner()
        if winner!=0:
            return infinity if winner==jogador else -infinity
        return 0

    numero_pecas = clone.number_pieces(jogador)
    total = numero_pecas[0] + numero_pecas[1]

    K1 = 100
    K2 = 100

    #Estágios iniciais
    if total < 40:
        vals = K1 * (numero_pecas[1] - numero_pecas[0]) / total
    #Estágios finais
    else:
        vals = K2 *  (numero_pecas[0] - numero_pecas[1]) / total
    
    return vals
    

def mobility_49(estado,jogador):
    """
    Verifica quem é o jogador que tem mais acções possiveis para cada estado do tabuleiro.
    Se o número for positivo é vantajoso para o jogador e se for negativo é vantajoso para o oponente.
    """

    clone = copy.deepcopy(estado)

    player_state = states_to_evaluate_49(clone,jogador)[0]
    opponent_state = states_to_evaluate_49(clone,jogador)[1]

    player_actions = player_moves_49(player_state)
    opponent_actions = player_moves_49(opponent_state)

    player_mobility = len(player_actions)
    opponent_mobility = len(opponent_actions)
    
    if player_mobility + opponent_mobility != 0:
    
        return 100* (player_mobility-opponent_mobility)/(player_mobility+opponent_mobility)
    else:
        return 0


def pot_mobility_49(estado,jogador):

    clone = copy.deepcopy(estado)

    if clone.the_end():
        winner=clone.the_winner()
        if winner!=0:
            return infinity if winner==jogador else -infinity
        return 0

    keys = [key for key, val in clone.board.items() if val == jogador]

    all_directions=((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
    mob_opp = 0
    mob_ply = 0

    for key in clone.board.keys():
        for dir in all_directions:

            (x,y) = (key[0] + dir[0],key[1] + dir[1])
            if (x,y) not in clone.board.keys() and 1 <= x <= 8 and 1 <= y <=8:
                if key in keys:
                    mob_opp += 1
                else:
                    mob_ply += 1

    if mob_ply - mob_opp != 0:
        final = 100 * (mob_ply - mob_opp)/(mob_ply + mob_opp)
    else:
        final = 0

    return final


def corner_cap_49(estado,jogador):
    """
    Verifica quem é o jogador que capturou mais cantos para cada estado do tabuleiro.
    Se o valor for negativo, o adversário tem mais cantos capturados, o que não é vantajoso
    """
    
    clone = copy.deepcopy(estado)

    if clone.the_end():
        winner=clone.the_winner()
        if winner!=0:
            return infinity if winner==jogador else -infinity
        return 0

    corners = [(1,1),(1,8),(8,1),(8,8)]
    corner_w =0
    corner_l = 0


    for corner in corners:
        if corner in clone.board.keys():
            if clone.board[corner] == jogador:
                corner_w += 1
            else:
                corner_l += 1

    if corner_w + corner_l != 0:
        final = 100* (corner_w -corner_l)/ (corner_w + corner_l)
    else:
        final = 0
        
    return final


def start_game_49(estado,jogador):
    
    clone = copy.deepcopy(estado)
    numero_pecas = clone.number_pieces(jogador)
    total = numero_pecas[0] + numero_pecas[1]

    actual_pieces = []
    for key, player in clone.board:
        if player == jogador:
            actual_pieces.append(key)
    
    possible_moves = player_moves_49(estado)

    sum = 0
    #Estágios inicial
    if total < 6:
        for piece in actual_pieces:
            (x,y) = piece
            for move in possible_moves:
                (w,z) = move

                if w-x < 0 and z-y == 0:
                    sum -= 1
                
                elif w-x > 0 and z-y == 0:
                    sum -= 1
                
                else:
                    sum +=1
    return sum


def func_combina_com_pesos(estado,jogador,pesos,funcoes):
    """Função que devolve a combinação linear de várias funções de avaliação."""
    return sum([p*f(estado,jogador) for (p,f) in zip(pesos,funcoes)])

def func_49(estado,jogador):
    clone = copy.deepcopy(estado)
    numero_pecas = clone.number_pieces(jogador)
    total = numero_pecas[0] + numero_pecas[1]
    if total < 10:
        return func_combina_com_pesos(estado, jogador, [50, 100, 10, 50, 50, 100],
                                      [start_game_49, table_valsfinal_49, coin_numb_49, mobility_49, pot_mobility_49, corner_cap_49])
    elif total >= 10:
        return func_combina_com_pesos(estado, jogador, [0, 100, 20, 100, 50, 200],
                                      [start_game_49, table_valsfinal_49, coin_numb_49, mobility_49, pot_mobility_49, corner_cap_49])
    