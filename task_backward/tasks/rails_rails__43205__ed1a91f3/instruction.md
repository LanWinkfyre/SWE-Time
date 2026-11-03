# Locate the commit that introduced this regression

A regression was reported against `rails/rails`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Autoloading helpers fails initially in Rails 7.x, but succeeds on the second attempt

### Steps to reproduce

When I try loading a Rails Application in Ruby 7.0, the `app/helpers` autoload path does not appear to be working from my gems engine.

Here's the script to reproduce the issue **NOT working** under 7.0:

```ruby
require "bundler/inline"

gemfile(true) do
  source "https://rubygems.org"

  git_source(:github) { |repo| "https://github.com/#{repo}.git" }

  # Activate the gem you are reporting the issue against.
  gem "sitepress", github: "sitepress/sitepress", branch: "rails-7"
  gem "rails", github: "rails/rails", branch: "main"
end

require "sitepress/server"  # Load all the stuff needed setup the configuration below.

# Setup defaults for stand-alone Sitepress server in the current path. This
# can, and should, be over-ridden by the end-user in the `config/site.rb` file.
Sitepress.configure do |config|
  config.routes = false
  config.site = Sitepress::Site.new root_path: "."
end

# Create the module that should autoload without an issues.
require 'fileutils'
FileUtils.mkdir_p 'helpers'
File.write "helpers/foo_helper.rb", "module FooHelper; end;"

# Boot the Rails app
app = Sitepress::Server
app.initialize!

puts "Loading ::SiteController fails in Rails 7.0"
# See https://github.com/sitepress/sitepress/blob/rails-7/sitepress-rails/lib/sitepress/engine.rb#L15 for helper path configuration
# See https://github.com/sitepress/sitepress/blob/rails-7/sitepress-server/lib/sitepress/server.rb for the configuration of the Rails app this boots
p ::SiteController # This will raise an exception
```

Now for code that shows this **WORKING** under Rails 6:

```ruby
require "bundler/inline"

gemfile(true) do
  source "https://rubygems.org"

  git_source(:github) { |repo| "https://github.com/#{repo}.git" }

  # Activate the gem you are reporting the issue against.
  gem "sitepress", github: "sitepress/sitepress", branch: "rails-7"
  gem "rails"
end

require "sitepress/server"  # Load all the stuff needed setup the configuration below.

# Setup defaults for stand-alone Sitepress server in the current path. This
# can, and should, be over-ridden by the end-user in the `config/site.rb` file.
Sitepress.configure do |config|
  config.routes = false
  config.site = Sitepress::Site.new root_path: "."
end

# Create the module that should autoload without an issues.
require 'fileutils'
FileUtils.mkdir_p 'helpers'
File.write "helpers/foo_helper.rb", "module FooHelper; end;"

# Boot the Rails app
app = Sitepress::Server
app.initialize!

puts "Loading ::SiteController succeeds in Rails 6.x"
p ::SiteController # This will not raise an exception
```

Finally, in a third example under Rails 7.0, I demonstrate that this is **WORKING** when I attempt to load the constant a second time:

```ruby
require "bundler/inline"

gemfile(true) do
  source "https://rubygems.org"

  git_source(:github) { |repo| "https://github.com/#{repo}.git" }

  # Activate the gem you are reporting the issue against.
  gem "sitepress", github: "sitepress/sitepress", branch: "rails-7"
  gem "rails", github: "rails/rails", branch: "main"
end

# require "sitepress/boot"
require "sitepress/server"  # Load all the stuff needed setup the configuration below.

# Setup defaults for stand-alone Sitepress server in the current path. This
# can, and should, be over-ridden by the end-user in the `config/site.rb` file.
Sitepress.configure do |config|
  config.routes = false
  config.site = Sitepress::Site.new root_path: "."
end

# Create the module that should autoload without an issues.
require 'fileutils'
FileUtils.mkdir_p 'helpers'
File.write "helpers/foo_helper.rb", "module FooHelper; end;"

# Boot the Rails app
app = Sitepress::Server
app.initialize!

puts "Loading ::SiteController fails in Rails 7.0 on the first attempt"
begin
  p ::SiteController
rescue => e
  puts "Failed with #{e.inspect}"
end

puts "Loading ::SiteController succeeds in Rails 7.0 on the second attempt"
p ::SiteController
```

The following source files may be helpful to help diagnose the issue:
* https://github.com/sitepress/sitepress/blob/rails-7/sitepress-rails/lib/sitepress/engine.rb#L15 for helper path configuration
* https://github.com/sitepress/sitepress/blob/rails-7/sitepress-server/lib/sitepress/server.rb for the configuration of the Rails app this boots

### Expected behavior

I expect the `FooHelper` to be resolved in Rails 7.x, as it does in Rails 6.x. Here's what a succesful script run looks like from above:

```
SiteController
```

### Actual behavior

The `FooHelper` module is not resolved when Rails attempts to find it. Here's what the error looks like from the first Rails 7.x script above:



### System configuration

**Rails version**: 7.x

**Ruby version**: 3.x


I did a git bisect.
```

## What you have

- `/testbed/repo` is a git clone of `rails/rails` truncated just after the regression was
  reported.  `HEAD` is `a692e63bf4000cdeb9f230fb395c97edd3b12b99` and the full history behind it is present.
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
