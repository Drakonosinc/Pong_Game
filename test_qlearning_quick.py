#!/usr/bin/env python3
import sys
import os
sys.path.append('src')

def test_qlearning():
    try:
        from Game.Space_Pong import Space_pong_game
        from Type_Training import q_learning_algorithm
        
        print("Creating game instance...")
        game = Space_pong_game()
        
        print("Starting Q-learning test with 2 episodes...")
        
        # Run Q-learning for just 2 episodes
        model = q_learning_algorithm(
            game, 
            input_size=len(game.ai_handler.get_state()), 
            output_size=2, 
            episodes=2,
            lr=0.01,
            epsilon_decay=0.5
        )
        
        print("✓ Q-learning test completed successfully!")
        print("✓ Model type:", type(model).__name__)
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_qlearning()
    print("Test result:", "PASSED" if success else "FAILED")
