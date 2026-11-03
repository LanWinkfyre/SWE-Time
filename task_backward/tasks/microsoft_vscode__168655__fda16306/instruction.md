# Locate the commit that introduced this regression

A regression was reported against `microsoft/vscode`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
`Code - OSS` doesn't launch when using Dev Container locally or in codespaces

<!-- ⚠️⚠️ Do Not Delete This! bug_report_template ⚠️⚠️ -->
<!-- Please read our Rules of Conduct: https://opensource.microsoft.com/codeofconduct/ -->
<!-- 🕮 Read our guide about submitting issues: https://github.com/microsoft/vscode/wiki/Submitting-Bugs-and-Suggestions -->
<!-- 🔎 Search existing issues to avoid creating duplicates. -->
<!-- 🧪 Test using the latest Insiders build to see if your issue has already been fixed: https://code.visualstudio.com/insiders/ -->
<!-- 💡 Instead of creating your report here, use 'Report Issue' from the 'Help' menu in VS Code to pre-fill useful information. -->
<!-- 🔧 Launch with `code --disable-extensions` to check. -->
Does this issue occur when all extensions are disabled?: Yes

<!-- 🪓 If you answered No above, use 'Help: Start Extension Bisect' from Command Palette to try to identify the cause. -->
 The 'Help > Report Issue' dialog can assist with this. -->
- VS Code Version: 1.72.0 (also happens on Codespaces)
- OS Version: Windows 11; Version 10.0.22621 Build 22621 (also happens on Codespaces)

I was trying to get a development VS Code OSS build running with dev containers. After following the steps from https://github.com/microsoft/vscode/tree/main/.devcontainer, I only got the following error when trying to execute `bash scripts/code.sh`:

```bash
@Bassadin ➜ /workspaces/vscode $ bash scripts/code.sh
yarn run v1.22.19
$ node build/lib/electron
Downloading ffmpeg: [====================================================================================================] 100% ETA: 0.0 seconds 
Downloading ffmpeg: [====================================================================================================] 100% ETA: 0.0 seconds 
Done in 4.49s.
yarn run v1.22.19
$ node --max_old_space_size=4095 ./node_modules/gulp/bin/gulp.js compile
[19:22:43] Using gulpfile /workspaces/vscode/gulpfile.js
[19:22:43] Starting 'compile'...
[19:22:43] Starting monaco-typecheck ...
[19:22:43] Starting clean-out ...
[19:22:43] Starting clean-extension-authentication-proxy ...
[19:22:43] Starting clean-extension-configuration-editing-build ...
[19:22:43] Starting clean-extension-configuration-editing ...
[19:22:43] Starting clean-extension-css-language-features-client ...
[19:22:43] Starting clean-extension-css-language-features-server ...
[19:22:43] Starting clean-extension-debug-auto-launch ...
[19:22:43] Starting clean-extension-debug-server-ready ...
[19:22:43] Starting clean-extension-emmet ...
[19:22:43] Starting clean-extension-extension-editing ...
[19:22:43] Starting clean-extension-git ...
[19:22:43] Starting clean-extension-git-base ...
[19:22:43] Starting clean-extension-github-authentication ...
[19:22:43] Starting clean-extension-github ...
[19:22:43] Starting clean-extension-grunt ...
[19:22:43] Starting clean-extension-gulp ...
[19:22:43] Starting clean-extension-html-language-features-client ...
[19:22:43] Starting clean-extension-html-language-features-server ...
[19:22:43] Starting clean-extension-ipynb ...
[19:22:43] Starting clean-extension-jake ...
[19:22:43] Starting clean-extension-json-language-features-client ...
[19:22:43] Starting clean-extension-json-language-features-server ...
[19:22:43] Starting clean-extension-markdown-language-features-preview-src ...
[19:22:43] Starting clean-extension-markdown-language-features-server ...
[19:22:43] Starting clean-extension-markdown-language-features ...
[19:22:43] Starting clean-extension-markdown-math ...
[19:22:43] Starting clean-extension-media-preview ...
[19:22:43] Starting clean-extension-merge-conflict ...
[19:22:43] Starting clean-extension-microsoft-authentication ...
[19:22:43] Starting clean-extension-npm ...
[19:22:43] Starting clean-extension-php-language-features ...
[19:22:43] Starting clean-extension-search-result ...
[19:22:43] Starting clean-extension-references-view ...
[19:22:43] Starting clean-extension-simple-browser ...
[19:22:43] Starting clean-extension-typescript-language-features-test-workspace ...
[19:22:43] Starting clean-extension-typescript-language-features-web ...
[19:22:43] Starting clean-extension-typescript-language-features ...
[19:22:43] Starting clean-extension-vscode-api-tests ...
[19:22:43] Starting clean-extension-vscode-colorize-tests ...
[19:22:43] Starting clean-extension-vscode-test-resolver ...
[19:22:43] Starting compile-extension-media ...
[19:22:43] Finished clean-out after 80 ms
[19:22:43] Starting build-web-node-paths ...
[19:22:44] Finished build-web-node-paths after 46 ms
[19:22:44] Starting compile-api-proposal-names ...
[19:22:44] Starting compilation api-proposal-names...
[19:22:44] Finished clean-extension-authentication-proxy after 160 ms
[19:22:44] Starting compile-extension:authentication-proxy ...
[19:22:44] Starting compilation extensions...
[19:22:44] Finished clean-extension-configuration-editing-build after 981 ms
[19:22:44] Starting compile-extension:configuration-editing-build ...
[19:22:44] Finished clean-extension-configuration-editing after 1005 ms
[19:22:44] Starting compile-extension:configuration-editing ...
[19:22:44] Finished clean-extension-css-language-features-client after 1024 ms
[19:22:44] Starting compile-extension:css-language-features-client ...
[19:22:44] Finished clean-extension-css-language-features-server after 1039 ms
[19:22:44] Starting compile-extension:css-language-features-server ...
[19:22:44] Finished clean-extension-debug-auto-launch after 1047 ms
[19:22:44] Starting compile-extension:debug-auto-launch ...
[19:22:44] Finished clean-extension-debug-server-ready after 1063 ms
[19:22:44] Starting compile-extension:debug-server-ready ...
[19:22:45] Finished clean-extension-emmet after 1081 ms
[19:22:45] Starting compile-extension:emmet ...
[19:22:45] Finished clean-extension-extension-editing after 1120 ms
[19:22:45] Starting compile-extension:extension-editing ...
[19:22:45] Finished clean-extension-git after 1132 ms
[19:22:45] Starting compile-extension:git ...
[19:22:45] Finished clean-extension-git-base after 1157 ms
[19:22:45] Starting compile-extension:git-base ...
[19:22:45] Finished clean-extension-github-authentication after 1170 ms
[19:22:45] Starting compile-extension:github-authentication ...
[19:22:45] Finished clean-extension-github after 1188 ms
[19:22:45] Starting compile-extension:github ...
[19:22:45] Finished clean-extension-grunt after 1204 ms
[19:22:45] Starting compile-extension:grunt ...
[19:22:45] Finished clean-extension-gulp after 1219 ms
[19:22:45] Starting compile-extension:gulp ...
[19:22:45] Finished clean-extension-html-language-features-client after 1232 ms
[19:22:45] Starting compile-extension:html-language-features-client ...
[19:22:45] Finished clean-extension-html-language-features-server after 1244 ms
[19:22:45] Starting compile-extension:html-language-features-server ...
[19:22:45] Finished clean-extension-ipynb after 1262 ms
[19:22:45] Starting compile-extension:ipynb ...
[19:22:45] Finished clean-extension-jake after 1276 ms
[19:22:45] Starting compile-extension:jake ...
[19:22:45] Finished clean-extension-json-language-features-client after 1287 ms
[19:22:45] Starting compile-extension:json-language-features-client ...
[19:22:45] Finished clean-extension-json-language-features-server after 1301 ms
[19:22:45] Starting compile-extension:json-language-features-server ...
[19:22:45] Finished clean-extension-markdown-language-features-preview-src after 1310 ms
[19:22:45] Starting compile-extension:markdown-language-features-preview-src ...
[19:22:45] Finished clean-extension-markdown-language-features-server after 1316 ms
[19:22:45] Starting compile-extension:markdown-language-features-server ...
[19:22:45] Finished clean-extension-markdown-language-features after 1325 ms
[19:22:45] Starting compile-extension:markdown-language-features ...
[19:22:45] Finished clean-extension-markdown-math after 1352 ms
[19:22:45] Starting compile-extension:markdown-math ...
[19:22:45] Finished clean-extension-media-preview after 1368 ms
[19:22:45] Starting compile-extension:media-preview ...
[19:22:45] Finished clean-extension-merge-conflict after 1385 ms
[19:22:45] Starting compile-extension:merge-conflict ...
[19:22:45] Finished clean-extension-microsoft-authentication after 1417 ms
[19:22:45] Starting compile-extension:microsoft-authentication ...
[19:22:45] Finished clean-extension-npm after 1435 ms
[19:22:45] Starting compile-extension:npm ...
[19:22:45] Finished clean-extension-php-language-features after 1453 ms
[19:22:45] Starting compile-extension:php-language-features ...
[19:22:45] Finished clean-extension-search-result after 1475 ms
[19:22:45] Starting compile-extension:search-result ...
[19:22:45] Finished clean-extension-references-view after 1488 ms
[19:22:45] Starting compile-extension:references-view ...
[19:22:45] Finished clean-extension-simple-browser after 1505 ms
[19:22:45] Starting compile-extension:simple-browser ...
[19:22:45] Finished clean-extension-typescript-language-features-test-workspace after 1515 ms
[19:22:45] Starting compile-extension:typescript-language-features-test-workspace ...
[19:22:45] Finished clean-extension-typescript-language-features-web after 1518 ms
[19:22:45] Starting compile-extension:typescript-language-features-web ...
[19:22:45] Finished clean-extension-typescript-language-features after 1521 ms
[19:22:45] Starting compile-extension:typescript-language-features ...
[19:22:45] Finished clean-extension-vscode-api-tests after 1561 ms
[19:22:45] Starting compile-extension:vscode-api-tests ...
[19:22:45] Finished clean-extension-vscode-colorize-tests after 1594 ms
[19:22:45] Starting compile-extension:vscode-colorize-tests ...
[19:22:45] Finished clean-extension-vscode-test-resolver after 1607 ms
[19:22:45] Starting compile-extension:vscode-test-resolver ...
[19:22:51] Finished compile-extension:authentication-proxy after 7074 ms
[19:22:51] Finished compile-extension:typescript-language-features-test-workspace after 5711 ms
[19:22:51] Finished esbuilding extension media /workspaces/vscode/extensions/markdown-math/esbuild.js with 0 errors.
[19:22:51] Finished esbuilding extension media /workspaces/vscode/extensions/markdown-language-features/esbuild-notebook.js with 0 errors.
[19:22:51] Finished esbuilding extension media /workspaces/vscode/extensions/simple-browser/esbuild-preview.js with 0 errors.
[19:22:51] Finished esbuilding extension media /workspaces/vscode/extensions/ipynb/esbuild.js with 0 errors.
[19:22:51] Finished esbuilding extension media /workspaces/vscode/extensions/notebook-renderers/esbuild.js with 0 errors.
[19:22:51] Finished esbuilding extension media /workspaces/vscode/extensions/markdown-language-features/esbuild-preview.js with 0 errors.
[19:22:51] Finished compile-extension-media after 7226 ms
[19:22:55] Finished compile-extension:configuration-editing-build after 10195 ms
[19:22:55] Finished compile-extension:typescript-language-features-web after 9647 ms
[19:22:58] Finished compile-extension:debug-auto-launch after 13917 ms
[19:22:58] Finished compile-extension:debug-server-ready after 13902 ms
[19:22:58] Finished compile-extension:grunt after 13758 ms
[19:22:58] Finished compile-extension:gulp after 13743 ms
[19:22:58] Finished compile-extension:jake after 13686 ms
[19:22:58] Finished compile-extension:markdown-math after 13618 ms
[19:23:05] Finished compile-extension:search-result after 19778 ms
[19:23:05] Finished monaco-typecheck after 21274 ms
[19:23:05] Finished compile-extension:vscode-colorize-tests after 19661 ms
[19:23:06] Finished compile-extension:vscode-test-resolver after 20549 ms
[19:23:09] Finished compile-extension:extension-editing after 23963 ms
[19:23:09] Finished compile-extension:simple-browser after 23580 ms
[19:23:14] Finished compile-extension:configuration-editing after 29326 ms
[19:23:15] Finished compile-extension:css-language-features-client after 30504 ms
[19:23:15] Finished compile-extension:markdown-language-features-preview-src after 30223 ms
[19:23:15] Finished compile-extension:json-language-features-client after 30248 ms
[19:23:15] Finished compile-extension:html-language-features-client after 30331 ms
[19:23:15] Finished compile-extension:json-language-features-server after 30262 ms
[19:23:15] Finished compile-extension:git-base after 30412 ms
[19:23:15] Finished compile-extension:php-language-features after 30125 ms
[19:23:17] Finished compile-extension:media-preview after 32182 ms
[19:23:17] Finished compile-extension:merge-conflict after 32165 ms
[19:23:17] Finished compile-extension:references-view after 32070 ms
[19:23:17] Finished compile-extension:npm after 32129 ms
[19:23:17] Finished compile-extension:ipynb after 32308 ms
[19:23:17] Finished compile-extension:microsoft-authentication after 32165 ms
[19:23:17] Finished compile-extension:github after 32398 ms
[19:23:17] Finished compile-extension:css-language-features-server after 32552 ms
[19:23:17] Finished compile-extension:markdown-language-features-server after 32269 ms
[19:23:17] Finished compile-extension:github-authentication after 32419 ms
[19:23:25] Finished compilation api-proposal-names with 0 errors after 41811 ms
[19:23:25] Finished compile-api-proposal-names after 41843 ms
[19:23:25] Starting compile-client ...
[19:23:27] Starting compilation...
[19:23:28] Finished compile-extension:vscode-api-tests after 42633 ms
[19:23:28] Finished compile-extension:git after 43113 ms
[19:23:28] Finished compile-extension:emmet after 43167 ms
[19:23:28] Finished compile-extension:html-language-features-server after 43009 ms
[19:23:31] Finished compile-extension:markdown-language-features after 46377 ms
[19:23:31] Finished compilation extensions with 0 errors after 46896 ms
[19:23:31] Finished compile-extension:typescript-language-features after 46478 ms
[19:23:31] Starting compile-extensions ...
[19:23:31] Finished compile-extensions after 0 ms
[19:25:28] Finished compilation with 0 errors after 121180 ms
[19:25:28] Finished compile-client after 123052 ms
[19:25:28] Starting compile ...
[19:25:28] Finished compile after 0 ms
[19:25:28] Finished 'compile' after 2.75 min
Done in 174.63s.
[19:25:29] Synchronizing built-in extensions...
[19:25:29] You can manage built-in extensions with the --builtin flag
[19:25:30] Downloading extension from GH: ms-vscode.js-debug-companion@1.0.18 ...
[19:25:30] Downloading extension from GH: ms-vscode.js-debug@1.74.1 ...
[19:25:30] Downloading extension from GH: ms-vscode.vscode-js-profile-table@1.0.3 ...
[19:25:32] [github] ms-vscode.js-debug-companion ✔︎
[19:25:32] [github] ms-vscode.vscode-js-profile-table ✔︎
[19:25:32] [github] ms-vscode.js-debug ✔︎
[12206:1209/192535.689600:WARNING:bluez_dbus_manager.cc(248)] Floss manager not present, cannot set Floss enable/disable.
[14235:1209/192536.106642:ERROR:gl_surface_egl.cc(804)] No suitable EGL configs found.
[14235:1209/192536.107883:ERROR:gl_context_egl.cc(136)] eglGetConfigAttrib failed with error EGL_BAD_CONFIG
libva error: vaGetDriverNameByIndex() failed with unknown libva error, driver_name = (null)
[14235:1209/192536.197046:ERROR:gl_surface_egl.cc(804)] No suitable EGL configs found.
[14235:1209/192536.197131:ERROR:gl_surface_egl.cc(2250)] eglCreatePbufferSurface failed with error EGL_BAD_CONFIG
[14235:1209/192536.197187:ERROR:gpu_info_collector.cc(80)] gl::GLContext::CreateOffscreenGLSurface failed
[14235:1209/192536.197237:ERROR:gpu_info_collector.cc(342)] Could not create surface for info collection.
[14235:1209/192536.197291:ERROR:gpu_init.cc(86)] CollectGraphicsInfo failed.
[14235:1209/192536.199205:ERROR:viz_main_impl.cc(186)] Exiting GPU process due to errors during initialization
[14308:1209/192536.311447:ERROR:gl_surface_egl.cc(804)] No suitable EGL configs found.
[14308:1209/192536.311640:ERROR:gl_context_egl.cc(136)] eglGetConfigAttrib failed with error EGL_BAD_CONFIG
libva error: vaGetDriverNameByIndex() failed with unknown libva error, driver_name = (null)
[14308:1209/192536.312720:ERROR:gl_surface_egl.cc(804)] No suitable EGL configs found.
[14308:1209/192536.312791:ERROR:gl_surface_egl.cc(2250)] eglCreatePbufferSurface failed with error EGL_BAD_CONFIG
[14308:1209/192536.312839:ERROR:gpu_info_collector.cc(80)] gl::GLContext::CreateOffscreenGLSurface failed
[14308:1209/192536.312912:ERROR:gpu_info_collector.cc(342)] Could not create surface for info collection.
[14308:1209/192536.312967:ERROR:gpu_init.cc(86)] CollectGraphicsInfo failed.
[14308:1209/192536.314948:ERROR:viz_main_impl.cc(186)] Exiting GPU process due to errors during initialization
libva error: vaGetDriverNameByIndex() failed with unknown libva error, driver_name = (null)
[14337:1209/192536.419315:WARNING:sandbox_linux.cc(376)] InitializeSandbox() called with multiple threads in process gpu-process.
[14337:1209/192536.422261:ERROR:gpu_memory_buffer_support_x11.cc(44)] dri3 extension not supported.
[14288:1209/192536.424718:ERROR:command_buffer_proxy_impl.cc(126)] ContextResult::kTransientFailure: Failed to send GpuControl.CreateCommandBuffer.
[12206:1209/192538.149982:INFO:CONSOLE(261)] "[uncaught exception]: Error: [object Event]", source: vscode-file://vscode-app/workspaces/vscode/out/bootstrap-window.js (261)
[12206:1209/192538.150191:INFO:CONSOLE(264)] "Error: [object Event]
    at Object.ensureError (vscode-file://vscode-app/workspaces/vscode/out/vs/loader.js:256:22)
    at ModuleManager._createLoadError (vscode-file://vscode-app/workspaces/vscode/out/vs/loader.js:1508:33)
    at ModuleManager._onLoadError (vscode-file://vscode-app/workspaces/vscode/out/vs/loader.js:1519:30)
    at loadNextPath (vscode-file://vscode-app/workspaces/vscode/out/vs/loader.js:1665:27)
    at Object.errorback (vscode-file://vscode-app/workspaces/vscode/out/vs/loader.js:1685:25)
    at OnlyOnceScriptLoader.triggerErrorback (vscode-file://vscode-app/workspaces/vscode/out/vs/loader.js:631:36)
    at vscode-file://vscode-app/workspaces/vscode/out/vs/loader.js:618:151
    at HTMLScriptElement.errorEventListener (vscode-file://vscode-app/workspaces/vscode/out/vs/loader.js:654:17)", source: vscode-file://vscode-app/workspaces/vscode/out/bootstrap-window.js (264)
[12206:1209/192538.150405:INFO:CONSOLE(261)] "[uncaught exception]: Error: [object Event]", source: vscode-file://vscode-app/workspaces/vscode/out/bootstrap-window.js (261)
[12206:1209/192538.150459:INFO:CONSOLE(264)] "Error: [object Event]
    at Object.ensureError (vscode-file://vscode-app/workspaces/vscode/out/vs/loader.js:256:22)
    at ModuleManager._createLoadError (vscode-file://vscode-app/workspaces/vscode/out/vs/loader.js:1508:33)
    at ModuleManager._onLoadError (vscode-file://vscode-app/workspaces/vscode/out/vs/loader.js:1519:30)
    at loadNextPath (vscode-file://vscode-app/workspaces/vscode/out/vs/loader.js:1665:27)
    at Object.errorback (vscode-file://vscode-app/workspaces/vscode/out/vs/loader.js:1685:25)
    at OnlyOnceScriptLoader.triggerErrorback (vscode-file://vscode-app/workspaces/vscode/out/vs/loader.js:631:36)
    at vscode-file://vscode-app/workspaces/vscode/out/vs/loader.js:618:151
    at HTMLScriptElement.errorEventListener (vscode-file://vscode-app/workspaces/vscode/out/vs/loader.js:654:17)", source: vscode-file://vscode-app/workspaces/vscode/out/bootstrap-window.js (264)
[12206:1209/192538.150711:INFO:CONSOLE(261)] "[uncaught exception]: Error: [object Event]", source: vscode-file://vscode-app/workspaces/vscode/out/bootstrap-window.js (261)
[12206:1209/192538.150763:INFO:CONSOLE(264)] "Error: [object Event]
    at Object.ensureError (vscode-file://vscode-app/workspaces/vscode/out/vs/loader.js:256:22)
    at ModuleManager._createLoadError (vscode-file://vscode-app/workspaces/vscode/out/vs/loader.js:1508:33)
    at ModuleManager._onLoadError (vscode-file://vscode-app/workspaces/vscode/out/vs/loader.js:1519:30)
    at loadNextPath (vscode-file://vscode-app/workspaces/vscode/out/vs/loader.js:1665:27)
    at Object.errorback (vscode-file://vscode-app/workspaces/vscode/out/vs/loader.js:1685:25)
    at OnlyOnceScriptLoader.triggerErrorback (vscode-file://vscode-app/workspaces/vscode/out/vs/loader.js:631:36)
    at vscode-file://vscode-app/workspaces/vscode/out/vs/loader.js:618:151
    at HTMLScriptElement.errorEventListener (vscode-file://vscode-app/workspaces/vscode/out/vs/loader.js:654:17)", source: vscode-file://vscode-app/workspaces/vscode/out/bootstrap-window.js (264)
```

My `yarn` / `yarn install` command beforehand runs without errors.

The noVNC web interface shows this:

![image](https://user-images.githubusercontent.com/1810902/206783050-66256037-bf86-4a00-b70d-adf740638557.png)


@deepak1556 I have run Git bisect on this:
```

## What you have

- `/testbed/repo` is a git clone of `microsoft/vscode` truncated just after the regression was
  reported.  `HEAD` is `09b5220d78ed381fa02ca56b1fd4dbd5777a7e7a` and the full history behind it is present.
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
