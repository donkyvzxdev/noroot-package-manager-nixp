# Changelog

All notable changes to this project will be documented in this file.

## v0.3

This version focused on improving package selection, bilingual help, and command clarity.

### Added

- Added `--unstable` / `-u` support for:
  - `nrun`
  - `ninstall`
  - `nshell`
  - `nadd`
- Added support for packages from:

  ```bash
  github:NixOS/nixpkgs/nixpkgs-unstable#<package>
  ```

- Added `--help-br` for Brazilian Portuguese help in helper commands.
- Added better `--help` output for helper commands.
- Added README documentation for stable and unstable package usage.
- Added `nver --log` to show the nixp version and latest release log.
- Added `nixp --log` to show the nixp version and latest release log.
- Added explanation that stable and unstable packages can coexist, but the same app may conflict in the user profile.

### Changed

- Changed the Brazilian Portuguese help flag from `--br` to `--help-br`.
- Updated the project version from `0.2` to `0.3`.
- Improved English-first installer text.
- Improved internal variable names in the installer.
- Improved `nhelp` with examples for unstable packages.

### Notes

- `--unstable` is supported by:
  - `nrun`
  - `ninstall`
  - `nshell`
  - `nadd`
- Apps added from local executable files with `napp` or `nadd` are copied files and cannot be automatically updated by nixp.
- Installing the same app from stable and unstable into the same profile may cause command conflicts.

---

## v0.2

This version focused on making nixp easier to use as a small user-level app manager.

### Added

- Added `napp` command.
  - Allows adding local executables or AppImages to the app menu.
  - Copies local apps to:

    ```bash
    ~/.local/apps
    ```

  - Creates `.desktop` entries in:

    ```bash
    ~/.local/share/applications
    ```

- Added `nadd` command.
  - Creates `.desktop` menu entries for Nix packages.
  - Can also handle local executables/AppImages by passing them to `napp`.
  - Example:

    ```bash
    nadd firefox "Firefox"
    ```

- Added `nexp` command.
  - Opens nixp-related folders in the file manager.
  - Added:

    ```bash
    nexp
    nexp app
    nexp desktop
    ```

- Added `nupdate` command.
  - Updates nixp itself.
  - Updates apps installed in the Nix profile.
  - Added:

    ```bash
    nupdate
    nupdate --self
    nupdate --apps
    ```

- Added `nver` command to show the nixp version.
- Added `nixp --version` to show the nixp helper version.
- Added `nixp --nix-version` to show the real Nix version used by nix-portable.
- Added command help flags such as `--help`.
- Added Brazilian Portuguese help during development.

### Changed

- Updated the project version from `0.1` to `0.2`.
- Improved `nhelp` with more command examples.
- Improved README with more usage examples.
- Improved app menu integration.
- Improved organization of local executable/AppImage apps.

### Notes

- `nupdate --apps` updates packages installed through the Nix profile.
- Apps manually added with `napp` are copied local files and are not auto-updated by nixp.

---

## v0.1

This was the first public/basic version of nixp.

### Added

- Added the initial `install_nix_portable.py` installer.
- Added automatic nix-portable download.
- Installed nix-portable into:

  ```bash
  ~/.local/nix-portable/nix-portable
  ```

- Added automatic creation of helper commands in:

  ```bash
  ~/.local/bin
  ```

- Added `nixp` command.
  - Runs Nix through nix-portable.
  - Example:

    ```bash
    nixp run nixpkgs#htop
    ```

- Added `nrun` command.
  - Runs a package without installing it permanently.
  - Example:

    ```bash
    nrun htop
    ```

- Added `ninstall` command.
  - Installs packages into the user profile.
  - Example:

    ```bash
    ninstall git nodejs python3
    ```

- Added `nshell` command.
  - Opens a temporary shell with packages available.
  - Example:

    ```bash
    nshell git nodejs python3
    ```

- Added `nhelp` command.
  - Shows basic help and examples.

- Added automatic `PATH` setup for:

  ```bash
  ~/.local/bin
  ```

- Added support for using nixp without `sudo` or root access.
- Added default `NP_RUNTIME=bwrap`.

### Notes

- This version was focused on the basic goal: using Nix packages through nix-portable in a user directory.
- If `bwrap` failed in restricted environments, users could try:

  ```bash
  NP_RUNTIME=proot nrun htop
  ```
