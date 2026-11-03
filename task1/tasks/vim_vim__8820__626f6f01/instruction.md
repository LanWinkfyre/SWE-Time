# Locate the commit that introduced this regression

A regression was reported against `vim/vim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Buggy screen refresh in gVim with a Netrw window

**Describe the bug**
In gVim, when a Netrw window is visible and the screen is refreshed, either
automatically or by doing `CTRL-L`, gVim twitches and can even change size.

**To Reproduce**
1. `gvim --clean`
2. `:source $VIMRUNTIME/plugin/netrwPlugin.vim`
3. `:Sexplore`
4. Do `CTRL-L` and note how gVim twitches. Elements of the GUI quickly
   disappear and reappear.
5. `:set guioptions=egL`
6. Do `CTRL-L` several times and note how the gVim window becomes narrower.


**Expected behavior**
No twitching when the screen is refreshed. gVim window should not change size.

**Screenshots**
https://user-images.githubusercontent.com/57042631/131352404-440db7f7-4269-4a74-8637-7629371f0e47.mp4

**Environment (please complete the following information):**
 - Vim 8.2.3386
 - OS: Windows 10
 - Terminal: GUI

**Additional context**
This bug does not affect Vim 8.2.3384. It also does not affect Vim run in a
terminal.




The way I found out is described below, if this is not related, please let me know to open a new issue.

When I use ``` :Ex ``` the gVim windows flashes the toolbar and gets narrower by one character.
I also use https://www.vim.org/scripts/script.php?script_id=2596 in order to have F11 mapped to full screen(remove the border&titlebar). When I use F11, columns and lines are set to a big value, using ``` :Ex ``` in fullscreen will make gvim.exe run heavily for a minute (full CPU) before it displays the contents of directory.

I also use this script
```
function ToggleExplorer()
    if &ft == "netrw"
        if exists("w:netrw_rexfile")
            if w:netrw_rexfile == "" || w:netrw_rexfile == "NetrwTreeListing"
                exec 'q'
            else
                exec 'e ' . w:netrw_rexfile
            endif
        else
            if exists("w:netrw_rexlocal")
                Rexplore
            else
                exec 'q'
            endif
        endif
    else
        Explore
    endif
endfun
```
I use this to open/close the Explorer, with the bug above the script won't work correctly.
The expected result is that calling this function will open explorer, calling it again inside an explorer will close it, or close vim is that is the only buffer.
With the bug, explorer opens, gets narrower, calling the function again will just make the editor narrower.

Also using gvim in Windows 10, compiled using MSVC.
```

## What you have

- `/testbed/repo` is a git clone of `vim/vim` truncated just after the regression was
  reported.  `HEAD` is `a91871262670f9d3a4e5d1c5c6dbc02f85625f7d` and the full history behind it is present.
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
