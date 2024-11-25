from board import Board
from minimax_player import MinimaxPlayer

class AIGame:
    def __init__(self, ai1_depth: int, ai2_depth: int):
        self.board = Board()
        self.ai1 = MinimaxPlayer(ai1_depth, utility_function=1)
        self.ai2 = MinimaxPlayer(ai2_depth, utility_function=2)
        
    def play_game(self, verbose=False) -> int:
        """Simula un juego entre dos jugadores IA"""
        self.board.initialize_board()
        
        while not self.board.is_game_over():
            # Turno de la IA 1
            _, best_move = self.ai1.minimax(self.board, self.ai1.depth, float('-inf'), float('inf'), True, True)
            if best_move:
                self.board.make_move(best_move, True)
                if verbose:
                    print(f"IA1 mueve a {best_move}, puntaje: {self.board.white_score}")
            
            if self.board.is_game_over():
                break
                
            # Turno de la IA 2
            _, best_move = self.ai2.minimax(self.board, self.ai2.depth, float('-inf'), float('inf'), True, False)
            if best_move:
                self.board.make_move(best_move, False)
                if verbose:
                    print(f"IA2 mueve a {best_move}, puntaje: {self.board.black_score}")
        
        # Determinar ganador
        if self.board.white_score > self.board.black_score:
            return 1  # Gana IA1
        elif self.board.white_score < self.board.black_score:
            return 2  # Gana IA2
        return 0  # Empate
