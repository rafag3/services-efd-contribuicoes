"""
main.py — EFD Contribuições · Automação de Serviços
Interface Tkinter nativa. Empacote com PyInstaller para gerar o .exe.
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.ttk as ttk

# Path para funcionar no .exe PyInstaller
BASE_DIR = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from readers.excel_notas_reader import ler_notas, derivar_periodo
from writers.efd_writer import gerar_efd

# ── Cores e fontes ────────────────────────────────────────────────────────────
COR_PRINCIPAL  = "#8b1a1a"
COR_HOVER      = "#6f1515"
COR_FUNDO      = "#f0f2f5"
COR_CARD       = "#ffffff"
COR_TEXTO      = "#1a1a2e"
COR_SUBTEXTO   = "#6b7280"
COR_BORDA      = "#e5e7eb"
COR_SUCESSO    = "#166534"
COR_ERRO       = "#991b1b"
COR_AVISO_BG   = "#fef3c7"
COR_AVISO_TEXT = "#92400e"

FONTE_TITULO   = ("Segoe UI", 16, "bold")
FONTE_SUBTIT   = ("Segoe UI", 10)
FONTE_LABEL    = ("Segoe UI", 10, "bold")
FONTE_NORMAL   = ("Segoe UI", 10)
FONTE_PEQUENA  = ("Segoe UI", 9)
FONTE_BTN      = ("Segoe UI", 11, "bold")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EFD Contribuições — Automação de Serviços")
        self.configure(bg=COR_FUNDO)
        self.resizable(False, False)
        self._caminho_xlsx = tk.StringVar()
        self._construir_ui()
        self._centralizar()

    # ── Layout ────────────────────────────────────────────────────────────────
    def _construir_ui(self):
        # Card externo
        card = tk.Frame(self, bg=COR_CARD, bd=0, relief="flat",
                        highlightbackground=COR_BORDA, highlightthickness=1)
        card.pack(padx=32, pady=32, fill="both", expand=True)

        inner = tk.Frame(card, bg=COR_CARD)
        inner.pack(padx=36, pady=32, fill="both", expand=True)

        # Cabeçalho
        cab = tk.Frame(inner, bg=COR_CARD)
        cab.pack(fill="x", pady=(0, 24))

        icon_frame = tk.Frame(cab, bg=COR_PRINCIPAL, width=44, height=44)
        icon_frame.pack(side="left", padx=(0, 12))
        icon_frame.pack_propagate(False)
        tk.Label(icon_frame, text="📄", bg=COR_PRINCIPAL, font=("Segoe UI Emoji", 18)
                 ).place(relx=.5, rely=.5, anchor="center")

        txt_cab = tk.Frame(cab, bg=COR_CARD)
        txt_cab.pack(side="left")
        tk.Label(txt_cab, text="Sompo Services", bg=COR_CARD,
                 font=("Segoe UI", 12, "bold"), fg=COR_TEXTO).pack(anchor="w")
        tk.Label(txt_cab, text="EFD Contribuições — Automação Fiscal",
                 bg=COR_CARD, font=FONTE_PEQUENA, fg=COR_SUBTEXTO).pack(anchor="w")

        # Título
        tk.Label(inner, text="Gerar TXT da EFD", bg=COR_CARD,
                 font=FONTE_TITULO, fg=COR_TEXTO).pack(anchor="w")
        tk.Label(inner,
                 text="Selecione a planilha de notas fiscais emitidas (.xlsx) para\n"
                      "gerar o arquivo de importação da EFD Contribuições.",
                 bg=COR_CARD, font=FONTE_SUBTIT, fg=COR_SUBTEXTO,
                 justify="left").pack(anchor="w", pady=(4, 20))

        # Campo de seleção de arquivo
        tk.Label(inner, text="Planilha de notas fiscais emitidas (.xlsx)",
                 bg=COR_CARD, font=FONTE_LABEL, fg=COR_TEXTO).pack(anchor="w")

        sel_frame = tk.Frame(inner, bg=COR_CARD)
        sel_frame.pack(fill="x", pady=(6, 0))

        entry = tk.Entry(sel_frame, textvariable=self._caminho_xlsx,
                         font=FONTE_NORMAL, fg=COR_TEXTO, bg="#f9fafb",
                         relief="flat", bd=0,
                         highlightbackground=COR_BORDA, highlightthickness=1,
                         state="readonly", readonlybackground="#f9fafb")
        entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))

        btn_sel = tk.Button(sel_frame, text="Procurar…",
                            font=FONTE_NORMAL, fg=COR_PRINCIPAL, bg=COR_CARD,
                            relief="flat", bd=1, cursor="hand2",
                            highlightbackground=COR_PRINCIPAL, highlightthickness=1,
                            padx=12, pady=6,
                            command=self._selecionar_arquivo)
        btn_sel.pack(side="right")

        self._label_arquivo = tk.Label(inner, text="", bg=COR_CARD,
                                       font=FONTE_PEQUENA, fg="#059669")
        self._label_arquivo.pack(anchor="w", pady=(4, 0))

        # Botão principal
        self._btn_gerar = tk.Button(
            inner, text="Gerar TXT da EFD",
            font=FONTE_BTN, fg="white", bg=COR_PRINCIPAL,
            activebackground=COR_HOVER, activeforeground="white",
            relief="flat", bd=0, cursor="hand2",
            padx=0, pady=12, state="disabled",
            command=self._processar_thread,
        )
        self._btn_gerar.pack(fill="x", pady=(20, 0))

        # Barra de progresso (oculta por padrão)
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("Sompo.Horizontal.TProgressbar",
                        troughcolor=COR_BORDA,
                        background=COR_PRINCIPAL,
                        thickness=6)
        self._progress = ttk.Progressbar(inner, style="Sompo.Horizontal.TProgressbar",
                                         mode="indeterminate", length=400)

        # Status
        self._status = tk.Label(inner, text="", bg=COR_CARD,
                                font=FONTE_NORMAL, fg=COR_TEXTO,
                                wraplength=400, justify="left")

        # Rodapé com aviso de dados provisórios
        sep = tk.Frame(inner, bg=COR_BORDA, height=1)
        sep.pack(fill="x", pady=(24, 12))

        aviso = tk.Frame(inner, bg=COR_AVISO_BG,
                         highlightbackground="#fde68a", highlightthickness=1)
        aviso.pack(fill="x")
        tk.Label(aviso,
                 text="⚠  Dados provisórios (aguardando área responsável): "
                      "F100 (receitas financeiras) · 1300/1700 (saldo anterior de retenções)\n"
                      "Atualizar em config/constantes.py após retorno.",
                 bg=COR_AVISO_BG, font=("Segoe UI", 8), fg=COR_AVISO_TEXT,
                 justify="left", wraplength=400,
                 ).pack(padx=12, pady=8, anchor="w")

    # ── Interações ────────────────────────────────────────────────────────────
    def _selecionar_arquivo(self):
        caminho = filedialog.askopenfilename(
            title="Selecionar planilha de notas fiscais",
            filetypes=[("Excel", "*.xlsx *.xls"), ("Todos os arquivos", "*.*")],
        )
        if caminho:
            self._caminho_xlsx.set(caminho)
            self._label_arquivo.config(
                text=f"✓  {os.path.basename(caminho)}", fg="#059669")
            self._btn_gerar.config(state="normal")
            self._set_status("")

    def _processar_thread(self):
        """Roda o processamento em thread separada para não travar a UI."""
        self._btn_gerar.config(state="disabled")
        self._progress.pack(fill="x", pady=(12, 0))
        self._progress.start(12)
        self._set_status("Processando notas e gerando TXT…", COR_SUBTEXTO)
        threading.Thread(target=self._processar, daemon=True).start()

    def _processar(self):
        try:
            notas = ler_notas(self._caminho_xlsx.get())
            if not notas:
                self._finalizar_erro("Nenhuma nota encontrada no arquivo.")
                return

            dt_ini, dt_fin = derivar_periodo(notas)
            conteudo = gerar_efd(notas, dt_ini, dt_fin)

            periodo = notas[0].comp_emissao.replace("/", "")
            nome_sugerido = f"EFD_CONTRIBUICOES_{periodo}.txt"

            # Precisa voltar para a thread principal para abrir diálogo
            self.after(0, lambda: self._salvar_arquivo(conteudo, nome_sugerido))

        except Exception as e:
            import traceback
            self._finalizar_erro(f"Erro: {e}\n{traceback.format_exc()}")

    def _salvar_arquivo(self, conteudo: bytes, nome_sugerido: str):
        caminho_saida = filedialog.asksaveasfilename(
            title="Salvar TXT da EFD",
            defaultextension=".txt",
            initialfile=nome_sugerido,
            filetypes=[("Arquivo texto", "*.txt"), ("Todos os arquivos", "*.*")],
        )

        if not caminho_saida:
            self._finalizar_erro("Operação cancelada.")
            return

        with open(caminho_saida, "wb") as f:
            f.write(conteudo)

        self._progress.stop()
        self._progress.pack_forget()
        self._btn_gerar.config(state="normal")
        self._set_status(
            f"✅  Arquivo gerado com sucesso!\n{caminho_saida}\n\n"
            f"Importe no PVA da EFD Contribuições e valide.",
            COR_SUCESSO,
        )

    def _finalizar_erro(self, msg: str):
        self.after(0, lambda: (
            self._progress.stop(),
            self._progress.pack_forget(),
            self._btn_gerar.config(state="normal"),
            self._set_status(f"❌  {msg}", COR_ERRO),
        ))

    def _set_status(self, msg: str, cor: str = COR_TEXTO):
        self._status.config(text=msg, fg=cor)
        if msg:
            self._status.pack(anchor="w", pady=(12, 0))
        else:
            self._status.pack_forget()

    # ── Utilitários ───────────────────────────────────────────────────────────
    def _centralizar(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"+{(sw - w) // 2}+{(sh - h) // 2}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
