import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import string
import pyperclip  # For clipboard functionality
import hashlib
import json
import os
from datetime import datetime

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator Pro")
        self.root.geometry("700x750")
        self.root.configure(bg='#f0f0f0')
    
        self.password_history = []
        self.history_limit = 20
        
        # Load history from file
        self.load_history()
        
        # Create UI elements
        self.create_widgets()
        
        # Set initial values
        self.length_var.set(16)
        self.update_strength_indicator()
        
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="🔐 Password Generator Pro", 
                              font=('Arial', 24, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Password display frame
        display_frame = tk.LabelFrame(main_frame, text="Generated Password", 
                                     font=('Arial', 10, 'bold'), bg='#f0f0f0', fg='#34495e')
        display_frame.pack(fill=tk.X, pady=(0, 20))

          # Copy button
        copy_btn = tk.Button(display_frame, text="📋 Copy to Clipboard", 
                            command=self.copy_to_clipboard, bg='#3498db', fg='white',
                            font=('Arial', 10, 'bold'), bd=0, padx=15, pady=8)
        copy_btn.pack(pady=(0, 10))
        
        # Password display
        self.password_var = tk.StringVar()
        password_entry = tk.Entry(display_frame, textvariable=self.password_var, 
                                 font=('Courier', 14), bd=0, bg='#ecf0f1', 
                                 fg='#2c3e50', justify='center', state='readonly')
        password_entry.pack(fill=tk.X, padx=10, pady=10, ipady=8)
        
      
        # Settings frame
        settings_frame = tk.LabelFrame(main_frame, text="Password Settings", 
                                      font=('Arial', 10, 'bold'), bg='#f0f0f0', fg='#34495e')
        settings_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Password length
        length_frame = tk.Frame(settings_frame, bg='#f0f0f0')
        length_frame.pack(fill=tk.X, padx=10, pady=10)
        
        length_label = tk.Label(length_frame, text="Length:", 
                               font=('Arial', 11), bg='#f0f0f0', fg='#2c3e50', width=12, anchor='w')
        length_label.pack(side=tk.LEFT)
        
        self.length_var = tk.IntVar(value=16)
        length_scale = tk.Scale(length_frame, from_=6, to=50, variable=self.length_var, 
                               orient=tk.HORIZONTAL, length=300, bg='#f0f0f0', 
                               fg='#2c3e50', highlightthickness=0)
        length_scale.pack(side=tk.LEFT, padx=(10, 0))
        
        length_value = tk.Label(length_frame, textvariable=self.length_var, 
                               font=('Arial', 11, 'bold'), bg='#f0f0f0', fg='#e74c3c', width=3)
        length_value.pack(side=tk.LEFT, padx=(10, 0))
        
        # Character types
        char_frame = tk.Frame(settings_frame, bg='#f0f0f0')
        char_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.use_uppercase = tk.BooleanVar(value=True)
        uppercase_cb = tk.Checkbutton(char_frame, text="Uppercase Letters (A-Z)", 
                                     variable=self.use_uppercase, bg='#f0f0f0',
                                     font=('Arial', 10))
        uppercase_cb.pack(anchor='w', pady=2)
        
        self.use_lowercase = tk.BooleanVar(value=True)
        lowercase_cb = tk.Checkbutton(char_frame, text="Lowercase Letters (a-z)", 
                                     variable=self.use_lowercase, bg='#f0f0f0',
                                     font=('Arial', 10))
        lowercase_cb.pack(anchor='w', pady=2)
        
        self.use_digits = tk.BooleanVar(value=True)
        digits_cb = tk.Checkbutton(char_frame, text="Digits (0-9)", 
                                  variable=self.use_digits, bg='#f0f0f0',
                                  font=('Arial', 10))
        digits_cb.pack(anchor='w', pady=2)
        
        self.use_symbols = tk.BooleanVar(value=True)
        symbols_cb = tk.Checkbutton(char_frame, text="Symbols (!@#$%^&*)", 
                                   variable=self.use_symbols, bg='#f0f0f0',
                                   font=('Arial', 10))
        symbols_cb.pack(anchor='w', pady=2)
        
        # Exclude similar characters
        self.exclude_similar = tk.BooleanVar(value=False)
        similar_cb = tk.Checkbutton(char_frame, text="Exclude similar characters (i, l, 1, L, o, 0, O)", 
                                   variable=self.exclude_similar, bg='#f0f0f0',
                                   font=('Arial', 10))
        similar_cb.pack(anchor='w', pady=2)
        
        # Exclude ambiguous characters
        self.exclude_ambiguous = tk.BooleanVar(value=False)
        ambiguous_cb = tk.Checkbutton(char_frame, text="Exclude ambiguous characters ({[()]}, ;: ,  < >)", 
                                     variable=self.exclude_ambiguous, bg='#f0f0f0',
                                     font=('Arial', 10))
        ambiguous_cb.pack(anchor='w', pady=2)
        
        # Password strength indicator
        strength_frame = tk.Frame(settings_frame, bg='#f0f0f0')
        strength_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        strength_label = tk.Label(strength_frame, text="Strength:", 
                                 font=('Arial', 11), bg='#f0f0f0', fg='#2c3e50', width=12, anchor='w')
        strength_label.pack(side=tk.LEFT)
        
        self.strength_bar = ttk.Progressbar(strength_frame, length=300, mode='determinate')
        self.strength_bar.pack(side=tk.LEFT, padx=(10, 0))
        
        self.strength_text = tk.Label(strength_frame, text="", font=('Arial', 10, 'bold'), 
                                     bg='#f0f0f0', width=15)
        self.strength_text.pack(side=tk.LEFT, padx=(10, 0))
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg='#f0f0f0')
        buttons_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Generate button
        generate_btn = tk.Button(buttons_frame, text="🔄 Generate Password", 
                                command=self.generate_password, bg='#2ecc71', fg='white',
                                font=('Arial', 12, 'bold'), bd=0, padx=20, pady=12)
        generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear button
        clear_btn = tk.Button(buttons_frame, text="🗑️ Clear", 
                             command=self.clear_password, bg='#e74c3c', fg='white',
                             font=('Arial', 12, 'bold'), bd=0, padx=20, pady=12)
        clear_btn.pack(side=tk.LEFT)
        
        # History frame
        history_frame = tk.LabelFrame(main_frame, text="Password History", 
                                     font=('Arial', 10, 'bold'), bg='#f0f0f0', fg='#34495e')
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        # History text area
        self.history_text = scrolledtext.ScrolledText(history_frame, height=8, 
                                                     font=('Courier', 9), wrap=tk.WORD)
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # History buttons frame
        history_buttons_frame = tk.Frame(history_frame, bg='#f0f0f0')
        history_buttons_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Clear history button
        clear_history_btn = tk.Button(history_buttons_frame, text="Clear History", 
                                     command=self.clear_history, bg='#95a5a6', fg='white',
                                     font=('Arial', 10), bd=0, padx=15, pady=6)
        clear_history_btn.pack(side=tk.LEFT)
        
        # Export history button
        export_btn = tk.Button(history_buttons_frame, text="Export History", 
                              command=self.export_history, bg='#9b59b6', fg='white',
                              font=('Arial', 10), bd=0, padx=15, pady=6)
        export_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to generate passwords")
        status_bar = tk.Label(main_frame, textvariable=self.status_var, 
                             bd=1, relief=tk.SUNKEN, anchor=tk.W, 
                             bg='#34495e', fg='white', font=('Arial', 9))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Load history into text widget
        self.update_history_display()
        
    def generate_password(self):
        # Get settings
        length = self.length_var.get()
        use_upper = self.use_uppercase.get()
        use_lower = self.use_lowercase.get()
        use_digits = self.use_digits.get()
        use_symbols = self.use_symbols.get()
        exclude_similar = self.exclude_similar.get()
        exclude_ambiguous = self.exclude_ambiguous.get()
        
        # Check if at least one character type is selected
        if not (use_upper or use_lower or use_digits or use_symbols):
            messagebox.showerror("Error", "Please select at least one character type!")
            return
        
        # Define character pools
        upper_chars = string.ascii_uppercase
        lower_chars = string.ascii_lowercase
        digit_chars = string.digits
        symbol_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Handle exclusions
        if exclude_similar:
            similar_chars = "il1Lo0O"
            upper_chars = ''.join(c for c in upper_chars if c not in similar_chars)
            lower_chars = ''.join(c for c in lower_chars if c not in similar_chars)
            digit_chars = ''.join(c for c in digit_chars if c not in similar_chars)
        
        if exclude_ambiguous:
            ambiguous_chars = "{}[]()/\\'\"`~,;:.<>"
            symbol_chars = ''.join(c for c in symbol_chars if c not in ambiguous_chars)
        
        # Build character pool based on selections
        char_pool = ""
        if use_upper:
            char_pool += upper_chars
        if use_lower:
            char_pool += lower_chars
        if use_digits:
            char_pool += digit_chars
        if use_symbols:
            char_pool += symbol_chars
        
        # Check if character pool is empty
        if not char_pool:
            messagebox.showerror("Error", "Character pool is empty! Please adjust your settings.")
            return
        
        # Generate password
        try:
            # Ensure we have at least one character from each selected type
            password_chars = []
            
            if use_upper and upper_chars:
                password_chars.append(random.choice(upper_chars))
            if use_lower and lower_chars:
                password_chars.append(random.choice(lower_chars))
            if use_digits and digit_chars:
                password_chars.append(random.choice(digit_chars))
            if use_symbols and symbol_chars:
                password_chars.append(random.choice(symbol_chars))
            
            # Fill the rest with random characters from the pool
            remaining_length = length - len(password_chars)
            if remaining_length > 0:
                password_chars.extend(random.choices(char_pool, k=remaining_length))
            
            # Shuffle the characters
            random.shuffle(password_chars)
            
            # Create the final password
            password = ''.join(password_chars)
            
            # Set the password
            self.password_var.set(password)
            
            # Add to history
            self.add_to_history(password)
            
            # Update strength indicator
            self.update_strength_indicator()
            
            # Update status
            self.status_var.set(f"Password generated with {length} characters")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate password: {str(e)}")
    
    def add_to_history(self, password):
        # Create a hash of the password (for display safety)
        password_hash = hashlib.sha256(password.encode()).hexdigest()[:8]
        
        # Create history entry
        entry = {
            'password': password,
            'hash': password_hash,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'length': len(password)
        }
        
        # Add to history
        self.password_history.insert(0, entry)
        
        # Limit history size
        if len(self.password_history) > self.history_limit:
            self.password_history = self.password_history[:self.history_limit]
        
        # Update history display
        self.update_history_display()
        
        # Save history to file
        self.save_history()
    
    def update_history_display(self):
        # Clear the text widget
        self.history_text.delete(1.0, tk.END)
        
        # Add history entries
        for i, entry in enumerate(self.password_history):
            # Display masked password (show first 2 and last 2 chars)
            pwd = entry['password']
            if len(pwd) > 4:
                masked = f"{pwd[:2]}{'*' * (len(pwd)-4)}{pwd[-2:]}"
            else:
                masked = "*" * len(pwd)
            
            # Add entry to text widget
            self.history_text.insert(tk.END, 
                                   f"{i+1:2}. {masked} | Length: {entry['length']:2} | {entry['timestamp']}\n")
    
    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            try:
                pyperclip.copy(password)
                self.status_var.set("Password copied to clipboard!")
                
                # Show a temporary message
                messagebox.showinfo("Copied", "Password has been copied to clipboard!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to copy to clipboard: {str(e)}")
        else:
            messagebox.showwarning("Warning", "No password to copy!")
    
    def clear_password(self):
        self.password_var.set("")
        self.status_var.set("Password cleared")
    
    def clear_history(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear the password history?"):
            self.password_history = []
            self.update_history_display()
            self.save_history()
            self.status_var.set("Password history cleared")
    
    def export_history(self):
        if not self.password_history:
            messagebox.showinfo("Info", "No password history to export!")
            return
        
        # Create a simple text export
        export_text = "Password Generator Pro - Password History\n"
        export_text += "=" * 50 + "\n\n"
        
        for i, entry in enumerate(self.password_history):
            export_text += f"{i+1}. Password: {entry['password']} | Length: {entry['length']} | Generated: {entry['timestamp']}\n"
        
        # Show in a dialog
        export_window = tk.Toplevel(self.root)
        export_window.title("Export Password History")
        export_window.geometry("600x500")
        export_window.configure(bg='#f0f0f0')
        
        text_widget = scrolledtext.ScrolledText(export_window, wrap=tk.WORD, font=('Courier', 10))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, export_text)
        text_widget.configure(state='disabled')
        
        # Add a copy button
        copy_btn = tk.Button(export_window, text="Copy to Clipboard", 
                           command=lambda: pyperclip.copy(export_text), 
                           bg='#3498db', fg='white', font=('Arial', 10, 'bold'))
        copy_btn.pack(pady=(0, 10))
    
    def update_strength_indicator(self):
        password = self.password_var.get()
        if not password:
            self.strength_bar['value'] = 0
            self.strength_text.config(text="", fg='black')
            return
        
        length = len(password)
        
        # Calculate strength based on length and character variety
        strength = 0
        
        # Length factor (max 50 points)
        strength += min(length * 2, 50)
        
        # Character variety (max 50 points)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(not c.isalnum() for c in password)
        
        variety_score = 0
        if has_upper:
            variety_score += 10
        if has_lower:
            variety_score += 10
        if has_digit:
            variety_score += 15
        if has_symbol:
            variety_score += 15
        
        strength += variety_score
        
        # Update progress bar
        self.strength_bar['value'] = strength
        
        # Update text and color
        if strength < 30:
            strength_label = "Weak"
            color = '#e74c3c'  # Red
        elif strength < 60:
            strength_label = "Fair"
            color = '#f39c12'  # Orange
        elif strength < 80:
            strength_label = "Good"
            color = '#3498db'  # Blue
        else:
            strength_label = "Strong"
            color = '#2ecc71'  # Green
        
        self.strength_text.config(text=strength_label, fg=color)
    
    def save_history(self):
        try:
            # Don't save the actual passwords for security
            safe_history = []
            for entry in self.password_history:
                safe_entry = entry.copy()
                # Don't save the actual password
                if 'password' in safe_entry:
                    del safe_entry['password']
                safe_history.append(safe_entry)
            
            with open('password_history.json', 'w') as f:
                json.dump(safe_history, f)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def load_history(self):
        try:
            if os.path.exists('password_history.json'):
                with open('password_history.json', 'r') as f:
                    self.password_history = json.load(f)
        except Exception as e:
            print(f"Error loading history: {e}")
            self.password_history = []

def main():
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
