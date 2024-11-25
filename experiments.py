from collections import defaultdict
from ai_game import AIGame
from tabulate import tabulate

def run_experiments():
    """Ejecuta experimentos para evaluar diferentes configuraciones de dificultad"""
    difficulty_levels = {
        'Principiante': 2,
        'Amateur': 4,
        'Experto': 6
    }
    
    results = defaultdict(lambda: defaultdict(lambda: [0, 0, 0]))
    total_ai1, total_ai2, total_draws = 0, 0, 0
    
    for ai1_level in difficulty_levels:
        for ai2_level in difficulty_levels:
            print(f"\nCombinación {ai1_level} vs {ai2_level}")
            for game in range(10):
                print(f"Jugando partida {game + 1}/10", end='\r')
                game = AIGame(difficulty_levels[ai1_level], difficulty_levels[ai2_level])
                result = game.play_game()
                
                if result == 1:
                    results[ai1_level][ai2_level][0] += 1
                    total_ai1 += 1
                elif result == 2:
                    results[ai1_level][ai2_level][1] += 1
                    total_ai2 += 1
                else:
                    results[ai1_level][ai2_level][2] += 1
                    total_draws += 1
    
    table = []
    headers = ['IA1 vs IA2'] + list(difficulty_levels.keys())
    
    for ai1_level in difficulty_levels:
        row = [ai1_level]
        for ai2_level in difficulty_levels:
            wins_ai1, wins_ai2, draws = results[ai1_level][ai2_level]
            row.append(f"{wins_ai1}-{wins_ai2}-{draws}")
        table.append(row)
    
    print("\nResultados finales (IA1-IA2-Empates):")
    print(tabulate(table, headers=headers, tablefmt="grid"))
    print(f"\nTotal IA1: {total_ai1} ({(total_ai1/(total_ai1+total_ai2+total_draws))*100:.2f}%)")
    print(f"Total IA2: {total_ai2} ({(total_ai2/(total_ai1+total_ai2+total_draws))*100:.2f}%)")
    print(f"Empates: {total_draws} ({(total_draws/(total_ai1+total_ai2+total_draws))*100:.2f}%)")
