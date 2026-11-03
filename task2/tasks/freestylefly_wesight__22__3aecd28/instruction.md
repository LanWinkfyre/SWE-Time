# Recover the symbolic verification state this change produces

A regression report was filed against `freestylefly/wesight`.  The report is quoted verbatim below.

## Report

```
fix(cowork): CLI discovery fails to find agents installed via nvm/fnm/volta

## 问题描述

在 macOS 上，以打包后的 Electron 应用启动时（即使授予了 Full Disk Access），WeSight 无法发现用户通过 nvm/fnm/volta 安装的 Agent CLI。

具体表现为：
- 用户在终端中能正常使用这些 CLI（如 `claude`, `codex` 等）
- 但 WeSight 的 "Agent Engines" 设置页面中显示这些 CLI 为 "Not Found"

## 复现步骤

1. 通过 nvm/fnm/volta 安装 Node.js 版本管理器
2. 通过 npm/pnpm 安装 Agent CLI（如 `claude-code`, `codex` 等）
3. 在终端中验证 CLI 可用：`claude --version`
4. 打开 WeSight 应用
5. 进入 "Agent Engines" 设置页面
6. 观察：所有通过 nvm/fnm/volta 安装的 CLI 均显示为 "Not Found"

## 根本原因

文件 `src/main/libs/externalAgentEnvironment.ts` 中的 `resolveCommand()` 函数（第 323-362 行）在 `which` 命令找不到 CLI 时，使用硬编码的 PATH 列表作为 fallback：

```typescript
PATH: [
  path.join(homeDir(), '.npm-global', 'bin'),
  path.join(homeDir(), '.local', 'bin'),
  '/opt/homebrew/bin',
  '/usr/local/bin',
  process.env.PATH ?? '',
].join(path.delimiter),
```

**这个列表不完整，缺少了：**
- `~/.nvm/current/bin` (Node Version Manager)
- `~/.fnm/current/bin` (Fast Node Manager)
- `~/.volta/bin` (Volta)
- Homebrew Cellar 中的其他路径
- 用户在 shell profile 中自定义的 PATH 条目

## 对比：正确的实现已存在于代码库中

同一代码库中 `src/main/libs/coworkUtil.ts` 已有正确实现的 `resolveUserShellPath()` 函数（第 114-154 行），它通过运行 login shell 来获取用户完整的 PATH：

```typescript
export function resolveUserShellPath(): string | null {
  // ...
  const pathProbes = [
    `${shell} -lc 'echo __PATH__=$PATH'`,
  ];
  // ...解析输出获取完整 PATH
}
```

该函数被 `applyPackagedEnvOverrides()` 使用，用于 cowork 会话的环境变量。但 `externalAgentEnvironment.ts` 没有复用它，而是自己维护了一个不完整的硬编码列表。

## 建议的修复方案

在 `resolveCommand()` 的 shell fallback 部分，复用 `coworkUtil.ts` 中已有的 `resolveUserShellPath()` 函数：

```typescript
// 之前（硬编码列表）
const shellResult = spawnSync(shellPath, ['-lc', `command -v ${quoteForShell(command)}`], {
  env: {
    ...process.env,
    PATH: [
      path.join(homeDir(), '.npm-global', 'bin'),
      path.join(homeDir(), '.local', 'bin'),
      '/opt/homebrew/bin',
      '/usr/local/bin',
      process.env.PATH ?? '',
    ].join(path.delimiter),
  },
});

// 之后（使用 resolveUserShellPath）
const userPath = resolveUserShellPath() ?? process.env.PATH;
const shellResult = spawnSync(shellPath, ['-lc', `command -v ${quoteForShell(command)}`], {
  env: {
    ...process.env,
    PATH: userPath,
  },
});
```

## 环境信息

- 操作系统：macOS
- 应用：WeSight（Electron 打包应用）
- 权限：Full Disk Access 已授权
- 安装方式：nvm / fnm / volta
- 目标 CLI：claude-code, codex 等 Agent CLI
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `3aecd287e8d52907767f7170fbe4dddb9e240ed9`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `main`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "freestylefly_wesight__22__3aecd28",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
