
## Nixp

**Version:** `0.2`

**nixp** is a small helper that makes [nix-portable](https://github.com/DavHau/nix-portable) easier to install and use without `sudo` or root access.

It is useful for WSL, shared machines, restricted Linux environments, or any system where you do not want to install Nix globally in `/nix`.

## What it does

The installer:

- downloads `nix-portable`
- saves it in `~/.local/nix-portable`
- creates simple commands in `~/.local/bin`
- adds `~/.local/bin` to your `PATH` if needed
- adds helpers for app menu entries and file explorer shortcuts
- adds a helper for updating nixp and installed Nix profile apps

Everything is installed inside your user directory.

## Install

```bash
curl -fsSL "https://raw.githubusercontent.com/donkyvzxdev/noroot-package-manager-nixp/main/install_nix_portable.py" | python3 && exec "$SHELL" -l
```

This runs the installer and reloads your shell automatically.

Then check the help menu:

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
| `napp` | Adds a local executable/AppImage to your app menu |
| `nadd` | Creates a `.desktop` menu entry for a Nix package or local executable |
| `nexp` | Opens nixp folders in the file manager |
| `nupdate` | Updates nixp and/or installed Nix profile apps |
| `nver` | Shows the nixp version |
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

Add a Nix package to your app menu:

```bash
nadd firefox "Firefox"
```

Add a Nix package with an icon/category:

```bash
nadd vesktop "Vesktop" discord "Network;InstantMessaging;"
```

Add a local executable or AppImage to your app menu:

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

Update only apps installed through `ninstall` / `nixp profile install`:

```bash
nupdate --apps
```

Check versions:

```bash
nixp --version
nver
nixp --nix-version
```

Use Nix directly:

```bash
nixp profile list
nixp store gc
```

## App menu helpers

### `nadd`

`nadd` creates a `.desktop` menu entry automatically.

For Nix packages, it creates a launcher that runs the package with `nrun`:

```bash
nadd firefox "Firefox"
```

For local executables/AppImages, it copies the file to `~/.local/apps` and creates the menu entry:

```bash
nadd ~/Downloads/MyApp.AppImage "My App"
```

### `napp`

`napp` is focused only on local executables/AppImages:

```bash
napp ~/Downloads/MyApp.AppImage "My App"
```

Both commands create menu entries in:

```bash
~/.local/share/applications
```

If the app does not appear immediately, log out and log back in, or restart your app menu.

## File explorer helper

`nexp` opens useful nixp folders.

Open the nix-portable folder:

```bash
nexp
```

Open local apps added by `napp`/`nadd`:

```bash
nexp app
```

Open app menu `.desktop` entries:

```bash
nexp desktop
```

## Updating

`nupdate` has three modes:

```bash
nupdate
```

Updates nixp itself and upgrades apps installed in your Nix profile.

```bash
nupdate --self
```

Updates only nixp by downloading and running the latest installer from this repository.

```bash
nupdate --apps
```

Updates only packages installed through the Nix profile, usually with `ninstall`.

Manual apps added with `napp` or `nadd` from local executable files are copied executables/AppImages, so nixp cannot automatically update them.

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

## Credits

Credits go to the Nix/NixOS community and the nix-portable contributors.

This project only provides a simple installer and helper commands for nix-portable.
