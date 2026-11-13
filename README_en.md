<div align="center">

[🇧🇷 Português](README.md) · [🇺🇸 English](README_en.md)

</div>

# Educational ransomware and keylogger simulations

A DIO Cybersecurity learning track project for studying malware behavior locally in a controlled environment. Do not use these scripts on devices, accounts, networks, or files belonging to others. Use only disposable data that you own.

> **Read before running:** use only disposable files in an isolated VM. The two-minute timer ends the simulation without deleting files or the key. Decryption removes the key and note only after all files have been restored; keep backups during the exercise.
>> **During my tests on a Windows machine, Windows Defender automatically deleted the .py scripts, claiming that all of them were Trojans. Everything was executed within an Ubuntu machine to avoid any issues**.

## Contents

- [Overview and limitations](#overview-and-limitations)
- [Repository structure](#repository-structure)
- [Libraries](#libraries)
- [Safe setup and virtual environment](#safe-setup-and-virtual-environment)
- [Run the ransomware simulator](#run-the-ransomware-simulator)
- [Run the keyboard-event simulator](#run-the-keyboard-event-simulator)
- [Prevention and response](#prevention-and-response)

## Overview and limitations

### Ransomware

`ransomware/encrypt.py` encrypts regular files directly inside `ransomware/arquivos_teste/` with Fernet, writes `chave.key` to the current working directory, renames encrypted files with the `.locked` extension, and creates `LEIA_ME.txt`. After two minutes, the timer reports that the period has ended but does not delete data; the program continues waiting for terminal input. `decrypt.py` uses the local key to restore `.locked` files; it preserves the key and note if any file fails and removes them only after all files have been restored.

The target is the relative path `./arquivos_teste`, so the current working directory matters. Run commands from `ransomware/`. The key is written to the current directory, not the test folder. Keep it until recovery finishes. This demonstration is not a robust recovery tool and must not be treated as a backup solution.

### Keyboard-event simulator

`keylogger/keylogger.pyw` is a visible Tkinter application. It records keystrokes **only in its own text field**, along with clicks in its monitoring area. It does not capture keystrokes globally, hide itself, or install persistence. The local `registros.txt` report can be emailed manually when the user clicks the button.

Email uses implicit TLS SMTP to `smtp.gmail.com:465` and the `EMAIL_REMETENTE`, `EMAIL_DESTINATARIO`, and `EMAIL_SENHA` environment variables. Use only test accounts you control. Do not put real passwords in logs or the repository. A `.pyw` file may open without a console on Windows; to see output and errors, run it explicitly with `python keylogger.pyw`.

## Repository structure

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

The `arquivos_teste/`, `venv/`, cache, and log files are created locally as needed. This project does not include an images folder.

## Libraries

| Library | Source | Purpose |
|---|---|---|
| `cryptography` | Third party | `Fernet` encryption and decryption in the ransomware exercise. |
| `os`, `glob`, `random`, `threading`, `time` | Python standard library | File operations, artwork selection, timer, and countdown. |
| `tkinter`, `datetime`, `smtplib`, `email.message`, `os` | Python standard library | Visible interface, timestamps, optional report construction/email, and environment variable access. |

`requirements.txt` lists the only external dependency: `cryptography`, required by the ransomware simulator. Tkinter, `smtplib`, `email`, and the other modules used are part of the standard library. Tkinter is usually included with graphical Python installations; some Linux distributions may require installing the system Tk package.

## Safe setup and virtual environment

Use a disposable VM without shared folders, personal data, or real credentials. Keep networking disabled during the exercises; email is optional and should only be sent through a test account. Check your snapshots and backups before starting.

From the project root, create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate       # Linux/macOS
# Windows PowerShell: .\venv\Scripts\Activate.ps1
```

Install only the external dependency required by the ransomware simulator:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Windows, use `py -m venv venv` and `py -m pip ...` if `python` is unavailable. When finished, leave the virtual environment with `deactivate`.

## Run the ransomware simulator

Create fictitious files and start from the script directory so relative paths work:

```bash
mkdir -p ransomware/arquivos_teste
printf 'Disposable test content.\n' > ransomware/arquivos_teste/example.txt
cd ransomware
python encrypt.py
```

The program waits for Enter to cancel the timer. Before it expires, open another terminal at the root of the cloned repository (the folder containing this README), activate the same virtual environment, and run:

```bash
cd ransomware
python decrypt.py
```

Confirm that the content was restored. If the timer expires, it will not delete data; still, finish recovery and shut down the VM when done.

## Run the keyboard-event simulator

In another terminal, from the repository root and with a graphical session available:

```bash
source venv/bin/activate
python keylogger/keylogger.pyw
```

Enter fictitious text only in the window's text field; clicks on the canvas are also recorded. The log is written to `registros.txt` in the directory from which the command was started. Email is optional. Set variables in the terminal session (do not put them in code or versioned files):

```bash
export EMAIL_REMETENTE='test-account@example.com'
export EMAIL_DESTINATARIO='controlled-recipient@example.com'
export EMAIL_SENHA='test-credential'
```

For Gmail, use an appropriate app credential and enable sending only when needed. After the exercise, remove the variables from the session (`unset EMAIL_REMETENTE EMAIL_DESTINATARIO EMAIL_SENHA`) and delete the local log. `.gitignore` excludes virtual environments, keys, `.locked` files, generated notes, logs, and `.env` files (except `.env.example`); still check `git status` before publishing, and never commit credentials or logs.

## Prevention and response

- **Backups:** keep versioned or offline copies separate from the primary device, and test restoration regularly. A variation of the 3-2-1 rule helps reduce ransomware impact.
- **Updates:** apply patches to the operating system, browser, tools, and libraries.
- **Least privilege:** use non-administrator accounts for everyday work and restrict write and execution permissions.
- **Endpoint protection and firewall:** keep antivirus/EDR and firewall enabled, investigate alerts, and limit outbound traffic as appropriate.
- **Phishing and downloads:** verify sender and context, be cautious with unexpected attachments and links, and download software from official sources.
- **Segmentation and access:** limit shared folders and reused credentials; use MFA and segmentation to reduce lateral movement.
- **Sandboxing:** analyze suspicious samples in an isolated lab without data, credentials, shared folders, or production network access.
- **If infection is suspected:** disconnect the device from the network, preserve evidence, notify the responsible team, and follow the response and recovery plan using verified backups.

## References

- DIO Cybersecurity learning track challenge.
- [cryptography documentation](https://cryptography.io/en/latest/).
- [Python documentation](https://docs.python.org/3/), including `venv`, `tkinter`, and `smtplib`.

---
