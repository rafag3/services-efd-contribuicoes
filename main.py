"""
main.py — EFD Contribuições · Automação de Serviços
Interface Tkinter nativa com log de progresso.
"""

import calendar
import datetime
import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk

BASE_DIR = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from readers.excel_notas_reader import ler_notas
from writers.efd_writer import gerar_efd

# ── Paleta ────────────────────────────────────────────────────────────────────
C_VERM       = "#CC0000"
C_VERM_ESC   = "#a30000"
C_VERM_LIGHT = "#fff0f0"
C_BRANCO     = "#ffffff"
C_FUNDO      = "#f5f5f5"
C_HEADER_BG  = "#ffffff"
C_HEADER_BRD = "#e8e8e8"
C_TEXTO      = "#1a1a1a"
C_SUBTEXTO   = "#666666"
C_BORDA      = "#e0e0e0"
C_INPUT_BG   = "#fafafa"
C_SUCESSO_BG = "#f0fdf4"
C_SUCESSO_FG = "#166534"
C_ERRO_BG    = "#fff0f0"
C_ERRO_FG    = "#cc0000"
C_AVISO_BG   = "#fffbeb"
C_AVISO_FG   = "#92400e"
C_AVISO_BRD  = "#fde68a"
C_LOG_BG     = "#1e1e1e"
C_LOG_FG     = "#d4d4d4"

F_TITULO  = ("Segoe UI", 17, "bold")
F_SUBTIT  = ("Segoe UI", 10)
F_LABEL   = ("Segoe UI", 10, "bold")
F_NORMAL  = ("Segoe UI", 10)
F_PEQUENA = ("Segoe UI", 9)
F_BTN     = ("Segoe UI", 11, "bold")
F_LOG     = ("Courier New", 9)


def _carregar_logo(path: str, largura: int = 100):
    try:
        from PIL import Image, ImageTk
        img = Image.open(path)
        razao = largura / img.width
        img = img.resize((largura, int(img.height * razao)), Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception:
        return None


class ModernEntry(tk.Frame):
    def __init__(self, parent, textvariable=None, readonly=False, **kwargs):
        super().__init__(parent, bg=C_BRANCO,
                         highlightbackground=C_BORDA, highlightthickness=1, bd=0)
        self._var = textvariable or tk.StringVar()
        self._entry = tk.Entry(
            self, textvariable=self._var, font=F_NORMAL, fg=C_TEXTO,
            bg=C_INPUT_BG, relief="flat", bd=0,
            state="readonly" if readonly else "normal",
            readonlybackground=C_INPUT_BG, **kwargs,
        )
        self._entry.pack(fill="x", padx=10, pady=7)
        if not readonly:
            self._entry.bind("<FocusIn>",  lambda e: self.config(highlightbackground=C_VERM))
            self._entry.bind("<FocusOut>", lambda e: self.config(highlightbackground=C_BORDA))

    def get(self):
        return self._var.get()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EFD Contribuições — Automação de Serviços")
        self.configure(bg=C_FUNDO)
        self.resizable(False, True)

        hoje = datetime.date.today()
        self._caminho_xlsx = tk.StringVar()
        self._mes = tk.StringVar()
        self._ano = tk.StringVar(value=str(hoje.year))
        self._logo_img = None

        self._estilo_ttk()
        self._construir_ui()
        self._centralizar()

    # ── TTK Style ─────────────────────────────────────────────────────────────
    def _estilo_ttk(self):
        s = ttk.Style(self)
        s.theme_use("default")
        s.configure("S.TCombobox",
                    fieldbackground=C_INPUT_BG, background=C_BRANCO,
                    foreground=C_TEXTO, selectbackground=C_VERM,
                    selectforeground=C_BRANCO, borderwidth=0,
                    relief="flat", padding=(8, 6))
        s.map("S.TCombobox", fieldbackground=[("readonly", C_INPUT_BG)],
              foreground=[("readonly", C_TEXTO)])
        s.configure("S.Horizontal.TProgressbar",
                    troughcolor=C_BORDA, background=C_VERM, thickness=3)

    # ── Layout ────────────────────────────────────────────────────────────────
    def _construir_ui(self):
        root = tk.Frame(self, bg=C_FUNDO)
        root.pack(padx=0, pady=0)

        # Barra lateral vermelha
        tk.Frame(root, bg=C_VERM, width=5).pack(side="left", fill="y")

        card = tk.Frame(root, bg=C_BRANCO, bd=0,
                        highlightbackground=C_BORDA, highlightthickness=1)
        card.pack(side="left", fill="both")

        # ── Header ───────────────────────────────────────────────────────────
        header = tk.Frame(card, bg=C_HEADER_BG,
                          highlightbackground=C_HEADER_BRD, highlightthickness=1)
        header.pack(fill="x")

        logo_path = os.path.join(BASE_DIR, "assets", "logo.png")
        self._logo_img = _carregar_logo(logo_path, largura=100)
        if self._logo_img:
            tk.Label(header, image=self._logo_img, bg=C_HEADER_BG, bd=0
                     ).pack(side="right", padx=20, pady=14)
        else:
            tk.Label(header, text="SOMPO", bg=C_HEADER_BG, fg=C_VERM,
                     font=("Segoe UI", 14, "bold")).pack(side="right", padx=20, pady=16)

        hd = tk.Frame(header, bg=C_HEADER_BG)
        hd.pack(side="left", padx=20, pady=14)
        tk.Label(hd, text="Sompo Services", bg=C_HEADER_BG, fg=C_TEXTO,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w")
        tk.Label(hd, text="EFD Contribuições — Automação Fiscal",
                 bg=C_HEADER_BG, fg=C_SUBTEXTO, font=("Segoe UI", 9)).pack(anchor="w")

        tk.Frame(card, bg=C_VERM, height=2).pack(fill="x")

        # ── Corpo ─────────────────────────────────────────────────────────────
        body = tk.Frame(card, bg=C_BRANCO)
        body.pack(padx=30, pady=24, fill="both")

        tk.Label(body, text="Gerar TXT da EFD", bg=C_BRANCO,
                 fg=C_TEXTO, font=F_TITULO).pack(anchor="w")
        tk.Label(body,
                 text="Selecione a planilha de notas fiscais e o período de apuração\n"
                      "para gerar o arquivo de importação da EFD Contribuições.",
                 bg=C_BRANCO, fg=C_SUBTEXTO, font=F_SUBTIT,
                 justify="left").pack(anchor="w", pady=(4, 18))

        tk.Frame(body, bg=C_BORDA, height=1).pack(fill="x", pady=(0, 18))

        # Planilha
        tk.Label(body, text="Planilha de notas fiscais emitidas (.xlsx)",
                 bg=C_BRANCO, fg=C_TEXTO, font=F_LABEL).pack(anchor="w")
        row_arq = tk.Frame(body, bg=C_BRANCO)
        row_arq.pack(fill="x", pady=(6, 0))
        self._entry_arq = ModernEntry(row_arq, textvariable=self._caminho_xlsx, readonly=True)
        self._entry_arq.pack(side="left", fill="x", expand=True, padx=(0, 10))
        tk.Button(row_arq, text="Procurar…", font=F_NORMAL, fg=C_VERM, bg=C_BRANCO,
                  relief="flat", bd=1, cursor="hand2",
                  highlightbackground=C_VERM, highlightthickness=1,
                  padx=14, pady=6, activebackground=C_VERM_LIGHT,
                  activeforeground=C_VERM_ESC,
                  command=self._selecionar_arquivo).pack(side="right")
        self._lbl_arq = tk.Label(body, text="", bg=C_BRANCO, font=F_PEQUENA, fg=C_SUCESSO_FG)
        self._lbl_arq.pack(anchor="w", pady=(4, 0))

        # Período
        tk.Label(body, text="Período de apuração", bg=C_BRANCO,
                 fg=C_TEXTO, font=F_LABEL).pack(anchor="w", pady=(18, 0))
        row_per = tk.Frame(body, bg=C_BRANCO)
        row_per.pack(anchor="w", pady=(6, 0))

        MESES = ["01 - Janeiro", "02 - Fevereiro", "03 - Março",
                 "04 - Abril",   "05 - Maio",      "06 - Junho",
                 "07 - Julho",   "08 - Agosto",    "09 - Setembro",
                 "10 - Outubro", "11 - Novembro",  "12 - Dezembro"]
        self._mes.set(MESES[datetime.date.today().month - 1])
        ttk.Combobox(row_per, textvariable=self._mes, values=MESES,
                     state="readonly", style="S.TCombobox",
                     width=17, font=F_NORMAL).pack(side="left", padx=(0, 8))
        ANOS = [str(y) for y in range(2023, datetime.date.today().year + 3)]
        ttk.Combobox(row_per, textvariable=self._ano, values=ANOS,
                     state="readonly", style="S.TCombobox",
                     width=7, font=F_NORMAL).pack(side="left")

        # Botão
        self._btn_gerar = tk.Button(
            body, text="Gerar TXT da EFD",
            font=F_BTN, fg=C_BRANCO, bg=C_VERM,
            activebackground=C_VERM_ESC, activeforeground=C_BRANCO,
            relief="flat", bd=0, cursor="hand2",
            padx=0, pady=13, state="disabled",
            command=self._processar_thread,
        )
        self._btn_gerar.pack(fill="x", pady=(22, 0))

        # Barra de progresso
        self._progress = ttk.Progressbar(body, style="S.Horizontal.TProgressbar",
                                          mode="indeterminate")

        # ── Log de progresso (fundo escuro estilo terminal) ───────────────────
        self._frm_log = tk.Frame(body, bg=C_LOG_BG,
                                  highlightbackground="#444", highlightthickness=1)

        log_topo = tk.Frame(self._frm_log, bg="#2d2d2d")
        log_topo.pack(fill="x")
        tk.Label(log_topo, text="●  Log de processamento",
                 bg="#2d2d2d", fg="#aaaaaa",
                 font=("Segoe UI", 8, "bold")).pack(side="left", padx=10, pady=5)
        self._lbl_etapa = tk.Label(log_topo, text="",
                                    bg="#2d2d2d", fg="#888888",
                                    font=("Segoe UI", 8))
        self._lbl_etapa.pack(side="right", padx=10)

        log_inner = tk.Frame(self._frm_log, bg=C_LOG_BG)
        log_inner.pack(fill="both", expand=True)

        self._txt_log = tk.Text(
            log_inner, height=10, font=F_LOG,
            bg=C_LOG_BG, fg=C_LOG_FG,
            relief="flat", bd=0, state="disabled",
            wrap="word", cursor="arrow",
            highlightthickness=0, insertwidth=0,
        )
        sb = tk.Scrollbar(log_inner, command=self._txt_log.yview,
                           relief="flat", width=10,
                           bg="#333", troughcolor="#1e1e1e")
        self._txt_log.config(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y", pady=4, padx=(0, 2))
        self._txt_log.pack(side="left", fill="both", expand=True, padx=10, pady=8)

        # Tags de cor
        self._txt_log.tag_config("ok",     foreground="#4ec9b0", font=("Courier New", 9, "bold"))
        self._txt_log.tag_config("erro",   foreground="#f44747", font=("Courier New", 9, "bold"))
        self._txt_log.tag_config("info",   foreground="#9cdcfe")
        self._txt_log.tag_config("warn",   foreground="#dcdcaa")
        self._txt_log.tag_config("titulo", foreground="#ce9178", font=("Courier New", 9, "bold"))
        self._txt_log.tag_config("dim",    foreground="#555555")

        # Mostra log frame desde o início (vazio)
        self._frm_log.pack(fill="x", pady=(12, 0))

        # Status final
        self._frm_status = tk.Frame(body, bg=C_BRANCO, highlightthickness=0)
        self._lbl_status = tk.Label(self._frm_status, text="", bg=C_BRANCO,
                                     fg=C_TEXTO, font=F_NORMAL, wraplength=420, justify="left")
        self._lbl_status.pack(anchor="w", padx=12, pady=8)

        # Rodapé
        tk.Frame(body, bg=C_BORDA, height=1).pack(fill="x", pady=(22, 14))
        aviso = tk.Frame(body, bg=C_AVISO_BG,
                         highlightbackground=C_AVISO_BRD, highlightthickness=1)
        aviso.pack(fill="x")
        tk.Label(aviso,
                 text="⚠  Dados a atualizar mensalmente em config/constantes.py:\n"
                      "F100 (receitas financeiras)  ·  1300/1700 (saldo de retenções anterior)",
                 bg=C_AVISO_BG, fg=C_AVISO_FG, font=("Segoe UI", 8),
                 justify="left", wraplength=390).pack(padx=12, pady=10, anchor="w")

    # ── Log helpers ───────────────────────────────────────────────────────────
    def _log(self, msg: str, tag: str = "info"):
        """Adiciona uma linha ao log de progresso (thread-safe via after)."""
        def _append():
            self._txt_log.config(state="normal")
            self._txt_log.insert("end", msg + "\n", tag)
            self._txt_log.see("end")
            self._txt_log.config(state="disabled")
        self.after(0, _append)

    def _log_etapa(self, texto: str):
        self.after(0, lambda: self._lbl_etapa.config(text=texto))

    def _log_limpar(self):
        self._txt_log.config(state="normal")
        self._txt_log.delete("1.0", "end")
        self._txt_log.config(state="disabled")

    # ── Interações ────────────────────────────────────────────────────────────
    def _selecionar_arquivo(self):
        caminho = filedialog.askopenfilename(
            title="Selecionar planilha de notas fiscais",
            filetypes=[("Excel", "*.xlsx *.xls"), ("Todos os arquivos", "*.*")],
        )
        if caminho:
            self._caminho_xlsx.set(caminho)
            self._lbl_arq.config(text=f"✓  {os.path.basename(caminho)}", fg=C_SUCESSO_FG)
            self._btn_gerar.config(state="normal", bg=C_VERM)
            self._set_status("")

    # Substitua o método _processar_thread inteiro no main.py por este:

    def _processar_thread(self):
        self._btn_gerar.config(state="disabled", bg="#cccccc")

        # Mostra barra e log imediatamente
        self._progress.pack(fill="x", pady=(12, 0))
        self._progress.start(12)
        self._log_limpar()
        self._set_status("")

        # Força o redesenho da janela ANTES de iniciar a thread
        self.update()
        self.update_idletasks()

        # Só então inicia o processamento em background
        threading.Thread(target=self._processar, daemon=True).start()

    def _processar(self):
        try:
            mes = int(self._mes.get()[:2])
            ano = int(self._ano.get()[:4])

            self._log(f"═══ EFD Contribuições — {mes:02d}/{ano} ═══", "titulo")
            self._log("")

            # Leitura da planilha
            self._log_etapa("Lendo planilha...")
            self._log("📄  Lendo planilha de notas fiscais...", "info")
            notas = ler_notas(self._caminho_xlsx.get(), mes=mes, ano=ano)

            if not notas:
                self._log("✗  Nenhuma nota encontrada para o período selecionado.", "erro")
                self._finalizar_erro("Nenhuma nota encontrada para o período selecionado.")
                return

            com_ret = [n for n in notas if n.tem_retencao]
            sem_pgto = [n for n in notas if (n.pis_ret > 0 or n.cofins_ret > 0) and not n.tem_retencao]

            self._log(f"✓  {len(notas)} notas carregadas", "ok")
            self._log(f"   → {len(com_ret)} com retenção paga (geram F600)", "dim")
            self._log(f"   → {len(sem_pgto)} em aberto (sem F600)", "dim")
            self._log("")

            # Período
            import calendar as cal
            ultimo = cal.monthrange(ano, mes)[1]
            dt_ini = f"01{mes:02d}{ano}"
            dt_fin = f"{ultimo}{mes:02d}{ano}"
            self._log(f"📅  Período: {dt_ini} → {dt_fin}", "info")
            self._log("")

            # Callback de progresso para busca de municípios
            def progresso(atual, total, msg):
                self._log_etapa(f"Municípios {atual}/{total}")
                if atual == 1:
                    self._log("🌐  Consultando municípios via BrasilAPI...", "info")
                self._log(f"   [{atual:2d}/{total}] {msg}", "dim")

            # Geração do TXT
            self._log_etapa("Gerando TXT...")
            self._log("⚙️   Montando blocos SPED...", "info")
            conteudo = gerar_efd(notas, dt_ini, dt_fin, callback_progresso=progresso)

            n_linhas = len(conteudo.decode("latin-1", errors="replace").splitlines())
            self._log(f"✓  TXT gerado: {n_linhas} linhas", "ok")
            self._log("")

            nome = f"EFD_CONTRIBUICOES_{mes:02d}{ano}.txt"
            self._log_etapa("Concluído ✓")
            self.after(0, lambda: self._salvar_arquivo(conteudo, nome))

        except Exception as e:
            import traceback
            self._log(f"✗  ERRO: {e}", "erro")
            self._log(traceback.format_exc(), "dim")
            self._finalizar_erro(str(e))

    def _salvar_arquivo(self, conteudo: bytes, nome: str):
        dest = filedialog.asksaveasfilename(
            title="Salvar TXT da EFD", defaultextension=".txt", initialfile=nome,
            filetypes=[("Arquivo texto", "*.txt"), ("Todos os arquivos", "*.*")],
        )
        if not dest:
            self._finalizar_erro("Operação cancelada.")
            return
        with open(dest, "wb") as f:
            f.write(conteudo)
        self._progress.stop()
        self._progress.pack_forget()
        self._btn_gerar.config(state="normal", bg=C_VERM)
        self._log(f"💾  Salvo em: {os.path.basename(dest)}", "ok")
        self._set_status(
            f"✅  Arquivo gerado com sucesso!\n{os.path.basename(dest)}\n"
            f"Importe no PVA da EFD Contribuições e valide.",
            C_SUCESSO_FG, bg=C_SUCESSO_BG, borda=C_SUCESSO_FG,
        )

    def _finalizar_erro(self, msg: str):
        self.after(0, lambda: [
            self._progress.stop(), self._progress.pack_forget(),
            self._btn_gerar.config(state="normal", bg=C_VERM),
            self._set_status(f"❌  {msg}", C_ERRO_FG, bg=C_ERRO_BG, borda=C_ERRO_FG),
        ])

    def _set_status(self, msg: str, fg=C_TEXTO, bg=C_BRANCO, borda: str = ""):
        if not msg:
            self._frm_status.pack_forget()
            return
        self._frm_status.config(bg=bg,
                                 highlightbackground=borda or C_BORDA,
                                 highlightthickness=1 if borda else 0)
        self._lbl_status.config(text=msg, fg=fg, bg=bg)
        self._frm_status.pack(fill="x", pady=(14, 0))

    def _centralizar(self):
        self.update_idletasks()
        w, h = self.winfo_reqwidth(), self.winfo_reqheight()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
