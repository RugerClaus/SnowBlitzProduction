import argparse
from core.guts.app import App
from core.guts.window import Window
from core.state.ApplicationLayer.dev import DEVELOPER_MODE

def main():
    parser = argparse.ArgumentParser(description="Game Startup")
    
    parser.add_argument('--dev', action='store_true', help="Enable developer mode")

    args = parser.parse_args()

    window = Window()
    app = App(window)

    if args.dev:
        print("Developer mode enabled.")
        app.dev.set_state(DEVELOPER_MODE.ON)
    
    # Run the app
    app.run()

if __name__ == "__main__":
    main()
