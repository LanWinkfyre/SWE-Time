# Locate the commit that introduced this regression

A regression was reported against `darktable-org/darktable`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Compilation doesn't work

Hello,



`[ 49%] Linking C shared module libexport.so
[ 49%] Built target filter
[ 49%] Built target copy_history
[ 49%] Linking C shared module libhistory.so
/home/guillaume/git-darktable/src/libs/import.c: In function ‘_lib_import_get_extra_widget’:
/home/guillaume/git-darktable/src/libs/import.c:366:14: error: ‘main’ is usually a function [-Werror=main]
   GtkWidget *main = gtk_box_new(GTK_ORIENTATION_VERTICAL, 0);
              ^~~~
[ 49%] Built target modulelist
[ 49%] Linking C shared module liblighttable_mode.so
[ 49%] Linking C shared module libnavigation.so
cc1: all warnings being treated as errors
make[2]: *** [src/libs/CMakeFiles/import.dir/build.make:63: src/libs/CMakeFiles/import.dir/import.c.o] Error 1
make[1]: *** [CMakeFiles/Makefile2:3245: src/libs/CMakeFiles/import.dir/all] Error 2
make[1]: *** Attente des tâches non terminées....
[ 49%] Built target export
[ 49%] Built target snapshots
[ 49%] Built target lighttable_mode
[ 49%] Built target history
[ 49%] Built target navigation
make: *** [Makefile:152: all] Error 2
`

I am with Debian Buster. I compil dt with the the script in git and :
`libgtk-3-dev:
  Installé : 3.24.5-1
  Candidat : 3.24.5-1
 Table de version :
 *** 3.24.5-1 500
        500 http://ftp.fr.debian.org/debian buster/main amd64 Packages
        100 /var/lib/dpkg/status`

Is it ths version what is too low ?
Do you need other infos ?

Thanks for your return

Came here to report this and found this thread.

A git bisect shows this:

```




[ 54%] Building C object src/libs/CMakeFiles/copy_history.dir/copy_history.c.o
Scanning dependencies of target snapshots
[ 54%] Built target histogram
[ 54%] Building C object src/libs/CMakeFiles/snapshots.dir/snapshots.c.o
[ 54%] Linking C shared module libcollect.so
Scanning dependencies of target export
cc1: all warnings being treated as errors
make[2]: *** [src/libs/CMakeFiles/import.dir/build.make:63: src/libs/CMakeFiles/import.dir/import.c.o] Error 1
make[1]: *** [CMakeFiles/Makefile2:3245: src/libs/CMakeFiles/import.dir/all] Error 2
make[1]: *** Waiting for unfinished jobs....
[ 56%] Building C object src/libs/CMakeFiles/export.dir/export_metadata.c.o

EDIT: A word.
```

## What you have

- `/testbed/repo` is a git clone of `darktable-org/darktable` truncated just after the regression was
  reported.  `HEAD` is `de2cf0f4162ba2d5bb0144967ae1f27307fd5ae5` and the full history behind it is present.
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
