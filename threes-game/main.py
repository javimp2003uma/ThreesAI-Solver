from question_ui import QuestionUI
from threes_game import ThreeGame

def main():
    """Función principal que ejecuta el juego Threes."""
    while True:
        try:
            question_ui = QuestionUI()
            game_mode, seed, algorithm, heuristic = question_ui.run()

            if game_mode is None or seed is None:
                print("La ventana se cerró. Saliendo del programa.")
                break

            three_game = ThreeGame(seed, game_mode, algorithm, heuristic)
            three_game.run()

        except KeyboardInterrupt:
            print("\nPrograma terminado por el usuario.")
            break 
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
