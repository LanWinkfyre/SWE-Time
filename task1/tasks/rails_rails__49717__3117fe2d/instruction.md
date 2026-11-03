# Locate the commit that introduced this regression

A regression was reported against `rails/rails`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Rails 7.1 - can't define enums for attributes which don't exist in table

Not sure if this is an intended change or not. Pre 7.1, I could define an attr on a model using `attribute` and define enum values for it, then use enum helper methods. I'm using this heavily in my current project for i18ns etc, so defining the enum values as an array and manually validating won't cover all my use cases

Since 7.1, this isn't possible.

### Steps to reproduce

```ruby
# frozen_string_literal: true

require "bundler/inline"

gemfile(true) do
  source "https://rubygems.org"

  git_source(:github) { |repo| "https://github.com/#{repo}.git" }

  gem "rails", github: "rails/rails", branch: "main"
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
end

class Post < ActiveRecord::Base
  attribute :topic
  enum topic: %i[sports politics entertainment]
end

class BugTest < Minitest::Test
  def test_association_stuff
    post = Post.create!
    post.assign_attributes(topic: :sports)

    assert_equal true, post.sports?
  end
end# frozen_string_literal: true


```

### Expected behavior
Post should instantiate correctly and can use enum helper methods

### Actual behavior
Error thrown

`RuntimeError: Unknown enum attribute 'topic' for Post`

### System configuration
**Rails version**: 7.1.1

**Ruby version**: ruby 3.1.2p20


Thanks for your report!



It looks like intended behavior, but it's unclear to me why exactly this was changed. /cc @fatkodima
```

## What you have

- `/testbed/repo` is a git clone of `rails/rails` truncated just after the regression was
  reported.  `HEAD` is `a60a5d0f5bbe30a33f8562d77277ef19906944aa` and the full history behind it is present.
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
