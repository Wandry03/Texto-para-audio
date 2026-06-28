import asyncio
import os
import sys
import threading
from pathlib import Path

if getattr(sys, "frozen", False):
    sys.path.insert(0, sys._MEIPASS)

import tkinter as tk
from tkinter import messagebox, ttk

from texto_para_audio_edge import carregar_texto, gerar_mp3_unico, limpar_nome_arquivo


def pasta_base():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


BASE_DIR = pasta_base()
ARQUIVO_TEXTO = BASE_DIR / "texto.txt"
PASTA_SAIDA = BASE_DIR / "audios_gerados"


class GeradorAudioApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gerador de Audio")
        self.geometry("780x560")
        self.minsize(720, 520)
        self.configure(bg="#101820")

        self.nome_var = tk.StringVar(value="narracao")
        self.status_var = tk.StringVar(value="Pronto para gerar.")
        self.info_var = tk.StringVar(value="")
        self.gerando = False

        PASTA_SAIDA.mkdir(exist_ok=True)
        self.configurar_estilo()
        self.criar_interface()
        self.atualizar_info_texto()

    def configurar_estilo(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure(
            ".",
            background="#101820",
            foreground="#f4f7fb",
            font=("Segoe UI", 10),
        )
        self.style.configure(
            "Title.TLabel",
            background="#101820",
            foreground="#ffffff",
            font=("Segoe UI Semibold", 22),
        )
        self.style.configure(
            "Sub.TLabel",
            background="#101820",
            foreground="#a9b7c7",
            font=("Segoe UI", 10),
        )
        self.style.configure(
            "Panel.TFrame",
            background="#172331",
            relief="flat",
        )
        self.style.configure(
            "TLabel",
            background="#172331",
            foreground="#f4f7fb",
        )
        self.style.configure(
            "TEntry",
            fieldbackground="#0f1720",
            background="#0f1720",
            foreground="#ffffff",
            insertcolor="#ffffff",
            bordercolor="#2b3b4f",
            lightcolor="#2b3b4f",
            darkcolor="#2b3b4f",
            padding=10,
        )
        self.style.configure(
            "Primary.TButton",
            background="#2f80ed",
            foreground="#ffffff",
            borderwidth=0,
            focusthickness=0,
            padding=(16, 11),
            font=("Segoe UI Semibold", 10),
        )
        self.style.map(
            "Primary.TButton",
            background=[("active", "#1f6ed4"), ("disabled", "#355372")],
            foreground=[("disabled", "#a9b7c7")],
        )
        self.style.configure(
            "Secondary.TButton",
            background="#223044",
            foreground="#f4f7fb",
            borderwidth=0,
            focusthickness=0,
            padding=(14, 10),
            font=("Segoe UI", 10),
        )
        self.style.map(
            "Secondary.TButton",
            background=[("active", "#2d4059"), ("disabled", "#1b2635")],
            foreground=[("disabled", "#738094")],
        )
        self.style.configure(
            "Horizontal.TProgressbar",
            background="#2f80ed",
            troughcolor="#0f1720",
            bordercolor="#0f1720",
            lightcolor="#2f80ed",
            darkcolor="#2f80ed",
        )

    def criar_interface(self):
        container = ttk.Frame(self, style="Panel.TFrame", padding=28)
        container.pack(fill="both", expand=True, padx=24, pady=24)

        topo = ttk.Frame(container, style="Panel.TFrame")
        topo.pack(fill="x")

        ttk.Label(topo, text="Gerador de Audio", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            topo,
            text="Transforme o conteudo do texto.txt em MP3 com poucos cliques.",
            style="Sub.TLabel",
        ).pack(anchor="w", pady=(4, 0))

        acoes = ttk.Frame(container, style="Panel.TFrame")
        acoes.pack(fill="x", pady=(28, 18))
        acoes.columnconfigure(0, weight=1)
        acoes.columnconfigure(1, weight=1)
        acoes.columnconfigure(2, weight=1)

        ttk.Button(
            acoes,
            text="Abrir texto.txt",
            style="Secondary.TButton",
            command=self.abrir_texto,
        ).grid(row=0, column=0, sticky="ew", padx=(0, 10))
        ttk.Button(
            acoes,
            text="Abrir pasta de audios",
            style="Secondary.TButton",
            command=self.abrir_pasta_audios,
        ).grid(row=0, column=1, sticky="ew", padx=10)
        ttk.Button(
            acoes,
            text="Atualizar leitura",
            style="Secondary.TButton",
            command=self.atualizar_info_texto,
        ).grid(row=0, column=2, sticky="ew", padx=(10, 0))

        formulario = ttk.Frame(container, style="Panel.TFrame")
        formulario.pack(fill="x", pady=(6, 18))
        formulario.columnconfigure(0, weight=1)

        ttk.Label(formulario, text="Nome do audio").grid(row=0, column=0, sticky="w")
        self.nome_entry = ttk.Entry(formulario, textvariable=self.nome_var)
        self.nome_entry.grid(row=1, column=0, sticky="ew", pady=(8, 0))

        self.botao_gerar = ttk.Button(
            formulario,
            text="Gerar MP3",
            style="Primary.TButton",
            command=self.iniciar_geracao,
        )
        self.botao_gerar.grid(row=1, column=1, sticky="ew", padx=(14, 0), pady=(8, 0))

        self.progress = ttk.Progressbar(container, mode="determinate", maximum=1)
        self.progress.pack(fill="x", pady=(8, 10))

        ttk.Label(container, textvariable=self.status_var, style="Sub.TLabel").pack(anchor="w")
        ttk.Label(container, textvariable=self.info_var, style="Sub.TLabel").pack(anchor="w", pady=(4, 18))

        log_frame = ttk.Frame(container, style="Panel.TFrame")
        log_frame.pack(fill="both", expand=True)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.log = tk.Text(
            log_frame,
            height=9,
            bg="#0f1720",
            fg="#d8e3f0",
            insertbackground="#ffffff",
            relief="flat",
            padx=14,
            pady=12,
            wrap="word",
            font=("Consolas", 10),
        )
        self.log.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(log_frame, command=self.log.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log.configure(yscrollcommand=scrollbar.set)

        self.escrever_log("Abra o texto.txt, coloque seu texto e clique em Gerar MP3.")

    def abrir_texto(self):
        if not ARQUIVO_TEXTO.exists():
            ARQUIVO_TEXTO.write_text("", encoding="utf-8")
        os.startfile(ARQUIVO_TEXTO)
        self.escrever_log("texto.txt aberto para edicao.")

    def abrir_pasta_audios(self):
        PASTA_SAIDA.mkdir(exist_ok=True)
        os.startfile(PASTA_SAIDA)
        self.escrever_log("Pasta de audios aberta.")

    def atualizar_info_texto(self):
        if not ARQUIVO_TEXTO.exists():
            self.info_var.set("texto.txt ainda nao existe. Use o botao para criar e abrir.")
            return

        texto = carregar_texto(ARQUIVO_TEXTO)
        caracteres = len(texto.strip())
        palavras = len(texto.split())
        self.info_var.set(f"texto.txt: {caracteres} caracteres, {palavras} palavras.")

    def escrever_log(self, mensagem):
        self.log.configure(state="normal")
        self.log.insert("end", f"{mensagem}\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def iniciar_geracao(self):
        if self.gerando:
            return

        if not ARQUIVO_TEXTO.exists():
            messagebox.showerror("Arquivo nao encontrado", "O arquivo texto.txt nao foi encontrado.")
            return

        texto = carregar_texto(ARQUIVO_TEXTO)
        if not texto.strip():
            messagebox.showerror("Texto vazio", "Coloque algum texto no texto.txt antes de gerar.")
            return

        nome = limpar_nome_arquivo(self.nome_var.get())
        self.nome_var.set(nome)
        caminho_saida = PASTA_SAIDA / f"{nome}.mp3"

        self.gerando = True
        self.botao_gerar.configure(state="disabled")
        self.progress.configure(value=0, maximum=1)
        self.status_var.set("Gerando audio...")
        self.escrever_log(f"Iniciando geracao: {caminho_saida.name}")

        thread = threading.Thread(
            target=self.executar_geracao,
            args=(texto, caminho_saida),
            daemon=True,
        )
        thread.start()

    def executar_geracao(self, texto, caminho_saida):
        def progresso(atual, total):
            self.after(0, self.atualizar_progresso, atual, total)

        try:
            asyncio.run(gerar_mp3_unico(texto, caminho_saida, ao_processar_parte=progresso))
        except Exception as erro:
            self.after(0, self.geracao_falhou, str(erro))
            return

        self.after(0, self.geracao_concluida, caminho_saida)

    def atualizar_progresso(self, atual, total):
        self.progress.configure(maximum=total, value=atual)
        self.status_var.set(f"Processando parte {atual} de {total}...")
        self.escrever_log(f"Parte {atual}/{total} processada.")

    def geracao_falhou(self, erro):
        self.gerando = False
        self.botao_gerar.configure(state="normal")
        self.status_var.set("Falha ao gerar audio.")
        self.escrever_log(f"Erro: {erro}")
        messagebox.showerror("Erro ao gerar audio", erro)

    def geracao_concluida(self, caminho_saida):
        self.gerando = False
        self.botao_gerar.configure(state="normal")
        self.progress.configure(value=self.progress["maximum"])
        self.status_var.set("Audio gerado com sucesso.")
        self.atualizar_info_texto()
        self.escrever_log(f"Pronto: {caminho_saida}")
        messagebox.showinfo("Pronto", f"Audio gerado com sucesso:\n{caminho_saida}")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        teste = tk.Tk()
        teste.withdraw()
        teste.destroy()
        sys.exit(0)

    app = GeradorAudioApp()
    app.mainloop()
