from board import Board
from minimax_player import MinimaxPlayer
from experiments import run_experiments

class GameApp:
    def __init__(self):
        """Inicializa la lógica del juego"""
        self.board = None
        self.is_white_turn = True
        self.mode = "IA vs Humano"
        self.difficulty = 4
        self.ai_player = None
        self.ai_opponent = None

    def start_new_game(self, mode="IA vs Humano", difficulty=4):
        """Inicia un nuevo juego con el modo y la dificultad especificados"""
        self.mode = mode
        self.difficulty = difficulty
        self.board = Board()
        self.board.initialize_board()
        self.ai_player = MinimaxPlayer(difficulty, utility_function=1)
        self.ai_opponent = MinimaxPlayer(difficulty, utility_function=2)
        self.is_white_turn = True

    def run_ai_turn(self):

        history = []  # Lista para almacenar los estados antes y después del movimiento

        # Estado inicial del juego antes del movimiento de la IA
        game_state = self.get_game_state()
        history.append(game_state)

        _, best_move = self.ai_player.minimax(self.board, self.difficulty, float('-inf'), float('inf'), True, self.is_white_turn)
        if best_move:
            self.board.make_move(best_move, self.is_white_turn)

        self.is_white_turn = not self.is_white_turn

        game_state = self.get_game_state()
        history.append(game_state)
        return history


    def handle_player_move(self, x, y):
        history = []
        game_state = self.get_game_state()
        history.append(game_state)

        self.board.make_move((x, y), self.is_white_turn)
        self.is_white_turn = not self.is_white_turn

        game_state = self.get_game_state()
        history.append(game_state)

        return history


    def run_ai_vs_ai(self):

        history = []

        while not self.board.is_game_over():
            game_state = self.get_game_state()
            history.append(game_state)

            current_ai = self.ai_player if self.is_white_turn else self.ai_opponent
            _, best_move = current_ai.minimax(self.board, self.difficulty, float('-inf'), float('inf'), True, self.is_white_turn)
            if best_move:
                self.board.make_move(best_move, self.is_white_turn)
            self.is_white_turn = not self.is_white_turn
        history.append(self.get_game_state())

        return history


    def update_board(self):
        """Actualiza la representación del tablero"""
        return self.get_game_state()

    def end_game(self):
        """Finaliza el juego y determina el ganador"""
        if self.board.is_game_over():
            if self.board.white_score > self.board.black_score:
                winner = "Blanco"
            elif self.board.white_score < self.board.black_score:
                winner = "Negro"
            else:
                winner = "Empate"
            return {"winner": winner, "white_score": self.board.white_score, "black_score": self.board.black_score}
        return {"error": "El juego no ha terminado"}

    def run_experiments_mode(self):
        """Ejecuta experimentos y devuelve un mensaje de éxito"""
        run_experiments()
        return {"message": "Experimentos completados"}


    def get_game_state(self):
        """Devuelve el estado del juego como un diccionario"""
        board_state = self.board.get_state_as_dict()
        # Construir la representación de la matriz
        matrix = []
        for i in range(board_state['size']):
            row = []
            for j in range(board_state['size']):
                cell = 0  # Por defecto, celda vacía
                if (i, j) == board_state['white_horse']:
                    cell = 11  # Identificador del caballo blanco
                elif (i, j) == board_state['black_horse']:
                    cell = 12  # Identificador del caballo negro
                elif (i, j) in board_state['points']:
                    cell = board_state['points'][(i, j)]  # Valor del punto
                elif (i, j) in board_state['multipliers']:
                    cell = 20  # Identificador del multiplicador
                row.append(cell)
            matrix.append(row)

        # Devolver el estado completo del juego
        return {
            "matrix": matrix,  # Representación de la matriz
            "whiteHorsePoints": board_state['white_score'],
            "blackHorsePoints": board_state['black_score'],
            "whiteHorseMultiplier": board_state['white_multiplier'],
            "blackHorseMultiplier": board_state['black_multiplier'],
            "movesCount": board_state['moves_count'],
            "gameOver": self.board.is_game_over(),
            "turn": "white" if self.is_white_turn else "black"
        }


    def get_game(self):
        """
        Devuelve el estado actual del juego.
        Incluye el tablero, los jugadores y el modo.
        """
        if not self.board:
            return {"error": "El juego no ha sido inicializado."}
        return {
            "mode": self.mode,
            "difficulty": self.difficulty,
            "board": self.get_game_state(),
            "is_white_turn": self.is_white_turn
        }


