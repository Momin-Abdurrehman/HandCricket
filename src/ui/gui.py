"""
Tkinter GUI for Hand Cricket AI
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.game import Player, MatchManager
from src.ai import AdaptiveAgent


class HandCricketGUI:
    """
    Graphical user interface for Hand Cricket game
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Cricket AI")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        
        # Game components
        self.player = Player("Human Player")
        self.difficulty = tk.StringVar(value="balanced")
        self.agent = AdaptiveAgent(use_all_layers=True, difficulty="balanced")
        self.manager = MatchManager(self.player, self.agent)
        
        # Game state
        self.game_started = False
        self.waiting_for_move = False
        
        # Colors
        self.bg_color = "#1e1e2e"
        self.fg_color = "#cdd6f4"
        self.accent_color = "#89b4fa"
        self.button_color = "#313244"
        self.button_hover = "#45475a"
        self.success_color = "#a6e3a1"
        self.error_color = "#f38ba8"
        
        self.root.configure(bg=self.bg_color)
        
        # Setup UI
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the user interface"""
        # Title
        title_frame = tk.Frame(self.root, bg=self.bg_color)
        title_frame.pack(pady=20)
        
        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        title_label = tk.Label(
            title_frame, 
            text="🏏 Hand Cricket AI 🏏",
            font=title_font,
            bg=self.bg_color,
            fg=self.accent_color
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Adaptive AI that learns your patterns",
            font=("Helvetica", 10),
            bg=self.bg_color,
            fg=self.fg_color
        )
        subtitle_label.pack()
        
        # Difficulty selector
        self._create_difficulty_selector()
        
        # Scoreboard
        self._create_scoreboard()
        
        # Game info
        self._create_game_info()
        
        # Move buttons
        self._create_move_buttons()
        
        # Message area
        self._create_message_area()
        
        # Control buttons
        self._create_control_buttons()
        
        # AI Stats
        self._create_stats_area()
    
    def _create_difficulty_selector(self):
        """Create difficulty selector"""
        diff_frame = tk.Frame(self.root, bg=self.bg_color)
        diff_frame.pack(pady=5)
        
        tk.Label(
            diff_frame,
            text="Difficulty:",
            font=("Helvetica", 9, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(side=tk.LEFT, padx=5)
        
        difficulties = [
            ("Easy 😊", "easy"),
            ("Balanced ⚖️", "balanced"),
            ("Hard 💪", "hard")
        ]
        
        for text, value in difficulties:
            rb = tk.Radiobutton(
                diff_frame,
                text=text,
                variable=self.difficulty,
                value=value,
                font=("Helvetica", 9),
                bg=self.bg_color,
                fg=self.fg_color,
                selectcolor=self.button_color,
                activebackground=self.bg_color,
                activeforeground=self.accent_color,
                command=self._on_difficulty_change
            )
            rb.pack(side=tk.LEFT, padx=5)
        
    def _on_difficulty_change(self):
        """Handle difficulty change"""
        if not self.game_started:
            # Update agent with new difficulty
            self.agent = AdaptiveAgent(use_all_layers=True, difficulty=self.difficulty.get())
            self.manager = MatchManager(self.player, self.agent)
        
    def _create_scoreboard(self):
        """Create scoreboard display"""
        score_frame = tk.Frame(self.root, bg=self.bg_color)
        score_frame.pack(pady=15)
        
        # Player score
        player_frame = tk.Frame(score_frame, bg=self.button_color, relief=tk.RAISED, bd=2)
        player_frame.grid(row=0, column=0, padx=10)
        
        tk.Label(
            player_frame, 
            text="PLAYER",
            font=("Helvetica", 12, "bold"),
            bg=self.button_color,
            fg=self.success_color,
            padx=20,
            pady=5
        ).pack()
        
        self.player_score_label = tk.Label(
            player_frame,
            text="0",
            font=("Helvetica", 32, "bold"),
            bg=self.button_color,
            fg=self.fg_color,
            padx=20,
            pady=10
        )
        self.player_score_label.pack()
        
        # VS Label
        vs_label = tk.Label(
            score_frame,
            text="VS",
            font=("Helvetica", 16, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        vs_label.grid(row=0, column=1, padx=10)
        
        # AI score
        ai_frame = tk.Frame(score_frame, bg=self.button_color, relief=tk.RAISED, bd=2)
        ai_frame.grid(row=0, column=2, padx=10)
        
        tk.Label(
            ai_frame,
            text="AI",
            font=("Helvetica", 12, "bold"),
            bg=self.button_color,
            fg=self.error_color,
            padx=20,
            pady=5
        ).pack()
        
        self.ai_score_label = tk.Label(
            ai_frame,
            text="0",
            font=("Helvetica", 32, "bold"),
            bg=self.button_color,
            fg=self.fg_color,
            padx=20,
            pady=10
        )
        self.ai_score_label.pack()
        
    def _create_game_info(self):
        """Create game information display"""
        info_frame = tk.Frame(self.root, bg=self.button_color, relief=tk.RIDGE, bd=2)
        info_frame.pack(pady=10, padx=50, fill=tk.X)
        
        self.innings_label = tk.Label(
            info_frame,
            text="Press 'New Match' to start",
            font=("Helvetica", 11),
            bg=self.button_color,
            fg=self.accent_color,
            pady=8
        )
        self.innings_label.pack()
        
        self.batting_label = tk.Label(
            info_frame,
            text="",
            font=("Helvetica", 10, "italic"),
            bg=self.button_color,
            fg=self.fg_color,
            pady=5
        )
        self.batting_label.pack()
        
    def _create_move_buttons(self):
        """Create move selection buttons"""
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=20)
        
        tk.Label(
            button_frame,
            text="Choose your move:",
            font=("Helvetica", 12, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(pady=10)
        
        # Create 6 buttons in a row
        moves_frame = tk.Frame(button_frame, bg=self.bg_color)
        moves_frame.pack()
        
        self.move_buttons = []
        for i in range(1, 7):
            btn = tk.Button(
                moves_frame,
                text=str(i),
                font=("Helvetica", 18, "bold"),
                width=4,
                height=2,
                bg=self.button_color,
                fg=self.fg_color,
                activebackground=self.button_hover,
                activeforeground=self.accent_color,
                relief=tk.RAISED,
                bd=3,
                cursor="hand2",
                command=lambda move=i: self._make_move(move),
                state=tk.DISABLED
            )
            btn.grid(row=0, column=i-1, padx=5)
            self.move_buttons.append(btn)
            
            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.button_hover))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.button_color))
    
    def _create_message_area(self):
        """Create message display area"""
        msg_frame = tk.Frame(self.root, bg=self.bg_color)
        msg_frame.pack(pady=15, padx=50, fill=tk.BOTH, expand=True)
        
        tk.Label(
            msg_frame,
            text="Game Log:",
            font=("Helvetica", 10, "bold"),
            bg=self.bg_color,
            fg=self.fg_color,
            anchor=tk.W
        ).pack(anchor=tk.W)
        
        # Scrolled text for messages
        text_frame = tk.Frame(msg_frame, bg=self.button_color, relief=tk.SUNKEN, bd=2)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.message_text = tk.Text(
            text_frame,
            height=8,
            font=("Courier", 10),
            bg=self.button_color,
            fg=self.fg_color,
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.message_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.message_text.yview)
        
    def _create_control_buttons(self):
        """Create control buttons"""
        control_frame = tk.Frame(self.root, bg=self.bg_color)
        control_frame.pack(pady=10)
        
        self.new_match_btn = tk.Button(
            control_frame,
            text="🎮 New Match",
            font=("Helvetica", 12, "bold"),
            bg=self.success_color,
            fg=self.bg_color,
            activebackground=self.button_hover,
            padx=20,
            pady=10,
            relief=tk.RAISED,
            bd=3,
            cursor="hand2",
            command=self._start_new_match
        )
        self.new_match_btn.grid(row=0, column=0, padx=10)
        
        quit_btn = tk.Button(
            control_frame,
            text="❌ Quit",
            font=("Helvetica", 12, "bold"),
            bg=self.error_color,
            fg=self.bg_color,
            activebackground=self.button_hover,
            padx=20,
            pady=10,
            relief=tk.RAISED,
            bd=3,
            cursor="hand2",
            command=self.root.quit
        )
        quit_btn.grid(row=0, column=1, padx=10)
        
    def _create_stats_area(self):
        """Create AI statistics display"""
        stats_frame = tk.Frame(self.root, bg=self.button_color, relief=tk.RIDGE, bd=2)
        stats_frame.pack(pady=10, padx=50, fill=tk.X)
        
        tk.Label(
            stats_frame,
            text="AI Statistics:",
            font=("Helvetica", 10, "bold"),
            bg=self.button_color,
            fg=self.accent_color,
            pady=5
        ).pack()
        
        self.stats_label = tk.Label(
            stats_frame,
            text="No predictions yet",
            font=("Courier", 9),
            bg=self.button_color,
            fg=self.fg_color,
            pady=5
        )
        self.stats_label.pack()
        
    def _add_message(self, message, color=None):
        """Add a message to the message area"""
        self.message_text.config(state=tk.NORMAL)
        if color:
            # Add colored text (simplified)
            self.message_text.insert(tk.END, message + "\n")
        else:
            self.message_text.insert(tk.END, message + "\n")
        self.message_text.see(tk.END)
        self.message_text.config(state=tk.DISABLED)
        
    def _start_new_match(self):
        """Start a new match"""
        # Reset components
        self.player.reset_history()
        self.agent.reset()
        
        # Ask who bats first
        result = messagebox.askquestion(
            "Toss", 
            "Do you want to bat first?",
            icon='question'
        )
        
        player_bats_first = (result == 'yes')
        
        # Start match
        toss_result = self.manager.start_new_match(player_bats_first=player_bats_first)
        
        self.game_started = True
        self.waiting_for_move = True
        
        # Enable move buttons
        for btn in self.move_buttons:
            btn.config(state=tk.NORMAL)
        
        # Clear messages
        self.message_text.config(state=tk.NORMAL)
        self.message_text.delete(1.0, tk.END)
        self.message_text.config(state=tk.DISABLED)
        
        # Add welcome message
        self._add_message("=" * 50)
        self._add_message("🎮 NEW MATCH STARTED 🎮")
        self._add_message("=" * 50)
        self._add_message(toss_result['message'])
        self._add_message("")
        
        # Update display
        self._update_display()
        
    def _make_move(self, move):
        """Handle player move"""
        if not self.game_started or not self.waiting_for_move:
            return
        
        self.waiting_for_move = False
        
        # Disable buttons temporarily
        for btn in self.move_buttons:
            btn.config(state=tk.DISABLED)
        
        # Play turn
        result = self.manager.play_turn(move)
        
        # Display moves
        self._add_message(f"Your move: {result['player_move']} | AI move: {result['ai_move']}")
        
        # Show AI prediction if available
        if len(self.agent.prediction_history) > 0:
            predicted = self.agent.prediction_history[-1]
            confidence = self.agent.confidence_scores[-1] if self.agent.confidence_scores else 0.0
            self._add_message(f"[AI predicted: {predicted} (confidence: {confidence:.2f})]")
        
        self._add_message(result['message'])
        
        # Update scores
        self._update_display()
        
        # Check for innings complete
        if result['innings_complete']:
            self._add_message("")
            self._add_message("=" * 50)
            self._add_message("⚡ INNINGS COMPLETE ⚡")
            self._add_message("=" * 50)
            state = result['game_state']
            score = state['player_score'] if not state['player_batting'] else state['ai_score']
            self._add_message(f"First innings score: {score}")
            self._add_message("")
            messagebox.showinfo("Innings Complete", f"First innings complete!\nScore: {score}\n\nStarting second innings...")
        
        # Check for game over
        if result['game_over']:
            self._game_over(result)
            return
        
        # Re-enable buttons
        self.waiting_for_move = True
        for btn in self.move_buttons:
            btn.config(state=tk.NORMAL)
        
        # Update stats
        self._update_stats()
        
    def _update_display(self):
        """Update score and game state display"""
        state = self.manager.get_current_state()
        
        # Update scores
        self.player_score_label.config(text=str(state['player_score']))
        self.ai_score_label.config(text=str(state['ai_score']))
        
        # Update innings info
        innings_text = f"Innings {state['current_innings']}/2"
        if state['target']:
            innings_text += f" | Target: {state['target']}"
        self.innings_label.config(text=innings_text)
        
        # Update batting status
        if state['player_batting']:
            self.batting_label.config(text="🏏 You are BATTING", fg=self.success_color)
        else:
            self.batting_label.config(text="⚾ You are BOWLING", fg=self.error_color)
    
    def _update_stats(self):
        """Update AI statistics display"""
        stats = self.agent.get_statistics()
        
        stats_text = (
            f"Predictions: {stats['total_predictions']} | "
            f"Accuracy: {stats['prediction_accuracy']:.1f}% | "
            f"Avg Confidence: {stats['average_confidence']:.3f}"
        )
        
        self.stats_label.config(text=stats_text)
        
    def _game_over(self, result):
        """Handle game over"""
        self.game_started = False
        self.waiting_for_move = False
        
        # Disable move buttons
        for btn in self.move_buttons:
            btn.config(state=tk.DISABLED)
        
        # Display game over message
        self._add_message("")
        self._add_message("=" * 50)
        self._add_message("🏁 GAME OVER 🏁")
        self._add_message("=" * 50)
        
        state = result['game_state']
        self._add_message(f"Final Score:")
        self._add_message(f"  Player: {state['player_score']}")
        self._add_message(f"  AI: {state['ai_score']}")
        self._add_message("")
        
        winner = result['winner']
        if winner == 'player':
            winner_msg = "🎉 CONGRATULATIONS! YOU WON! 🎉"
            title = "Victory!"
            msg = f"You won!\n\nPlayer: {state['player_score']}\nAI: {state['ai_score']}"
        elif winner == 'ai':
            winner_msg = "🤖 AI WINS! Better luck next time! 🤖"
            title = "Defeat"
            msg = f"AI won!\n\nPlayer: {state['player_score']}\nAI: {state['ai_score']}"
        else:
            winner_msg = "🤝 IT'S A TIE! 🤝"
            title = "Tie"
            msg = f"It's a tie!\n\nBoth scored: {state['player_score']}"
        
        self._add_message(winner_msg)
        
        # Show AI stats
        stats = self.agent.get_statistics()
        self._add_message(f"\nAI Statistics:")
        self._add_message(f"  Prediction Accuracy: {stats['prediction_accuracy']:.1f}%")
        self._add_message(f"  Total Predictions: {stats['total_predictions']}")
        self._add_message(f"  Average Confidence: {stats['average_confidence']:.3f}")
        
        # Update final stats
        self._update_stats()
        
        # Show messagebox
        play_again = messagebox.askyesno(title, msg + f"\n\nPlay again?")
        
        if play_again:
            self._start_new_match()


def run():
    """Run the GUI application"""
    root = tk.Tk()
    app = HandCricketGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run()
