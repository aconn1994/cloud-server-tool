# AGENTS — Working Effectively in this Repository

This repo provisions and runs Steam-based game servers (currently Arma 3) using Python, Docker, and Terraform. The core Python package lives under lib/python/cst and is tested and linted via the .cicd toolchain and GitHub Actions.

## Repository Layout (high value areas)
- lib/python/cst — primary Python code
  - cst_game/common — core abstractions, arg parsing, SteamCMD client
  - cst_game/games/arma_three — Arma 3 implementation (GameConfig, Setup, parser)
  - cst_game/os_manager — OS abstractions and implementations (linux, macos, windows)
  - cst_game/platform_config — platform-specific config (Steam)
  - tests — unit tests for key abstractions and parser
- .cicd — local and CI runners for linting, testing, and image builds
- local_env — Dockerfiles for dev base and debug images
- .github/workflows — CI pipelines (linting, testing, image builds, terraform)
- docker-compose.yml — local containers (base, debug, linux game image)
- terraform/aws — Terraform roots and modules
- archived — historical code (do not modify for current work)

## Essential Commands

### Lint/Format/Type-check (Ruff + Mypy)
- Check only (CI-equivalent):
  - /bin/bash .cicd/bash/linters/python-format.sh .cicd/python .cicd/python cicd "check_arg" .cicd/python/pyproject.toml /usr/local/bin/python3
  - /bin/bash .cicd/bash/linters/python-format.sh lib/python/cst lib/python/cst cst "check_arg" lib/python/cst/pyproject.toml /root/venvs/cst/bin/python3
- Auto-fix locally for both packages:
  - /bin/bash .cicd/local/format-fix.sh

### Test with Coverage (Pytest + Coverage)
- Local helper (targets lib/python/cst):
  - /bin/bash .cicd/local/test_python_lib_w_coverage.sh
- Under the hood (exact CI invocation):
  - /bin/bash .cicd/bash/testers/coverage-pytest.sh lib/python/cst lib/python/cst cst pyproject.toml /root/venvs/cst/bin/python3

### Running lint/tests locally (Docker — the real workflow)
The lint/test scripts assume the `cst-base:latest` container environment (it provides `/usr/local/bin/python3` for the CICD package and `/root/venvs/cst/bin/python3` for the cst package, plus a `$TMP_DIR` for logs). PyCharm run configs in `.run/*.run.xml` mount the repo at `/root/cloud-server-tool` and run the `.cicd/local/*` scripts. To reproduce from a shell (mirrors the run configs; set `TMP_DIR`):
- Tests: docker run --rm -t -u root -w /root/cloud-server-tool -e TMP_DIR=/tmp -v "$PWD":/root/cloud-server-tool --entrypoint /bin/bash cst-base:latest .cicd/local/test_python_lib_w_coverage.sh
- Lint/format check: docker run --rm -t -u root -w /root/cloud-server-tool -e TMP_DIR=/tmp -v "$PWD":/root/cloud-server-tool --entrypoint /bin/bash cst-base:latest .cicd/bash/linters/python-format.sh lib/python/cst lib/python/cst cst "check_arg" lib/python/cst/pyproject.toml /root/venvs/cst/bin/python3
- Rebuild the base image if deps change: /bin/bash .cicd/local/docker-build-base-image.sh
- The debug image (local_env/images/debug_image) extends the base with SSH so PyCharm can attach to the in-container interpreter.
- The CI base image is published at ghcr.io/aconn1994/cst_base:main and used by the linting/testing GitHub workflows.

### Run the Game Setup (Arma 3)
- Ensure Python can import cst_game (set PYTHONPATH to lib/python/cst when running from source):
  - export PYTHONPATH=lib/python/cst
- Invoke runner (module name selects the game setup):
  - python3 -u .cicd/python/cst_cicd/runners/game_setup_runner.py \
    --module-name cst_game.games.arma_three.setup \
    --operating-system linux \
    --debug \
    [--username <steam-username> --password <steam-password>] \
    [--kwargs dlcs=<comma-separated-dlc-prefixes>] \
    [--expedite-launch]

### Docker (local dev)
- Build base image: /bin/bash .cicd/local/docker-build-base-image.sh
- Build debug image: /bin/bash .cicd/local/docker-build-debug-image.sh
- Start debug container: /bin/bash .cicd/local/docker-start-debug-image.sh
- Compose services (alternative to scripts): docker compose build && docker compose up -d

### Build Linux Game Image (local)
- docker build . -f .cicd/game-images/linux/Dockerfile -t <your_tag>

### Terraform (validation only, mirrors CI)
- cd terraform/aws && terraform init && terraform validate -no-color

## Architecture and Control Flow
- Entry-point: cst_game/common/game_setup_runner_parser.py:17-93 parses CLI args then importlib.import_module(module_name) and calls module.main(parsed_args).
- Game orchestration (Arma 3):
  - cst_game/games/arma_three/setup.py:116-171 orchestrates install and launch:
    - Optionally installs SteamCMD (SteamConfig.install_steamcmd_binary).
    - Installs the game via SteamCMDClient.install_game.
    - Symlinks configuration/assets (missions linking active; other links currently commented).
    - Parses mod-list.html to discover workshop items; downloads and links mods and keys.
    - Launches the server binary with selected flags and mods.
- Configuration model:
  - GameConfig extends SteamConfig, providing IDs, paths, and helpers (cst_game/games/arma_three/game_config.py).
  - SteamConfig extends AbstractPlatformConfig and wraps SteamCMD interactions (cst_game/platform_config/platforms/steam_config.py).
  - OS-specific paths come from cst_game/os_manager/systems/* and OperatingSystemManager (maps aliases to implementations).
- Arguments:
  - --module-name (e.g., cst_game.games.arma_three.setup) — required
  - --operating-system (linux|macos|windows) — required; maps via OperatingSystemManager.name_to_os_mapper
  - --username/--password — Steam credentials (optional; anonymous login used if omitted)
  - --debug — enables verbose logging
  - --local — reserved flag (not used in current flow)
  - --arch 32|64 — selects binary
  - --expedite-launch — skips installs/updates; uses existing files/links
  - --kwargs key=value — arbitrary pairs; currently dlcs is read by GameConfig.dlcs

## Code Organization and Patterns
- Abstractions enforce structure:
  - AbstractGameSetup (cst_game/common/abstract_game_setup.py) — logging, utilities, directory rename/symlink helpers, and template for setup flows.
  - AbstractPlatformConfig (cst_game/platform_config/abstract_platform_config.py) — platform-level binary names.
  - AbstractOS (cst_game/os_manager/abstract_os.py) — system/paths interface; linux/macos/windows implementations.
- Strict absolute imports only (ruff ban-relative-imports = all).
- Game-specific modules implement:
  - GameConfig: game IDs, binaries, paths, and adapters to platform/OS.
  - Setup: the end-to-end execution including SteamCMD calls and process launch.
- Tests live under lib/python/cst/tests with subpackages mirroring the code structure.

## Testing Approach
- Pytest with coverage thresholds configured in lib/python/cst/pyproject.toml (fail_under = 80).
- Coverage excludes clients/steam_cmd_client.py and setup.py (covered in CICD or excluded by config).
- Use the provided tester script for consistent env and logs (writes reports to $TMP_DIR if set).

## Naming, Style, and Tooling
- Python 3.11+; mypy configured with python_version = 3.13 for type checking.
- Ruff settings enforce import sorting, no relative imports, line-length 100, and selected lint rules.
- Type hints are expected (disallow_untyped_defs = true).
- Keep module/package imports absolute under cst_game.*

## Non-obvious Gotchas
- SteamCMD installation (SteamConfig.install_steamcmd_binary) invokes sudo apt-get and downloads to /home/gameuser/steamcmd; requires Linux with appropriate privileges. Use containers/EC2 where root/sudo is available.
- Arma 3 profile paths (GameConfig.profiles_dst_path) are hard-coded for Ubuntu under ~/.local/share/... with a TODO for dynamic resolution. Adjust if running under different users/OS.
- Anonymous Steam login is used if username/password are omitted; some games/workshop items may require authenticated login (see SteamCMDClient comments).
- Symlink helpers are idempotent (catch FileExistsError and print a notice). Missions linking is active; other config links are currently commented in Setup._link_game_config_files.
- README.md references cst_docker/build.py which does not exist in the active tree (only under archived/). Prefer the runner in .cicd/python/cst_cicd/runners.
- Dockerfile for the linux game image expects a wheel at lib/python/cloud_server_tool/dist/cloud_server_tool-0.1.0-py3-none-any.whl; ensure packaging/output paths match before building that image, or update the Dockerfile accordingly.

## Extending the System
- Add a new OS: implement cst_game/os_manager/systems/<os>.py extending AbstractOS, then map its alias in cst_game/os_manager/operating_system_manager.py:9-14.
- Add a new platform: extend AbstractPlatformConfig and implement a new platforms/<platform> config similar to SteamConfig.
- Add a new game: create cst_game/games/<game> with GameConfig (extending the appropriate platform config) and Setup (extending AbstractGameSetup). Expose a main(parsed_args) that constructs Setup and calls execute().

## CI/CD Reference
- Linting workflow runs Terraform fmt check and Python ruff/mypy checks using the linters script.
- Testing workflow runs Terraform init/validate and Python tests via the testers script inside ghcr.io/aconn1994/cst_base:main.
- Development image build publishes local_env/images/* Dockerfiles to GHCR.
- Game image build workflow builds and pushes a provided Dockerfile to AWS ECR using configured inputs.
