# Locate the commit that introduced this regression

A regression was reported against `rails/rails`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Jbuilder is broken in a new Rails app



### Steps to reproduce

1. Create a new Rails app from latest master: `railties/exe/rails new ~/Desktop/sandbox --edge`.

   * Note that [Jbuilder](https://github.com/rails/jbuilder) is included in the default Gemfile.
   * App generation may fail on the Webpacker installation step. Finish by `cd`ing into the app and running `bundle exec bin/rails webpacker:install`.

2. Add `FeedsController` with an empty `show` action:

   ```ruby
   # app/controllers/feeds_controller.rb
   class FeedsController < ApplicationController
     def show
     end
   end
   ```

3. Add singular resource routes to `FeedsController`:

   ```ruby
   # config/routes.rb
   Rails.application.routes.draw do
     resource :feed
   end
   ```

4. Add a Jbuilder view for `feeds#show`:

   ```ruby
   # app/views/feeds/show.json.jbuilder (or app/views/feeds/show.jbuilder)
   json.foo "bar"
   ```

5. Start the development web server: `bundle exec bin/rails s`.

6. Access `/feed.json`: `curl -i http://localhost:3000/feed.json`.

### Expected result

A JSON response is returned:

```
$ curl -i http://localhost:3000/feed.json
HTTP/1.1 200 OK
...
Content-Type: application/json
...

{"foo":"bar"}
```

### Actual result

The Jbuilder template is returned verbatim in the response body:

```
$ curl -i http://localhost:3000/feed.json
HTTP/1.1 200 OK
...
Content-Type: application/json
...

json.foo "bar"
```

### Notes

In attempting to reproduce this, I sometimes get the expected result after starting the development server for the first time. Requests after stopping and restarting the development server get the actual result. Stopping Spring doesn’t help. Clearing the Bootsnap cache doesn’t help.

I’ll share an example app shortly.

Using this command line repro:

```bash
$ bin/rails runner 'puts ApplicationController.renderer.render("feeds/show", formats: :json)'
json.foo "bar"
```
```

## What you have

- `/testbed/repo` is a git clone of `rails/rails` truncated just after the regression was
  reported.  `HEAD` is `ab06682534f63257f33ad81e4c87931e36658cb7` and the full history behind it is present.
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
