# Locate the commit that introduced this regression

A regression was reported against `rails/rails`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Order of operations for saving nested associations has changed in Rails v7.2 with automatically_invert_plural_associations enabled

### Steps to reproduce

Full reproduction script: https://gist.github.com/ezekg/df58f1e5d1c5a3786afbe8511913836b

```ruby
class Application < Rails::Application
  config.active_record.automatically_invert_plural_associations = true
  config.active_record.has_many_inversing = true
end

class Account < ActiveRecord::Base
  has_many :packages
  has_many :releases
  has_many :artifacts
end

class Package < ActiveRecord::Base
  belongs_to :account
  has_many :releases

  validates :account, presence: true
end

class Release < ActiveRecord::Base
  belongs_to :account, default: -> { package.account }
  belongs_to :package

  validates :account, presence: true
  validates :package, presence: true

  validate do
    errors.add :package unless package.account_id == account_id
  end
end

class Artifact < ActiveRecord::Base
  belongs_to :account, default: -> { release.account }
  belongs_to :release

  validates :account, presence: true
  validates :release, presence: true

  validate do
    errors.add :release unless release.account_id == account_id
  end
end

account  = Account.new(name: "Test")
package  = Package.new(account:)
release  = Release.new(account:, package:)
artifact = Artifact.new(account:, release:)

artifact.save! # => ActiveRecord::NotNullViolation: NOT NULL constraint failed: artifacts.release_id
```

### Expected behavior

I would expect the records to be saved successfully, as they are in v7.1. With `automatically_invert_plural_associations` enabled in Rails 7.2, saving the artifact also saves its implicit associations. Before that config was introduced, saving nested has-many/collection associations was always explicit. This is fine and "correct" behavior i.r.t. associations (even if it took a few days to debug). With this change, when the artifact is saved, it cascades down to the account, and saving the account saves its implicit has-many associations as well, which results in the account's artifacts, packages and releases being saved, which seemingly results in some associations being saved out of order (I'm still digging into this so I'm not 100% on this yet).

All this results in what is ultimately a change in order of operations when saving nested associations, and this change in order of operations results in some records being saved before they're ready, or without foreign key information they should have through precedingly saved associations, resulting in validation or constraint failures.

I'd expect the records to be saved regardless of any internal change in order of operations.

### Actual behavior

I receive an error because the release's `account_id` foreign key is out of sync with its account association's primary key. This shows that a record's implicit foreign keys aren't populated until after the record is saved, even though they may be known via the association's primary key (i.e. `association_id` vs `association.id`).

This results in a validation error, causing some nested associations to not be saved (without error), causing null values in the insert query, causing a SQL constraint failure.

```rb
ActiveRecord::NotNullViolation: NOT NULL constraint failed: artifacts.release_id
```

If the null constraint on `artifacts.release_id` wasn't there, this would fail silently — inserting only an account and a half-baked artifact, skipping the "invalid" release and package altogether (I'm putting quotations there because it's not actually _invalid_ — it's just "invalid" due to the order of operations changing between v7.1 and v7.2).

If you disable `automatically_invert_plural_associations`, the test passes. It also passes on `7-1-stable`. In addition, if you update the validations to check `account.id` instead of `account_id`, the test passes.

### System configuration

**Rails version**: 7.2.0-stable branch
**Ruby version**: 3.2.2


> @ezekg Are you willing to try and bisect with your repro script to help identify the cause of the change?

_Originally posted by @zzak in https://github.com/keygen-sh/keygen-api/issues/843#issuecomment-2122202890_





And here's my `tmp/test` script:

```ruby
#!/usr/local/bin/ruby

require "pathname"

Dir["*/lib/*.rb"].each do |file|
  path = Pathname.new(file) # add local rails libs to load path

  unless $LOAD_PATH.include?(path.dirname.to_s)
    $LOAD_PATH.unshift(path.dirname.to_s)
  end
end

require "rails"
require "active_record"

pp(
  revision: `git rev-parse HEAD --quiet 2>/dev/null`.chomp,
  version: Rails.version,
)

# This connection will do for database-independent bug reports.
ActiveRecord::Base.tap do |config|
  config.establish_connection(adapter: "sqlite3", database: ":memory:")
  config.logger = Logger.new(STDOUT)
  if config.respond_to?(:automatically_invert_plural_associations)
    config.automatically_invert_plural_associations = true
  end
  config.has_many_inversing = true
end

ActiveRecord::Schema.define do
  create_table :accounts, force: true do |t|
    t.string :name, null: false
  end

  create_table :packages, force: true do |t|
    t.references :account, null: false
  end

  create_table :releases, force: true do |t|
    t.references :account, null: false
    t.references :package, null: false
  end

  create_table :artifacts, force: true do |t|
    t.references :account, null: false
    t.references :release, null: false
  end
end

class Account < ActiveRecord::Base
  has_many :packages
  has_many :releases
  has_many :artifacts
end

class Package < ActiveRecord::Base
  belongs_to :account
  has_many :releases

  validates :account, presence: true
end

class Release < ActiveRecord::Base
  belongs_to :account, default: -> { package.account }
  belongs_to :package

  validates :account, presence: true
  validates :package, presence: true

  validate do
    # Passes:
    # errors.add :package unless package.account_id == account.id

    # Fails:
    errors.add :package unless package.account_id == account_id
  end
end

class Artifact < ActiveRecord::Base
  belongs_to :account, default: -> { release.account }
  belongs_to :release

  validates :account, presence: true
  validates :release, presence: true

  validate do
    # Passes:
    # errors.add :release unless release.account_id == account.id

    # Fails:
    errors.add :release unless release.account_id == account_id
  end
end

require "minitest/autorun"
require "rack/test"

class AutomaticInverseOfTest < Minitest::Test
  def test_automatic_inverse_of
    account  = Account.new(name: "Test")
    package  = Package.new(account:)
    release  = Release.new(account:, package:)
    artifact = Artifact.new(account:, release:)

    assert_not_raised ActiveRecord::RecordInvalid do
      artifact.save!
    end
  end

  private

  def assert_not_raised(exception_class, failure_message = nil)
    yield
  rescue => e
    if e.is_a?(exception_class)
      flunk(failure_message || "An exception was not expected but was raised: #{e.inspect}")
    else
      raise
    end
  end
end
```
```

## What you have

- `/testbed/repo` is a git clone of `rails/rails` truncated just after the regression was
  reported.  `HEAD` is `d0ce794e2d9e6f40934c2467dbf057b5e2cba88c` and the full history behind it is present.
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
