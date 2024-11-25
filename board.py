import random
import numpy as np
from typing import List, Tuple

class Board:
    def __init__(self):
        """Inicializa un tablero vacío con las configuraciones básicas"""
        self.size = 8
        self.board = np.zeros((self.size, self.size), dtype=int)
        self.multipliers = set()
        self.points = {}
        self.white_horse = None
        self.black_horse = None
        self.white_multiplier = False
        self.black_multiplier = False
        self.white_score = 0
        self.black_score = 0
        self.moves_count = 0
        self.position_history = []  # Historial de posiciones para detectar ciclos
    
    def initialize_board(self):
        """Configura el tablero con posiciones iniciales de los caballos, puntos y multiplicadores"""
        all_positions = [(i, j) for i in range(self.size) for j in range(self.size)]
        positions = random.sample(all_positions, 16)
        
        self.white_horse = positions[0]
        self.black_horse = positions[1]
        
        for i, pos in enumerate(positions[2:12]):
            self.points[pos] = i + 1
            
        self.multipliers = set(positions[12:16])
        self.moves_count = 0
        self.position_history = []
    
    def get_valid_moves(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Retorna los movimientos válidos de un caballo desde una posición dada"""
        moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        valid = []
        for dx, dy in moves:
            new_x = position[0] + dx
            new_y = position[1] + dy
            if (0 <= new_x < self.size and 0 <= new_y < self.size and 
                (new_x, new_y) != self.white_horse and 
                (new_x, new_y) != self.black_horse):
                valid.append((new_x, new_y))
        return valid

    def make_move(self, position: Tuple[int, int], is_white: bool) -> int:
        """Realiza un movimiento, actualizando puntajes y estado del tablero"""
        self.moves_count += 1
        score = 0
        self.position_history.append((position, is_white))
        
        # Limitar el historial a las últimas 12 posiciones
        if len(self.position_history) > 12:
            self.position_history.pop(0)
            
        # Actualizar puntajes y multiplicadores
        if position in self.points:
            base_points = self.points[position]
            if (is_white and self.white_multiplier) or (not is_white and self.black_multiplier):
                score = base_points * 2
                if is_white:
                    self.white_multiplier = False
                else:
                    self.black_multiplier = False
            else:
                score = base_points
            del self.points[position]
            
        if position in self.multipliers:
            if is_white and not self.white_multiplier:
                self.white_multiplier = True
            elif not is_white and not self.black_multiplier:
                self.black_multiplier = True
            self.multipliers.remove(position)
        
        # Actualizar posición y puntaje del caballo correspondiente
        if is_white:
            self.white_horse = position
            self.white_score += score
        else:
            self.black_horse = position
            self.black_score += score

        self.get_state_as_dict()
      #  print("Estado del tablero:")
        #print(self.get_state_as_dict())

        return score

    def is_game_over(self) -> bool:
        """Determina si el juego ha terminado"""
        return not self.points or self.moves_count >= 150
    
    def clone(self):
        """Crea una copia del estado actual del tablero"""
        new_board = Board()
        new_board.board = self.board.copy()
        new_board.points = self.points.copy()
        new_board.multipliers = self.multipliers.copy()
        new_board.white_horse = self.white_horse
        new_board.black_horse = self.black_horse
        new_board.white_score = self.white_score
        new_board.black_score = self.black_score
        new_board.white_multiplier = self.white_multiplier
        new_board.black_multiplier = self.black_multiplier
        new_board.moves_count = self.moves_count
        new_board.position_history = self.position_history.copy()
        return new_board

    def get_state_as_dict(self):
        """Devuelve un diccionario con los atributos y sus valores"""
        return self.__dict__.copy()

    def quedan_puntos(self) -> bool:
        return bool(self.points)

