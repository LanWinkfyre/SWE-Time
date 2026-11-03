# Locate the commit that introduced this regression

A regression was reported against `rails/rails`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Delivering mail causes tests to fail

### Steps to reproduce

```
rails new demo
cd demo
rails generate scaffold Order invoice:string
rails generate scaffold Cart
rails db:migrate
rails generate mailer OrderNotifier received shipped
edit app/controllers/orders_controller.rb
    >>> insert "OrderNotifierMailer.received.deliver_later"
rails test
```
- [Full log of scenario](http://intertwingly.net/tmp/aj_reload.html)
### Expected behavior

Tests should continue to pass
### Actual behavior

Tests fail
### System configuration


**Ruby version**: `ruby 2.3.0p0 (2015-12-25 revision 53290) [x86_64-linux]`
```

## What you have

- `/testbed/repo` is a git clone of `rails/rails` truncated just after the regression was
  reported.  `HEAD` is `a408645223f81613b45366aa69d28584c37f17f8` and the full history behind it is present.
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
