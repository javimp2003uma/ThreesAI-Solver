from question_ui import QuestionUI
from threes_game import ThreeGame

def main():
    while True:
        try:
            question_ui = QuestionUI()
            game_mode, seed, algorithm, heuristic = question_ui.run()
            
            # Verifica si la ventana se cerró sin seleccionar un juego
            if game_mode is None or seed is None:
                print("La ventana se cerró. Saliendo del programa.")
                break
            
            three_game = ThreeGame(seed, game_mode, algorithm, heuristic)
            three_game.run()
        
        except Exception as e:
            print("Se produjo un error:", e)

if __name__ == "__main__":
    main()
