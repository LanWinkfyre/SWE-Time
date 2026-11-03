# Locate the commit that introduced this regression

A regression was reported against `rails/rails`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
PG::SyntaxError on query serialize in Rails 7.2

### Description
Problem with serialization sql query with string condition and `nil` bind value with PostgreSQL adapter (it does work with sqlite3) 

### Steps to reproduce
```ruby
# frozen_string_literal: true

require 'bundler/inline'

gemfile(true) do
  source 'https://rubygems.org'

  gem 'rails'
  # If you want to test against edge Rails replace the previous line with this:
  # gem "rails", github: "rails/rails", branch: "main"

  gem 'pg'
end

require 'active_record'
require 'minitest/autorun'
require 'logger'

db_config = { adapter: 'postgresql', database: 'test', host: 'localhost' }
ActiveRecord::Tasks::DatabaseTasks.create(db_config)

# This connection will do for database-independent bug reports.
ActiveRecord::Base.establish_connection(adapter: 'postgresql', database: 'test')
ActiveRecord::Base.logger = Logger.new($stdout)

ActiveRecord::Schema.define do
  create_table :users, force: true do |t|
    t.string :name
  end
end

class User < ActiveRecord::Base
end

class BugTest < Minitest::Test
  def test_association_stuff
    user1 = User.create!(name: 'John Doe')
    user2 = User.create!

    assert_equal user1, User.find_by('LOWER(name) = ?', 'john doe')
    assert_equal nil, User.find_by('LOWER(name) = ?', 'jane doe')
    assert_equal user2, User.find_by('LOWER(name) IS ?', nil)
  end
end
```

### Expected behavior
Serialize query with `LOWER(name) IS NULL` condition

### Actual behavior
```
ActiveRecord::StatementInvalid: PG::SyntaxError: ERROR:  syntax error at or near "$1"
LINE 1: ...LECT "users".* FROM "users" WHERE (LOWER(name) IS $1) LIMIT ...
```

### System configuration
**Rails version**:
Rails 7.2.0
**Ruby version**:
ruby 3.3.4 (2024-07-09 revision be1089c8ec) [arm64-darwin23]


Using `git bisect`



Rails version: ">=v7.2.0" introduced the bug.

cc: @byroot
```

## What you have

- `/testbed/repo` is a git clone of `rails/rails` truncated just after the regression was
  reported.  `HEAD` is `16882b886e245f363cd61f5ea553fe2bc525d070` and the full history behind it is present.
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
