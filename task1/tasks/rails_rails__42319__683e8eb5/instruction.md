# Locate the commit that introduced this regression

A regression was reported against `rails/rails`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
`initialize!` raises `FrozenError` when called more than once from an app using `zeitwerk`

### Steps to reproduce
initialize a rails app twice:
```ruby
  require "action_controller/railtie"
  class App < Rails::Application; end

  a = App.new
  a.initialize!
  
  b = App.new
  b.initialize!
```
### Expected behavior
no errors should be raised - this is the case on `6.0.3.7` and `6.1.3.2` with default configs

### Actual behavior
on `main` i get this error:

i also found the same behavior when instantiating and initializing instances of two different classes. 



i found that in `6.1.3.2`  i could get a similar error by enabling `zeitwerk`
```ruby
  require "action_controller/railtie"
  class App < Rails::Application; end
  App.config.autoloader = :zeitwerk

  a = App.new
  a.config.autoloader = :zeitwerk
  a.initialize!
  
  b = App.new
  b.config.autoloader = :zeitwerk
  b.initialize!
```


### System configuration
**Rails version**:

`6.1.3.2`
`6.0.3.7`

**Ruby version**:
`ruby 2.7.3p183 (2021-04-05 revision 6847ee089d) [x86_64-darwin20]`
```

## What you have

- `/testbed/repo` is a git clone of `rails/rails` truncated just after the regression was
  reported.  `HEAD` is `b678667853b48751ea6134f1f8ba3d687c943889` and the full history behind it is present.
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
