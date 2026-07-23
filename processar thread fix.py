# Substitua o método _processar_thread inteiro no main.py por este:

    def _processar_thread(self):
        self._btn_gerar.config(state="disabled", bg="#cccccc")

        # Mostra barra e log imediatamente
        self._progress.pack(fill="x", pady=(12, 0))
        self._progress.start(12)
        self._log_limpar()
        self._frm_log.pack(fill="x", pady=(12, 0))
        self._set_status("")

        # Força o redesenho da janela ANTES de iniciar a thread
        self.update()
        self.update_idletasks()

        # Só então inicia o processamento em background
        threading.Thread(target=self._processar, daemon=True).start()
