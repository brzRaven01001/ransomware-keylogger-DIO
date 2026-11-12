import os
import glob
from cryptography.fernet import Fernet, InvalidToken


# =============================================================================
# CONFIGURAÇÕES
# =============================================================================

PASTA_ALVO      = "./arquivos_teste"
EXTENSAO_LOCKED = ".locked"
ARQUIVO_CHAVE   = "chave.key"


# =============================================================================
# FUNÇÕES
# =============================================================================

def carregar_chave() -> bytes:
    with open(ARQUIVO_CHAVE, "rb") as f:
        return f.read()


def descriptografar_arquivo(caminho: str, fernet: Fernet) -> None:
    with open(caminho, "rb") as f:
        dados = f.read()

    caminho_original = caminho[:-len(EXTENSAO_LOCKED)]
    if os.path.exists(caminho_original):
        raise FileExistsError(f"O arquivo de destino já existe: {caminho_original}")
    with open(caminho_original, "wb") as f:
        f.write(fernet.decrypt(dados))

    os.remove(caminho)
    print(f"  [+] {os.path.basename(caminho)} → {os.path.basename(caminho_original)}")


def limpar_rastros(pasta: str) -> None:
    for alvo in [os.path.join(pasta, "LEIA_ME.txt"), ARQUIVO_CHAVE]:
        if os.path.exists(alvo):
            os.remove(alvo)
            print(f"  [+] Removido: {alvo}")


# =============================================================================
# FLUXO PRINCIPAL
# =============================================================================

def main():
    print("=" * 50)
    print("       DECRYPT — Restaurando seus arquivos")
    print("=" * 50 + "\n")

    if not os.path.exists(ARQUIVO_CHAVE):
        print(f"[ERRO] Chave '{ARQUIVO_CHAVE}' não encontrada.")
        print("Execute o encrypt.py antes do decrypt.py.")
        return

    if not os.path.isdir(PASTA_ALVO):
        print(f"[ERRO] Pasta '{PASTA_ALVO}' não encontrada.")
        return

    try:
        fernet = Fernet(carregar_chave())
        print(f"[*] Chave carregada: {ARQUIVO_CHAVE}\n")
    except Exception as e:
        print(f"[ERRO] Falha ao carregar a chave: {e}")
        return

    arquivos = glob.glob(os.path.join(PASTA_ALVO, f"*{EXTENSAO_LOCKED}"))

    if not arquivos:
        print("[AVISO] Nenhum arquivo .locked encontrado.")
        return

    print("[*] Iniciando descriptografia...\n")
    erros = 0

    for arquivo in arquivos:
        try:
            descriptografar_arquivo(arquivo, fernet)
        except InvalidToken:
            print(f"  [ERRO] {os.path.basename(arquivo)} — chave incorreta ou arquivo corrompido.")
            erros += 1
        except Exception as e:
            print(f"  [ERRO] {os.path.basename(arquivo)}: {e}")
            erros += 1

    sucesso = len(arquivos) - erros
    if erros == 0:
        limpar_rastros(PASTA_ALVO)
    else:
        print("[AVISO] Chave e nota foram preservadas para permitir nova tentativa.")
    print(f"\n{'=' * 50}")
    print(f"  ✅ {sucesso}/{len(arquivos)} arquivo(s) restaurado(s) com sucesso.")
    if erros:
        print(f"  ⚠️  {erros} arquivo(s) com erro.")
    print("=" * 50)


if __name__ == "__main__":
    main()
