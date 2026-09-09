# hsc_model.py
from collections import deque
import numpy as np
import config

def apply_daily_decay(current_count, decay_rate):
    """ Calculates daily cell clearence based on physiological lifespan."""
    deaths = np.random.poisson(current_count * decay_rate)
    return max(0, current_count - deaths)

def run_hsc_simulation(initial_hsc, target_capacity = None):
    # ---------------------------------------------------------------------------------
    # Maturation Queues
    # ---------------------------------------------------------------------------------
    # MEP Derivatives 
    rbc_queue = deque([0] * config.ERYTHROCYTES_PARAMETERS["MATURATION_DAYS"], maxlen= config.ERYTHROCYTES_PARAMETERS["MATURATION_DAYS"])
    plt_queue = deque([0] * config.PLATELETS_PARAMETERS["MATURATION_DAYS"], maxlen= config.PLATELETS_PARAMETERS["MATURATION_DAYS"])

    # GMP Derivatives 
    neut_queue = deque([0] * config.NEUTROPHILS_PARAMETERS["MATURATION_DAYS"], maxlen= config.NEUTROPHILS_PARAMETERS["MATURATION_DAYS"])
    eos_queue = deque([0] * config.EOSINOPHILS_PARAMETERS["MATURATION_DAYS"], maxlen= config.EOSINOPHILS_PARAMETERS["MATURATION_DAYS"])
    bas_queue = deque([0] * config.BASOPHILS_PARAMETERS["MATURATION_DAYS"], maxlen= config.BASOPHILS_PARAMETERS["MATURATION_DAYS"])
    mast_queue = deque([0] * config.MAST_CELLS_PARAMETERS["MATURATION_DAYS"], maxlen= config.MAST_CELLS_PARAMETERS["MATURATION_DAYS"])
    mono_queue = deque([0] * config.MONOCYTE_PARAMETERS["MATURATION_DAYS"], maxlen= config.MONOCYTE_PARAMETERS["MATURATION_DAYS"])
    cdc_queue = deque([0] * config.CDC_PARAMETERS["MATURATION_DAYS"], maxlen= config.CDC_PARAMETERS["MATURATION_DAYS"])
    pdc_queue = deque([0] * config.PDC_PARAMETERS["MATURATION_DAYS"], maxlen= config.PDC_PARAMETERS["MATURATION_DAYS"])

    # ---------------------------------------------------------------------------------
    # Cumulative Counters for All lineages
    # ---------------------------------------------------------------------------------
    hsc_count = initial_hsc  
    cmp_accumulated, clp_accumulated = 0, 0
    mep_accumulated, gmp_accumulated = 0, 0

    # Mature Counts
    rbc_accumulated, plt_accumulated = 0, 0
    neut_accumulated, eos_accumulated, bas_accumulated, mast_accumulated = 0, 0, 0, 0
    mono_accumulated, cdc_accumulated, pdc_accumulated = 0, 0, 0
    b_cells_accumulated, t_cells_accumulated, nk_cells_accumulated  = 0, 0, 0

    gmp_fractions = [
        config.NEUTROPHILS_PARAMETERS["FRACTION"],
        config.EOSINOPHILS_PARAMETERS["FRACTION"],
        config.BASOPHILS_PARAMETERS["FRACTION"],
        config.MAST_CELLS_PARAMETERS["FRACTION"],
        config.MONOCYTE_PARAMETERS["FRACTION"],
        config.CDC_PARAMETERS["FRACTION"],
        config.PDC_PARAMETERS["FRACTION"]
    ]
    day = 0
    recovery_day = None #Tracks day target capacity (50,000) is first reached
    
    if target_capacity is None:
        if initial_hsc > 50000:
              target_capacity = 100000       
        else:
              target_capacity = 50000
    config.HSC_TARGET_CAPACITY = target_capacity
    
    history = {
        "days":[],
        "hsc":[],
        "cmp":[],"clp":[],
        "mep":[],"gmp":[],
        "rbc":[],"platelets":[],
        "neutrophils":[], "eosinophils":[], "basophils":[], "mast_cells":[],
        "monocytes":[], "cdc":[], "pdc":[],
        "b_cells":[],"t_cells":[],"nk_cells":[]
    }
    
    # A "while" loop throughout the full clinical monitoring timeframe
    while day <= config.CLINICAL_MONITORING_DAYS:
        # ---- Phase 1: HSC Self-Renweal & Differentiation ----

        # ---- Biological Continuous Feedback (Hill Equation)----
        capacity_ratio = (hsc_count/config.HSC_TARGET_CAPACITY) ** config.HILL
        current_lambda = config.LAMBDA_MAX/(1.0 + capacity_ratio)

        # To store the day full recovery was reached 
        if hsc_count >= config.HSC_TARGET_CAPACITY and recovery_day is None:
               recovery_day = day
        
        if hsc_count >=config.HSC_TARGET_CAPACITY:
               current_lambda = config.NU_DAILY + config.APOPTOSIS_DAILY

        # ---- Stochastic Daily Events ----
        n_self_renew = np.random.poisson(hsc_count * current_lambda)
        n_diff = np.random.poisson(hsc_count * config.NU_DAILY)
        n_deaths = np.random.poisson(hsc_count * config.APOPTOSIS_DAILY)

        hsc_count = max(0, hsc_count + n_self_renew - n_diff - n_deaths)

        if hsc_count > config.HSC_TARGET_CAPACITY:
            hsc_count = config.HSC_TARGET_CAPACITY

        # ---- Phase 2: HPC -> CMP / CLP Branching ----
        amplified_hpcs = n_diff *(2 ** config.HPC_DIVISIONS)
        new_cmp =  np.random.binomial(amplified_hpcs, config.CMP_FRACTION)
        new_clp = amplified_hpcs - new_cmp

        cmp_accumulated = apply_daily_decay(cmp_accumulated, config.CMP_DECAY) + new_cmp
        clp_accumulated = apply_daily_decay(clp_accumulated, config.CLP_DECAY) + new_clp

        # ---- Phase 3: Myeloid Branching (MEP / GMP)
        amplified_cmp = new_cmp * (2 ** config.CMP_DIVISIONS)
        new_mep = np.random.binomial(amplified_cmp, config.MEP_PARAMETERS["FRACTION"])
        new_gmp = amplified_cmp - new_mep

        mep_accumulated = apply_daily_decay(mep_accumulated, config.MEP_PARAMETERS["DECAY"]) + new_mep
        gmp_accumulated = apply_daily_decay(gmp_accumulated, config.GMP_PARAMETERS["DECAY"]) + new_gmp

        # ---- Phase 4: MEP Extensions (RBC & Platelets) ----
        amplified_mep = new_mep * (2 ** config.MEP_SUB_DIVISIONS)
        new_erythroid = np.random.binomial(amplified_mep, config.ERYTHROCYTES_PARAMETERS["FRACTION"])
        new_megakaryo = amplified_mep - new_erythroid

        rbc_queue.append(new_erythroid * config.ERYTHROCYTES_PARAMETERS["EXPANSION_FACTOR"])
        plt_queue.append(new_megakaryo * config.PLATELETS_PARAMETERS["EXPANSION_FACTOR"])

        # ---- Phase 5: GMP Extensions (Granulocytes, Monocytes, DCs, Mast) ----
        amplified_gmp = new_gmp * (2 ** config.GMP_SUB_DIVISIONS)
        gmp_split = np.random.multinomial(amplified_gmp, gmp_fractions)

        neut_queue.append(gmp_split[0] * config.NEUTROPHILS_PARAMETERS["EXPANSION_FACTOR"])
        eos_queue.append(gmp_split[1] * config.EOSINOPHILS_PARAMETERS["EXPANSION_FACTOR"])
        bas_queue.append(gmp_split[2] * config.BASOPHILS_PARAMETERS["EXPANSION_FACTOR"])
        mono_queue.append(gmp_split[4] * config.MONOCYTE_PARAMETERS["EXPANSION_FACTOR"])
        mast_queue.append(gmp_split[3] * config.MAST_CELLS_PARAMETERS["EXPANSION_FACTOR"])
        cdc_queue.append(gmp_split[5] * config.CDC_PARAMETERS["EXPANSION_FACTOR"])
        pdc_queue.append(gmp_split[6] * config.PDC_PARAMETERS["EXPANSION_FACTOR"])

        # ---- Phase 6: Lymphoid Branching(B,T,NK) ----
        amplified_clp = new_mep * (2 ** config.LYMPH_DIVISIONS)
        lymph_fractions = [config.B_CELL_FRACTION, config.T_CELL_FRACTION, config.NK_CELL_FRACTION]
        b_precursors, t_precursors, nk_precursors = np.random.multinomial(amplified_clp, lymph_fractions)

        b_cells_accumulated = apply_daily_decay(b_cells_accumulated, config.B_CELL_DECAY) +  b_precursors
        t_cells_accumulated = apply_daily_decay(t_cells_accumulated, config.T_CELL_DECAY) + t_precursors
        nk_cells_accumulated = apply_daily_decay(nk_cells_accumulated, config.NK_CELL_DECAY) + nk_precursors

        # ---- Phase 7: Maturation Release & Daily Decay ----
        rbc_accumulated = apply_daily_decay(rbc_accumulated, config.ERYTHROCYTES_PARAMETERS["DECAY"]) + rbc_queue.popleft()
        plt_accumulated = apply_daily_decay(plt_accumulated, config.PLATELETS_PARAMETERS["DECAY"]) + plt_queue.popleft()
        neut_accumulated = apply_daily_decay(neut_accumulated, config.NEUTROPHILS_PARAMETERS["DECAY"]) + neut_queue.popleft()
        eos_accumulated = apply_daily_decay(eos_accumulated, config.EOSINOPHILS_PARAMETERS["DECAY"]) + eos_queue.popleft()
        bas_accumulated = apply_daily_decay(bas_accumulated, config.BASOPHILS_PARAMETERS["DECAY"]) + bas_queue.popleft()
        mast_accumulated = apply_daily_decay(mast_accumulated, config.MAST_CELLS_PARAMETERS["DECAY"]) + mast_queue.popleft()
        mono_accumulated = apply_daily_decay(mono_accumulated, config.MONOCYTE_PARAMETERS["DECAY"]) + mono_queue.popleft()
        cdc_accumulated = apply_daily_decay(cdc_accumulated, config.CDC_PARAMETERS["DECAY"]) + cdc_queue.popleft()
        pdc_accumulated = apply_daily_decay(pdc_accumulated, config.PDC_PARAMETERS["DECAY"]) + pdc_queue.popleft()

        # ---- Phase 8: Recording History ----
        history["days"].append(day)
        history["hsc"].append(hsc_count)
        history["cmp"].append(cmp_accumulated)
        history["clp"].append(clp_accumulated)
        history["mep"].append(mep_accumulated)
        history["rbc"].append(rbc_accumulated)
        history["platelets"].append(plt_accumulated)
        history["gmp"].append(gmp_accumulated)
        history["neutrophils"].append(neut_accumulated)
        history["eosinophils"].append(eos_accumulated)
        history["basophils"].append(bas_accumulated)
        history["mast_cells"].append(mast_accumulated)
        history["monocytes"].append(mono_accumulated)
        history["cdc"].append(cdc_accumulated)
        history["pdc"].append(pdc_accumulated)
        history["b_cells"].append(b_cells_accumulated)
        history["t_cells"].append(t_cells_accumulated)
        history["nk_cells"].append(nk_cells_accumulated)


        # To store the day full recovery was reached 
        if hsc_count >= config.HSC_TARGET_CAPACITY and recovery_day is None:
            recovery_day = day

        if hsc_count >=config.HSC_TARGET_CAPACITY:
            current_lambda = config.NU_DAILY + config.APOPTOSIS_DAILY 
        
        day += 1
        if hsc_count == 0:
            print("Warning: No HSCs pool depleted")
            break
    return history, recovery_day, day