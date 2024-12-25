import tkinter as tk
from tkinter import messagebox, ttk
from typing import Any, Dict

import sv_ttk


class FlipFlop:
    """Base class for flip flop """
    def __init__(self) -> None:
        self.state = 0 # Da defult state
        self.history: list[int] = [0]  # Da be track Historty 

    def clock(self, *args: Any) -> int:
        """Base clock"""
        raise NotImplementedError("Subclasses must implement clock method")

    def get_history(self) -> list[int]:
        """Return state history."""
        return self.history

    def _update_history(self) -> None:
        """Update state history"""
        self.history.append(self.state)
        # Keep last 10 states 
        if len(self.history) > 10:
            self.history.pop(0)

class DFlipFlop(FlipFlop):
    """D Flip Flop """
    def clock(self, d: int) -> int:
        """Update state based on D input"""
        self.state = d # b5ly lo a5trt sfr al state b 0
        self._update_history() # b3den b uptade el history
        return self.state

class JKFlipFlop(FlipFlop):
    """JK Flip Flop """
    def clock(self, j: int, k: int) -> int:
        if j == 1 and k == 1:
            self.state = 1 - self.state # b3ks al state
        elif j == 1:
            self.state = 1
        elif k == 1:
            self.state = 0
        self._update_history()
        return self.state

class TFlipFlop(FlipFlop):
    """T Flip Flop """
    def clock(self, t: int) -> int:
        if t == 1:
            self.state = 1 - self.state # Nfs Elkalm b3ks el state 
        self._update_history() 
        return self.state

class Flip_Flop_Simulator: # Da GUI We Ezay Elbrnamg besht5l
    """Main application"""
    
    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        self.master.title("Flip Flop Simulator")
        self.master.geometry("600x400")
        
        sv_ttk.set_theme("dark") # sv_ttk da bs 3shan el theme 
        self.create_styles()
        
        self.flip_flop_type = tk.StringVar(value="D")
        self.input_values: Dict[str, tk.IntVar] = {
            "D": tk.IntVar(),
            "J": tk.IntVar(),
            "K": tk.IntVar(),
            "T": tk.IntVar()
        }
        self.output_q = tk.StringVar(value="0")
        self.auto_clock = tk.BooleanVar(value=False)
        self.clock_count = tk.IntVar(value=0)
        
        self.flip_flops = { # B3rf el Flip Flops
            "D": DFlipFlop(),
            "JK": JKFlipFlop(),
            "T": TFlipFlop()
        }
        
        self.create_widgets()
        self.setup_keyboard_shortcuts()

    def create_styles(self) -> None:
        """Create styles"""
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Helvetica", 14, "bold"))
        style.configure("Output.TLabel", font=("Helvetica", 12))
        style.configure("History.TLabel", font=("Helvetica", 10))

    def create_widgets(self) -> None:
        """all GUI widgets"""
        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

       
        ttk.Label(main_frame, text="Flip Flop Simulator", style="Title.TLabel").grid(row=0, column=0, columnspan=4, pady=(0, 20))

        
        type_frame = ttk.LabelFrame(main_frame, text="Flip Flop Type", padding="10")
        type_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0, 10))
        
        for i, ff_type in enumerate(["D", "JK", "T"]):
            ttk.Radiobutton(type_frame, text=ff_type, variable=self.flip_flop_type, value=ff_type, 
                           command=self.update_inputs).grid(row=0, column=i, padx=20)

        
        self.input_frame = ttk.LabelFrame(main_frame, text="Inputs", padding="10")
        self.input_frame.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(0, 10))

        
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.grid(row=3, column=0, columnspan=4, sticky="ew", pady=(0, 10))

        ttk.Checkbutton(control_frame, text="Auto Clock", variable=self.auto_clock, 
                       command=self.toggle_auto_clock).grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="Clock Pulse", command=self.clock_pulse).grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="Reset", command=self.reset_simulation).grid(row=0, column=2, padx=5)

        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="10")
        output_frame.grid(row=4, column=0, columnspan=4, sticky="ew")
        
        ttk.Label(output_frame, text="State (Q):").grid(row=0, column=0, padx=5)
        ttk.Label(output_frame, textvariable=self.output_q, style="Output.TLabel").grid(row=0, column=1, padx=5)
        ttk.Label(output_frame, text="Clock Count:").grid(row=0, column=2, padx=5)
        ttk.Label(output_frame, textvariable=self.clock_count, style="Output.TLabel").grid(row=0, column=3, padx=5)

        self.history_label = ttk.Label(output_frame, text="", style="History.TLabel")
        self.history_label.grid(row=1, column=0, columnspan=4, pady=(10, 0))

        self.update_inputs()

    def setup_keyboard_shortcuts(self) -> None:
        """Configure keyboard shortcuts"""
        self.master.bind("<space>", lambda e: self.clock_pulse())
        self.master.bind("<r>", lambda e: self.reset_simulation())

    def create_input(self, input_name: str) -> None:
        """Create input controls for a specific input type"""
        frame = ttk.Frame(self.input_frame)
        frame.grid(row=0, column=len(self.input_frame.winfo_children()), padx=10)

        ttk.Label(frame, text=f"{input_name}:").grid(row=0, column=0, padx=5)
        ttk.Radiobutton(frame, text="0", variable=self.input_values[input_name], value=0).grid(row=0, column=1)
        ttk.Radiobutton(frame, text="1", variable=self.input_values[input_name], value=1).grid(row=0, column=2)

    def update_inputs(self) -> None:
        """Update input controls based on selected flip flop type"""
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        ff_type = self.flip_flop_type.get()
        if ff_type == "D":
            self.create_input("D")
        elif ff_type == "JK":
            self.create_input("J")
            self.create_input("K")
        else:
            self.create_input("T")

    def clock_pulse(self) -> None:
        """Process a clock pulse and update"""
        try:
            ff_type = self.flip_flop_type.get()
            ff = self.flip_flops[ff_type]

            if ff_type == "D":
                q = ff.clock(self.input_values["D"].get())
            elif ff_type == "JK":
                q = ff.clock(self.input_values["J"].get(), self.input_values["K"].get())
            else:
                q = ff.clock(self.input_values["T"].get())

            self.output_q.set(str(q))
            self.clock_count.set(self.clock_count.get() + 1)
            self.update_history_display(ff)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_history_display(self, ff: FlipFlop) -> None:
        """Update the history display with recent states"""
        history = ff.get_history()
        history_str = "History: " + " → ".join(map(str, history))
        self.history_label.config(text=history_str)

    def toggle_auto_clock(self) -> None:
        """Toggle automatic clock pulsing."""
        if self.auto_clock.get():
            self.auto_clock_pulse()

    def auto_clock_pulse(self) -> None:
        """Generate automatic clock pulses"""
        if self.auto_clock.get():
            self.clock_pulse()
            self.master.after(1000, self.auto_clock_pulse)

    def reset_simulation(self) -> None:
        """Reset the simulation state"""
        self.clock_count.set(0)
        ff_type = self.flip_flop_type.get()
        self.flip_flops[ff_type] = self.flip_flops[ff_type].__class__()
        self.output_q.set("0")
        self.auto_clock.set(False)
        self.update_history_display(self.flip_flops[ff_type])

def main() -> None:
    root = tk.Tk()
    app = Flip_Flop_Simulator(root)
    root.mainloop()
    

if __name__ == "__main__":
    main()