from sync_engine import run_full_sync
from agent import get_vegas_recommendation
from database import print_all_events

def main():
    print("--- 🎰 Vegas Insider Agent Dashboard ---")
    print("Commands: 'sync', 'sync --wipe', 'events', 'exit'")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == 'sync':
            run_full_sync()
        elif user_input.lower() == 'sync --wipe':
            run_full_sync(wipe_first=True)
        elif user_input.lower() == 'events':
            print_all_events()
        elif user_input.lower() == 'exit':
            break
        else:
            print("Thinking...")
            response = get_vegas_recommendation(user_input)
            print(f"\nConcierge: {response}")

if __name__ == "__main__":
    main()
