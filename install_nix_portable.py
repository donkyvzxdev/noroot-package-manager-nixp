#!/usr/bin/env python3
# nixp installer v0.3
# A no-root helper for nix-portable.

from __future__ import annotations

import os
import platform
import stat
import subprocess
import sys
import urllib.request
from pathlib import Path


NIXP_VERSION = "0.3"
INSTALLER_URL = "https://raw.githubusercontent.com/donkyvzxdev/noroot-package-manager-nixp/main/install_nix_portable.py"

HOME_DIR = Path.home()
INSTALL_DIR = HOME_DIR / ".local" / "nix-portable"
BIN_DIR = HOME_DIR / ".local" / "bin"
LOCAL_APPS_DIR = HOME_DIR / ".local" / "apps"
DESKTOP_ENTRIES_DIR = HOME_DIR / ".local" / "share" / "applications"
NIX_PORTABLE_BIN = INSTALL_DIR / "nix-portable"

DEFAULT_RUNTIME = "bwrap"
DEFAULT_NIXPKGS = "nixpkgs"
UNSTABLE_NIXPKGS = "github:NixOS/nixpkgs/nixpkgs-unstable"


LATEST_RELEASE_LOG = """Latest release log (v0.3)

Added:
  - --unstable / -u support for nrun, ninstall, nshell, and nadd.
  - --help-br for Brazilian Portuguese help.
  - Better --help output for helper commands.
  - nver for checking the nixp version.
  - nixp --version for showing the nixp helper version.
  - nixp --nix-version for showing the real Nix version.
  - nexp for opening nixp folders in the file manager.
  - nadd for creating .desktop menu entries for Nix packages or local executables.
  - nupdate for updating nixp and/or apps installed in the Nix profile.
  - nver --log and nixp --log for showing the latest release log.

Changed:
  - Brazilian Portuguese help flag changed from --br to --help-br.
  - Project version updated from 0.2 to 0.3.
  - Installer text is English-first.
  - README and help messages were improved.

Notes:
  - Stable and unstable packages can both be used.
  - Installing the same app from stable and unstable into the same profile may cause command conflicts.
  - Apps added from local files with napp or nadd are copied files and cannot be auto-updated by nixp.
"""


def info(message: str) -> None:
    print(f"[INFO] {message}")


def ok(message: str) -> None:
    print(f"[OK] {message}")


def warn(message: str) -> None:
    print(f"[WARNING] {message}")


def fail(message: str) -> None:
    print(f"[ERROR] {message}")
    sys.exit(1)


def machine_architecture() -> str:
    architecture = platform.machine().strip()

    if not architecture:
        fail("Could not detect machine architecture.")

    return architecture


def download_nix_portable() -> None:
    architecture = machine_architecture()
    download_url = f"https://github.com/DavHau/nix-portable/releases/latest/download/nix-portable-{architecture}"

    INSTALL_DIR.mkdir(parents=True, exist_ok=True)

    info(f"Downloading nix-portable to: {NIX_PORTABLE_BIN}")
    info(f"Download URL: {download_url}")

    try:
        with urllib.request.urlopen(download_url) as response:
            if response.status != 200:
                fail(f"Download failed with HTTP status {response.status}")

            temporary_file = NIX_PORTABLE_BIN.with_suffix(".tmp")

            with temporary_file.open("wb") as file_handle:
                while True:
                    chunk = response.read(1024 * 1024)

                    if not chunk:
                        break

                    file_handle.write(chunk)

            temporary_file.replace(NIX_PORTABLE_BIN)

    except Exception as error:
        fail(f"Could not download nix-portable: {error}")

    current_mode = NIX_PORTABLE_BIN.stat().st_mode
    NIX_PORTABLE_BIN.chmod(
        current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    )

    ok("nix-portable was downloaded and marked as executable.")


def write_executable(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")
    path.chmod(0o755)
    ok(f"Command created: {path}")


def apply_template(content: str) -> str:
    return (
        content.replace("@NIXP_VERSION@", NIXP_VERSION)
        .replace("@INSTALLER_URL@", INSTALLER_URL)
        .replace("@NIX_PORTABLE_BIN@", str(NIX_PORTABLE_BIN))
        .replace("@INSTALL_DIR@", str(INSTALL_DIR))
        .replace("@BIN_DIR@", str(BIN_DIR))
        .replace("@LOCAL_APPS_DIR@", str(LOCAL_APPS_DIR))
        .replace("@DESKTOP_ENTRIES_DIR@", str(DESKTOP_ENTRIES_DIR))
        .replace("@DEFAULT_RUNTIME@", DEFAULT_RUNTIME)
        .replace("@DEFAULT_NIXPKGS@", DEFAULT_NIXPKGS)
        .replace("@UNSTABLE_NIXPKGS@", UNSTABLE_NIXPKGS)
        .replace("@LATEST_RELEASE_LOG@", LATEST_RELEASE_LOG.rstrip())
    )


def create_cli_commands() -> None:
    BIN_DIR.mkdir(parents=True, exist_ok=True)
    LOCAL_APPS_DIR.mkdir(parents=True, exist_ok=True)
    DESKTOP_ENTRIES_DIR.mkdir(parents=True, exist_ok=True)

    nixp = r'''#!/usr/bin/env bash
set -e
export NP_RUNTIME="${NP_RUNTIME:-@DEFAULT_RUNTIME@}"

show_help_en() {
  cat <<'EOF'
nixp - run Nix through nix-portable

Usage:
  nixp <nix command>
  nixp --version
  nixp --nix-version
  nixp --log
  nixp --help
  nixp --help-br

Examples:
  nixp run nixpkgs#htop
  nixp profile list
  nixp store gc

Version:
  nixp --version      show nixp helper version
  nixp --nix-version  show the real Nix version used by nix-portable
  nixp --log          show nixp version and latest release log
EOF
}

show_help_br() {
  cat <<'EOF'
nixp - executa o Nix usando o nix-portable

Uso:
  nixp <comando do nix>
  nixp --version
  nixp --nix-version
  nixp --log
  nixp --help
  nixp --help-br

Exemplos:
  nixp run nixpkgs#htop
  nixp profile list
  nixp store gc

Versão:
  nixp --version      mostra a versão do helper nixp
  nixp --nix-version  mostra a versão real do Nix usado pelo nix-portable
  nixp --log          mostra a versão do nixp e o log mais recente
EOF
}

show_latest_log() {
  cat <<'EOF'
nixp @NIXP_VERSION@

@LATEST_RELEASE_LOG@
EOF
}

case "${1:-}" in
  --help|-h|help)
    show_help_en
    exit 0
    ;;
  --help-br)
    show_help_br
    exit 0
    ;;
  --version|-v|--nixp-version|version)
    echo "nixp @NIXP_VERSION@"
    exit 0
    ;;
  --nix-version)
    exec "@NIX_PORTABLE_BIN@" nix --version
    ;;
  --log)
    show_latest_log
    exit 0
    ;;
esac

exec "@NIX_PORTABLE_BIN@" nix "$@"
'''

    nrun = r'''#!/usr/bin/env bash
set -e

default_nixpkgs="@DEFAULT_NIXPKGS@"
unstable_nixpkgs="@UNSTABLE_NIXPKGS@"

show_help_en() {
  cat <<'EOF'
nrun - run a Nix package without installing it permanently

Usage:
  nrun [--unstable] <package>
  nrun [--unstable] <flake-or-package-reference>
  nrun --help
  nrun --help-br

Examples:
  nrun htop
  nrun fastfetch
  nrun --unstable firefox
  nrun nixpkgs#firefox

What it does:
  Stable/default:
    nixp run nixpkgs#<package>

  Unstable:
    nixp run github:NixOS/nixpkgs/nixpkgs-unstable#<package>
EOF
}

show_help_br() {
  cat <<'EOF'
nrun - executa um pacote Nix sem instalar permanentemente

Uso:
  nrun [--unstable] <pacote>
  nrun [--unstable] <referência-flake-ou-pacote>
  nrun --help
  nrun --help-br

Exemplos:
  nrun htop
  nrun fastfetch
  nrun --unstable firefox
  nrun nixpkgs#firefox

O que ele faz:
  Padrão/estável:
    nixp run nixpkgs#<pacote>

  Unstable:
    nixp run github:NixOS/nixpkgs/nixpkgs-unstable#<pacote>
EOF
}

use_unstable=0

case "${1:-}" in
  --help|-h|help)
    show_help_en
    exit 0
    ;;
  --help-br)
    show_help_br
    exit 0
    ;;
  --unstable|-u)
    use_unstable=1
    shift
    ;;
esac

if [ -z "${1:-}" ]; then
  show_help_en
  exit 1
fi

package_name="$1"
shift

case "$package_name" in
  *#*|github:*|gitlab:*|path:*)
    exec nixp run "$package_name" "$@"
    ;;
  *)
    if [ "$use_unstable" = "1" ]; then
      exec nixp run "$unstable_nixpkgs#$package_name" "$@"
    else
      exec nixp run "$default_nixpkgs#$package_name" "$@"
    fi
    ;;
esac
'''

    ninstall = r'''#!/usr/bin/env bash
set -e

default_nixpkgs="@DEFAULT_NIXPKGS@"
unstable_nixpkgs="@UNSTABLE_NIXPKGS@"

show_help_en() {
  cat <<'EOF'
ninstall - install Nix packages into your user profile

Usage:
  ninstall [--unstable] <package> [other packages...]
  ninstall --help
  ninstall --help-br

Examples:
  ninstall git
  ninstall nodejs python3 neovim
  ninstall --unstable firefox
  ninstall --unstable neovide vesktop

What it does:
  Stable/default:
    nixp profile install nixpkgs#<package>

  Unstable:
    nixp profile install github:NixOS/nixpkgs/nixpkgs-unstable#<package>
EOF
}

show_help_br() {
  cat <<'EOF'
ninstall - instala pacotes Nix no perfil do usuário

Uso:
  ninstall [--unstable] <pacote> [outros pacotes...]
  ninstall --help
  ninstall --help-br

Exemplos:
  ninstall git
  ninstall nodejs python3 neovim
  ninstall --unstable firefox
  ninstall --unstable neovide vesktop

O que ele faz:
  Padrão/estável:
    nixp profile install nixpkgs#<pacote>

  Unstable:
    nixp profile install github:NixOS/nixpkgs/nixpkgs-unstable#<pacote>
EOF
}

use_unstable=0

case "${1:-}" in
  --help|-h|help)
    show_help_en
    exit 0
    ;;
  --help-br)
    show_help_br
    exit 0
    ;;
  --unstable|-u)
    use_unstable=1
    shift
    ;;
esac

if [ -z "${1:-}" ]; then
  show_help_en
  exit 1
fi

package_references=()

for package_name in "$@"; do
  case "$package_name" in
    *#*|github:*|gitlab:*|path:*)
      package_references+=("$package_name")
      ;;
    *)
      if [ "$use_unstable" = "1" ]; then
        package_references+=("$unstable_nixpkgs#$package_name")
      else
        package_references+=("$default_nixpkgs#$package_name")
      fi
      ;;
  esac
done

exec nixp profile install "${package_references[@]}"
'''

    nshell = r'''#!/usr/bin/env bash
set -e

default_nixpkgs="@DEFAULT_NIXPKGS@"
unstable_nixpkgs="@UNSTABLE_NIXPKGS@"

show_help_en() {
  cat <<'EOF'
nshell - open a temporary shell with Nix packages available

Usage:
  nshell [--unstable] <package> [other packages...]
  nshell --help
  nshell --help-br

Examples:
  nshell git nodejs python3
  nshell rustc cargo
  nshell --unstable git nodejs python3

What it does:
  Stable/default:
    nixp shell nixpkgs#<package>

  Unstable:
    nixp shell github:NixOS/nixpkgs/nixpkgs-unstable#<package>
EOF
}

show_help_br() {
  cat <<'EOF'
nshell - abre um shell temporário com pacotes Nix disponíveis

Uso:
  nshell [--unstable] <pacote> [outros pacotes...]
  nshell --help
  nshell --help-br

Exemplos:
  nshell git nodejs python3
  nshell rustc cargo
  nshell --unstable git nodejs python3

O que ele faz:
  Padrão/estável:
    nixp shell nixpkgs#<pacote>

  Unstable:
    nixp shell github:NixOS/nixpkgs/nixpkgs-unstable#<pacote>
EOF
}

use_unstable=0

case "${1:-}" in
  --help|-h|help)
    show_help_en
    exit 0
    ;;
  --help-br)
    show_help_br
    exit 0
    ;;
  --unstable|-u)
    use_unstable=1
    shift
    ;;
esac

if [ -z "${1:-}" ]; then
  show_help_en
  exit 1
fi

package_references=()

for package_name in "$@"; do
  case "$package_name" in
    *#*|github:*|gitlab:*|path:*)
      package_references+=("$package_name")
      ;;
    *)
      if [ "$use_unstable" = "1" ]; then
        package_references+=("$unstable_nixpkgs#$package_name")
      else
        package_references+=("$default_nixpkgs#$package_name")
      fi
      ;;
  esac
done

exec nixp shell "${package_references[@]}"
'''

    napp = r'''#!/usr/bin/env bash
set -e

local_apps_dir="$HOME/.local/apps"
desktop_entries_dir="$HOME/.local/share/applications"

show_help_en() {
  cat <<'EOF'
napp - add a local executable or AppImage to your app menu

Usage:
  napp <executable-path> [app-name] [icon-path-or-icon-name] [categories]
  napp --help
  napp --help-br

Examples:
  napp ~/Downloads/MyApp.AppImage "My App"
  napp ~/Downloads/myapp "My App" ~/Pictures/myapp.png
  napp ~/.local/apps/myapp/myapp "My App" ~/.local/apps/myapp/icon.png "Utility;"

What it does:
  - copies the executable to ~/.local/apps/<app-id>
  - makes it executable
  - creates a .desktop file in ~/.local/share/applications
EOF
}

show_help_br() {
  cat <<'EOF'
napp - adiciona um executável local ou AppImage ao menu de apps

Uso:
  napp <caminho-do-executável> [nome-do-app] [caminho-do-ícone-ou-nome-do-ícone] [categorias]
  napp --help
  napp --help-br

Exemplos:
  napp ~/Downloads/MyApp.AppImage "My App"
  napp ~/Downloads/myapp "My App" ~/Pictures/myapp.png
  napp ~/.local/apps/myapp/myapp "My App" ~/.local/apps/myapp/icon.png "Utility;"

O que ele faz:
  - copia o executável para ~/.local/apps/<id-do-app>
  - torna o arquivo executável
  - cria um arquivo .desktop em ~/.local/share/applications
EOF
}

case "${1:-}" in
  --help|-h|help)
    show_help_en
    exit 0
    ;;
  --help-br)
    show_help_br
    exit 0
    ;;
esac

if [ -z "${1:-}" ]; then
  show_help_en
  exit 1
fi

source_path="$1"
app_name="${2:-$(basename "$source_path")}"
icon_value="${3:-}"
categories="${4:-Utility;}"

source_path="${source_path/#\~/$HOME}"
icon_value="${icon_value/#\~/$HOME}"

if [ ! -f "$source_path" ]; then
  echo "Error: executable not found: $source_path"
  exit 1
fi

app_id="$(echo "$app_name" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9._-')"

if [ -z "$app_id" ]; then
  app_id="$(basename "$source_path" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9._-')"
fi

target_dir="$local_apps_dir/$app_id"
mkdir -p "$target_dir" "$desktop_entries_dir"

target_executable="$target_dir/$(basename "$source_path")"
cp "$source_path" "$target_executable"
chmod +x "$target_executable"

icon_line=""

if [ -n "$icon_value" ] && [ -f "$icon_value" ]; then
  target_icon="$target_dir/$(basename "$icon_value")"
  cp "$icon_value" "$target_icon"
  icon_line="Icon=$target_icon"
elif [ -n "$icon_value" ]; then
  icon_line="Icon=$icon_value"
fi

desktop_file="$desktop_entries_dir/$app_id.desktop"

cat > "$desktop_file" <<EOF
[Desktop Entry]
Name=$app_name
Comment=$app_name added by nixp
Exec=$target_executable
Terminal=false
Type=Application
Categories=$categories
$icon_line
EOF

chmod +x "$desktop_file"
update-desktop-database "$desktop_entries_dir" 2>/dev/null || true

echo "App added to your menu:"
echo "  $app_name"
echo
echo "Executable copied to:"
echo "  $target_executable"
echo
echo "Desktop entry created at:"
echo "  $desktop_file"
echo
echo "If it does not appear immediately, log out and log back in, or restart your app menu."
'''

    nadd = r'''#!/usr/bin/env bash
set -e

desktop_entries_dir="$HOME/.local/share/applications"
local_apps_dir="$HOME/.local/apps"

show_help_en() {
  cat <<'EOF'
nadd - create an app menu entry for a Nix package or local executable

Usage:
  nadd [--unstable] <package-or-executable> [app-name] [icon-path-or-icon-name] [categories]
  nadd --help
  nadd --help-br

Examples:
  nadd firefox "Firefox"
  nadd --unstable firefox "Firefox Unstable"
  nadd vesktop "Vesktop" discord "Network;InstantMessaging;"
  nadd neovide "Neovide" neovide "Development;TextEditor;"
  nadd ~/Downloads/MyApp.AppImage "My App"

What it does:
  - for Nix packages, creates a .desktop entry that runs the app through nrun
  - with --unstable, the menu entry runs the app through nrun --unstable
  - for local executables/AppImages, copies the file to ~/.local/apps and creates a .desktop entry
EOF
}

show_help_br() {
  cat <<'EOF'
nadd - cria um atalho de menu para pacote Nix ou executável local

Uso:
  nadd [--unstable] <pacote-ou-executável> [nome-do-app] [caminho-do-ícone-ou-nome-do-ícone] [categorias]
  nadd --help
  nadd --help-br

Exemplos:
  nadd firefox "Firefox"
  nadd --unstable firefox "Firefox Unstable"
  nadd vesktop "Vesktop" discord "Network;InstantMessaging;"
  nadd neovide "Neovide" neovide "Development;TextEditor;"
  nadd ~/Downloads/MyApp.AppImage "My App"

O que ele faz:
  - para pacotes Nix, cria um .desktop que executa o app pelo nrun
  - com --unstable, o atalho executa o app pelo nrun --unstable
  - para executáveis/AppImages locais, copia o arquivo para ~/.local/apps e cria o .desktop
EOF
}

use_unstable=0

case "${1:-}" in
  --help|-h|help)
    show_help_en
    exit 0
    ;;
  --help-br)
    show_help_br
    exit 0
    ;;
  --unstable|-u)
    use_unstable=1
    shift
    ;;
esac

if [ -z "${1:-}" ]; then
  show_help_en
  exit 1
fi

target_value="$1"
app_name="${2:-}"
icon_value="${3:-}"
categories="${4:-Utility;}"

target_value="${target_value/#\~/$HOME}"
icon_value="${icon_value/#\~/$HOME}"

mkdir -p "$desktop_entries_dir" "$local_apps_dir"

if [ -f "$target_value" ]; then
  exec napp "$target_value" "${app_name:-$(basename "$target_value")}" "$icon_value" "$categories"
fi

package_name="$target_value"

if [ -z "$app_name" ]; then
  app_name="$package_name"
fi

app_id="$(echo "$app_name" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9._-')"

if [ -z "$app_id" ]; then
  app_id="$(echo "$package_name" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9._-')"
fi

desktop_file="$desktop_entries_dir/$app_id.desktop"

if [ -n "$icon_value" ]; then
  icon_line="Icon=$icon_value"
else
  icon_line="Icon=$package_name"
fi

if [ "$use_unstable" = "1" ]; then
  exec_line="nrun --unstable $package_name"
else
  exec_line="nrun $package_name"
fi

cat > "$desktop_file" <<EOF
[Desktop Entry]
Name=$app_name
Comment=$app_name running through nixp
Exec=$exec_line
Terminal=false
Type=Application
Categories=$categories
$icon_line
EOF

chmod +x "$desktop_file"
update-desktop-database "$desktop_entries_dir" 2>/dev/null || true

echo "Desktop entry created:"
echo "  $desktop_file"
echo
echo "It will run:"
echo "  $exec_line"
echo
echo "If it does not appear immediately, log out and log back in, or restart your app menu."
'''

    nexp = r'''#!/usr/bin/env bash
set -e

nixp_dir="$HOME/.local/nix-portable"
local_apps_dir="$HOME/.local/apps"
desktop_entries_dir="$HOME/.local/share/applications"

show_help_en() {
  cat <<'EOF'
nexp - open nixp folders in your file manager

Usage:
  nexp
  nexp app
  nexp desktop
  nexp --help
  nexp --help-br

Options:
  nexp          opens ~/.local/nix-portable
  nexp app      opens ~/.local/apps
  nexp desktop  opens ~/.local/share/applications
EOF
}

show_help_br() {
  cat <<'EOF'
nexp - abre pastas do nixp no explorador de arquivos

Uso:
  nexp
  nexp app
  nexp desktop
  nexp --help
  nexp --help-br

Opções:
  nexp          abre ~/.local/nix-portable
  nexp app      abre ~/.local/apps
  nexp desktop  abre ~/.local/share/applications
EOF
}

open_directory() {
  directory_path="$1"
  mkdir -p "$directory_path"

  echo "Opening:"
  echo "  $directory_path"

  if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$directory_path" >/dev/null 2>&1 &
    exit 0
  fi

  if command -v gio >/dev/null 2>&1; then
    gio open "$directory_path" >/dev/null 2>&1 &
    exit 0
  fi

  if command -v explorer.exe >/dev/null 2>&1; then
    windows_path="$(wslpath -w "$directory_path" 2>/dev/null || true)"
    if [ -n "$windows_path" ]; then
      explorer.exe "$windows_path" >/dev/null 2>&1 &
      exit 0
    fi
  fi

  echo
  echo "Could not open a file manager automatically."
  echo "Open this folder manually:"
  echo "  $directory_path"
}

case "${1:-nix}" in
  --help|-h|help)
    show_help_en
    ;;
  --help-br)
    show_help_br
    ;;
  nix|nixp|"")
    open_directory "$nixp_dir"
    ;;
  app|apps)
    open_directory "$local_apps_dir"
    ;;
  desktop|menu|applications)
    open_directory "$desktop_entries_dir"
    ;;
  *)
    echo "Unknown option: $1"
    echo
    show_help_en
    exit 1
    ;;
esac
'''

    nupdate = r'''#!/usr/bin/env bash
set -e

installer_url="@INSTALLER_URL@"

show_help_en() {
  cat <<'EOF'
nupdate - update nixp and/or apps installed in your Nix profile

Usage:
  nupdate
  nupdate --self
  nupdate --apps
  nupdate --help
  nupdate --help-br

Options:
  nupdate         update nixp and Nix profile apps
  nupdate --self  update only nixp helper files
  nupdate --apps  update only packages installed through ninstall / nixp profile install

Note:
  Apps added from local files with napp/nadd are copied files and cannot be auto-updated by nixp.
EOF
}

show_help_br() {
  cat <<'EOF'
nupdate - atualiza o nixp e/ou apps instalados no perfil do Nix

Uso:
  nupdate
  nupdate --self
  nupdate --apps
  nupdate --help
  nupdate --help-br

Opções:
  nupdate         atualiza o nixp e os apps do perfil Nix
  nupdate --self  atualiza apenas os arquivos do helper nixp
  nupdate --apps  atualiza apenas pacotes instalados com ninstall / nixp profile install

Observação:
  Apps adicionados de arquivos locais com napp/nadd são arquivos copiados e não podem ser atualizados automaticamente pelo nixp.
EOF
}

update_nixp_itself() {
  echo "[nixp] Updating nixp from:"
  echo "  $installer_url"
  echo

  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$installer_url" | python3
  elif command -v wget >/dev/null 2>&1; then
    wget -qO- "$installer_url" | python3
  else
    echo "Error: curl or wget is required to update nixp."
    exit 1
  fi
}

update_nix_profile_apps() {
  echo "[nixp] Upgrading packages installed in your Nix profile..."
  echo
  nixp profile upgrade '.*'
  echo
  echo "[nixp] Nix profile upgrade finished."
}

case "${1:-both}" in
  --help|-h|help)
    show_help_en
    ;;
  --help-br)
    show_help_br
    ;;
  both)
    update_nixp_itself
    echo
    update_nix_profile_apps
    ;;
  --self|self)
    update_nixp_itself
    ;;
  --apps|apps)
    update_nix_profile_apps
    ;;
  *)
    echo "Unknown option: $1"
    echo
    show_help_en
    exit 1
    ;;
esac
'''

    nver = r'''#!/usr/bin/env bash
set -e

show_help_en() {
  cat <<'EOF'
nver - show the nixp version

Usage:
  nver
  nver --log
  nver --help
  nver --help-br

Examples:
  nver
  nver --log

What it does:
  nver shows the nixp helper version.
  nver --log shows the version and the latest release log.
EOF
}

show_help_br() {
  cat <<'EOF'
nver - mostra a versão do nixp

Uso:
  nver
  nver --log
  nver --help
  nver --help-br

Exemplos:
  nver
  nver --log

O que ele faz:
  nver mostra a versão do helper nixp.
  nver --log mostra a versão e o log mais recente.
EOF
}

show_latest_log() {
  cat <<'EOF'
nixp @NIXP_VERSION@

@LATEST_RELEASE_LOG@
EOF
}

case "${1:-}" in
  --help|-h|help)
    show_help_en
    ;;
  --help-br)
    show_help_br
    ;;
  --log)
    show_latest_log
    ;;
  *)
    exec nixp --version
    ;;
esac
'''

    nhelp = r'''#!/usr/bin/env bash
set -e

show_help_en() {
  cat <<'EOF'
nixp help
version: @NIXP_VERSION@

Commands:
  nixp      run Nix through nix-portable
  nrun      run a package without installing it
  ninstall  install packages in your user profile
  nshell    open a temporary shell with packages
  nadd      create a menu entry for a Nix package or executable
  napp      add a local executable/AppImage to your menu
  nexp      open nixp folders in the file manager
  nupdate   update nixp and/or Nix profile apps
  nver      show nixp version and latest release log
  nhelp     show this help message

Examples:
  nrun htop
  nrun --unstable firefox
  ninstall git nodejs python3
  ninstall --unstable neovide vesktop
  nshell --unstable git nodejs python3
  nadd firefox "Firefox"
  nadd --unstable firefox "Firefox Unstable"
  nadd ~/Downloads/MyApp.AppImage "My App"
  nexp
  nexp app
  nexp desktop
  nupdate
  nupdate --self
  nupdate --apps
  nver
  nver --log

Version log:
  Use nver --log or nixp --log to show the current version and the latest release log.

Unstable packages:
  Use --unstable or -u with nrun, ninstall, nshell, and nadd.
  It uses:
    github:NixOS/nixpkgs/nixpkgs-unstable#<package>

Language:
  Use --help-br with any nixp helper command to see help in Brazilian Portuguese.
  Examples:
    nhelp --help-br
    nrun --help-br
    nadd --help-br

Runtime:
  Default runtime:
    NP_RUNTIME=@DEFAULT_RUNTIME@

  If you get namespace, mount, or permission errors:
    NP_RUNTIME=proot nrun htop

Useful folders:
  nix-portable:
    @INSTALL_DIR@

  local apps:
    @LOCAL_APPS_DIR@

  menu entries:
    @DESKTOP_ENTRIES_DIR@
EOF
}

show_help_br() {
  cat <<'EOF'
ajuda do nixp
versão: @NIXP_VERSION@

Comandos:
  nixp      executa o Nix pelo nix-portable
  nrun      executa um pacote sem instalar
  ninstall  instala pacotes no perfil do usuário
  nshell    abre um shell temporário com pacotes
  nadd      cria atalho de menu para pacote Nix ou executável
  napp      adiciona executável/AppImage local ao menu
  nexp      abre pastas do nixp no explorador de arquivos
  nupdate   atualiza o nixp e/ou apps do perfil Nix
  nver      mostra a versão do nixp e o log mais recente
  nhelp     mostra esta ajuda

Exemplos:
  nrun htop
  nrun --unstable firefox
  ninstall git nodejs python3
  ninstall --unstable neovide vesktop
  nshell --unstable git nodejs python3
  nadd firefox "Firefox"
  nadd --unstable firefox "Firefox Unstable"
  nadd ~/Downloads/MyApp.AppImage "My App"
  nexp
  nexp app
  nexp desktop
  nupdate
  nupdate --self
  nupdate --apps
  nver
  nver --log

Log da versão:
  Use nver --log ou nixp --log para mostrar a versão atual e o log mais recente.

Pacotes unstable:
  Use --unstable ou -u com nrun, ninstall, nshell e nadd.
  Ele usa:
    github:NixOS/nixpkgs/nixpkgs-unstable#<pacote>

Idioma:
  Use --help-br com qualquer comando helper do nixp para ver ajuda em português brasileiro.
  Exemplos:
    nhelp --help-br
    nrun --help-br
    nadd --help-br

Runtime:
  Runtime padrão:
    NP_RUNTIME=@DEFAULT_RUNTIME@

  Se aparecer erro de namespace, mount ou permissão:
    NP_RUNTIME=proot nrun htop

Pastas úteis:
  nix-portable:
    @INSTALL_DIR@

  apps locais:
    @LOCAL_APPS_DIR@

  atalhos de menu:
    @DESKTOP_ENTRIES_DIR@
EOF
}

case "${1:-}" in
  --help|-h|help|"")
    show_help_en
    ;;
  --help-br)
    show_help_br
    ;;
  *)
    echo "Unknown option: $1"
    echo
    show_help_en
    exit 1
    ;;
esac
'''

    commands = {
        "nixp": nixp,
        "nrun": nrun,
        "ninstall": ninstall,
        "nshell": nshell,
        "napp": napp,
        "nadd": nadd,
        "nexp": nexp,
        "nupdate": nupdate,
        "nver": nver,
        "nhelp": nhelp,
    }

    for command_name, command_content in commands.items():
        write_executable(BIN_DIR / command_name, apply_template(command_content))


def ensure_local_bin_in_shell_path() -> None:
    path_line = 'export PATH="$HOME/.local/bin:$PATH"'
    marker_line = "# Added by nixp installer"

    shell_config_files = [HOME_DIR / ".bashrc"]

    if (HOME_DIR / ".zshrc").exists():
        shell_config_files.append(HOME_DIR / ".zshrc")

    for config_file in shell_config_files:
        if not config_file.exists():
            config_file.touch()

        config_text = config_file.read_text(encoding="utf-8", errors="ignore")

        if "$HOME/.local/bin" in config_text or "~/.local/bin" in config_text:
            ok(f"PATH already seems configured in {config_file}")
            continue

        with config_file.open("a", encoding="utf-8") as file_handle:
            file_handle.write(f"\n{marker_line}\n{path_line}\n")

        ok(f"Added ~/.local/bin to PATH in {config_file}")


def test_installation() -> None:
    info("Testing nixp --version...")

    environment = os.environ.copy()
    environment["PATH"] = f"{BIN_DIR}:{environment.get('PATH', '')}"
    environment.setdefault("NP_RUNTIME", DEFAULT_RUNTIME)

    try:
        result = subprocess.run(
            [str(BIN_DIR / "nixp"), "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=environment,
            timeout=60,
        )

        if result.returncode == 0:
            ok(result.stdout.strip() or "nixp is working.")
        else:
            warn("nixp was installed, but the test returned an error.")

            if result.stderr.strip():
                print(result.stderr.strip())

            print()
            print("Try manually:")
            print("  nixp --version")
            print("  NP_RUNTIME=proot nixp --nix-version")

    except subprocess.TimeoutExpired:
        warn("The test took too long, but the files were installed.")
    except Exception as error:
        warn(f"Could not test automatically: {error}")


def main() -> None:
    print(f"nixp installer v{NIXP_VERSION}")
    print()

    download_nix_portable()
    create_cli_commands()
    ensure_local_bin_in_shell_path()
    test_installation()

    print()
    ok("Installation finished.")
    print()
    print("Reload your shell if needed:")
    print('  exec "$SHELL" -l')
    print()
    print("Then run:")
    print("  nhelp")
    print()
    print("For Brazilian Portuguese help:")
    print("  nhelp --help-br")
    print()
    print("Examples:")
    print("  nrun htop")
    print("  nrun --unstable firefox")
    print("  ninstall git")
    print("  ninstall --unstable neovide vesktop")
    print("  nshell --unstable nodejs python3")
    print('  nadd firefox "Firefox"')
    print('  nadd --unstable firefox "Firefox Unstable"')
    print('  nadd ~/Downloads/MyApp.AppImage "My App"')
    print("  nexp")
    print("  nexp app")
    print("  nexp desktop")
    print("  nupdate")
    print("  nver --log")
    print()
    print("If you get namespace or mount errors, try:")
    print("  NP_RUNTIME=proot nrun htop")


if __name__ == "__main__":
    main()
