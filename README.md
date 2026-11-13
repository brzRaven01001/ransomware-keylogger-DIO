<div align="center">

[🇧🇷 Português](README.md) · [🇺🇸 English](README_en.md)

</div>

# Simulações educacionais de ransomware e keylogger

Projeto da trilha de Cibersegurança da DIO para estudar comportamentos de malware em ambiente local e controlado. Os scripts não devem ser usados em dispositivos, contas, redes ou arquivos de terceiros. Use somente dados descartáveis e próprios.

> **Atenção antes de executar:** use apenas arquivos descartáveis em uma VM isolada. O timer de dois minutos encerra a simulação sem apagar arquivos nem chave. A descriptografia remove a chave e a nota somente quando todos os arquivos forem restaurados; mantenha cópias de segurança durante o exercício.
> **Durante meus testes em uma máquina windows, o Windows Defender automaticamente deletou os scripts .py, alegando ter idenficados todos como trojan. Tudo foi executado dentro de uma máquina Ubuntu para evitar quaisquer problemas**.

## Conteúdo

- [Visão geral e limites](#visão-geral-e-limites)
- [Estrutura](#estrutura)
- [Bibliotecas](#bibliotecas)
- [Preparação segura e ambiente virtual](#preparação-segura-e-ambiente-virtual)
- [Executar o simulador de ransomware](#executar-o-simulador-de-ransomware)
- [Executar o simulador de eventos de teclado](#executar-o-simulador-de-eventos-de-teclado)
- [Prevenção e resposta](#prevenção-e-resposta)

## Visão geral e limites

### Ransomware

`ransomware/encrypt.py` criptografa arquivos regulares diretamente dentro de `ransomware/arquivos_teste/` usando Fernet, grava `chave.key` no diretório de trabalho atual, renomeia os resultados com `.locked` e cria `LEIA_ME.txt`. Após dois minutos, o timer informa o fim do período, mas não apaga dados; o programa continua aguardando uma ação no terminal. `decrypt.py` usa a chave local para recuperar arquivos `.locked`; preserva a chave e a nota se algum arquivo falhar e só as remove quando todos forem restaurados.

O alvo está definido como caminho relativo `./arquivos_teste`, portanto o diretório corrente importa. Rode os comandos a partir de `ransomware/`. A chave é criada no diretório corrente, não dentro da pasta de teste. Preserve-a até a recuperação terminar. Esta demonstração não implementa recuperação robusta nem deve ser tratada como ferramenta de backup.

### Simulador de eventos de teclado

`keylogger/keylogger.pyw` é uma aplicação Tkinter visível. Registra teclas digitadas **somente no campo de texto da própria janela**, além de cliques na área de monitoramento. Não captura globalmente o teclado, não se oculta e não instala persistência. O relatório local `registros.txt` pode ser enviado manualmente por e-mail quando o usuário clica no botão.

O envio usa SMTP sobre TLS implícito para `smtp.gmail.com:465` e as variáveis `EMAIL_REMETENTE`, `EMAIL_DESTINATARIO` e `EMAIL_SENHA`. Use apenas contas de teste sob seu controle. Não armazene senhas reais nos logs nem no repositório. O arquivo `.pyw` pode abrir sem console no Windows; para observar mensagens/erros, execute-o explicitamente com `python keylogger.pyw`.

## Estrutura

```text
.
├── README.md
├── README_en.md
├── ransomware/
│   ├── encrypt.py
│   ├── decrypt.py
│   └── nota_resgate.py
└── keylogger/
    └── keylogger.pyw
```

As pastas `arquivos_teste/`, `venv/`, caches e logs são criadas localmente conforme necessário; não há pasta de imagens neste projeto.

## Bibliotecas

| Biblioteca | Origem | Uso |
|---|---|---|
| `cryptography` | Externa | `Fernet` para criptografia e descriptografia no exercício de ransomware. |
| `os`, `glob`, `random`, `threading`, `time` | Biblioteca padrão | Operações de arquivos, seleção de arte, timer e contagem regressiva. |
| `tkinter`, `datetime`, `smtplib`, `email.message`, `os` | Biblioteca padrão | Interface visível, horários, montagem/envio opcional do relatório e leitura de variáveis de ambiente. |

O `requirements.txt` lista a única dependência externa: `cryptography`, necessária ao simulador de ransomware. Tkinter, `smtplib`, `email` e os demais módulos usados são da biblioteca padrão. Tkinter normalmente acompanha as instalações de Python com suporte gráfico; em algumas distribuições Linux pode ser necessário instalar o pacote Tk do sistema.

## Preparação segura e ambiente virtual

Use uma VM descartável, sem pastas compartilhadas, dados pessoais ou credenciais reais. Mantenha a rede desligada durante os exercícios; o envio de e-mail é opcional e deve ser feito apenas em uma conta de teste. Verifique snapshots e backups antes de começar.

Na raiz do projeto, crie e ative uma venv:

```bash
python3 -m venv venv
source venv/bin/activate       # Linux/macOS
# No Windows PowerShell: .\venv\Scripts\Activate.ps1
```

Instale somente a dependência externa necessária ao ransomware:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

No Windows, use `py -m venv venv` e `py -m pip ...` se `python` não estiver disponível. Ao terminar, saia da venv com `deactivate`.

## Executar o simulador de ransomware

Crie arquivos fictícios e inicie a partir do diretório do script para que os caminhos relativos funcionem:

```bash
mkdir -p ransomware/arquivos_teste
printf 'Conteúdo descartável para teste.\n' > ransomware/arquivos_teste/exemplo.txt
cd ransomware
python encrypt.py
```

O programa aguarda Enter para cancelar o timer. Antes de expirar, abra outro terminal na raiz do repositório clonado (a pasta que contém este README), ative a mesma venv e execute:

```bash
cd ransomware
python decrypt.py
```

Confirme o conteúdo restaurado. Se o timer expirar, ele não apaga os dados; ainda assim, conclua a recuperação e encerre a VM ao terminar.

## Executar o simulador de eventos de teclado

Em outro terminal, na raiz do repositório, com ambiente gráfico disponível:

```bash
source venv/bin/activate
python keylogger/keylogger.pyw
```

Digite apenas texto fictício no campo da janela; cliques no canvas também são registrados. O log é gravado em `registros.txt` no diretório de onde o comando foi iniciado. O envio por e-mail é opcional. Configure as variáveis na sessão do terminal (não as coloque no código nem em arquivos versionados):

```bash
export EMAIL_REMETENTE='conta-de-teste@example.com'
export EMAIL_DESTINATARIO='destino-controlado@example.com'
export EMAIL_SENHA='credencial-de-teste'
```

Para Gmail, use uma credencial apropriada para aplicativo e habilite o envio somente quando necessário. Depois do teste, remova as variáveis da sessão (`unset EMAIL_REMETENTE EMAIL_DESTINATARIO EMAIL_SENHA`) e apague o log local. O `.gitignore` exclui ambientes virtuais, chaves, arquivos `.locked`, notas geradas, logs e arquivos `.env` (com exceção de `.env.example`); ainda assim, confira `git status` antes de publicar e nunca versione credenciais ou registros.

## Prevenção e resposta

- **Backups:** mantenha cópias versionadas ou offline, separadas do dispositivo principal; teste periodicamente a restauração. Uma variação da regra 3-2-1 ajuda a reduzir o impacto de ransomware.
- **Atualizações:** aplique correções em sistema operacional, navegador, ferramentas e bibliotecas.
- **Menor privilégio:** use contas sem privilégios administrativos no dia a dia e restrinja permissões de escrita e execução.
- **Proteção de endpoint e firewall:** mantenha antivírus/EDR e firewall ativos, investigue alertas e limite tráfego de saída conforme a necessidade.
- **Phishing e downloads:** confirme remetente e contexto, desconfie de anexos/links inesperados e baixe software de fontes oficiais.
- **Segmentação e acesso:** limite compartilhamentos e credenciais reutilizadas; use MFA e segmentação para reduzir movimentação lateral.
- **Sandbox:** analise amostras suspeitas em laboratório isolado, sem dados, credenciais, pastas compartilhadas ou rede de produção.
- **Se houver suspeita de infecção:** desconecte o equipamento da rede, não apague evidências, avise a equipe responsável e siga o plano de resposta e restauração a partir de cópias verificadas.

## Referências

- Desafio da trilha de Cibersegurança — DIO.
- [Documentação da biblioteca cryptography](https://cryptography.io/en/latest/).
- [Documentação do Python](https://docs.python.org/3/), incluindo `venv`, `tkinter` e `smtplib`.

---
