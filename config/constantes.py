# =============================================================================
# constantes.py — Dados fixos da empresa e registros provisórios
# Atualizar conforme retorno das áreas responsáveis
# =============================================================================

# --- Identificação da empresa (0000 / 0140) ----------------------------------
EMPRESA = {
    "CNPJ":            "46206637000130",
    "NOME":            "SOMPO SERVICES GESTAO DE RISCOS E VISTORIA LTDA",
    "UF":              "SP",
    "COD_MUN":         "3550308",
    "SUFRAMA":         "000000000",
    "IND_SIT_ESP":     "00",
    "IND_APUR_IPI":    "1",       # 0000 campo 14
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

# --- Indicadores (0110 / 0111) -----------------------------------------------
IND_0110 = {"IND_INC_IMOB": "1", "IND_ATIV_IMOB": "2", "IND_ATIV": "1"}
IND_0111 = {"REC_BRU_NCUM_TRIB_MI": "0", "REC_BRU_NCUM_NT_MI": "0",
            "REC_BRU_NCUM_EXP": "0", "REC_BRU_CUM": "0", "REC_BRU_TOTAL": "0"}

# --- Unidades de medida (0190) -----------------------------------------------
UNIDADES = [
    ("UN", "UNIDADE"),
]

# --- Itens/serviços (0200) ---------------------------------------------------
ITENS = [
    # COD_ITEM | DESCR_ITEM | COD_BARRA | COD_ANT | UM | TIPO_ITEM | COD_NCM | EX_IPI | COD_GEN | COD_LST | ALIQ_ICMS
    # 12 campos — sem CEST (campo não existe na EFD Contribuições)
    ("2018",               "FIC FI FUNDACOES RENDA FIXA",  "", "", "UN", "09", "", "", "99", "", "0"),
    ("6621501",            "Serviço",                      "", "", "UN", "09", "", "", "99", "", "0"),
    ("JUROSSALDO NEGATIVO", "JUROS SALDO NEGATIVO",        "", "", "",   "99", "", "", "",   "", "" ),
]

# --- Plano de contas (0500) --------------------------------------------------
CONTAS = [
    # DT_ALT | COD_NAT_CC | IND_CTA | NIVEL | COD_CTA | NOME_CTA | COD_CTA_REF | CNPJ_EST
    ("01012012", "04", "A", "6", "3.2.4.01.002.00004", "Creditos Financeiros",     "3.01.01.05.01.05", ""),
    ("01012012", "04", "A", "6", "4.1.1.01.001.00001", "Prestação de Serviços",   "3.01.01.01.01.06", ""),
    ("01012012", "04", "A", "6", "361140001",           "FDO NEX VC (DPV) GAIN",  "",                  ""),
    ("01012012", "04", "A", "6", "36990099",            "OUTRAS RECEITAS FINANCEIRAS", "",             ""),
    ("01012012", "04", "A", "6", "36910001",            "JUROS S/CRED.TRIBUT",    "",                  ""),
    ("30122025", "04", "A", "6", "35199995",            "Receita Sompo Risk",      "",                  ""),
]

# --- Padrões para A100 / A170 ------------------------------------------------
A100_IND_EMIT  = "1"    # 1 = emitente é o próprio contribuinte
A100_IND_OPER  = "0"    # 0 = saída
A100_COD_SIT   = "00"   # 00 = documento regular
A100_IND_PGTO  = "1"    # 1 = à vista
A170_NUM_ITEM  = "1"
A170_COD_ITEM  = "6621501"
A170_CST_PIS   = "01"   # tributado a alíquota básica
A170_ALIQ_PIS  = 1.65
A170_CST_COFINS= "01"
A170_ALIQ_COFINS = 7.6
A170_COD_CTA   = "4.1.1.01.001.00001"

# --- Padrões para F600 -------------------------------------------------------
F600_IND_NAT_RET = "03"  # retenção por pessoa jurídica em geral
F600_COD_REC     = "5952"
F600_IND_NAT_PJ  = "0"
F600_IND_DEC     = "0"

# --- F100 — Receitas financeiras (PROVISÓRIO — aguardando área responsável) --
# Fonte: TXT de referência 03/2026. Substituir quando a área retornar.
# Campos: IND_OPER|IND_ORIG|COD_ITEM|DT_OPER|VL_OPER|
#         CST_PIS|VL_BC_PIS|ALIQ_PIS|VL_PIS|
#         CST_COFINS|VL_BC_COFINS|ALIQ_COFINS|VL_COFINS|
#         NAT_BC_CRED|IND_ORIG_CRED|COD_CTA|COD_CENTRO|COD_PART|DESC_DOC_OPE
F100_FIXAS = [
    # Valores de 03/2026 extraídos do relatório SAP (imagem de referência)
    {
        "IND_OPER": "1", "IND_ORIG": "", "COD_ITEM": "2018",
        "DT_OPER": "31032026", "VL_OPER": 7276.93,
        "CST_PIS": "02", "VL_BC_PIS": 7276.93, "ALIQ_PIS": 0.65, "VL_PIS": 47.30,
        "CST_COFINS": "02", "VL_BC_COFINS": 7276.93, "ALIQ_COFINS": 4.0, "VL_COFINS": 291.08,
        "NAT_BC_CRED": "", "IND_ORIG_CRED": "", "COD_CTA": "361140001",
        "COD_CENTRO": "", "COD_PART": "", "DESC_DOC_OPE": "",
    },
    {
        "IND_OPER": "1", "IND_ORIG": "", "COD_ITEM": "2018",
        "DT_OPER": "31032026", "VL_OPER": 8607.69,
        "CST_PIS": "02", "VL_BC_PIS": 8607.69, "ALIQ_PIS": 0.65, "VL_PIS": 55.95,
        "CST_COFINS": "02", "VL_BC_COFINS": 8607.69, "ALIQ_COFINS": 4.0, "VL_COFINS": 344.31,
        "NAT_BC_CRED": "", "IND_ORIG_CRED": "", "COD_CTA": "36910001",
        "COD_CENTRO": "", "COD_PART": "", "DESC_DOC_OPE": "",
    },
    {
        "IND_OPER": "1", "IND_ORIG": "", "COD_ITEM": "2018",
        "DT_OPER": "31032026", "VL_OPER": 528.68,
        "CST_PIS": "02", "VL_BC_PIS": 528.68, "ALIQ_PIS": 0.65, "VL_PIS": 3.44,
        "CST_COFINS": "02", "VL_BC_COFINS": 528.68, "ALIQ_COFINS": 4.0, "VL_COFINS": 21.15,
        "NAT_BC_CRED": "", "IND_ORIG_CRED": "", "COD_CTA": "36990099",
        "COD_CENTRO": "", "COD_PART": "", "DESC_DOC_OPE": "",
    },
]

# --- 1300 / 1700 — Controle de retenções acumuladas -----------------------
# Fonte: resalvas confirmadas pela área responsável (03/2026)
# VL_RET_APU = total acumulado de bônus retidos (PIS/COFINS DZ)
# VL_RET_EFE = calculado dinamicamente a partir das F600s do período atual
RETENCAO_ACUMULADA_PIS    = 14229.56   # 1300 — PIS  0,65%
RETENCAO_ACUMULADA_COFINS = 70453.17   # 1700 — COFINS 3,00%
RETENCAO_PER_APU          = "022026"   # período de apuração anterior
