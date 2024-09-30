from jogos import *

stateOthello = namedtuple('stateOthello', 'to_move, board, last_move')

class EstadoOthello(stateOthello):
    
    def next_move(self,move):
        """Execute move from self (state), flip all colors under bridge, returning next state"""
        board = self.board.copy()
        if move != 'None': # if there is a valid move to play
            board[move] = self.to_move
            all_directions=((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
            cells_to_flip=[]
            for direction in all_directions:
                makes_bridge = self.find_bridge(move, self.to_move, self.board, direction)
                if makes_bridge != None:
                    bridge,to_flip = makes_bridge
                    cells_to_flip += to_flip
            for f in cells_to_flip:
                board[f] = self.to_move
        else: # if there is no valid move for this player
            if self.last_move == 'None': # if last player did not play
                move = 'NoneNone' # this will cause the game to end
        return EstadoOthello(to_move=self.other(),board=board,last_move=move)
    
    def used_cells(self):
        """Returns all used cells"""
        return self.board.keys()
    
    def find_bridge(self,move,to_move,board,direction):
        """Find a square that forms a bridge with square 'move' for player 'to_move' in the given 'direction'.
           First pilar is square 'move'; Second pilar will be square 'bridge'; returns None if no such square exists."""
        bridge = (move[0]+direction[0], move[1]+direction[1]) #move one step to see what is adjacent in this direction
        if board.get(bridge) == to_move: #if first step falls on one of own squares, bridge is not possible in this direction
            return None
        opp = self.other()
        to_flip=[]
        while board.get(bridge) == opp: #if it falls on an opponent's square, keep advancing until you find something else
            to_flip.append(bridge)
            bridge = (bridge[0]+direction[0], bridge[1]+direction[1])
        return (bridge, to_flip) if board.get(bridge) == to_move else None
        # bridge is only possible if that something else is one of own squares    
    
    def legal_move(self,move):
        """A legal move is a square that is empty and makes a 'bridge' over the opponent's color"""
        makes_bridge = None
        if move not in self.board.keys(): # if square 'move' is not yet occupied
            all_directions=((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
            for direction in all_directions:
                makes_bridge = self.find_bridge(move, self.to_move, self.board, direction)
                if makes_bridge != None:
                    break
        return makes_bridge
    
    def number_pieces(self,player):
        """Counts the number of pieces of player and the other"""
        n_pieces_player = 0
        for n in list(self.board.keys()):
            if self.board.get(n) == player:
                n_pieces_player += 1
        n_pieces_other = len(self.used_cells()) - n_pieces_player
        return n_pieces_player, n_pieces_other
    
    def other(self):
        """Who is the other, the one that is not the next to move"""
        return 'X' if self.to_move == 'O' else 'O'
    
    def the_end(self):
        if len(self.used_cells()) == self.h*self.v or self.last_move=='NoneNone':
            return True
        l = list([(x, y) for x in range(1,self.h+1) for y in range(1,self.v+1) if self.legal_move((x,y))])
        if l==[]:
            if self.last_move=='None':
                return True
            nmove = self.other()
            nstate=EstadoOthello(nmove,self.board,self.last_move)      
            l = list([(x, y) for x in range(1,self.h+1) for y in range(1,self.v+1) if nstate.legal_move((x,y))])
            if l==[]:
                return True
        return False

    def the_winner(self):
        n_pieces1,n_pieces2=self.number_pieces(self.to_move)
        if n_pieces1 > n_pieces2:
            return self.to_move
        elif n_pieces1 < n_pieces2:
            return self.other()
        return 0
    
    def display(self,h,v):
        """Display the state given the number of lines and columns"""
        print('   ',end='')
        for y in range(1, v + 1):
            print('__', end='')
        print('_')
        for x in range(1, h + 1):
            print(x, '|', end=' ')
            for y in range(1, v + 1):
                print(self.board.get((x, y), '.'), end=' ')
            print('|', end=' ')
            print()
        print('  |',end='')
        for y in range(1, v + 1):
            print('__', end='')
        print('_|')
        print('    ',end='')
        for y in range(1, v + 1):
            print(y, end=' ')
        print()
        



class Othello(Game):
    """Play Othello on an h x v board (h is the height of the board, and v the width), with first player being 'X'.
    A state has: the player to move; a board, in the form of a dictionary of {(x, y): Player} entries, where
    Player is 'X' or 'O'; the last move (x,y) made, 'None' in the beginning and if last player could not play,
    'NoneNone' is none of the players could play (which signals the end of the game)."""

    def __init__(self, h=8, v=8):
        "The board is empty, it is 'X' that begins, and 'None' last move"
        self.h = 8
        self.v = 8
        self.initial = EstadoOthello(to_move='X',board={(4, 4): 'O', (5, 5): 'O', (4, 5): 'X', (5, 4): 'X'},last_move="None")
        EstadoOthello.h=8
        EstadoOthello.v=8

    def actions(self, state):
        "List of legal moves are any squares that pass the 'legal_move' test."
        l = list([(x, y) for x in range(1, self.h + 1)
                 for y in range(1, self.v + 1) if state.legal_move((x,y))])
        if len(l) == 0:
            l=['None']
        return l

    def result(self, state, move):
        "Execute move from state, returning next state"
        return state.next_move(move)
    
    
    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise.
        Number of pieces determines the score"""
        n_pieces1, n_pieces2 = state.number_pieces(player)
        if n_pieces1 > n_pieces2:
            player_won = 1
        elif n_pieces1 < n_pieces2:
            player_won = -1
        else:
            player_won = 0
        return n_pieces1, n_pieces2, player_won
        
    def terminal_test(self, state):
        """A state is terminal if the board is full OR none of the players could play."""
        return (len(state.used_cells()) == self.h * self.v) or (state.last_move == 'NoneNone')
        
    def display(self, state):
        is_final = self.terminal_test(state);
        if not(is_final):
            print("   Tabuleiro atual:")
        else:
            print("   Tabuleiro final:")
        state.display(self.h,self.v)
        if not(is_final):
            print("   Próximo jogador: {}\n".format(state.to_move))
        else:
            n_pieces1, n_pieces2, player1_won = self.utility(state,'X')
            print("   \nFIM do jogo")
            print("   X conseguiu", n_pieces1)
            print("   O conseguiu", n_pieces2)
            if player1_won > 0:
                print('   Ganhou X')
            elif player1_won < 0:
                print('   Ganhou O')
            else:
                print('   Empate!')
            print()