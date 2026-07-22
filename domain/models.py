from dataclasses import dataclass
from typing import Optional


@dataclass
class NotaFiscal:
    comp_emissao: str
    dt_emissao: str
    prefeitura: str
    num_nf: str
    num_sap: str
    vl_doc: float
    iss: float
    irrf: float
    csll: float
    cofins_ret: float
    pis_ret: float
    total_csrf: float
    vl_liquido: float
    doc_banco: str
    dt_deposito: Optional[str]
    comp_recebimento: Optional[str]
    cod_cliente: str
    bp: str
    razao: str
    cnpj: str
    regime: str
    is_simples: bool
    tem_retencao: bool


@dataclass
class RegistroF600:
    cnpj_tomador: str
    dt_ret: str
    vl_bc_ret: float
    vl_ret_pis: float
    vl_ret_cofins: float

    @property
    def vl_ret_total(self) -> float:
        return round(self.vl_ret_pis + self.vl_ret_cofins, 2)
