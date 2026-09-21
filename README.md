# IHP__CDR4176

CDR4176 is a 2 GHz, four-quadrant phase interpolator targeting the IHP SG13G2 process. It combines a four-phase clock generator, an 8x phase-interpolator network, a divide-by-eight stage, and an output buffer.

**Status:** a layout is published in [`release/v.1.0.0/gds/CDR4176.gds`](release/v.1.0.0/gds/CDR4176.gds). This layout is DRC and LVS clean, with wiring to the pad frame.


## 1. Set up your checkout

```bash
git clone https://github.com/Fundacion-Fulgor/IHP__CDR4176.git
cd IHP__CDR4176
./eda setup
```

`./eda setup` initializes the pinned `IHP-Open-PDK` and `openpdk-libraries` submodules and installs the path-checking pre-commit hook. It refuses to overwrite dirty submodules or an unrelated existing hook. If your dependencies are already initialized, use `./eda install-hooks` to install only the hook.

The hook fixes exact tracked absolute Xschem source references in staged `.sch` and `.sym` files to source-relative paths. Automatic rewriting coverage is strictly scoped to component references (`C {path} ...`) in `.sch` and `.sym` files. Generated `.spice`/`.cir` comments, including `** sch_path:` and `** sym_path:`, are ignored and preserved byte-for-byte, even when they contain absolute paths; executable directives, embedded Tcl scripts, and complex attributes remain checker validation-only and are never automatically rewritten. Use `--library-root` only for roots searched by `xschemrc`; unknown, ambiguous, and other-machine references require manual review without basename guessing. It refuses partially staged files that need fixes. The `--all --check` option performs a read-only full index scan across all tracked sources (requires `--check`). CI runs the fixer read-only (`--all --check`) and the path checker without modifying files. By default, the path checker verifies path portability syntax (rejecting literal absolute POSIX, Windows drive, UNC, tilde, and traversal outside approved roots) while accepting portable relative references and dynamic Tcl roots even if targets are missing. Passing `--check-existence` (`./eda check-paths --check-existence` or `python3 scripts/check_xschem_paths.py --check-existence`) opts into a dependency audit to verify that referenced local files and symbols exist on disk or in the index. Note that actual stale renamed cell references (such as unupdated consumer references following cell renaming) are still reported when opting into `--check-existence` as missing dependencies, not fixed by portability rewriting.

Required tools depend on the task:

| Task | Tools |
| --- | --- |
| Repository checks | Git, Python 3.10+, Tcl (`tclsh`), Bash; Zsh tests run when available |
| Schematic editing and netlisting | Xschem |
| Circuit simulation | ngspice with OSDI support and compiled SG13G2 models |
| Layout editing and DRC | KLayout and the PDK's DRC runner dependencies |
| LVS | Netgen |
| Notebook analysis / waveform comparison | Jupyter, NumPy, Matplotlib, plus imports used by the selected notebook |

<!--
### EDA container

`./eda open`, `./eda netlist`, and `./eda doctor` can enter an existing `iic-osic-tools2` distrobox. The helper also supports running IIC-OSIC-TOOLS containers. It does not install tools or create containers.

For a consistent environment when mixing `eda`, KLayout, ngspice, and Netgen, enter your EDA container first, then run the following from the repository root inside that container:

```bash
source ./SOURCEME
export EDA_NATIVE=1
./eda doctor
```

For distrobox, enter it with `distrobox enter iic-osic-tools2`. The checkout must be accessible inside the container.

### Native tools

If the tools are installed directly on your workstation, use the same environment commands above. Alternatively, pass `--native` to individual commands:

```bash
./eda --native doctor
./eda --native open
```

`SOURCEME` must be **sourced**, not executed. It supports Bash and Zsh, configures `PDK_ROOT`, `PDK`, and KLayout's technology/library paths, and preserves unrelated existing paths. Source it again in each new terminal. It does not install software or change global tool configuration.

By default, use the repository's pinned SG13G2 PDK. A valid external `PDK_ROOT` can be supplied before sourcing `SOURCEME`; it must contain an `ihp-sg13g2/` directory. External PDKs can differ from the pinned revision, so record that choice when reporting results. Do not change submodule revisions as an incidental part of editing a cell.

### Compiled simulation models

The PDK submodule contains Verilog-A sources, but a fresh checkout may not contain compiled `.osdi` files. Use an OSDI-enabled ngspice build and OpenVAF in your EDA environment. The PDK provides its compilation script:

```bash
(
  cd "$PDK_ROOT/$PDK/libs.tech/verilog-a"
  ./openvaf-compile-va.sh
)
```

This creates models under the selected PDK's `libs.tech/ngspice/osdi/` directory. See the [PDK's Verilog-A instructions](IHP-Open-PDK/ihp-sg13g2/libs.tech/verilog-a/README.md). Run netlisting or `./eda init-sim` again after installing models so managed simulation directories pick them up. Do not commit compiled models or modify the pinned dependency commits just to configure your machine.
-->
## 2. Where files belong

```text
CDR4176-main/
  schematic/xschem/<cell>/    Schematic, symbol, netlist and extracted views
  schematic/xschem/project_io/
                             Project-specific IO cells, explicitly namespaced
  layout/klayout/<cell>/      Editable GDS layouts
  testbenches/tran/xschem/    Transient testbenches and retained SPICE decks
  verification/python/       Analysis notebooks
  verification/results/      Local verification data and reports (ignored)
  simulation/<testbench>/    Generated netlists and simulation output (ignored)
doc/                         Existing PEX, LVS and layout-helper instructions
scripts/                     Path checker and analysis/layout helpers
tests/                       Tooling regression tests
release/v.1.0.0/gds/          Published versioned layout
IHP-Open-PDK/                Pinned PDK submodule
openpdk-libraries/           Pinned IO-library submodule
eda                          Project command-line helper
SOURCEME                     Shell environment setup
xschemrc                     Shared Xschem configuration
```

**Keep extracted views next to their non-PEX counterparts in the same cell folder.** For example:

```text
CDR4176-main/schematic/xschem/8xPI/
  8xPI.sch
  8xPI.sym
  8xPI.spice
  8xPI_extracted.cir
  8xPI_pex.sym
  8xPI_pex.spice
```

<!--
An LVS extraction (`*_extracted.cir`) is not necessarily a parasitic netlist (`*_pex.spice`). Do not rename one into the other to satisfy a missing include.

Directories named `legacy/` retain distinct historical artifacts; do not overwrite current cell views with them. The `project_io/` cells differ from the pinned IO library and must not silently replace its bare symbol names.

## 3. Edit schematics and layouts

Open the default top schematic:

```bash
./eda open
```

Open a particular cell or testbench:

```bash
./eda open CDR4176-main/schematic/xschem/8xPI/8xPI.sch
./eda open CDR4176-main/testbenches/tran/xschem/tb_inv.sch
```

`eda` loads the root `xschemrc` explicitly. Its schematic arguments are repository-relative or absolute, and must point inside the project's schematic or testbench directories. Prefer this launcher over starting Xschem from an arbitrary cell directory without a project configuration.

Use library-relative symbol references such as `8xPI/8xPI.sym` and `project_io/sg13g2_IOPadIn/sg13g2_IOPadIn.sym`. Do not save references to personal `/home/...`, `/foss/designs/...`, Windows drive paths, or another checkout. For SPICE file dependencies in Xschem, follow the existing isolated `tcleval` include blocks; do not Tcl-evaluate ngspice control blocks containing `$` variables.

After sourcing `SOURCEME`, open the working top layout in edit mode:

```bash
klayout -e CDR4176-main/layout/klayout/CDR4176/CDR4176.gds
```

The working `CDR4176` cell and the published pad-frame assembly are separate views. Choose the intended hierarchy when editing or verifying. Keep internal subcell names unless a design change actually requires renaming them.

**Do not use `release/` as a working directory.** Edit under `CDR4176-main/`; publish a new version through a deliberate release update. Preserve the existing Git history rather than replacing it with a new repository or rewriting shared commits.

## 4. Netlist and simulate

Generate a normal top-level netlist:

```bash
./eda netlist
```

For a testbench:

```bash
./eda netlist CDR4176-main/testbenches/tran/xschem/tb_inv.sch
(
  cd CDR4176-main/simulation/tb_inv
  ngspice -b tb_inv.spice
)
```

Run ngspice in the **individual output directory**, in the same EDA environment used for netlisting. `eda` does not automatically wrap a separate `ngspice` command in a container.

Normal netlisting writes `CDR4176-main/simulation/<stem>/<stem>.spice` and initializes local model-search paths and available OSDI libraries. Generated files can be replaced on the next run. Use unique testbench names to avoid output-directory collisions.

For an independently prepared simulation directory:

```bash
./eda init-sim CDR4176-main/simulation/my_run
```

`init-sim` resolves its directory argument from the current working directory. It preserves a user-authored `.spiceinit`, refreshes its own managed configuration, and refuses to overwrite unexpected custom files. It does not install missing OSDI models. If a managed configuration has been edited manually, save your changes and resolve the reported conflict rather than deleting unrelated files.

## 5. DRC, LVS and PEX

### DRC: use the official PDK decks

There are no copied DRC rule decks in this repository. Run the selected PDK's runner and keep its outputs outside the release tree:

```bash
python3 "$PDK_ROOT/$PDK/libs.tech/klayout/tech/drc/run_drc.py" \
  --path=release/v.1.0.0/gds/CDR4176.gds \
  --run_dir=CDR4176-main/verification/results/drc_release_v1
```

Use `--help` for rule-selection and execution options, and the [official DRC documentation](IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/tech/drc/README.md) for dependencies. If a layout has multiple top cells, inspect it and supply the intended `--topcell`. Do not disable rule groups merely to obtain a passing report.

### LVS

Generate an LVS-oriented schematic netlist and compare it with the corresponding extracted cell view:

```bash
./eda netlist --lvs
netgen -batch lvs \
  "CDR4176-main/schematic/xschem/CDR4176/CDR4176_extracted.cir CDR4176" \
  "CDR4176-main/simulation/CDR4176/CDR4176.spice CDR4176" \
  "$PDK_ROOT/$PDK/libs.tech/netgen/ihp-sg13g2_setup.tcl" \
  CDR4176-main/simulation/CDR4176/CDR4176_lvs.out
```

This example compares the working `CDR4176` cell, not automatically the published pad-frame assembly. Regenerate extraction after layout changes and check the cell names and pin order. `--lvs` does not initialize a simulation environment; rerun normal netlisting before simulating that testbench.

See [LVS notes](doc/readme_lvs.txt), [PEX notes](doc/PEX.txt), and [hierarchical layout-helper examples](doc/readme_hierarchical.txt). Recovered historical PEX files are retained for their existing benches, not certified against the latest layouts.

## 6. Analyze results

Notebooks live under `CDR4176-main/verification/python/`. Their bootstrap code works from the repository root or a notebook directory and resolves explicit dataset locations through `scripts/notebook_data.py`.

Waveform dumps are not tracked. Existing local historical data resides under `CDR4176-main/verification/results/legacy/`. To analyze a fresh run, point `CDR4176_RESULTS` at the directory containing the expected waveform files before launching Jupyter. If launching from outside the checkout, also set `CDR4176_ROOT` to this repository's absolute path. Missing datasets raise an error rather than substituting a different run.

For comparing two waveform dumps, inspect the standalone helper:

```bash
python3 scripts/extract_comparison.py --help
```

Clear notebook outputs before committing. Keep analysis source, not waveform dumps, caches, generated netlists, or machine-specific configuration.

## 7. Check and submit changes

Start a topic branch from an up-to-date checkout:

```bash
git pull --ff-only
git switch -c my-change
```

Before committing:

```bash
./eda check-paths
python3 -m unittest discover -s tests -v
python3 -m compileall -q eda scripts tests
bash -n SOURCEME
git status --short
git diff
```

These are tooling checks, not circuit signoff. The static path checker (`./eda check-paths`, or `./eda check-paths --check-existence` for dependency audit) and unit tests also run in GitHub Actions without requiring PDK submodule downloads. For circuit changes, additionally netlist the affected hierarchy and run the appropriate simulation, DRC, and LVS checks in an EDA environment.

Stage only the files you intend to submit, then check the actual index:

```bash
git add CDR4176-main/schematic/xschem/8xPI/8xPI.sch
./eda check-paths --staged
git diff --cached --check
git diff --cached
git commit -m "Describe the change"
git push -u origin my-change
```

Replace the example staged file and branch with your own. Verify `git remote -v` first: **older checkouts may still point at `Fundacion-Fulgor/PhaseInterpolator`**. The destination for this project is `Fundacion-Fulgor/IHP__CDR4176`. Open a pull request there and state which verification was run, the tool/PDK versions, and any outstanding failures. Do not force-push shared history.
-->

## Contributors

Agustina Trabichet, Victor Muñoz, Macarena Gonzalez, Juana Pucheta Valentín Ramirez, and Pablo Dominguez. Project metadata is maintained in [`project.yml`](project.yml).
