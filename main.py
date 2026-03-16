from sync_engine import run_full_sync
from agent import get_vegas_recommendation

def main():
    print("--- 🎰 Vegas Insider Agent Dashboard ---")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == 'sync':
            run_full_sync() # Now this actually runs your logic!
            
        elif user_input.lower() == 'exit':
            break
            
        else:
            print("Thinking...")
            response = get_vegas_recommendation(user_input)
            print(f"\nConcierge: {response}")

if __name__ == "__main__":
    main()