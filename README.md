# nixp

**nixp** is a small helper that makes [nix-portable](https://github.com/DavHau/nix-portable) easier to install and use without `sudo` or root access.

It is useful for WSL, shared machines, restricted Linux environments, or any system where you do not want to install Nix globally in `/nix`.

## What it does

The installer:

- downloads `nix-portable`
- saves it in `~/.local/nix-portable`
- creates simple commands in `~/.local/bin`
- adds `~/.local/bin` to your `PATH` if needed
- reloads your shell after installation, so the new commands can be used right away

Everything is installed inside your user directory.

## Install

```bash
curl -fsSL "https://raw.githubusercontent.com/donkyvzxdev/noroot-package-manager-nixp/main/install_nix_portable.py" | python3 && exec "$SHELL" -l
```

This runs the installer and then reloads your shell automatically.  
After that, you can use the new commands directly:

```bash
nhelp
```

## Commands

| Command | Description |
|---|---|
| `nixp` | Runs Nix through nix-portable |
| `nrun` | Runs a package without installing it |
| `ninstall` | Installs packages in your user profile |
| `nshell` | Opens a temporary shell with packages |
| `nhelp` | Shows help and examples |

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

Use Nix directly:

```bash
nixp --version
nixp profile list
nixp store gc
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
~/.local/bin/nhelp
```

## Uninstall

```bash
rm -rf ~/.local/nix-portable
rm -f ~/.local/bin/nixp ~/.local/bin/nrun ~/.local/bin/ninstall ~/.local/bin/nshell ~/.local/bin/nhelp
```

You can also remove this line from `~/.bashrc` if the installer added it:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Notes

nixp is only a helper around nix-portable. It does not replace Nix or nix-portable.

Some graphical apps or Wayland compositors may not work correctly in WSL or restricted environments.

## Credits

Credits go to the Nix/NixOS community and the nix-portable contributors.

This project only provides a simple installer and helper commands for nix-portable.
