#app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from game_app import GameApp
from collections import defaultdict
from ai_game import AIGame

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})

# Instancia global del juego
game = GameApp()

@app.route('/api/start', methods=['POST'])
def start_game():
    """Inicia un nuevo juego y devuelve la matriz inicial"""
    data = request.json
    mode = data.get('mode', 'IA vs Humano')
    difficulty = data.get('difficulty', 4)
    game.start_new_game(mode, difficulty)
    print("juego iniciado")
    return jsonify(game.get_game_state()), 200

@app.route('/api/partidaIaVSIa', methods=['POST'])
def run_simulation():

    if not game.board:
        return jsonify({"error": "El juego no ha sido inicializado. Por favor, inicia un nuevo juego primero."}), 400

    try:
        history = game.run_ai_vs_ai()
        if not history:
            return jsonify({"error": "No se pudo generar la simulación"}), 500

        report = {
            "result": "Empate",
            "Puntos IA 1, caballo blanco": game.board.white_score,
            "Puntos IA 2, caballo negro": game.board.black_score
        }

        if game.board.white_score > game.board.black_score:
            report["result"] = "Gana el caballo blanco"
        elif game.board.white_score < game.board.black_score:
            report["result"] = "Gana el caballo negro"

        return jsonify({
            "simulation": history,
            "report": report
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/human-move', methods=['POST'])
def handle_move():
    data = request.json
    print("data desde el front", data)
    row, col = data["row"], data["col"]

    history = game.handle_player_move(row, col)

    if not history or len(history) < 2:
        return jsonify({"error": "No se pudo procesar el movimiento correctamente"}), 500

    return jsonify({
        "simulation": history
    }), 200

@app.route('/api/ai-turn', methods=['GET'])
def handle_ai_turn():

    try:
        history = game.run_ai_turn()

        if not history or len(history) < 2:
            return jsonify({"error": "No se pudo procesar el turno de la IA correctamente"}), 500

        return jsonify({
            "simulation": history
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/update-difficulty', methods=['POST'])
def update_difficulty():
    data = request.json
    if 'difficulty' not in data:
        return jsonify({"error": "El nivel de dificultad no fue proporcionado"}), 400

    new_difficulty = data['difficulty']
    if not isinstance(new_difficulty, int) or new_difficulty <= 0:
        return jsonify({"error": "El nivel de dificultad debe ser un número entero positivo"}), 400

    game.difficulty = new_difficulty
    print("dificultad actualizada a", game.difficulty)

    return jsonify({
        "message": "Nivel de dificultad actualizado",
        "difficulty": game.difficulty,
        "new_matrix": game.get_game_state()["matrix"]
    }), 200

@app.route('/api/quedan-puntos', methods=['GET'])
def quedan_puntos():

    if not game.board:
        return jsonify({"error": "El juego no ha sido inicializado. Por favor, inicia un nuevo juego primero."}), 400

    quedan = game.board.quedan_puntos()
    return jsonify({"quedan_puntos": quedan}), 200

@app.route('/api/run-experiments', methods=['GET'])
def run_experiments():
    """Ejecuta experimentos y devuelve resultados organizados en JSON"""
    print("corriendo experimentos")
    difficulty_levels = {
        'Principiante': 2,
        'Amateur': 4,
        'Experto': 6
    }

    results = defaultdict(lambda: defaultdict(lambda: [0, 0, 0]))
    total_ai1, total_ai2, total_draws = 0, 0, 0

    for ai1_level in difficulty_levels:
        for ai2_level in difficulty_levels:
            for game in range(10):
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

    # Enviar solo los valores necesarios
    experiments = {
        "totals": {
            "ia1": total_ai1,
            "ia1_percentage": round((total_ai1 / (total_ai1 + total_ai2 + total_draws)) * 100, 2),
            "ia2": total_ai2,
            "ia2_percentage": round((total_ai2 / (total_ai1 + total_ai2 + total_draws)) * 100, 2),
            "draws": total_draws,
            "draws_percentage": round((total_draws / (total_ai1 + total_ai2 + total_draws)) * 100, 2),
        },
        "details": {
            ai1_level: {
                ai2_level: {
                    "wins_ai1": results[ai1_level][ai2_level][0],
                    "wins_ai2": results[ai1_level][ai2_level][1],
                    "draws": results[ai1_level][ai2_level][2]
                } for ai2_level in difficulty_levels
            } for ai1_level in difficulty_levels
        }
    }

    return jsonify(experiments)

if __name__ == '__main__':
    app.run(debug=True)