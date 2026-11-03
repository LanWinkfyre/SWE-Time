# Locate the commit that introduced this regression

A regression was reported against `rails/rails`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Rails 5.1 regression - unscope broken with a specific where value

### Steps to reproduce

Added this spec to `test/cases/relations_test.rb`

``` ruby
def test_unscope_specific_where_value
  posts = Post.where(title: "Welcome to the weblog", body: "Such a lovely day")

  assert_equal 1, posts.count
  assert_equal 1, posts.unscope(where: :title).count
  assert_equal 1, posts.unscope(where: :body).count
end
```

Which fails on the final assertion with:

```
RelationTest#test_unscope_specific_where_value [test/cases/relations_test.rb:1978]:
Expected: 1
  Actual: 0
```

Unscoping the last argument should allow it to return the same record. We're only removing a condition so it shouldn't return _fewer_ record. AR is constructing the query incorrectly and returning no records.

### What's going on?

When unscoping the individual attribute it isn't treating binds correctly.

``` ruby
posts.to_sql
# SELECT "posts".* FROM "posts" WHERE "posts"."title" = 'Welcome to the weblog'
#                                 AND "posts"."body" = 'Such a lovely day'

posts.unscope(where: :title).to_sql
# SELECT "posts".* FROM "posts" WHERE "posts"."body" = 'Such a lovely day'

posts.unscope(where: :body).to_sql
# SELECT "posts".* FROM "posts" WHERE "posts"."title" = 'Such a lovely day'
```

So the bind intended for the `title` is now being used on the `body`. Whoops!

### Expected behavior

Binds stay attached to the correct attribute.

### Actual behavior

Binds become messed up. And the resulting query is incorrect.

### System configuration
**Rails version**:
5.1.0.rc1

**Ruby version**:
2.3.3
```

## What you have

- `/testbed/repo` is a git clone of `rails/rails` truncated just after the regression was
  reported.  `HEAD` is `5c0d00072d1309dbc77bb5d97e42956bac3e8684` and the full history behind it is present.
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
