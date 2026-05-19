from dataclasses import dataclass, field
from typing import Optional


@dataclass
class NotaFiscal:
    comp_emissao: str        # "03/2026"
    dt_emissao: str          # "05032026" (DDMMAAAA)
    prefeitura: str          # "SP"
    num_nf: str              # "270"
    num_sap: str             # "1800000241"
    vl_doc: float            # valor bruto da NF
    iss: float               # ISS retido
    irrf: float              # IRRF retido
    csll: float              # CSLL retida
    cofins_ret: float        # COFINS retida pelo tomador (0,65% base)
    pis_ret: float           # PIS retido pelo tomador (0,65% base)
    total_csrf: float        # soma IRRF+CSLL+COFINS+PIS retidos
    vl_liquido: float        # valor líquido recebido
    doc_banco: str           # documento bancário
    dt_deposito: Optional[str]   # "05032026" ou None (EM ABERTO)
    comp_recebimento: Optional[str]
    cod_cliente: str         # código interno
    bp: str                  # business partner SAP
    razao: str               # nome do tomador
    cnpj: str                # CNPJ 14 dígitos zero-padded
    regime: str              # texto completo do regime
    is_simples: bool         # True se optante pelo Simples Nacional
    tem_retencao: bool       # True se pis_ret > 0 ou cofins_ret > 0


@dataclass
class RegistroF600:
    """Retenção agregada por CNPJ do tomador."""
    cnpj_tomador: str
    dt_ret: str              # DDMMAAAA (data da nota ou depósito)
    vl_bc_ret: float         # base de cálculo total
    vl_ret_pis: float
    vl_ret_cofins: float

    @property
    def vl_ret_total(self) -> float:
        return round(self.vl_ret_pis + self.vl_ret_cofins, 2)
