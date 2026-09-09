#gui.py
import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.style as mplstyle
from matplotlib.animation import FuncAnimation
from PIL import ImageGrab
from tkinter import messagebox
import ctypes
import config
import sys
import os
from hsc_model import run_hsc_simulation

mplstyle.use("dark_background")

class HSCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hematopoietic Reconstitution Simulator")
        self.root.geometry("1200x800")

        #The Icon's features
        
        try:
          myappid = "HSCs.Simulator.app"
          ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
          pass
        if hasattr(sys, "_MEIPASS"):
           icon_path = os.path.join(sys._MEIPASS, "app_icon.ico")
        else:
           icon_path = os.path.join(os.path.abspath("."), 'app_icon.ico')
    
        if os.path.exists(icon_path):
           self.root.iconbitmap(icon_path)

        self.style = Style(theme="darkly")

        self.anim1 = None
        self.anim2 = None
        self.anim3 = None
        self.anim4 = None
        # Layout Main Frame
        main_frame = tb.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ---- Left Panel: Controls & Clinical Metrics ----
        control_panel = tb.LabelFrame(main_frame, text="Controls & Clinical Summary",bootstyle="primary", padding=15)
        control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Input Slider 
        tb.Label(control_panel, text="Transplanted HSCs Count: ", font=("Segoe UI", 10, "italic")).pack(anchor=tk.W, pady=(0,5)) 

        self.hsc_slider = tb.Scale(control_panel, from_=1000, to=70000,value=30000, orient=tk.HORIZONTAL, command=self.update_slider_label, bootstyle="info")
        self.hsc_slider.pack(fill=tk.X, pady=5)

        self.slider_val_label = tb.Label(control_panel, text="30,000 HSCs", font=("Segoe UI", 10, "italic"), bootstyle="warning")
        self.slider_val_label.pack(anchor=tk.W, pady=(0, 5))

        # Action Buttons Frame
        btn_frame = tb.Frame(control_panel)
        btn_frame.pack(fill=tk.X, pady=5)

        # Run Button
        run_btn = tb.Button(control_panel, text="⚡Run Simulation", command=self.run_simulation, bootstyle="success")
        run_btn.pack(fill=tk.X, pady=5)

        copy_btn = tb.Button(control_panel, text="📋Copy Text Report", bootstyle="info-outline", command=self.copy_report_to_clipboard)
        copy_btn.pack(fill=tk.X, pady=3)

        snap_btn = tb.Button(control_panel, text="📸Export Full Snapshot", bootstyle="warning-outline", command=self.take_snapshot)
        snap_btn.pack(fill=tk.X, pady=3)

        tb.Separator(control_panel, orient="horizontal").pack(fill="x", pady=15)

        # Report Text Display
        tb.Label(control_panel, text="Clinical Report", font=("Segoe UI", 11,"bold"), bootstyle="info").pack(anchor=tk.W, pady=(0, 5))
        self.report_text = tb.Text(control_panel, width=40, height=25, font=("Consolas", 9), bg="#1e1e1e", fg="#00ffc8", insertbackground="white", relief="flat" )
        self.report_text.pack(fill=tk.BOTH, expand=True)

        # ---- Right Panel: Notebook Tabs for Figures ----
        notebook_frame = tb.Frame(main_frame)
        notebook_frame.pack(side=tk.RIGHT,fill=tk.BOTH, expand=True)

        self.notebook = tb.Notebook(notebook_frame, bootstyle="primary")
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tab1 = tb.Frame(self.notebook, padding=10)
        self.tab2 = tb.Frame(self.notebook, padding=10)
        self.tab3 = tb.Frame(self.notebook, padding=10)
        self.tab4 = tb.Frame(self.notebook, padding=10)

        self.notebook.add(self.tab1, text="Fig 1: Stem & Primary Progenitors")
        self.notebook.add(self.tab2, text="Fig 2: Myeloid & Erythroid")
        self.notebook.add(self.tab3, text="Fig 3: Granulocytes & Adaptive")
        self.notebook.add(self.tab4, text="Fig 4: Low-Density Immune") 

        # Initial Simulation Run
        self.run_simulation()
    def apply_custom_figure_style(self, fig, axes):
        fig.patch.set_facecolor('#121212')
        axes_list = axes if isinstance(axes, (list, tuple, range)) or hasattr(axes, '__iter__') else [axes]
        for ax in axes_list:
            ax.set_facecolor('#1e1e1e')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#444444')
            ax.spines['bottom'].set_color('#444444')
            ax.tick_params(colors='#cccccc', which='both')
            ax.yaxis.label.set_color('#e0e0e0')
            ax.xaxis.label.set_color('#e0e0e0')
            ax.title.set_color('#00e6c3')

    def update_slider_label(self, val):
        count = int(float(val))
        self.slider_val_label.config(text=f"{count:,} HSCs")

    def clear_previous_animations(self):
        for anim in [self.anim1, self.anim2, self.anim3, self.anim4]:
            if anim is not None:
                try:
                    anim.event_source.stop()
                except Exception:
                    pass

        self.anim1 = None
        self.anim2 = None
        self.anim3 = None
        self.anim4 = None

    def run_simulation(self):
        self.clear_previous_animations()

        hsc_input = int(self.hsc_slider.get())
        history, recovery_day, total_monitored_days = run_hsc_simulation(hsc_input)

        # Update Report Box
        self.report_text.delete("1.0", tk.END)
        report = f"---- CLINICAL SUMMARY ----\n"
        report += f"Transplanted HSCs Count   : {hsc_input:,}\n" 
        report += f"Total Monitored Period    : {total_monitored_days - 1} Days\n"
        if recovery_day is not None:
            report +=f"Full Capacity Reached Day : Day {recovery_day}\n"
        else:
            report += f"Full Capacity Reached Day : Not Reached within monitoring timeframe\n"
        report += "-"*28 + "\n"
        report += "Final Cell Counts at Day 365:\n"
        report += f"• HSC Pool      : {history['hsc'][-1]:,.0f}\n"
        report += f"• RBCs          : {history['rbc'][-1]:,.0f}\n"
        report += f"• Platelets     : {history['platelets'][-1]:,.0f}\n"
        report += f"• Neutrophils   : {history['neutrophils'][-1]:,.0f}\n"
        report += f"• Eosinophils   : {history['eosinophils'][-1]:,.0f}\n"
        report += f"• Basophils     : {history['basophils'][-1]:,.0f}\n"
        report += f"• Monocytes     : {history['monocytes'][-1]:,.0f}\n"
        report += f"• cDC           : {history['cdc'][-1]:,.0f}\n"
        report += f"• pDC           : {history['pdc'][-1]:,.0f}\n"
        report += f"• B Cells       : {history['b_cells'][-1]:,.0f}\n"
        report += f"• T Cells       : {history['t_cells'][-1]:,.0f}\n"
        report += f"• NK Cells      : {history['nk_cells'][-1]:,.0f}\n"

        self.report_text.insert(tk.END, report)

        # Plot Figures into Tabs
        self.plot_figure_1(history, recovery_day)
        self.plot_figure_2(history)
        self.plot_figure_3(history)
        self.plot_figure_4(history)

    def clear_tab(self, tab):
        for widget in tab.winfo_children():
            widget.destroy()

    def copy_report_to_clipboard(self):
        content = self.report_text.get("1.0", tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        messagebox.showinfo("Copied!", "Clinical Report text copied to clipboard successfully.")

    def take_snapshot(self):
        try:
           self.root.update_idletasks()
           try:
              scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100.0
           except Exception:
              scale_factor = 1.0


           x = int(self.root.winfo_rootx() * scale_factor)
           y = int(self.root.winfo_rooty() * scale_factor)
           w = int(self.root.winfo_width() * scale_factor)
           h = int(self.root.winfo_height() * scale_factor)

           img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
           img.save("snapshot.png")
           messagebox.showinfo("Saved!", "Snapshot saved as snapshot.png")
        except Exception as e:
           messagebox.showerror("Error", f"Failed to take snapshot: {str(e)}")


    def embed_canvas(self, fig, tab):
        self.clear_tab(tab)
        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, tab)
        toolbar.update()
        bg_color = "#222222"
        fg_color = "#ffffff"
        toolbar.config(background=bg_color)
        for child in toolbar.winfo_children():
         try:
            child.config(background="#222222", activebackground="#444444")
         except Exception:
           pass
        for button in toolbar.winfo_children():
            if isinstance(button, tk.Button):
                button.config(background=bg_color,
                              state="normal",
                              activebackground="#333333",
                              relief= "flat",
                              bd=0,
                              highlightthickness=0)
        
        canvas.get_tk_widget().pack(fill= tk.BOTH, expand=True)

    def plot_figure_1(self, history, recovery_day):
        fig1, axes1 = plt.subplots(2,1,figsize=(8,6), sharex=True)
        self.apply_custom_figure_style(fig1, axes1)
        fig1.suptitle("Figure 1: Bone Marrow Stem & Primary Progenitor Kinetics", fontsize=11, fontweight="bold", color="#00e6c3")

        total_frames = len(history["days"])
        interval_ms = max(1, round(30000 / total_frames))

        for ax in axes1:
            ax.set_xlim(0,max(history["days"]))
            ax.minorticks_on()
            ax.grid(which='major', linestyle='-', linewidth=0.7, alpha=0.5) 
            ax.grid(which='minor', linestyle='--', linewidth=0.4, alpha=0.3)

        axes1[0].set_ylim(0,110000)
        axes1[1].set_ylim(0, max(max(history["cmp"]), max(history["clp"])) * 1.1 if max(history["cmp"]) > 0 else 100)

        # Subplot 1.1: Stem and Progenitor Kinetics
        line1, = axes1[0].plot([],[], color="r", linewidth=2,label="HSC Pool (R)")
        axes1[0].axhline(y=config.HSC_TARGET_CAPACITY, color="g", linestyle="--", label="Target Capacity 50,000 or 100,000")
        if recovery_day:
           axes1[0].axvline(x=recovery_day, color="orange", linestyle=":", label=f"Full Recovery (Day {recovery_day})")

        axes1[0].set_ylabel("Number of HSCs")
        axes1[0].set_title("Clinical HSCs Recovery & Post-Transplant Homeostasis Diagram")
        axes1[0].legend(loc="upper left", facecolor="#1e1e1e", edgecolor="none")

        # Subplot 1.2: Primary Progenitors
        line2, = axes1[1].plot([],[], color="purple", linewidth=2, label="CMP (Myeloid Branch)")
        line3, = axes1[1].plot([],[], color="blue", linewidth=2, label="CLP (Lymphoid Branch)")
        axes1[1].set_title("Primary Progenitors")
        axes1[1].set_ylabel("Primary Progenitors")
        axes1[1].legend(loc="upper left", facecolor="#1e1e1e", edgecolor="none")

        def animate(frame):
            x = history["days"][:frame]
            line1.set_data(x, history["hsc"][:frame])
            line2.set_data(x, history["cmp"][:frame])
            line3.set_data(x, history["clp"][:frame])
            return line1, line2, line3
        self.anim1 = FuncAnimation(fig1, animate, frames=total_frames + 1, interval=interval_ms, blit=True, repeat=False)
        fig1.tight_layout(rect=[0, 0, 1, 0.96])
        self.embed_canvas(fig1, self.tab1)

    def plot_figure_2(self, history):
        fig2,axes2 = plt.subplots(2,1, figsize=(8,6), sharex=True)
        self.apply_custom_figure_style(fig2, axes2)
        fig2.suptitle("Figure 2: Sub-Progenitors & Erythroid/Platelets", fontsize=11, fontweight="bold", color="#00e6c3")

        total_frames = len(history["days"])
        interval_ms = max(1, round(30000 / total_frames))

        for ax in axes2:
            ax.set_xlim(0, max(history["days"]))
            ax.minorticks_on()
            ax.grid(which='major', linestyle='-', linewidth=0.7, alpha=0.5) 
            ax.grid(which='minor', linestyle="--", linewidth=0.4, alpha=0.3)

        axes2[0].set_ylim(0, max(max(history["mep"]), max(history["gmp"])) * 1.1 if max(history["mep"]) > 0 else 100)
        axes2[1].set_ylim(0, max(max(history["rbc"]), max(history["platelets"])) * 1.1 if max(history["rbc"]) > 0 else 100)

        # Subplot 2.1: Secondary Progenitors Myeloid Branch
        line1, = axes2[0].plot([], [], color="darkred", linewidth=2,label="MEP (Erythrocyte/Megakaryocyte)")
        line2, = axes2[0].plot([], [], color="orange", linewidth=2, label="GMP (Granulocyte/Monocyte)")
        axes2[0].set_ylabel("Myeloid Lineages")
        axes2[0].set_title("Myeloid Sub-Lineage Branching (MEP & GMP)")
        axes2[0].legend(loc="upper left")

        # Subplot 2.2: Erythrocytes & Plateles (High Volume Lineages)
        line3, = axes2[1].plot([], [], color="r", linewidth=2, label="Erythrocytes (RBCs)")
        line4, = axes2[1].plot([], [], color="darkorange", linewidth=2, label="Platelets")
        axes2[1].set_ylabel("Cell Count")
        axes2[1].set_title("Erythroid & Thromboid Recovery (RBCs & Platelets)")
        axes2[1].legend(loc="upper left", facecolor="#1e1e1e", edgecolor="none")

        def animate(frame):
            x = history["days"][:frame]
            line1.set_data(x, history["mep"][:frame])
            line2.set_data(x, history["gmp"][:frame])
            line3.set_data(x, history["rbc"][:frame])
            line4.set_data(x, history["platelets"][:frame])
            return line1, line2, line3, line4
        self.anim2 = FuncAnimation(fig2, animate, frames=total_frames + 1, interval = interval_ms, blit=True, repeat = False)
        fig2.tight_layout(rect=[0, 0, 1, 0.96])
        self.embed_canvas(fig2, self.tab2)

    def plot_figure_3(self, history):
        fig3,axes3 = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
        self.apply_custom_figure_style(fig3, axes3)
        fig3.suptitle("Figure 3: Innate Granulocyte & Adaptive Immune Reconstitution", fontsize=11, fontweight="bold", color="#00e6c3")

        total_frames = len(history["days"])
        interval_ms = max(1, round(30000/total_frames))
        for ax in axes3:
            ax.set_xlim(0, max(history["days"]))
            ax.minorticks_on()
            ax.grid(which='major', linestyle='-', linewidth=0.7, alpha=0.5) 
            ax.grid(which='minor', linestyle="--", linewidth=0.4, alpha=0.3)

        axes3[0].set_ylim(0, max(max(history["neutrophils"]), max(history["monocytes"])) * 1.1 if max(history["neutrophils"]) > 0 else 100)
        axes3[1].set_ylim(0, max(max(history["t_cells"]), max(history["b_cells"])) * 1.1 if max(history["b_cells"]) > 0 else 100)

        # Subplot 3.1: Innate Immune / Granulocyte Lineages
        line1, = axes3[0].plot([], [], color="#448aff", linewidth=2, label="Neutrophils")
        line2, = axes3[0].plot([], [], color="#69f0ae", linewidth=2, label="Eosinophils")
        line3, = axes3[0].plot([], [], color="#7c4dff", linewidth=2, label="Basophils")
        line4, = axes3[0].plot([], [], color="#ff5252", linewidth=2, label = "Monocytes")
        line5, = axes3[0].plot([], [], color="#ffd740", linewidth=2, label = "Convential Dendritic Cells")
        line6, = axes3[0].plot([], [], color="#ff4081", linewidth=2, label = "Plasmacytoid Dendritic Cells")
        axes3[0].set_ylabel("Cell Count")
        axes3[0].set_title("Innate Immune & Granulocyte Recovery")
        axes3[0].legend(loc="upper left", facecolor="#1e1e1e", edgecolor="none")


        # Subplot 3.2: Adaptive Immune / Lymphoid Lineages
        line7, = axes3[1].plot([], [], color="#e040fb", linewidth=2, label="B Lymphocytes")
        line8, = axes3[1].plot([], [], color="#1de9b6", linewidth=2, label="T Lymphocytes")
        line9, = axes3[1].plot([], [], color="#00b0ff", linewidth=2, label="NK Lymphocytes")
        axes3[1].set_ylabel("Cell Count")
        axes3[1].set_title("Adaptive Immune Reconstitution (Lymphoid Lineages)")
        axes3[1].legend(loc="upper left", facecolor="#1e1e1e", edgecolor="none")

        def animate(frame):
            x = history["days"][:frame]
            line1.set_data(x, history["neutrophils"][:frame])
            line2.set_data(x, history["eosinophils"][:frame])
            line3.set_data(x, history["basophils"][:frame])
            line4.set_data(x, history["monocytes"][:frame])
            line5.set_data(x, history["cdc"][:frame])
            line6.set_data(x, history["pdc"][:frame])
            line7.set_data(x, history["b_cells"][:frame])
            line8.set_data(x, history["t_cells"][:frame])
            line9.set_data(x, history["nk_cells"][:frame])

            return line1,line2,line3,line4,line5,line6,line7,line8,line9
        self.anim3 = FuncAnimation(fig3, animate, frames=total_frames + 1, interval=interval_ms, blit=True, repeat=False)
        fig3.tight_layout(rect=[0, 0, 1, 0.96])
        self.embed_canvas(fig3, self.tab3)

    # Tab 4: 2 Graphs (Magnified Low-Density Immune Sub-Lineages)
    def plot_figure_4(self, history):
        fig4, axes4 = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
        self.apply_custom_figure_style(fig4, axes4)
        fig4.suptitle("Figure 4: Low-Density Immune Sub-Lineages (Magnified View)", fontsize=11, fontweight="bold", color="#00e6c3")

        total_frames = len(history["days"])
        interval_ms = max(1, round(30000 / total_frames))

        for ax in axes4:
            ax.set_xlim(0, max(history["days"]))
            ax.minorticks_on()
            ax.grid(which='major', linestyle='-', linewidth=0.6, alpha=0.3, color='#555555')
            ax.grid(which='minor', linestyle='--', linewidth=0.3, alpha=0.15, color='#444444')

        
        max_graph1 = max(max(history["monocytes"]), max(history["eosinophils"]), max(history["nk_cells"]))
        max_graph2 = max(max(history["basophils"]), max(history["cdc"]), max(history["pdc"]))

        axes4[0].set_ylim(0, max_graph1 * 1.15 if max_graph1 > 0 else 100)
        axes4[1].set_ylim(0, max_graph2 * 1.15 if max_graph2 > 0 else 100)

        # Graph 1: Monocytes, Eosinophils & NK Lymphocytes
        line1, = axes4[0].plot([], [], color="#ff5252", linewidth=2, label="Monocytes")
        line2, = axes4[0].plot([], [], color="#69f0ae", linewidth=2, label="Eosinophils")
        line3, = axes4[0].plot([], [], color="#00b0ff", linewidth=2, label="NK Lymphocytes")
        axes4[0].set_ylabel("Cell Count")
        axes4[0].set_title("Low-Density Myeloid & NK Lineages")
        axes4[0].legend(loc="upper left", facecolor='#1e1e1e', edgecolor='none')

        # Graph 2: Basophils & Dendritic Cells (cDC, pDC)
        line4, = axes4[1].plot([], [], color="#7c4dff", linewidth=2, label="Basophils")
        line5, = axes4[1].plot([], [], color="#ffd740", linewidth=2, label="cDC")
        line6, = axes4[1].plot([], [], color="#ff4081", linewidth=2, label="pDC")
        axes4[1].set_xlabel("Days Post-Transplantation")
        axes4[1].set_ylabel("Cell Count")
        axes4[1].set_title("Basophils & Dendritic Cells")
        axes4[1].legend(loc="upper left", facecolor='#1e1e1e', edgecolor='none')

        def animate(frame):
            x = history["days"][:frame]
            line1.set_data(x, history["monocytes"][:frame])
            line2.set_data(x, history["eosinophils"][:frame])
            line3.set_data(x, history["nk_cells"][:frame])
            line4.set_data(x, history["basophils"][:frame])
            line5.set_data(x, history["cdc"][:frame])
            line6.set_data(x, history["pdc"][:frame])
            return line1, line2, line3, line4, line5, line6

        self.anim4 = FuncAnimation(fig4, animate, frames=total_frames + 1, interval=interval_ms, blit=True, repeat=False)
        fig4.tight_layout(rect=[0, 0, 1, 0.96])
        self.embed_canvas(fig4, self.tab4)


if __name__ == "__main__":
    root = tk.Tk()
    app = HSCApp(root)
    root.mainloop()        


    