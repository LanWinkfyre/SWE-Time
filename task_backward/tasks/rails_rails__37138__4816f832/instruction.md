# Locate the commit that introduced this regression

A regression was reported against `rails/rails`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
AR: new instance of unscoped association ignores unscope

When initializing a new AR object from an `unscoped` association, the `unscope` is not taken into account.

See `steps to reproduce` for an example





### Steps to reproduce

```ruby
# frozen_string_literal: true

require "bundler/inline"

gemfile(true) do
  source "https://rubygems.org"

  git_source(:github) { |repo| "https://github.com/#{repo}.git" }

  # Activate the gem you are reporting the issue against.
  gem "activerecord", "6.0.0"
  gem "sqlite3"
end

require "active_record"
require "minitest/autorun"
require "logger"

# This connection will do for database-independent bug reports.
ActiveRecord::Base.establish_connection(adapter: "sqlite3", database: ":memory:")
ActiveRecord::Base.logger = Logger.new(STDOUT)

ActiveRecord::Schema.define do
  create_table :posts, force: true do |t|
  end

  create_table :comments, force: true do |t|
    t.integer :post_id
    t.boolean :visible, default: false
  end
end

class Post < ActiveRecord::Base
  has_many :comments
end

class Comment < ActiveRecord::Base
  belongs_to :post
  default_scope -> { where(visible: true) }
end

class BugTest < Minitest::Test
  def test_association_stuff
    post = Post.create!
    post.comments << Comment.create!

    new_comment = post.comments.unscope(where: :visible).new

    assert_equal false, new_comment.visible
  end
end
```

### Expected behavior

in `new_comment = post.comments.unscope(where: :visible).new`, since the default scope is unscoped, I expect `new_comment.visible` to be false, since it's the default database value for the field

### Actual behavior

in `new_comment = post.comments.unscope(where: :visible).new`, the unscope is ignored and `new_comment.visible` is true (due to `default_scope`)

### System configuration
**Rails version**: 6.0.0

**Ruby version**: 2.6.3
```

## What you have

- `/testbed/repo` is a git clone of `rails/rails` truncated just after the regression was
  reported.  `HEAD` is `3f27aa8cdf8c3c7f36d630f0241854f712e4c937` and the full history behind it is present.
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
