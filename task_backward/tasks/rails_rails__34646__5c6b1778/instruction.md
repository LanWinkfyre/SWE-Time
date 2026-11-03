# Locate the commit that introduced this regression

A regression was reported against `rails/rails`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Deprecating column accessor fails in 5.2.2

### Steps to reproduce
```ruby
# frozen_string_literal: true

require "bundler/inline"

gemfile(true) do
  source "https://rubygems.org"

  git_source(:github) { |repo| "https://github.com/#{repo}.git" }

  # Activate the gem you are reporting the issue against.
  gem "rails", "5.2.2"
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
    t.string :content
  end
end

class Post < ActiveRecord::Base
  deprecate :content
end

class BugTest < Minitest::Test
  def test_stuff
    Post.create!
  end
end
```

### Expected behavior
Exit without error, as 5.2.1

### Actual behavior
```
Traceback (most recent call last):
	7: from ./test.rb:31:in `<main>'
	6: from ./test.rb:34:in `<class:Post>'
	5: from /Users/yskkin/projects/rails/activesupport/lib/active_support/core_ext/module/deprecation.rb:23:in `deprecate'
	4: from /Users/yskkin/projects/rails/activesupport/lib/active_support/deprecation/instance_delegator.rb:22:in `deprecate_methods'
	3: from /Users/yskkin/projects/rails/activesupport/lib/active_support/deprecation/method_wrappers.rb:57:in `deprecate_methods'
	2: from /Users/yskkin/projects/rails/activesupport/lib/active_support/deprecation/method_wrappers.rb:57:in `each'
	1: from /Users/yskkin/projects/rails/activesupport/lib/active_support/deprecation/method_wrappers.rb:67:in `block in deprecate_methods'
/Users/yskkin/projects/rails/activesupport/lib/active_support/deprecation/method_wrappers.rb:67:in `alias_method': undefined method `content' for class `Post(id: integer, content: string)' (NameError)
```

### System configuration
**Rails version**: 5.2.2

**Ruby version**: 2.5.0p0
```

## What you have

- `/testbed/repo` is a git clone of `rails/rails` truncated just after the regression was
  reported.  `HEAD` is `b86f65a816546ff8eea39d25b62c995c7efc21dc` and the full history behind it is present.
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
