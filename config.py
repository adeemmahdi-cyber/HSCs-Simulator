#Parameters:
#1.HSC Target number
HSC_TARGET_CAPACITY = 50000
CLINICAL_MONITORING_DAYS = 365
#2.Kinetics Rates
LAMBDA_MAX = (4.0/52.0)/7 #Rapid expansion phase based on:(Research paper)
HILL= 2.0 #HILL Coefficient based on :()
NU_DAILY = (0.60/52.0)/7 #Differentiation rate:()
APOPTOSIS_DAILY = (0.05/52.0)/7 #Apoptosis rate of HSCs:()

#3.Progenitors expansion & Branching
HPC_DIVISIONS = 5 #Based on:()
CMP_FRACTION = 0.75 #Based on:()
CLP_FRACTION = 0.25 
CMP_DECAY = 0.20
CLP_DECAY = 0.15
CMP_DIVISIONS = 4

#4.CMP Sub-lineages
MEP_PARAMETERS = { #Megakaryocyte-Erythroid Progenitors
    "FRACTION" : 0.60,
    "DECAY" : 0.10
}

GMP_PARAMETERS = { #Granulocyte-Monocyte Progenitors
    "FRACTION" : 0.40,
    "DECAY" : 0.25
}

#5.Sub-lineages Divisions
MEP_SUB_DIVISIONS = 3
GMP_SUB_DIVISIONS = 3

#6.Mast cells
MAST_CELLS_PARAMETERS ={
    "FRACTION" : 0.01,
    "DECAY" : 1.0/30.0,
    "MATURATION_DAYS" : 4,
    "EXPANSION_FACTOR" : 4

}
#6.MEP Sub-lineages parameters

ERYTHROCYTES_PARAMETERS = {#Erythropoiesis Pipeline (MEP -> RBC):
    "FRACTION":0.85,
    "DECAY" : 1.0/120.0, 
    "MATURATION_DAYS" : 6,
    "EXPANSION_FACTOR": 16
    }

PLATELETS_PARAMETERS ={ #Thrombopoiesis Pipeline (MEP -> Platelets)
    "FRACTION":0.15,
    "DECAY":1.0/9.0,
    "MATURATION_DAYS" : 5,
    "EXPANSION_FACTOR" : 8
}

#7.GMP Sub-lineages parameters

#A) Granulocyte Sub-lineages: #Granulopoiesis Pipeline (GMP -> Granulocyte)

NEUTROPHILS_PARAMETERS = {
    "FRACTION" : 0.74,
    "DECAY" : 1.0/2.0, 
    "MATURATION_DAYS" : 10,
    "EXPANSION_FACTOR" : 32
}

EOSINOPHILS_PARAMETERS = {
    "FRACTION" : 0.04,
    "DECAY" : 1.0/4.0,
    "MATURATION_DAYS" : 8,
    "EXPANSION_FACTOR" : 16
}

BASOPHILS_PARAMETERS = {
    "FRACTION" : 0.01,
    "DECAY" : 1.0/3.0,
    "MATURATION_DAYS" : 7,
    "EXPANSION_FACTOR" : 8
}

#B) Agranulocyte Sub-lineages:

MONOCYTE_PARAMETERS ={ # 70% OF remaining Macrophage/Dendritic cell Progenitor (MDP) pool
    "FRACTION" : 0.14,
    "DECAY" : 1.0/5.0,
    "MATURATION_DAYS" : 3,
    "EXPANSION_FACTOR" : 8
}

CDC_PARAMETERS = { # 20% of MDP 
    #Dendritic Cell Pipeline (cDC)
    "FRACTION" : 0.04,
    "DECAY" : 1.0/7.0,
    "MATURATION_DAYS" : 4,
    "EXPANSION_FACTOR" : 1
}

PDC_PARAMETERS = { # 10% of MDP 
    #Dendritic Cell Pipeline (pDC)
    "FRACTION" : 0.02,
    "DECAY" : 1.0/14.0,
    "MATURATION_DAYS" : 5,
    "EXPANSION_FACTOR" : 1
}


#5.CLP Sub-lineages
B_CELL_FRACTION = 0.50 #B-cell Progenitors
T_CELL_FRACTION = 0.40 #T-cell Progenitors
NK_CELL_FRACTION = 0.10 #NK-cell Progenitors
LYMPH_DIVISIONS = 3
B_CELL_DECAY = 0.05
T_CELL_DECAY = 0.02
NK_CELL_DECAY = 0.10