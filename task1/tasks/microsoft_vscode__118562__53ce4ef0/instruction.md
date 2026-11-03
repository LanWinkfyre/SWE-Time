# Locate the commit that introduced this regression

A regression was reported against `microsoft/vscode`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
VS Code is unable to activate a debugger extension because of path casing discrepancies

<!-- ⚠️⚠️ Do Not Delete This! bug_report_template ⚠️⚠️ -->
<!-- Please read our Rules of Conduct: https://opensource.microsoft.com/codeofconduct/ -->
<!-- 🕮 Read our guide about submitting issues: https://github.com/microsoft/vscode/wiki/Submitting-Bugs-and-Suggestions -->
<!-- 🔎 Search existing issues to avoid creating duplicates. -->
<!-- 🧪 Test using the latest Insiders build to see if your issue has already been fixed: https://code.visualstudio.com/insiders/ -->
<!-- 💡 Instead of creating your report here, use 'Report Issue' from the 'Help' menu in VS Code to pre-fill useful information. -->
- VS Code Version: 1.54.1
- OS Version: Windows 10 19041

More information here: https://github.com/microsoft/vscode-cpptools/issues/7114

I want to highlight this from the customer's logs.  They are trying to load the `ms-vscode.cpptools` extension, but the reasoning in the log does not make sense because `ms-vscode.cpptools` registers the `'cppvsdbg'` debugger type).  Downgrading VS Code to 1.53.2 fixes the issue for the customer.  We're not sure what would cause this.

```
[2021-03-05 16:49:27.882] [exthost] [error] Activating extension ms-vscode.cpptools failed due to an error:
[2021-03-05 16:49:27.886] [exthost] [error] Error: a DebugAdapterDescriptorFactory can only be registered from the extension that defines the 'cppvsdbg' debugger.
	at m.registerDebugAdapterDescriptorFactory (c:\Program Files\Microsoft VS Code\resources\app\out\vs\workbench\services\extensions\node\extensionHostProcess.js:91:25505)
	at Object.registerDebugAdapterDescriptorFactory (c:\Program Files\Microsoft VS Code\resources\app\out\vs\workbench\services\extensions\node\extensionHostProcess.js:95:37807)
	at Object.initialize (c:\Users\sesa404214\.vscode\extensions\ms-vscode.cpptools-1.2.2\dist\main.js:18300:35)
	at c:\Users\sesa404214\.vscode\extensions\ms-vscode.cpptools-1.2.2\dist\main.js:26903:27
	at Generator.next (<anonymous>)
	at c:\Users\sesa404214\.vscode\extensions\ms-vscode.cpptools-1.2.2\dist\main.js:26841:71
	at new Promise (<anonymous>)
	at module.exports.__awaiter (c:\Users\sesa404214\.vscode\extensions\ms-vscode.cpptools-1.2.2\dist\main.js:26837:12)
	at activate (c:\Users\sesa404214\.vscode\extensions\ms-vscode.cpptools-1.2.2\dist\main.js:26870:12)
	at Function._callActivateOptional (c:\Program Files\Microsoft VS Code\resources\app\out\vs\workbench\services\extensions\node\extensionHostProcess.js:91:14037)
	at Function._callActivate (c:\Program Files\Microsoft VS Code\resources\app\out\vs\workbench\services\extensions\node\extensionHostProcess.js:91:13714)
	at c:\Program Files\Microsoft VS Code\resources\app\out\vs\workbench\services\extensions\node\extensionHostProcess.js:91:11746
	at processTicksAndRejections (internal/process/task_queues.js:97:5)
```

<!-- 🔧 Launch with `code --disable-extensions` to check. -->
Does this issue occur when all extensions are disabled?: No

<!-- 🪓 If you answered No above, use 'Help: Start Extension Bisect' from Command Palette to try to identify the cause. -->
 The 'Help > Report Issue' dialog can assist with this. -->
```

## What you have

- `/testbed/repo` is a git clone of `microsoft/vscode` truncated just after the regression was
  reported.  `HEAD` is `112bd0900270e49b27b81e8c06a1f44227901a82` and the full history behind it is present.
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
