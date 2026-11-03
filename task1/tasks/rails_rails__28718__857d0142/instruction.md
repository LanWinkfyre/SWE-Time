# Locate the commit that introduced this regression

A regression was reported against `rails/rails`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Freeze attributes when I create new Active record object with them

I faced one unexpected behavior: when I have one new active record object and build second with first's attributes, attributes of first object will be frozen.

For example:
I have ActiveRecord model 'User' with 2 attributes - 'first_name' and 'last_name'
### Steps to reproduce
```ruby
user = User.new(first_name: 'Alex', last_name: 'Kosh')
user.first_name.frozen? #=> false
User.new(user.attributes)
user.first_name.frozen? #=> true
```

### Expected behavior
user.attributes are not frozen

### System configuration
Rails version: 5.0.2
Ruby version: 2.3.3


Ahh, I see! I was inspecting the wrong thing.
```

## What you have

- `/testbed/repo` is a git clone of `rails/rails` truncated just after the regression was
  reported.  `HEAD` is `2144e70a86e6403a6298d61862e2e85615cd2a82` and the full history behind it is present.
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
