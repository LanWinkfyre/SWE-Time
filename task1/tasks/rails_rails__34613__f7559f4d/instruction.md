# Locate the commit that introduced this regression

A regression was reported against `rails/rails`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Wrong query with scope and has_many polymorphic association

### Steps to reproduce
I created a test.rb to reproduce it:

```
# frozen_string_literal: true

require "bundler/inline"

gemfile(true) do
  source "https://rubygems.org"

  git_source(:github) { |repo| "https://github.com/#{repo}.git" }

  # Activate the gem you are reporting the issue against.
  gem "activerecord", "5.2.0"
  gem "sqlite3"
end

require "active_record"
require "minitest/autorun"
require "logger"

# This connection will do for database-independent bug reports.
ActiveRecord::Base.establish_connection(adapter: "sqlite3", database: ":memory:")
ActiveRecord::Base.logger = Logger.new(STDOUT)

ActiveRecord::Schema.define do
  create_table :pages, force: true do |t|
  end

  create_table :elements, force: true do |t|
    t.integer :page_id
  end

  create_table :contents, force: true do |t|
    t.integer :element_id
    t.integer :essence_id
    t.string  :essence_type
  end

  create_table :essence_texts, force: true do |t|
    t.boolean :searchable
  end
end

class Page < ActiveRecord::Base
  has_many :elements

  has_many :contents,
           through: :elements

  has_many :essence_texts,
           through: :contents,
           source: :essence,
           source_type: 'EssenceText'

  has_many :searchable_essence_texts,
           -> { where(searchable: true) },
           through: :contents,
           source: :essence,
           source_type: 'EssenceText',
           class_name: 'EssenceText'
end

class Element < ActiveRecord::Base
  belongs_to :page,
             inverse_of: :elements

  has_many :contents
end

class Content < ActiveRecord::Base
  belongs_to :essence,
             polymorphic: true

  belongs_to :element,
             inverse_of: :contents

  has_one :page,
          through: :element
end

class EssenceText < ActiveRecord::Base
  has_one :content,
          as: :essence

  has_one :element,
          through: :content

  has_one :page,
          through: :element
end

class BugTest < Minitest::Test
  def test_association_stuff
    page1 = Page.create!
    element1 = Element.create!
    Content.create! element: element1,
                    essence: EssenceText.create!(searchable: true)

    page1.elements << element1

    assert_equal 1, Page.joins(:essence_texts).count
    assert_equal 1, Page.joins(:searchable_essence_texts).count
  end
end
```

### Expected behavior
The test should pass.

### Actual behavior
The second assertion fails, because the SQL query generated is wrong.
It applies the scope of the `has_many` association `searchable_essence_texts` to the table `contents` and also to the right table (`essence_texts`).

Rails 5.0.7.1
```
SELECT COUNT(*)
FROM "pages"
INNER JOIN "elements" ON "elements"."page_id" = "pages"."id"
INNER JOIN "contents" ON "contents"."element_id" = "elements"."id" AND "contents"."essence_type" = ?
INNER JOIN "essence_texts" ON "essence_texts"."id" = "contents"."essence_id" AND "essence_texts"."searchable" = ?
```
Rails 5.2.1.1
```
SELECT COUNT(*)
FROM "pages"
INNER JOIN "elements" ON "elements"."page_id" = "pages"."id"
INNER JOIN "contents" ON "contents"."element_id" = "elements"."id" AND "contents"."searchable" = ? AND "contents"."essence_type" = ?
INNER JOIN "essence_texts" ON "essence_texts"."id" = "contents"."essence_id" AND "essence_texts"."searchable" = ?
```

### System configuration
**Rails version**: 5.1.0 / 5.2.0 / master, **it works with 5.0.7.1**

**Ruby version**: ruby 2.4.4
```

## What you have

- `/testbed/repo` is a git clone of `rails/rails` truncated just after the regression was
  reported.  `HEAD` is `609c58bfa6df58b88e3eadebb1f1d49354541d24` and the full history behind it is present.
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
