# EFD Contribuições — Automação de Serviços

Automação da geração do TXT de importação da EFD Contribuições a partir da
planilha de notas fiscais emitidas de serviços.

## Como usar

### Modo desenvolvimento
```bash
pip install -r requirements.txt
python main.py
```
O browser abrirá automaticamente em http://127.0.0.1:5000

### Gerar executável (.exe)
```bat
build.bat
```
O arquivo `dist/EFD_Services.exe` não requer instalação.

## Dados provisórios (aguardando área responsável)
- **F100** (receitas financeiras): valores hardcoded em `config/constantes.py`
- **1300/1700** (saldo de retenções anterior): idem

Após retorno da área, atualizar `F100_FIXAS`, `REGISTRO_1300` e `REGISTRO_1700`.

## Estrutura gerada
- Bloco 0: abertura, cadastros, participantes (automático da planilha)
- Bloco A: A100/A170 para cada nota
- Bloco F: F100 (fixo) + F600 (das notas com retenção, agrupado por CNPJ)
- Bloco M: apuração PIS/COFINS calculada
- Bloco 1: 1300/1700 (provisório)
- Bloco 9: contadores automáticos
