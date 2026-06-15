# Nixp

**Version:** `0.3`

[![Changelog](https://img.shields.io/badge/Changelog-View%20updates-blue?style=for-the-badge)](https://github.com/donkyvzxdev/noroot-package-manager-nixp/blob/main/CHANGELOG.md)

**nixp** is a small helper that makes [nix-portable](https://github.com/DavHau/nix-portable) easier to install and use without `sudo` or root access.

It is useful for WSL, shared machines, restricted Linux environments, or any system where you do not want to install Nix globally in `/nix`.

## Install

```bash
curl -fsSL "https://raw.githubusercontent.com/donkyvzxdev/noroot-package-manager-nixp/main/install_nix_portable.py" | python3 && exec "$SHELL" -l
```

Then run:

```bash
nhelp
```

For Brazilian Portuguese help:

```bash
nhelp --help-br
```

## What it does

The installer:

- downloads `nix-portable`
- saves it in `~/.local/nix-portable`
- creates helper commands in `~/.local/bin`
- adds `~/.local/bin` to your `PATH` if needed
- keeps everything inside your user directory
- does not require `sudo` or root

## Commands

| Command | Description |
|---|---|
| `nixp` | Runs Nix through nix-portable |
| `nrun` | Runs a package without installing it |
| `ninstall` | Installs packages in your user profile |
| `nshell` | Opens a temporary shell with packages |
| `nadd` | Creates a menu entry for a Nix package or executable |
| `napp` | Adds a local executable/AppImage to your menu |
| `nexp` | Opens nixp folders in the file manager |
| `nupdate` | Updates nixp and/or Nix profile apps |
| `nver` | Shows the nixp version and latest release log |
| `nhelp` | Shows help |

Every helper command supports:

```bash
--help
```

Brazilian Portuguese help is available with:

```bash
--help-br
```

Examples:

```bash
nrun --help
nrun --help-br
nadd --help
nadd --help-br
```

## Unstable packages

Some commands support `--unstable` or `-u`.

This uses:

```bash
github:NixOS/nixpkgs/nixpkgs-unstable#<package>
```

Supported commands:

```bash
nrun --unstable <package>
ninstall --unstable <package>
nshell --unstable <package>
nadd --unstable <package>
```

Examples:

```bash
nrun --unstable firefox
ninstall --unstable neovide vesktop
nshell --unstable nodejs python3
nadd --unstable firefox "Firefox Unstable"
```

## Examples

Run a package:

```bash
nrun htop
```

Install packages:

```bash
ninstall git nodejs python3
```

Open a temporary shell:

```bash
nshell git nodejs python3
```

Create a menu entry for a Nix package:

```bash
nadd firefox "Firefox"
```

Create a menu entry with icon/category:

```bash
nadd vesktop "Vesktop" discord "Network;InstantMessaging;"
```

Add a local executable or AppImage to your menu:

```bash
nadd ~/Downloads/MyApp.AppImage "My App"
```

Open nixp folders:

```bash
nexp
nexp app
nexp desktop
```

Update everything:

```bash
nupdate
```

Update only nixp:

```bash
nupdate --self
```

Update only apps installed with `ninstall` / `nixp profile install`:

```bash
nupdate --apps
```

## Version log

Show only the nixp version:

```bash
nver
```

or:

```bash
nixp --version
```

Show the nixp version and the latest release log:

```bash
nver --log
```

or:

```bash
nixp --log
```

Check the real Nix version used by nix-portable:

```bash
nixp --nix-version
```

For the full update history, open the changelog button at the top of this README or read `CHANGELOG.md`.

## Useful folders

nix-portable:

```bash
~/.local/nix-portable
```

Local apps added by `napp` or local-file `nadd`:

```bash
~/.local/apps
```

Menu entries:

```bash
~/.local/share/applications
```

## Runtime

By default, nixp uses:

```bash
NP_RUNTIME=bwrap
```

If you get permission, mount, or namespace errors, try:

```bash
NP_RUNTIME=proot nrun htop
```

## Installed files

```bash
~/.local/nix-portable/nix-portable
~/.local/bin/nixp
~/.local/bin/nrun
~/.local/bin/ninstall
~/.local/bin/nshell
~/.local/bin/napp
~/.local/bin/nadd
~/.local/bin/nexp
~/.local/bin/nupdate
~/.local/bin/nver
~/.local/bin/nhelp
```

## Uninstall

```bash
rm -rf ~/.local/nix-portable ~/.local/apps
rm -f ~/.local/bin/nixp ~/.local/bin/nrun ~/.local/bin/ninstall ~/.local/bin/nshell ~/.local/bin/napp ~/.local/bin/nadd ~/.local/bin/nexp ~/.local/bin/nupdate ~/.local/bin/nver ~/.local/bin/nhelp
```

You can also remove this line from `~/.bashrc` if the installer added it:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Notes

nixp is only a helper around nix-portable. It does not replace Nix or nix-portable.

Some graphical apps or Wayland compositors may not work correctly in WSL or restricted environments.

Stable and unstable packages can both be used, but installing the same app from both channels may cause command conflicts in the user profile.

Apps added from local executable files with `napp` or `nadd` are copied files and cannot be automatically updated by nixp.

## Credits

Credits go to the Nix/NixOS community and the nix-portable contributors.

This project only provides a simple installer and helper commands for nix-portable.
