# =============================================================================
# constantes.py — Dados fixos da empresa e registros que precisam atualização mensal
# =============================================================================

# --- Identificação da empresa ------------------------------------------------
EMPRESA = {
    "CNPJ":            "46206637000130",
    "NOME":            "SOMPO SERVICES GESTAO DE RISCOS E VISTORIA LTDA",
    "UF":              "SP",
    "COD_MUN":         "3550308",
    "SUFRAMA":         "000000000",
    "IND_SIT_ESP":     "00",
    "IND_APUR_IPI":    "1",
    "INSCR_MUN":       "2.116.583-1",
}

# --- Contato (0100) ----------------------------------------------------------
CONTATO = {
    "NOME":    "MARCELO BATISTA DA SILVA",
    "CPF":     "02829855736",
    "CRC":     "RJ093224/O-1",
    "CEP":     "04013001",
    "END":     "RUA CUBATÃO",
    "NUM":     "320",
    "COMPL":   "11º ANDAR",
    "BAI":     "CENTRO",
    "FONE":    "1131566767",
    "FAX":     "1131561908",
    "EMAIL":   "fiscal@maritima.com.br",
    "COD_MUN": "3550308",
}

# --- Indicadores -------------------------------------------------------------
IND_0110 = {"IND_INC_IMOB": "1", "IND_ATIV_IMOB": "2", "IND_ATIV": "1"}
IND_0111 = {"REC_BRU_NCUM_TRIB_MI": "0", "REC_BRU_NCUM_NT_MI": "0",
            "REC_BRU_NCUM_EXP": "0", "REC_BRU_CUM": "0", "REC_BRU_TOTAL": "0"}

# --- Unidades de medida (0190) -----------------------------------------------
UNIDADES = [("UN", "UNIDADE")]

# --- Itens/serviços (0200) — 11 campos, sem CEST ----------------------------
ITENS = [
    ("2018",               "FIC FI FUNDACOES RENDA FIXA",  "", "", "UN", "09", "", "", "99", "", "0"),
    ("6621501",            "Servico",                      "", "", "UN", "09", "", "", "99", "", "0"),
    ("JUROSSALDO NEGATIVO", "JUROS SALDO NEGATIVO",        "", "", "",   "99", "", "", "",   "", "" ),
]

# --- Plano de contas (0500) --------------------------------------------------
CONTAS = [
    ("01012012", "04", "A", "6", "3.2.4.01.002.00004", "Creditos Financeiros",        "3.01.01.05.01.05", ""),
    ("01012012", "04", "A", "6", "4.1.1.01.001.00001", "Prestacao de Servicos",       "3.01.01.01.01.06", ""),
    ("01012012", "04", "A", "6", "361140001",           "FDO NEX VC (DPV) GAIN",       "",                ""),
    ("01012012", "04", "A", "6", "36990099",            "OUTRAS RECEITAS FINANCEIRAS", "",                ""),
    ("01012012", "04", "A", "6", "36910001",            "JUROS S/CRED.TRIBUT",         "",                ""),
    ("30122025", "04", "A", "6", "35199995",            "Receita Sompo Risk",           "",                ""),
]

# --- Padrões A100 / A170 -----------------------------------------------------
A100_IND_EMIT   = "1"
A100_IND_OPER   = "0"
A100_COD_SIT    = "00"
A100_IND_PGTO   = "1"
A170_NUM_ITEM   = "1"
A170_COD_ITEM   = "6621501"
A170_CST_PIS    = "01"
A170_ALIQ_PIS   = 1.65
A170_CST_COFINS = "01"
A170_ALIQ_COFINS = 7.6
A170_COD_CTA    = "4.1.1.01.001.00001"

# --- F600 --------------------------------------------------------------------
F600_IND_NAT_RET = "03"
F600_COD_REC     = "5952"
F600_IND_NAT_PJ  = "0"
F600_IND_DEC     = "0"

# --- F100 — Receitas financeiras ---------------------------------------------
# !! ATUALIZAR A CADA MÊS com os valores reais do SAP !!
# Contas: 361140001 (FDO NÉX), 36910001 (Juros), 36990099 (Outras Rec. Fin.)
# VL_RET_EFE nos registros 1300/1700 = soma VL_PIS / VL_COFINS daqui
F100_FIXAS = [
    {
        "IND_OPER": "1", "IND_ORIG": "", "COD_ITEM": "2018",
        "DT_OPER": "30042026", "VL_OPER": 6578.34,
        "CST_PIS": "02", "VL_BC_PIS": 6578.34, "ALIQ_PIS": 0.65, "VL_PIS": 42.76,
        "CST_COFINS": "02", "VL_BC_COFINS": 6578.34, "ALIQ_COFINS": 4.0, "VL_COFINS": 263.13,
        "NAT_BC_CRED": "", "IND_ORIG_CRED": "", "COD_CTA": "361140001",
        "COD_CENTRO": "", "COD_PART": "",
    },
    {
        "IND_OPER": "1", "IND_ORIG": "", "COD_ITEM": "2018",
        "DT_OPER": "30042026", "VL_OPER": 4495.54,
        "CST_PIS": "02", "VL_BC_PIS": 4495.54, "ALIQ_PIS": 0.65, "VL_PIS": 29.22,
        "CST_COFINS": "02", "VL_BC_COFINS": 4495.54, "ALIQ_COFINS": 4.0, "VL_COFINS": 179.82,
        "NAT_BC_CRED": "", "IND_ORIG_CRED": "", "COD_CTA": "36910001",
        "COD_CENTRO": "", "COD_PART": "",
    },
    {
        "IND_OPER": "1", "IND_ORIG": "", "COD_ITEM": "2018",
        "DT_OPER": "30042026", "VL_OPER": 528.68,
        "CST_PIS": "02", "VL_BC_PIS": 528.68, "ALIQ_PIS": 0.65, "VL_PIS": 3.44,
        "CST_COFINS": "02", "VL_BC_COFINS": 528.68, "ALIQ_COFINS": 4.0, "VL_COFINS": 21.15,
        "NAT_BC_CRED": "", "IND_ORIG_CRED": "", "COD_CTA": "36990099",
        "COD_CENTRO": "", "COD_PART": "",
    },
]

# --- 1300 / 1700 — Saldo acumulado de retenções ------------------------------
# !! ATUALIZAR A CADA MÊS !!
# VL_RET_APU = soma bônus retidos acumulados (docs DZ + DA no SAP)
# VL_RET_EFE = calculado automaticamente (soma VL_PIS/VL_COFINS do F100)
# VL_RET_A_EFET = calculado automaticamente (APU - EFE)
RETENCAO_ACUMULADA_PIS    = 14229.56   # 1300 — PIS
RETENCAO_ACUMULADA_COFINS = 70453.17   # 1700 — COFINS
RETENCAO_PER_APU          = "032026"   # período anterior (formato MMAAAA)
