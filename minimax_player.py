from typing import List, Tuple, Optional
from board import Board

class MinimaxPlayer:
    def __init__(self, depth: int, utility_function: int):
        """Inicializa el jugador Minimax con una profundidad y una función de utilidad"""
        self.depth = depth
        self.utility_function = utility_function
        self.MAX_MOVES = 150
    
    def detect_cycle(self, board: Board, position: Tuple[int, int], is_white: bool) -> bool:
        """Detecta si un movimiento podría crear un ciclo"""
        if len(board.position_history) < 4:
            return False
        
        recent_moves = [(pos, player) for pos, player in board.position_history[-4:] 
                        if player == is_white]
        return position in [pos for pos, _ in recent_moves]

    def get_valid_moves(self, board: Board, is_white: bool) -> List[Tuple[int, int]]:
        """Obtiene movimientos válidos priorizando puntos y evitando ciclos"""
        current_pos = board.white_horse if is_white else board.black_horse
        basic_moves = board.get_valid_moves(current_pos)
        
        point_moves = []
        multiplier_moves = []
        other_moves = []
        
        for move in basic_moves:
            if move in board.points:
                point_moves.append(move)
            elif move in board.multipliers:
                multiplier_moves.append(move)
            elif not self.detect_cycle(board, move, is_white):
                other_moves.append(move)
        
        if point_moves:
            return point_moves
        if multiplier_moves and not (is_white and board.white_multiplier) and \
           not (not is_white and board.black_multiplier):
            return multiplier_moves
            
        return other_moves if other_moves else basic_moves

    def utility_function_1(self, board: Board, is_white: bool) -> float:
        """Primera función de utilidad: prioriza diferencia de puntos y distancia"""
        my_pos = board.white_horse if is_white else board.black_horse
        my_score = board.white_score if is_white else board.black_score
        opp_score = board.black_score if is_white else board.white_score
        my_multiplier = board.white_multiplier if is_white else board.black_multiplier
        
        min_distance = float('inf')
        max_point_value = 0
        for point_pos, value in board.points.items():
            distance = abs(my_pos[0] - point_pos[0]) + abs(my_pos[1] - point_pos[1])
            if distance < min_distance:
                min_distance = distance
                max_point_value = value
        
        score_diff = my_score - opp_score
        distance_factor = -min_distance if min_distance != float('inf') else 0
        point_value_factor = max_point_value * (2 if my_multiplier else 1)
        
        repetition_penalty = 0
        if len(board.position_history) >= 4:
            recent_positions = [pos for pos, player in board.position_history[-12:] if player == is_white]
            if len(set(recent_positions)) < len(recent_positions):
                repetition_penalty = -5.0

        return (
            score_diff * 10.0 +
            distance_factor * 1.5 +
            point_value_factor * 3.0 +
            (my_multiplier * 5.0) +
            repetition_penalty
        )
    
    def utility_function_2(self, board: Board, is_white: bool) -> float:
        """Segunda función de utilidad: prioriza multiplicadores y penaliza más los ciclos"""
        my_pos = board.white_horse if is_white else board.black_horse
        my_score = board.white_score if is_white else board.black_score
        opp_score = board.black_score if is_white else board.white_score
        my_multiplier = board.white_multiplier if is_white else board.black_multiplier
        
        min_distance = float('inf')
        max_point_value = 0
        for point_pos, value in board.points.items():
            distance = abs(my_pos[0] - point_pos[0]) + abs(my_pos[1] - point_pos[1])
            if distance < min_distance:
                min_distance = distance
                max_point_value = value

        if board.multipliers:
            min_distance_to_multiplier = float('inf')
            for mult_pos in board.multipliers:
                distance = abs(my_pos[0] - mult_pos[0]) + abs(my_pos[1] - mult_pos[1])
                min_distance_to_multiplier = min(min_distance_to_multiplier, distance)
        else:
            min_distance_to_multiplier = 0

        score_diff = my_score - opp_score
        distance_factor = -min_distance if min_distance != float('inf') else 0
        point_value_factor = max_point_value * (2 if my_multiplier else 1)
        
        repetition_penalty = 0
        if len(board.position_history) >= 8:
            recent_positions = [pos for pos, player in board.position_history[-12:] 
                                if player == (not is_white)]
            if len(set(recent_positions)) < len(recent_positions):
                repetition_penalty = -10.0

        return (
            score_diff * 8.0 +
            distance_factor * 2.0 +
            point_value_factor * 4.0 +
            (my_multiplier * 10.0) +
            (8-min_distance_to_multiplier * 1.5) +
            repetition_penalty
        )
    
    def evaluate_board(self, board: Board, is_white: bool) -> float:
        """Evalúa el tablero usando la función de utilidad seleccionada"""
        if self.utility_function == 1:
            return self.utility_function_1(board, is_white)
        elif self.utility_function == 2:
            return self.utility_function_2(board, is_white)
        return 0
    
    def minimax(self, board: Board, depth: int, alpha: float, beta: float, 
                is_maximizing: bool, is_white: bool) -> Tuple[float, Optional[Tuple[int, int]]]:
        """Implementa el algoritmo Minimax con poda alfa-beta"""
        if depth == 0 or board.is_game_over() or board.moves_count >= self.MAX_MOVES:
            return self.evaluate_board(board, is_white), None
        
        valid_moves = self.get_valid_moves(board, is_white if is_maximizing else not is_white)
        
        if not valid_moves:
            return self.evaluate_board(board, is_white), None
        
        best_move = None
        if is_maximizing:
            max_eval = float('-inf')
            for move in valid_moves:
                board_copy = board.clone()
                board_copy.make_move(move, is_white)
                eval_score, _ = self.minimax(board_copy, depth - 1, alpha, beta, False, is_white)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in valid_moves:
                board_copy = board.clone()
                board_copy.make_move(move, not is_white)
                eval_score, _ = self.minimax(board_copy, depth - 1, alpha, beta, True, is_white)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move
    
    def make_move(self, board: Board, is_white: bool) -> Optional[Tuple[int, int]]:
        """Determina el mejor movimiento para el jugador"""
        if board.moves_count >= self.MAX_MOVES:
            return None
        
        _, best_move = self.minimax(board, self.depth, float('-inf'), float('inf'), True, is_white)
        return best_move
