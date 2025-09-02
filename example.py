import streamlit as st
import random
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Rock Paper Scissors Game",
    page_icon="✂️",
    layout="wide"
)

# Initialize session state for game statistics
if 'wins' not in st.session_state:
    st.session_state.wins = 0
if 'losses' not in st.session_state:
    st.session_state.losses = 0
if 'ties' not in st.session_state:
    st.session_state.ties = 0
if 'game_history' not in st.session_state:
    st.session_state.game_history = []

# Game logic
def determine_winner(player_choice, computer_choice):
    """Determine the winner of the game"""
    if player_choice == computer_choice:
        return "tie"
    
    winning_combinations = {
        "rock": "scissors",
        "paper": "rock", 
        "scissors": "paper"
    }
    
    if winning_combinations[player_choice] == computer_choice:
        return "win"
    else:
        return "loss"

def get_computer_choice():
    """Get random computer choice"""
    return random.choice(["rock", "paper", "scissors"])

def get_emoji(choice):
    """Get emoji for each choice"""
    emojis = {
        "rock": "🪨",
        "paper": "📄",
        "scissors": "✂️"
    }
    return emojis.get(choice, "")

# Main app
def main():
    st.title("🎮 Rock Paper Scissors Game")
    st.markdown("---")
    
    # Create two columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎯 Make Your Choice!")
        
        # Player choice buttons
        player_choice = None
        choice_col1, choice_col2, choice_col3 = st.columns(3)
        
        with choice_col1:
            if st.button("🪨 Rock", use_container_width=True, key="rock"):
                player_choice = "rock"
        with choice_col2:
            if st.button("📄 Paper", use_container_width=True, key="paper"):
                player_choice = "paper"
        with choice_col3:
            if st.button("✂️ Scissors", use_container_width=True, key="scissors"):
                player_choice = "scissors"
        
        # Game logic
        if player_choice:
            computer_choice = get_computer_choice()
            result = determine_winner(player_choice, computer_choice)
            
            # Update statistics
            if result == "win":
                st.session_state.wins += 1
            elif result == "loss":
                st.session_state.losses += 1
            else:
                st.session_state.ties += 1
            
            # Add to game history
            game_record = {
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "player": player_choice,
                "computer": computer_choice,
                "result": result
            }
            st.session_state.game_history.append(game_record)
            
            # Display results
            st.markdown("---")
            st.subheader("🎲 Game Result!")
            
            result_col1, result_col2, result_col3 = st.columns(3)
            
            with result_col1:
                st.markdown("**Your Choice:**")
                st.markdown(f"<h1 style='text-align: center;'>{get_emoji(player_choice)}</h1>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center;'>{player_choice.title()}</p>", unsafe_allow_html=True)
            
            with result_col2:
                st.markdown("**VS**")
                st.markdown("<h1 style='text-align: center;'>⚔️</h1>", unsafe_allow_html=True)
            
            with result_col3:
                st.markdown("**Computer Choice:**")
                st.markdown(f"<h1 style='text-align: center;'>{get_emoji(computer_choice)}</h1>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center;'>{computer_choice.title()}</p>", unsafe_allow_html=True)
            
            # Display result message
            if result == "win":
                st.success("🎉 Congratulations! You won!")
            elif result == "loss":
                st.error("😔 Better luck next time! Computer won.")
            else:
                st.info("🤝 It's a tie!")
    
    with col2:
        st.header("📊 Game Statistics")
        
        # Display current stats
        st.metric("Wins", st.session_state.wins)
        st.metric("Losses", st.session_state.losses)
        st.metric("Ties", st.session_state.ties)
        
        # Calculate win rate
        total_games = st.session_state.wins + st.session_state.losses + st.session_state.ties
        if total_games > 0:
            win_rate = (st.session_state.wins / total_games) * 100
            st.metric("Win Rate", f"{win_rate:.1f}%")
        
        st.markdown("---")
        
        # Reset button
        if st.button("🔄 Reset Game", use_container_width=True):
            st.session_state.wins = 0
            st.session_state.losses = 0
            st.session_state.ties = 0
            st.session_state.game_history = []
            st.rerun()
    
    # Game history
    if st.session_state.game_history:
        st.markdown("---")
        st.header("📜 Game History")
        
        # Create a DataFrame-like display
        history_data = []
        for record in st.session_state.game_history[-10:]:  # Show last 10 games
            history_data.append({
                "Time": record["timestamp"],
                "You": f"{get_emoji(record['player'])} {record['player'].title()}",
                "Computer": f"{get_emoji(record['computer'])} {record['computer'].title()}",
                "Result": record["result"].title()
            })
        
        # Display history in a nice format
        for i, record in enumerate(reversed(history_data)):
            col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
            with col1:
                st.write(record["Time"])
            with col2:
                st.write(record["You"])
            with col3:
                st.write(record["Computer"])
            with col4:
                if record["Result"] == "Win":
                    st.success(record["Result"])
                elif record["Result"] == "Loss":
                    st.error(record["Result"])
                else:
                    st.info(record["Result"])
    
    # Footer
    st.markdown("---")
    st.markdown("🎮 **How to play:** Choose Rock, Paper, or Scissors and see if you can beat the computer!")
    st.markdown("🪨 Rock crushes Scissors | 📄 Paper covers Rock | ✂️ Scissors cut Paper")

if __name__ == "__main__":
    main()


