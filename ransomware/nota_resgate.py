import os


CONTEUDO_NOTA = """
=================================================================
       !! TODOS OS SEUS ARQUIVOS FORAM CRIPTOGRAFADOS !!
=================================================================

O que aconteceu com meus arquivos?
-----------------------------------
Seus arquivos foram bloqueados com criptografia AES-128.
Documentos, imagens e outros arquivos não podem ser acessados
sem a chave de descriptografia.

Como recupero meus arquivos?
------------------------------
Execute o script decrypt.py com a chave correta (chave.key)
antes que o tempo se esgote.

Ao fim do prazo, a simulação será encerrada sem apagar arquivos ou a chave.

⏳ O tempo está correndo.

-----------------------------------------------------------------
   [SIMULAÇÃO FICTÍCIA — NENHUM DANO REAL FOI CAUSADO]
-----------------------------------------------------------------
"""


def criar_nota(pasta: str) -> None:
    caminho = os.path.join(pasta, "LEIA_ME.txt")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(CONTEUDO_NOTA)
    print(f"  [+] Nota de resgate criada em: {caminho}")
