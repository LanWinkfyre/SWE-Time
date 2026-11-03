# Locate the commit that introduced this regression

A regression was reported against `rails/rails`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
postgres enum array + db:prepare regression in rails 7.1.1

### Steps to reproduce
repo is here: https://github.com/modosc/rails-7-bug-repro

the `schema.rb` is a snippet from a rails 7.0 app we have. when upgrading to 7.1 various db tasks broken. i isolated the issue down to what's committed in `db/schema.rb`. 

### Expected behavior
`rails db:prepare`  should work and not remove the `accounts` table from `db/schema.rb`

### Actual behavior
```bash
$ rails db:drop db:prepare
Dropped database 'rails_bug_development'
Dropped database 'rails_bug_test'
Created database 'rails_bug_development'
unknown OID 824692: failed to recognize type of 'account_types'. It will be treated as String.
Created database 'rails_bug_test'
$ git diff
diff --git a/db/schema.rb b/db/schema.rb
index c7a182a..45937af 100644
--- a/db/schema.rb
+++ b/db/schema.rb
@@ -18,7 +18,4 @@ ActiveRecord::Schema[7.1].define(version: 2023_10_24_155210) do
   # Note that some types may not work with other database engines. Be careful if changing database.
   create_enum "account_type", ["customer", "vendor"]

-  create_table "accounts", force: :cascade do |t|
-    t.enum "account_types", array: true, enum_type: "account_type"
-  end
 end
```

there seems to be an intermediate change to `db/schema.rb` which includes these contents:
```
# Could not dump table "accounts" because of following StandardError
#   Unknown type 'account_type' for column 'account_types'
```
but that gets overwritten almost immediately.

note that `db:schema:load` does work as expected:
```bash
$ rails db:drop db:create db:schema:load
Dropped database 'rails_bug_development'
Dropped database 'rails_bug_test'
Created database 'rails_bug_development'
Created database 'rails_bug_test'
```

also note that in both cases the underlying db table is created. however, any subsequent db migration will cause the `accounts` table to be removed from `db/schema.rb`

finally, note that if i remove `array: true` from both the initial migration and `db/schema.rb` everything works as expected.

### System configuration
**Rails version**:
```bash
$ rails -v
Rails 7.1.1
```

**Ruby version**:
```bash
$  ruby -v
ruby 3.2.2 (2023-03-30 revision e51014f9c0) [arm64-darwin22]
```

**Postgres version**:
```
psql (16.0, server 15.4 (Homebrew))
```
```

## What you have

- `/testbed/repo` is a git clone of `rails/rails` truncated just after the regression was
  reported.  `HEAD` is `574ea20dac09ff5e9879b78157c34d168ec52101` and the full history behind it is present.
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
