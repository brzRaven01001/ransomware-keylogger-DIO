import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import smtplib
import os

from email.message import EmailMessage


class Logger:

    def __init__(self, arquivo="registros.txt"):
        self.arquivo = arquivo

    def registrar(self, mensagem):

        horario = datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        )

        with open(
            self.arquivo,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                f"[{horario}] {mensagem}\n"
            )


class EmailSender:

    def __init__(self):

        self.remetente = os.getenv(
            "EMAIL_REMETENTE"
        )

        self.destinatario = os.getenv(
            "EMAIL_DESTINATARIO"
        )

        self.senha = os.getenv(
            "EMAIL_SENHA"
        )

    def enviar_arquivo(self, arquivo):

        if not all([
            self.remetente,
            self.destinatario,
            self.senha
        ]):

            raise ValueError(
                "Configure as variáveis de ambiente "
                "de e-mail antes de enviar."
            )

        mensagem = EmailMessage()

        mensagem["Subject"] = (
            "Relatório - Simulador Educacional"
        )

        mensagem["From"] = self.remetente
        mensagem["To"] = self.destinatario

        mensagem.set_content(
            "Segue o relatório gerado pelo "
            "simulador educacional de eventos."
        )

        with open(arquivo, "rb") as anexo:

            conteudo = anexo.read()

        mensagem.add_attachment(
            conteudo,
            maintype="text",
            subtype="plain",
            filename=os.path.basename(arquivo)
        )

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465,
            timeout=20
        ) as servidor:

            servidor.login(
                self.remetente,
                self.senha
            )

            servidor.send_message(mensagem)


class KeyloggerSimulado:

    def __init__(self, janela):

        self.janela = janela

        self.janela.title(
            "Simulador Educacional de Keylogger"
        )

        self.janela.geometry("650x520")

        self.logger = Logger()

        self.email = EmailSender()

        self.criar_interface()

    def criar_interface(self):

        titulo = tk.Label(
            self.janela,
            text="SIMULADOR DE KEYLOGGER",
            font=("Arial", 18, "bold")
        )

        titulo.pack(pady=15)

        aviso = tk.Label(
            self.janela,
            text=(
                "Simulação educacional: "
                "os eventos são capturados somente nesta janela."
            ),
            fg="blue",
            wraplength=580
        )

        aviso.pack(pady=5)

        # Área de digitação

        tk.Label(
            self.janela,
            text="Área de captura de teclado:"
        ).pack(pady=5)

        self.entrada = tk.Text(
            self.janela,
            height=5,
            width=65
        )

        self.entrada.pack(pady=5)

        self.entrada.bind(
            "<KeyPress>",
            self.capturar_tecla
        )

        # Área de monitoramento do mouse

        tk.Label(
            self.janela,
            text="Área de monitoramento do mouse:"
        ).pack(pady=10)

        self.area_mouse = tk.Canvas(
            self.janela,
            width=550,
            height=170,
            bg="lightgray"
        )

        self.area_mouse.pack(pady=5)

        self.area_mouse.bind(
            "<Button-1>",
            self.capturar_clique
        )

        self.area_mouse.bind(
            "<Double-Button-1>",
            self.capturar_duplo_clique
        )

        # Status

        self.status = tk.Label(
            self.janela,
            text="Aguardando eventos...",
            fg="green"
        )

        self.status.pack(pady=10)

        # Botão de envio

        botao_email = tk.Button(
            self.janela,
            text="Enviar relatório por e-mail",
            command=self.enviar_relatorio,
            bg="#2878C8",
            fg="white",
            font=("Arial", 10, "bold")
        )

        botao_email.pack(pady=10)

    # Captura de teclado

    def capturar_tecla(self, evento):

        if evento.char and evento.char.isprintable():

            mensagem = (
                f"Tecla pressionada: {evento.char}"
            )

        else:

            mensagem = (
                f"Tecla pressionada: {evento.keysym}"
            )

        self.logger.registrar(mensagem)

        self.status.config(
            text=mensagem,
            fg="green"
        )

    # Captura de clique simples

    def capturar_clique(self, evento):

        mensagem = (
            f"CLIQUE SIMPLES - "
            f"X: {evento.x} | Y: {evento.y}"
        )

        self.logger.registrar(mensagem)

        self.status.config(
            text=mensagem
        )

    # Captura de clique duplo

    def capturar_duplo_clique(self, evento):

        mensagem = (
            f"CLIQUE DUPLO - "
            f"X: {evento.x} | Y: {evento.y}"
        )

        self.logger.registrar(mensagem)

        self.status.config(
            text=mensagem
        )

    # Envio do relatório

    def enviar_relatorio(self):

        arquivo = self.logger.arquivo

        if not os.path.exists(arquivo):

            messagebox.showwarning(
                "Aviso",
                "Nenhum relatório foi encontrado."
            )

            return

        try:

            self.email.enviar_arquivo(arquivo)

            messagebox.showinfo(
                "Sucesso",
                "Relatório enviado com sucesso!"
            )

            self.status.config(
                text="Relatório enviado!",
                fg="green"
            )

        except Exception as erro:

            messagebox.showerror(
                "Erro no envio",
                str(erro)
            )

            self.status.config(
                text="Falha no envio do relatório.",
                fg="red"
            )


# ==========================================
# EXECUÇÃO PRINCIPAL
# ==========================================

if __name__ == "__main__":

    janela = tk.Tk()

    aplicativo = KeyloggerSimulado(janela)

    janela.mainloop()
