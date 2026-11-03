# Locate the commit that introduced this regression

A regression was reported against `rails/rails`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
When validates_uniqness_of is used on primary key column of type uuid validation fails on update

I ran into this on 5.0.0.beta1 but it behaves the same on beta2.

I'm using uuid column type as primary key for table. Update when model doesn't have validation works as expected. If model have validation, update fails with error of uuid not being uniq. I'm not sure if this is because of incorrect table declaration or if this is bug.

Here is failing test

``` ruby
begin
  require 'bundler/inline'
rescue LoadError => e
  $stderr.puts 'Bundler version 1.10 or later is required. Please update your Bundler'
  raise e
end

gemfile(true) do
  source 'https://rubygems.org'
  gem 'rails', git: 'git@github.com:rails/rails.git', branch: 'v5.0.0.beta2'
  gem 'arel', github: 'rails/arel'
  gem 'rack', github: 'rack/rack'
  gem 'sprockets', github: 'rails/sprockets'
  gem 'sprockets-rails', github: 'rails/sprockets-rails'
  gem 'sass-rails', github: 'rails/sass-rails'
  gem 'pg'
end

require 'active_record'
require 'minitest/autorun'
require 'logger'

# This connection will do for database-independent bug reports.
ActiveRecord::Base.establish_connection(adapter: 'postgresql', database: 'report_db')
ActiveRecord::Base.logger = Logger.new(STDOUT)

ActiveRecord::Schema.define do
  create_table :items, force: true, id: false do |t|
    t.uuid :uuid, primary_key: true
    t.string :title
  end
end

class Item < ActiveRecord::Base
end

class ValidatingItem < Item
  validates_uniqueness_of :uuid
end

class BugTest < Minitest::Test
  def test_update
    item = Item.create!(uuid: SecureRandom.uuid, title: 'item1')
    item.update(title: 'item1-title2')

    assert_empty item.errors

    item2 = ValidatingItem.create!(uuid: SecureRandom.uuid, title: 'item2')
    item2.update(title: 'item2-title2')

    assert_empty item2.errors

  end
end
```

and output

``` bash
-- create_table(:items, {:force=>true, :id=>false})
D, [2016-02-12T01:55:14.428369 #96236] DEBUG -- :    (4.7ms)  DROP TABLE "items"
D, [2016-02-12T01:55:14.434925 #96236] DEBUG -- :    (6.2ms)  CREATE TABLE "items" ("uuid" uuid PRIMARY KEY, "title" character varying)
   -> 0.0584s
D, [2016-02-12T01:55:14.454753 #96236] DEBUG -- :   ActiveRecord::InternalMetadata Load (0.6ms)  SELECT  "ar_internal_metadata".* FROM "ar_internal_metadata" ORDER BY "ar_internal_metadata"."key" ASC LIMIT $1  [["LIMIT", 1]]
D, [2016-02-12T01:55:14.465138 #96236] DEBUG -- :    (0.1ms)  BEGIN
D, [2016-02-12T01:55:14.466125 #96236] DEBUG -- :    (0.1ms)  COMMIT
Run options: --seed 15933

# Running:

D, [2016-02-12T01:55:14.497080 #96236] DEBUG -- :    (0.1ms)  BEGIN
D, [2016-02-12T01:55:14.498754 #96236] DEBUG -- :   SQL (0.7ms)  INSERT INTO "items" ("uuid", "title") VALUES ($1, $2) RETURNING "uuid"  [["uuid", "18d12e5c-e9b9-4eaa-b325-8d6c480313f3"], ["title", "item1"]]
D, [2016-02-12T01:55:14.499456 #96236] DEBUG -- :    (0.3ms)  COMMIT
D, [2016-02-12T01:55:14.499714 #96236] DEBUG -- :    (0.1ms)  BEGIN
D, [2016-02-12T01:55:14.501272 #96236] DEBUG -- :   SQL (0.5ms)  UPDATE "items" SET "title" = $1 WHERE "items"."uuid" = $2  [["title", "item1-title2"], ["uuid", "18d12e5c-e9b9-4eaa-b325-8d6c480313f3"]]
D, [2016-02-12T01:55:14.501778 #96236] DEBUG -- :    (0.4ms)  COMMIT
D, [2016-02-12T01:55:14.503960 #96236] DEBUG -- :    (0.1ms)  BEGIN
D, [2016-02-12T01:55:14.512227 #96236] DEBUG -- :   ValidatingItem Exists (0.4ms)  SELECT  1 AS one FROM "items" WHERE "items"."uuid" = $1 LIMIT $2  [["uuid", "b0db8b7c-291e-4206-a819-435428d4e7a8"], ["LIMIT", 1]]
D, [2016-02-12T01:55:14.513066 #96236] DEBUG -- :   SQL (0.3ms)  INSERT INTO "items" ("uuid", "title") VALUES ($1, $2) RETURNING "uuid"  [["uuid", "b0db8b7c-291e-4206-a819-435428d4e7a8"], ["title", "item2"]]
D, [2016-02-12T01:55:14.513550 #96236] DEBUG -- :    (0.3ms)  COMMIT
D, [2016-02-12T01:55:14.513746 #96236] DEBUG -- :    (0.1ms)  BEGIN
D, [2016-02-12T01:55:14.515572 #96236] DEBUG -- :   ValidatingItem Exists (1.0ms)  SELECT  1 AS one FROM "items" WHERE "items"."uuid" = $1 LIMIT $2  [["uuid", "b0db8b7c-291e-4206-a819-435428d4e7a8"], ["LIMIT", 1]]
D, [2016-02-12T01:55:14.532580 #96236] DEBUG -- :    (0.2ms)  ROLLBACK
F

Finished in 0.045453s, 22.0008 runs/s, 88.0030 assertions/s.

  1) Failure:
BugTest#test_update [report.rb:51]:
Expected #<ActiveModel::Errors:0x007fc4854b2458 @base=#<ValidatingItem uuid: "b0db8b7c-291e-4206-a819-435428d4e7a8", title: "item2-title2">, @messages={:uuid=>["has already been taken"]}, @details={:uuid=>[{:error=>:taken, :value=>"b0db8b7c-291e-4206-a819-435428d4e7a8"}]}> to be empty.

1 runs, 4 assertions, 1 failures, 0 errors, 0 skips
```
```

## What you have

- `/testbed/repo` is a git clone of `rails/rails` truncated just after the regression was
  reported.  `HEAD` is `737b718ea0c88d3f6c139343f957f386e06fffc9` and the full history behind it is present.
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
