# Locate the commit that introduced this regression

A regression was reported against `rails/rails`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Rails4 can't use :defaults in url_for ?



``` ruby
# routes
  get 'foo/a'=>'users#edit', defaults:{bar:1}
  get 'foo/b'=>'users#edit', defaults:{bar:2}
  get 'foo/c'=>'users#edit', defaults:{bar:3}


url_for(controller:'users', action:'edit', bar:1) #=> '/foo/a'
url_for(controller:'users', action:'edit', bar:2) #=> '/foo/a'
url_for(controller:'users', action:'edit', bar:3) #=> '/foo/a'

```

  Is there a better way of writing those routes?
```

## What you have

- `/testbed/repo` is a git clone of `rails/rails` truncated just after the regression was
  reported.  `HEAD` is `474ebc55bd13ad58626a49dfc44c8e6407813935` and the full history behind it is present.
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
