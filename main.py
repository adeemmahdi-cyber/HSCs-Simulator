# main.py
import matplotlib.pyplot as plt
import config
from hsc_model import run_hsc_simulation

hsc_input = int(input("Enter the number of transplanted HSCs : ")) #Normally from 10,000 to 70,000

history, recovery_day, total_monitored_days = run_hsc_simulation(hsc_input)

# ---- Clinical Report Printing ----
print("\n" + "="*55)
print("         HEMATOPOIETIC RECONSTITUTION CLINICAL REPORT     ")
print("="*55)
print(f"Transplanted HSCs Count   : {hsc_input:,}")
print(f"Total Monitored Period    : {total_monitored_days - 1} Days")

if recovery_day is not None:
    print(f"Full Capacity Reached Day : Day {recovery_day}")
else:
    print("Full Capacity Reached Day : Not Reached within monitoring timeframe")

print("-" * 55)
print("Final Cell Counts at Day 365:")
print(f"  * HSC Pool        : {history['hsc'][-1]:,.0f}")
print(f"  * Neutrophils     : {history['neutrophils'][-1]:,.0f}")
print(f"  * Erythrocytes    : {history['rbc'][-1]:,.0f}")
print(f"  * Platelets       : {history['platelets'][-1]:,.0f}")
print(f"  * B-Lymphocytes   : {history['b_cells'][-1]:,.0f}")
print(f"  * T-Lymphocytes   : {history['t_cells'][-1]:,.0f}")
print("="*55 + "\n")
# =================================================================================
# FIGURE 1: Stem & Progenitor Kinetics (Bone Marrow Dynamics)
# =================================================================================

fig1, axes1 = plt.subplots(3,1,figsize=(12,10), sharex=True)
fig1.suptitle("Figure 1: Bone Marrow Stem & Progenitor Kinetics", fontsize=14, fontweight="bold")

# Subplot 1.1: Stem and Progenitor Kinetics
axes1[0].plot(history["days"], history["hsc"], color="r", label="HSC Pool (R)")
axes1[0].axhline(y=config.HSC_TARGET_CAPACITY, color="g", linestyle="--", label="Target Capacity 50,000")
if recovery_day is not None:
   axes1[0].axvline(x=recovery_day, color="orange", linestyle=":", label=f"Full Recovery (Day {recovery_day})")

axes1[0].minorticks_on()
axes1[0].set_ylim(0, 70000)
axes1[0].set_ylabel("Number of HSCs")
axes1[0].set_title("Clinical HSCs Recovery & Post-Transplant Homeostasis Diagram")
axes1[0].legend(loc="upper left")
axes1[0].grid(which='major', linestyle='-', linewidth=0.7, alpha=0.5) 
axes1[0].grid(which='minor', linestyle='--', linewidth=0.4, alpha=0.3)

# Subplot 1.2: Primary Progenitors
axes1[1].plot(history["days"], history["cmp"], color="purple", label="CMP (Myeloid Branch)")
axes1[1].plot(history["days"], history["clp"], color="blue", label="CLP (Lymphoid Branch)")
axes1[1].set_title("Primary Progenitors")
axes1[1].set_ylabel("Primary Progenitors")
axes1[1].legend(loc="upper left")
axes1[1].minorticks_on()
axes1[1].grid(which='major', linestyle='-', linewidth=0.7, alpha=0.5) 
axes1[1].grid(which='minor', linestyle='--', linewidth=0.4, alpha=0.3)

# Subplot 1.3: Secondary Progenitors Myeloid Branch
axes1[2].plot(history["days"], history["mep"], color="darkred", label="MEP (Erythrocyte/Megakaryocyte)")
axes1[2].plot(history["days"], history["gmp"], color="orange", label="GMP (Granulocyte/Monocyte)")
axes1[2].set_ylabel("Myeloid Lineages")
axes1[2].set_xlabel("Days Post-Transplantation")
axes1[2].set_title("Myeloid Sub-Lineage Branching (MEP & GMP)")
axes1[2].legend(loc="upper left")
axes1[2].minorticks_on()
axes1[2].grid(which='major', linestyle='-', linewidth=0.7, alpha=0.5) 
axes1[2].grid(which='minor', linestyle="--", linewidth=0.4, alpha=0.3)

fig1.tight_layout(rect=[0, 0, 1, 0.96])

# =================================================================================
# FIGURE 2: Peripheral Blood Mature Lineage Reconstitution (Linear Scale)
# =================================================================================

fig2,axes2 = plt.subplots(3,1, figsize=(12,10), sharex=True)
fig2.suptitle("Figure 2: Peripheral Blood Immune & Mature Cell Reconstitution", fontsize=14, fontweight="bold")

# Subplot 2.1: Erythrocytes & Plateles (High Volume Lineages)
axes2[0].plot(history["days"], history["rbc"], color="r", label="Erythrocytes (RBCs)")
axes2[0].plot(history["days"], history["platelets"], color="darkorange", label="Platelets")
axes2[0].set_ylabel("Cell Count")
axes2[0].set_title("Erythroid & Thromboid Recovery (RBCs & Platelets)")
axes2[0].legend(loc="upper left")
axes2[0].minorticks_on()
axes2[0].grid(which='major', linestyle='-', linewidth=0.7, alpha=0.5) 
axes2[0].grid(which='minor', linestyle='--', linewidth=0.4, alpha=0.3)

# Subplot 2.2: Innate Immune / Granulocyte Lineages
axes2[1].plot(history["days"], history["neutrophils"], color="darkblue", label="Neutrophils")
axes2[1].plot(history["days"], history["eosinophils"], color="green", label="Eosinophils")
axes2[1].plot(history["days"], history["basophils"], color="blue", label="Basophils")
axes2[1].plot(history["days"], history["monocytes"], color="red", label="Monocytes")
axes2[1].plot(history["days"], history["cdc"], color="orange", label="Convential Dendritic Cells")
axes2[1].plot(history["days"], history["pdc"], color="magenta", label="Plasmacytoid Dendritic Cells")
axes2[1].set_ylabel("Cell Count")
axes2[1].set_title("Innate Immune & Granulocyte Recovery")
axes2[1].legend(loc="upper left")
axes2[1].minorticks_on()
axes2[1].grid(which='major', linestyle='-', linewidth=0.7, alpha=0.5) 
axes2[1].grid(which='minor', linestyle="--", linewidth=0.4, alpha=0.3)

# Subplot 2.3: Adaptive Immune / Lymphoid Lineages
axes2[2].plot(history["days"], history["b_cells"], color="darkmagenta", label="B Lymphocytes")
axes2[2].plot(history["days"], history["t_cells"], color="teal", label="T Lymphocytes")
axes2[2].plot(history["days"], history["nk_cells"], color="dodgerblue", label="NK Lymphocytes")
axes2[2].set_xlabel("Days Post-Transplantation")
axes2[2].set_ylabel("Cell Count")
axes2[2].set_title("Adaptive Immune Reconstitution (Lymphoid Lineages)")
axes2[2].legend(loc="upper left")
axes2[2].minorticks_on()
axes2[2].grid(which='major', linestyle='-', linewidth=0.7, alpha=0.5) 
axes2[2].grid(which='minor', linestyle='--', linewidth=0.4, alpha=0.3)

fig2.tight_layout(rect=[0, 0, 1, 0.96])

# =================================================================================
# FIGURE 3: Low-Density & Specialized Sub-Lineages (Combined Magnified View)
# =================================================================================
plt.figure(figsize=(11, 6))
plt.title("Figure 3: Low-Density Immune Sub-Lineages (Magnified Kinetic View)", fontsize=13, fontweight="bold", pad=12)

plt.plot(history["days"], history["monocytes"], color="red", label="Monocytes")
plt.plot(history["days"], history["eosinophils"], color="green", label="Eosinophils")
plt.plot(history["days"], history["basophils"], color="blue", label="Basophils")
plt.plot(history["days"], history["cdc"], color="orange", label="cDC")
plt.plot(history["days"], history["pdc"], color="magenta", label="pDC")
plt.plot(history["days"], history["nk_cells"], color="dodgerblue", label="NK Lymphocytes")

plt.xlabel("Days Post-Transplantation")
plt.ylabel("Cell Count (Low Range)")
plt.legend(loc="upper left")
plt.minorticks_on()
plt.grid(which='major', linestyle='-', linewidth=0.7, alpha=0.5) 
plt.grid(which='minor', linestyle='--', linewidth=0.4, alpha=0.3)
plt.tight_layout()

plt.show()