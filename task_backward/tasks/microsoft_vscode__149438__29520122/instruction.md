# Locate the commit that introduced this regression

A regression was reported against `microsoft/vscode`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Cannot read properties of undefined (reading 'getRuntimeValue')

On launch, the following stack trace appears:

```
ERR Cannot read properties of undefined (reading 'getRuntimeValue'): TypeError: Cannot read properties of undefined (reading 'getRuntimeValue')
    at Workbench.isVisible (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/workbench/browser/layout.js:679:45)
    at PanelPart.showOrHideViewContainer (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/workbench/browser/parts/panel/panelPart.js:236:40)
    at PanelPart.onDidRegisterPanels (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/workbench/browser/parts/panel/panelPart.js:153:22)
    at vscode-file://vscode-app/Users/alex/src/vscode/out/vs/workbench/browser/parts/panel/panelPart.js:261:70
    at Listener.invoke (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/base/common/event.js:420:27)
    at PrivateEventDeliveryQueue.deliver (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/base/common/event.js:592:38)
    at Emitter.fire (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/base/common/event.js:557:37)
    at PaneCompositeRegistry.registerComposite (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/workbench/browser/composite.js:211:33)
    at PaneCompositeRegistry.registerPaneComposite (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/workbench/browser/panecomposite.js:141:19)
    at ViewsService.registerPaneComposite (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/workbench/browser/parts/views/viewsService.js:505:86)
    at ViewsService.onDidRegisterViewContainer (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/workbench/browser/parts/views/viewsService.js:76:18)
    at vscode-file://vscode-app/Users/alex/src/vscode/out/vs/workbench/browser/parts/views/viewsService.js:36:85
    at Array.forEach (<anonymous>)
    at new ViewsService (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/workbench/browser/parts/views/viewsService.js:36:55)
    at InstantiationService._createInstance (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/platform/instantiation/common/instantiationService.js:89:20)
    at InstantiationService._createServiceInstance (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/platform/instantiation/common/instantiationService.js:196:29)
    at InstantiationService._createServiceInstanceWithOwner (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/platform/instantiation/common/instantiationService.js:184:29)
    at InstantiationService._createAndCacheServiceInstance (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/platform/instantiation/common/instantiationService.js:174:47)
    at InstantiationService._safeCreateAndCacheServiceInstance (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/platform/instantiation/common/instantiationService.js:127:29)
    at InstantiationService._getOrCreateServiceInstance (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/platform/instantiation/common/instantiationService.js:114:29)
    at InstantiationService._createInstance (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/platform/instantiation/common/instantiationService.js:70:36)
    at InstantiationService.createInstance (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/platform/instantiation/common/instantiationService.js:60:31)
    at new TextFileEditorModelManager (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/workbench/services/textfile/common/textFileEditorModelManager.js:61:78)
    at InstantiationService._createInstance (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/platform/instantiation/common/instantiationService.js:89:20)
    at InstantiationService.createInstance (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/platform/instantiation/common/instantiationService.js:60:31)
    at new AbstractTextFileService (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/workbench/services/textfile/browser/textFileService.js:43:67)
    at new NativeTextFileService (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/workbench/services/textfile/electron-sandbox/nativeTextFileService.js:20:13)
    at InstantiationService._createInstance (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/platform/instantiation/common/instantiationService.js:89:20)
    at InstantiationService._createServiceInstance (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/platform/instantiation/common/instantiationService.js:196:29)
    at InstantiationService._createServiceInstanceWithOwner (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/platform/instantiation/common/instantiationService.js:184:29)
    at InstantiationService._createAndCacheServiceInstance (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/platform/instantiation/common/instantiationService.js:174:47)
    at InstantiationService._safeCreateAndCacheServiceInstance (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/platform/instantiation/common/instantiationService.js:127:29)
    at InstantiationService._getOrCreateServiceInstance (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/platform/instantiation/common/instantiationService.js:114:29)
    at InstantiationService._createInstance (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/platform/instantiation/common/instantiationService.js:70:36)
    at InstantiationService.createInstance (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/platform/instantiation/common/instantiationService.js:60:31)
    at WorkspaceService.acquireInstantiationService (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/workbench/services/configuration/browser/configurationService.js:333:69)
    at vscode-file://vscode-app/Users/alex/src/vscode/out/vs/workbench/browser/workbench.js:119:42
    at InstantiationService.invokeFunction (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/platform/instantiation/common/instantiationService.js:44:24)
    at Workbench.initServices (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/workbench/browser/workbench.js:114:34)
    at Workbench.startup (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/workbench/browser/workbench.js:61:51)
    at DesktopMain.open (vscode-file://vscode-app/Users/alex/src/vscode/out/vs/workbench/electron-sandbox/desktop.main.js:54:52)
    at async vscode-file://vscode-app/Users/alex/src/vscode/out/bootstrap-window.js:183:6
```
```

## What you have

- `/testbed/repo` is a git clone of `microsoft/vscode` truncated just after the regression was
  reported.  `HEAD` is `a28eab68734e629c61590fae8c4b231c91f0eaaa` and the full history behind it is present.
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
