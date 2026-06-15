#!/usr/bin/env python3
"""
Instalador simples do nix-portable sem sudo/root.

O que ele faz:
- Baixa o nix-portable para ~/.local/nix-portable/nix-portable
- Cria comandos em ~/.local/bin:
  - nixp
  - nrun
  - ninstall
  - nshell
  - nhelp
- Adiciona ~/.local/bin ao PATH no ~/.bashrc, se necessário

Uso:
  python3 install_nix_portable.py
"""

from __future__ import annotations

import os
import platform
import stat
import subprocess
import sys
import urllib.request
from pathlib import Path


HOME = Path.home()
INSTALL_DIR = HOME / ".local" / "nix-portable"
BIN_DIR = HOME / ".local" / "bin"
NIX_PORTABLE_BIN = INSTALL_DIR / "nix-portable"

# Runtime padrão.
# No seu caso anterior, NP_RUNTIME=bwrap funcionou.
# Se der erro de namespace, rode: NP_RUNTIME=proot nrun htop
DEFAULT_RUNTIME = "bwrap"


def info(msg: str) -> None:
    print(f"[INFO] {msg}")


def ok(msg: str) -> None:
    print(f"[OK] {msg}")


def warn(msg: str) -> None:
    print(f"[AVISO] {msg}")


def fail(msg: str) -> None:
    print(f"[ERRO] {msg}")
    sys.exit(1)


def machine_arch() -> str:
    """
    Equivalente simples a `uname -m`.
    O release do nix-portable usa nomes como x86_64 e aarch64.
    """
    arch = platform.machine().strip()
    if not arch:
        fail("Não consegui detectar a arquitetura da máquina.")
    return arch


def download_nix_portable() -> None:
    arch = machine_arch()
    url = f"https://github.com/DavHau/nix-portable/releases/latest/download/nix-portable-{arch}"

    INSTALL_DIR.mkdir(parents=True, exist_ok=True)

    info(f"Baixando nix-portable para: {NIX_PORTABLE_BIN}")
    info(f"URL: {url}")

    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                fail(f"Download falhou com status HTTP {response.status}")

            tmp_path = NIX_PORTABLE_BIN.with_suffix(".tmp")
            with tmp_path.open("wb") as f:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)

            tmp_path.replace(NIX_PORTABLE_BIN)

    except Exception as e:
        fail(f"Não foi possível baixar o nix-portable: {e}")

    current_mode = NIX_PORTABLE_BIN.stat().st_mode
    NIX_PORTABLE_BIN.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    ok("nix-portable baixado e marcado como executável.")


def write_executable(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")
    path.chmod(0o755)
    ok(f"Comando criado: {path}")


def create_cli_commands() -> None:
    BIN_DIR.mkdir(parents=True, exist_ok=True)

    nixp = f"""#!/usr/bin/env bash
set -e
export NP_RUNTIME="${{NP_RUNTIME:-{DEFAULT_RUNTIME}}}"
exec "{NIX_PORTABLE_BIN}" nix "$@"
"""

    nrun = """#!/usr/bin/env bash
set -e

if [ -z "$1" ]; then
  echo "Uso: nrun <pacote>"
  echo "Exemplo: nrun htop"
  echo "Exemplo: nrun nixpkgs#htop"
  exit 1
fi

pkg="$1"
shift

case "$pkg" in
  *#*|github:*|gitlab:*|path:*)
    exec nixp run "$pkg" "$@"
    ;;
  *)
    exec nixp run "nixpkgs#$pkg" "$@"
    ;;
esac
"""

    ninstall = """#!/usr/bin/env bash
set -e

if [ -z "$1" ]; then
  echo "Uso: ninstall <pacote> [outros pacotes...]"
  echo "Exemplo: ninstall htop"
  echo "Exemplo: ninstall git nodejs python3"
  exit 1
fi

args=()

for pkg in "$@"; do
  case "$pkg" in
    *#*|github:*|gitlab:*|path:*)
      args+=("$pkg")
      ;;
    *)
      args+=("nixpkgs#$pkg")
      ;;
  esac
done

exec nixp profile install "${args[@]}"
"""

    nshell = """#!/usr/bin/env bash
set -e

if [ -z "$1" ]; then
  echo "Uso: nshell <pacote> [outros pacotes...]"
  echo "Exemplo: nshell git nodejs python3"
  exit 1
fi

args=()

for pkg in "$@"; do
  case "$pkg" in
    *#*|github:*|gitlab:*|path:*)
      args+=("$pkg")
      ;;
    *)
      args+=("nixpkgs#$pkg")
      ;;
  esac
done

exec nixp shell "${args[@]}"
"""

    nhelp = f"""#!/usr/bin/env bash
cat <<'EOF'
nix-portable helper

Comandos principais:

  nhelp
    Mostra esta ajuda.

  nixp <comando do nix>
    Executa o Nix pelo nix-portable.
    Exemplos:
      nixp --version
      nixp run nixpkgs#htop
      nixp profile list

  nrun <pacote>
    Roda um programa sem instalar permanentemente.
    Exemplos:
      nrun htop
      nrun btop
      nrun fastfetch
      nrun neovim

  ninstall <pacote>
    Instala um pacote no perfil do usuário.
    Exemplos:
      ninstall htop
      ninstall git
      ninstall nodejs
      ninstall python3
      ninstall neovim

  nshell <pacote> [outros pacotes...]
    Abre um shell temporário com os pacotes disponíveis.
    Exemplos:
      nshell git
      nshell git nodejs python3
      nshell rustc cargo

  nixp profile list
    Lista pacotes instalados no perfil.

  nixp profile remove <número-ou-pacote>
    Remove um pacote instalado no perfil.

  nixp store gc
    Limpa arquivos antigos do store do Nix.

Exemplos úteis:

  nrun htop
  nrun fastfetch
  ninstall neovim
  nshell git nodejs python3

Runtime:

  Por padrão, estes comandos usam:
    NP_RUNTIME={DEFAULT_RUNTIME}

  Se der erro de namespace/mount, tente:
    NP_RUNTIME=proot nrun htop

  Se quiser trocar temporariamente:
    NP_RUNTIME=proot ninstall git

Arquivos instalados:

  Binário do nix-portable:
    {NIX_PORTABLE_BIN}

  Comandos criados:
    {BIN_DIR}/nixp
    {BIN_DIR}/nrun
    {BIN_DIR}/ninstall
    {BIN_DIR}/nshell
    {BIN_DIR}/nhelp

EOF
"""

    write_executable(BIN_DIR / "nixp", nixp)
    write_executable(BIN_DIR / "nrun", nrun)
    write_executable(BIN_DIR / "ninstall", ninstall)
    write_executable(BIN_DIR / "nshell", nshell)
    write_executable(BIN_DIR / "nhelp", nhelp)


def ensure_path_in_shell_rc() -> None:
    line = 'export PATH="$HOME/.local/bin:$PATH"'
    marker = "# Added by install_nix_portable.py"

    rc_files = [HOME / ".bashrc"]

    # Se o usuário tiver zshrc, também ajusta.
    if (HOME / ".zshrc").exists():
        rc_files.append(HOME / ".zshrc")

    for rc in rc_files:
        if not rc.exists():
            rc.touch()

        text = rc.read_text(encoding="utf-8", errors="ignore")

        if "$HOME/.local/bin" in text or "~/.local/bin" in text:
            ok(f"PATH já parece configurado em {rc}")
            continue

        with rc.open("a", encoding="utf-8") as f:
            f.write(f"\n{marker}\n{line}\n")

        ok(f"Adicionado ~/.local/bin ao PATH em {rc}")


def test_installation() -> None:
    info("Testando o comando nixp --version...")

    env = os.environ.copy()
    env["PATH"] = f"{BIN_DIR}:{env.get('PATH', '')}"
    env.setdefault("NP_RUNTIME", DEFAULT_RUNTIME)

    try:
        result = subprocess.run(
            [str(BIN_DIR / "nixp"), "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
            timeout=60,
        )

        if result.returncode == 0:
            ok(result.stdout.strip() or "nixp funcionando.")
        else:
            warn("O nixp foi instalado, mas o teste retornou erro.")
            if result.stderr.strip():
                print(result.stderr.strip())
            print()
            print("Tente manualmente:")
            print("  nixp --version")
            print("  NP_RUNTIME=proot nixp --version")

    except subprocess.TimeoutExpired:
        warn("O teste demorou demais, mas os arquivos foram instalados.")
    except Exception as e:
        warn(f"Não consegui testar automaticamente: {e}")


def main() -> None:
    print("Instalador do nix-portable sem sudo/root")
    print()

    download_nix_portable()
    create_cli_commands()
    ensure_path_in_shell_rc()
    test_installation()

    print()
    ok("Instalação finalizada.")
    print()
    print("Agora rode:")
    print("  source ~/.bashrc")
    print("  nhelp")
    print()
    print("Exemplos:")
    print("  nrun htop")
    print("  ninstall git")
    print("  nshell nodejs python3")
    print()
    print("Se der erro de namespace/mount, tente:")
    print("  NP_RUNTIME=proot nrun htop")


if __name__ == "__main__":
    main()
