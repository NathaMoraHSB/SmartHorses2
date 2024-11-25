import tkinter as tk
from tkinter import messagebox, ttk
from board import Board
from minimax_player import MinimaxPlayer
from experiments import run_experiments

class GameInterface:
    def __init__(self, root):
        """Inicializa la interfaz gráfica"""
        self.root = root
        self.root.title("Caballos en el Tablero")
        
        self.board = None
        self.cell_size = 60
        self.is_white_turn = True
        self.mode = "IA vs Humano"
        self.difficulty = 4
        self.ai_player = MinimaxPlayer(self.difficulty, utility_function=1)
        self.ai_opponent = MinimaxPlayer(self.difficulty, utility_function=2)
        
        self.create_menu()
        self.info_label = tk.Label(root, text="")
        self.info_label.pack()
        self.canvas = tk.Canvas(root, width=8 * self.cell_size, height=8 * self.cell_size)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)
        
        self.start_new_game()
    
    def create_menu(self):
        """Crea el menú de configuración"""
        menu_frame = tk.Frame(self.root)
        menu_frame.pack()
        
        tk.Label(menu_frame, text="Modo:").pack(side=tk.LEFT)
        self.mode_combo = ttk.Combobox(menu_frame, values=["IA vs Humano", "IA vs IA", "Experimentos"], state="readonly")
        self.mode_combo.current(0)
        self.mode_combo.pack(side=tk.LEFT)
        
        tk.Label(menu_frame, text="Dificultad:").pack(side=tk.LEFT)
        self.difficulty_combo = ttk.Combobox(menu_frame, values=["Principiante (2)", "Amateur (4)", "Experto (6)"], state="readonly")
        self.difficulty_combo.current(1)
        self.difficulty_combo.pack(side=tk.LEFT)
        
        tk.Button(menu_frame, text="Ejecutar", command=self.start_action).pack(side=tk.LEFT)
    
    def start_action(self):
        """Maneja el botón de ejecutar según el modo seleccionado"""
        if self.mode_combo.get() == "Experimentos":
            self.run_experiments_mode()
        else:
            self.mode = self.mode_combo.get()
            self.start_new_game()
    
    def start_new_game(self):
        """Inicia un nuevo juego"""
        self.mode = self.mode_combo.get()#iavs IA o IA vs Humano
        difficulty_text = self.difficulty_combo.get()#dificultad
        self.difficulty = int(difficulty_text[difficulty_text.find("(") + 1:difficulty_text.find(")")])
        
        self.board = Board()
        self.board.initialize_board()
        self.ai_player = MinimaxPlayer(self.difficulty, utility_function=1)
        self.ai_opponent = MinimaxPlayer(self.difficulty, utility_function=2)
        self.is_white_turn = True
        self.update_board()

        
        if self.mode == "IA vs IA":
            self.run_ai_vs_ai()
        elif self.mode == "IA vs Humano":
            self.run_ai_turn()
    
    def run_experiments_mode(self):
        """Ejecuta experimentos y muestra los resultados"""
        messagebox.showinfo("Experimentos", "Ejecutando experimentos, esto puede tomar varios minutos.")
        run_experiments()
        messagebox.showinfo("Resultados", "Experimentos completados. Ver la consola para detalles.")
    
    def run_ai_turn(self):
        """Gestiona el turno de la IA en modo IA vs Humano"""
        _, best_move = self.ai_player.minimax(self.board, self.difficulty, float('-inf'), float('inf'), True, True)
        
        if best_move:
            self.board.make_move(best_move, True)
            
        self.is_white_turn = not self.is_white_turn
        self.update_board()
        self.board.get_state_as_dict()
        print("Estado del tablero:")
        print(self.board.get_state_as_dict())
        
        if self.board.is_game_over():
            self.end_game()
    
    def handle_click(self, event):
        """Gestiona clics del jugador en el tablero"""
        if self.mode == "IA vs IA" or (self.mode == "IA vs Humano" and self.is_white_turn):
            return
        
        x, y = event.x // self.cell_size, event.y // self.cell_size #posicion del click
        current_pos = self.board.white_horse if self.is_white_turn else self.board.black_horse#posicion del caballo jugando en ese turno
        valid_moves = self.board.get_valid_moves(current_pos)
        
        if (x, y) not in valid_moves:
            messagebox.showwarning("Movimiento Inválido", "Elige un movimiento válido.")
            return
        
        self.board.make_move((x, y), False)#mueve el caballo negro white is false
        self.is_white_turn = not self.is_white_turn#cambio de turno
        self.update_board()
        
        if self.board.is_game_over():
            self.end_game()
        elif self.mode == "IA vs Humano" and self.is_white_turn:
            self.run_ai_turn()
    
    def update_board(self):
        """Actualiza la visualización del tablero"""
        self.canvas.delete("all")
        
        for i in range(self.board.size):
            for j in range(self.board.size):
                x1, y1 = i * self.cell_size, j * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                fill_color = "white" if (i + j) % 2 == 0 else "gray"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color)
        
        for pos, value in self.board.points.items():
            x, y = pos
            cx, cy = x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2
            self.canvas.create_text(cx, cy, text=str(value), fill="blue", font=("Arial", 16))
        
        for x, y in self.board.multipliers:
            cx, cy = x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2
            self.canvas.create_oval(cx-10, cy-10, cx+10, cy+10, fill="green")
        
        wx, wy = self.board.white_horse
        bx, by = self.board.black_horse
        self.canvas.create_oval(wx * self.cell_size + 10, wy * self.cell_size + 10,
                                (wx+1) * self.cell_size - 10, (wy+1) * self.cell_size - 10, fill="white")
        self.canvas.create_oval(bx * self.cell_size + 10, by * self.cell_size + 10,
                                (bx+1) * self.cell_size - 10, (by+1) * self.cell_size - 10, fill="black")
        
        if self.mode == "IA vs Humano":
            current_player = "IA" if self.is_white_turn else "Humano"
            self.info_label.config(
                text=f"Turno: {current_player} ({'Blanco' if self.is_white_turn else 'Negro'}) | "
                     f"Puntos IA (Blanco): {self.board.white_score} | Puntos Humano (Negro): {self.board.black_score}"
            )
        else:
            self.info_label.config(
                text=f"Turno: {'Blanco' if self.is_white_turn else 'Negro'} | "
                     f"Puntos Blanco: {self.board.white_score} | Puntos Negro: {self.board.black_score}"
            )
    
    def run_ai_vs_ai(self):
        """Gestiona partidas automáticas entre IA"""
        if not self.board.is_game_over():
            current_ai = self.ai_player if self.is_white_turn else self.ai_opponent
            _, best_move = current_ai.minimax(self.board, self.difficulty, float('-inf'), float('inf'), True, self.is_white_turn)
            if best_move:
                self.board.make_move(best_move, self.is_white_turn)
            self.is_white_turn = not self.is_white_turn
            self.update_board()

            self.root.after(500, self.run_ai_vs_ai)
        else:
            self.end_game()
    
    def end_game(self):
        """Finaliza el juego y muestra el ganador"""
        if self.board.moves_count >= self.ai_player.MAX_MOVES:
            messagebox.showinfo("Juego Terminado", "¡Empate por límite de movimientos (150)!")
            return
        
        if self.board.white_score > self.board.black_score:
            winner = "Blanco"
        elif self.board.white_score < self.board.black_score:
            winner = "Negro"
        else:
            winner = "Empate"
        
        messagebox.showinfo("Juego Terminado", f"¡El juego ha terminado! \nGanador: {winner}")

