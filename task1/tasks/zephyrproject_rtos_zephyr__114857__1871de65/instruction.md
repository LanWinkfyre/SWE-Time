# Locate the commit that introduced this regression

A regression was reported against `zephyrproject-rtos/zephyr`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
bluetooth: stm32wb: any BT_STM32_IPM application fails to build for stm32wb5mmg — IPCC IRQs invisible to automatic NUM_IRQS computation

### Describe the bug

### Describe the bug

Building `samples/bluetooth/hci_uart` for the in-tree board `stm32wb5mmg` fails at
link time:

```
gen_isr_tables.py: error: IRQ 45 (offset=0) exceeds the maximum of 40
```

This is the exact command sequence that the `stm32wb5mmg` board documentation
instructs users to run in order to bring up Bluetooth on the B-U585I-IOT02A
Discovery kit, so the documented bring-up path for that board is currently
broken.

**Root cause**




For the lean `hci_uart` image the highest devicetree-visible IRQ is 40 (EXTI),
giving `CONFIG_NUM_IRQS=41`.

However, `CONFIG_BT_STM32_IPM` is enabled for this target, and
`drivers/bluetooth/hci/ipm_stm32wb.c` connects the IPCC interrupts using
hardcoded CMSIS enums rather than devicetree:

```c
/* drivers/bluetooth/hci/ipm_stm32wb.c */
IRQ_CONNECT(IPCC_C1_RX_IRQn, 0, HW_IPCC_Rx_Handler, NULL, 0);   /* IRQ 44 */
IRQ_CONNECT(IPCC_C1_TX_IRQn, 0, HW_IPCC_Tx_Handler, NULL, 0);   /* IRQ 45 */
```

The `st,stm32wb-rf` node has no `interrupts` property, and there is no `ipcc`
node in `dts/arm/st/wb/stm32wb.dtsi`. IRQs 44 and 45 are therefore invisible to
the automatic computation, and the generated vector table is five entries too
small.

**Why this cannot be worked around by the user**

`CONFIG_NUM_IRQS` is declared promptless (`arch/arm/core/Kconfig`):

```kconfig
config NUM_IRQS
	int
```

so `-DCONFIG_NUM_IRQS=...` and `.conf` fragment assignments are ignored. The
value can only be changed from a Kconfig file.

### Regression

 Verified by building
`samples/bluetooth/hci_uart` for `stm32wb5mmg` at that commit and at its parent,
with `west update` run at each revision so module revisions matched the
manifest:

| Revision | Result | `CONFIG_NUM_IRQS` |
|----------|--------|-------------------|






### Regression

- [x] This is a regression.

### Steps to reproduce



```bash
west build -b stm32wb5mmg samples/bluetooth/hci_uart --pristine
```

### Relevant log output

```shell
[173/176] Generating isr_tables.c, isr_tables_vt.ld, isr_tables_swi.ld
FAILED: [code=1] zephyr/isr_tables.c zephyr/isr_tables_vt.ld zephyr/isr_tables_swi.ld
gen_isr_tables.py: error: IRQ 45 (offset=0) exceeds the maximum of 40
ninja: build stopped: subcommand failed.
```

### Impact

Functional Limitation – Some features not working as expected, but system usable.

### Environment


- Board: `stm32wb5mmg` (BLE module on B-U585I-IOT02A)
- Host OS: macOS (arm64)
- Toolchain: Zephyr SDK

### Additional Context

**Scope: `stm32wb5mmg` specifically, not the whole STM32WB series**

Other STM32WBX boards are unaffected, because they enable enough devicetree
nodes that the computed `NUM_IRQS` happens to land above 45 anyway:

| Board | Sample | `CONFIG_NUM_IRQS` | Result |
|-------|--------|-------------------|--------|
| `stm32wb5mmg` | `bluetooth/hci_uart` | 41 | fails |
| `stm32wb5mmg` | `bluetooth/peripheral_hr` | 41 | fails |
| `nucleo_wb55rg` | `bluetooth/hci_uart` | 54 | builds |
| `nucleo_wb55rg` | `bluetooth/peripheral_hr` | 54 | builds |
| `stm32wb5mm_dk` | `bluetooth/peripheral_hr` | 52 | builds |

So the failure is not sample-specific — any `CONFIG_BT_STM32_IPM` application
fails on `stm32wb5mmg` — but it is board-specific in practice. `stm32wb5mmg` is
a bare module target with a minimal devicetree, so the highest `status = "okay"`
interrupt is EXTI at 40, whereas the richer Nucleo/DK boards enable peripherals
with higher interrupt numbers.

This is worth emphasising because it means the other boards are only passing by
coincidence. The full STM32WB55 vector table extends to IRQ 62 (`dmamux1`), and
`nucleo_wb55rg` gets 54 — so any of these targets could regress the moment a
devicetree node is disabled. The correctness of `NUM_IRQS` on STM32WB currently
depends on unrelated peripherals happening to be enabled.

**Missing test coverage**

`samples/bluetooth/hci_uart/tests.yaml` defines 12 scenarios, and every one of
them restricts `platform_allow` to Nordic platforms
(`nrf52dk`, `nrf52840dk`, `nrf21540dk`, `nrf54l15dk`, `nrf54lm20dk`,
`nrf52833dk`, `nrf5340dk` cpuapp/cpunet, `nrf5340_audio_dk`, `nrf52_bsim`).
No STM32 platform appears in the file, and `samples/bluetooth/hci_uart/boards/`
contains no STM32 overlays. Since `platform_allow` is a whitelist, twister never
builds this sample for `stm32wb5mmg`, which is why CI does not catch this.

`boards/st/stm32wb5mmg/stm32wb5mmg.yaml` places no `testing:` restrictions on
the board, so the gap is specific to the sample's whitelist.

**Suggested fix**


the IPCC interrupts visible to devicetree — either by adding an `ipcc` node to
`dts/arm/st/wb/stm32wb.dtsi`, or by giving the `st,stm32wb-rf` node an
`interrupts` property — and switching `ipm_stm32wb.c` to `DT_INST_IRQ()` instead
of the CMSIS `IPCC_C1_*_IRQn` enums. That removes the hardcoded IRQ numbers and
lets the existing automatic computation produce the correct result.

A narrower alternative is a `configdefault` override in
`soc/st/stm32/stm32wbx/Kconfig.defconfig` (series files are `rsource`d before
the family defaults, and `configdefault` is first-match-wins):

```kconfig
configdefault NUM_IRQS
	default 46 if BT_STM32_IPM
```

This is what I am using locally as a workaround, and it does resolve the build.
I note however that a similar per-series approach was proposed and not merged in


It would also be worth adding a `build_only` `stm32wb5mmg` scenario to
`samples/bluetooth/hci_uart/tests.yaml` so this combination cannot regress
silently again.

**Related**

- #107585 — same class of problem on STM32H7 (closed)

- #107674 — proposal to give `CONFIG_NUM_IRQS` a prompt, by the author of

- #107808 / #108023 — migration-guide note on setting promptless Kconfig values
  (merged)

Those all concerned a user's own application needing a larger `NUM_IRQS`. This
report is different in that an in-tree board, in-tree sample and in-tree driver
do not build together, with no user configuration involved.
```

## What you have

- `/testbed/repo` is a git clone of `zephyrproject-rtos/zephyr` truncated just after the regression was
  reported.  `HEAD` is `d820dddaab31c7c1752f4f2ecb61dc1c59063b34` and the full history behind it is present.
- The commit that introduced the regression is an ancestor of `HEAD`.  The commit that
  *fixes* it is not in this repository -- it was written after the cutoff.
- You do not need to build or test the project.  Reading history, `git log`, `git diff`,
  `git show` and writing your own probe scripts is the intended way to work.
- Some release-note and changelog files have been removed from the working tree on purpose.

## What to produce

Write the full 40-character hexadecimal SHA of the **first bad commit** -- the single
commit that introduced this regression -- into `/testbed/answer.txt`, and nothing else:

```
echo <40-char-sha> > /testbed/answer.txt
```

Requirements:

- Exactly one line, exactly 40 lowercase hex characters.  Abbreviated SHAs are rejected.
- No explanation, no extra lines, no surrounding punctuation.
- The commit must exist in this repository.

## Rules

- Do **not** use the network.  This task is derived from a public issue report and the
  answer is published on the internet; fetching it is cheating and is detected and
  scored zero.  Solve it from the repository.
- Do not rewrite history, add remotes, or fetch objects.
