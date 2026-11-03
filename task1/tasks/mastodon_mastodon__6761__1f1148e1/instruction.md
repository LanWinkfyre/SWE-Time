# Locate the commit that introduced this regression

A regression was reported against `mastodon/mastodon`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Attempting to connect to IPv6 address on IPv4-only host 

This is with 2.3.1rc2, but I believe the issue started earlier.

```
2018-03-12T13:21:45.094Z 86844 TID-a3oqxw ActivityPub::ProcessingWorker JID-d54802549aadb871df136517 INFO: start
2018-03-12T13:21:45.161Z 86844 TID-a3oqxw ActivityPub::ProcessingWorker JID-d54802549aadb871df136517 INFO: fail: 0.067 sec
2018-03-12T13:21:45.161Z 86844 TID-a3oqxw WARN: {"context":"Job raised exception","job":{"class":"ActivityPub::ProcessingWorker","args":[36,"{\"@context\":[\"https://www.w3.org/ns/activitystreams\",\"https://w3id.org/security/v1\",{\"manuallyApprovesFollowers\":\"as:manuallyApprovesFollowers\",\"sensitive\":\"as:sensitive\",\"movedTo\":\"as:movedTo\",\"Hashtag\":\"as:Hashtag\",\"ostatus\":\"http://ostatus.org#\",\"atomUri\":\"ostatus:atomUri\",\"inReplyToAtomUri\":\"ostatus:inReplyToAtomUri\",\"conversation\":\"ostatus:conversation\",\"toot\":\"http://joinmastodon.org/ns#\",\"Emoji\":\"toot:Emoji\",\"focalPoint\":{\"@container\":\"@list\",\"@id\":\"toot:focalPoint\"},\"featured\":\"toot:featured\"}],\"id\":\"https://mastodon.social/users/Gargron/statuses/99670053839562591/activity\",\"type\":\"Announce\",\"actor\":\"https://mastodon.social/users/Gargron\",\"published\":\"2018-03-12T08:45:27Z\",\"to\":[\"https://www.w3.org/ns/activitystreams#Public\"],\"cc\":[\"https://mastodon.social/users/Noa89\",\"https://mastodon.social/users/Gargron/followers\"],\"object\":\"https://mastodon.social/users/Noa89/statuses/99668292355953925\",\"atomUri\":\"https://mastodon.social/users/Gargron/statuses/99670053839562591/activity\",\"signature\":{\"type\":\"RsaSignature2017\",\"creator\":\"https://mastodon.social/users/Gargron#main-key\",\"created\":\"2018-03-12T08:45:30Z\",\"signatureValue\":\"PxWbVG2+8ALQMLnPJqLiCfSOd+FGFb2O3EhwKv13z5Z/TPHOwYRb4ghCprUzeWLXigukCIDjseenBXzb4xA//UzErs594y54culgoha0mrL+gvnkg4QfzJ2p32kReHzK40OEvFiZFoUV5UBhsHvqUhx5s2b34l68VKHPqMxk01jJoA5tr2LphKxQnQHPjtpIo/MKKynlJCtLxxmCunK1z30CEEwzYyqkY9Z4txRmxIpoHsygAt6GuukrX/R6JntzUTcOhBw2648Ny+0Mj5beSIk2GPG7JvlBL2Z3flzB7ts6oHDSJVxtcfqU7yxTARyZYF/GbH3VjxKk9rujw5MUhQ==\"}}"],"retry":true,"queue":"default","backtrace":true,"jid":"d54802549aadb871df136517","created_at":1520844342.6147585,"enqueued_at":1520860905.0932858,"error_message":"failed to connect: No route to host - connect(2) for \"2001:bc8:3890:a100::1\" port 443 on https://mastodon.social/users/Noa89/statuses/99668292355953925","error_class":"HTTP::ConnectionError","failed_at":1520844342.7385914,"retry_count":9,"error_backtrace":["/usr/local/www/mastodon/app/lib/request.rb:99:in `initialize'"],"retried_at":1520854242.3667173},"jobstr":"{\"class\":\"ActivityPub::ProcessingWorker\",\"args\":[36,\"{\\\"@context\\\":[\\\"https://www.w3.org/ns/activitystreams\\\",\\\"https://w3id.org/security/v1\\\",{\\\"manuallyApprovesFollowers\\\":\\\"as:manuallyApprovesFollowers\\\",\\\"sensitive\\\":\\\"as:sensitive\\\",\\\"movedTo\\\":\\\"as:movedTo\\\",\\\"Hashtag\\\":\\\"as:Hashtag\\\",\\\"ostatus\\\":\\\"http://ostatus.org#\\\",\\\"atomUri\\\":\\\"ostatus:atomUri\\\",\\\"inReplyToAtomUri\\\":\\\"ostatus:inReplyToAtomUri\\\",\\\"conversation\\\":\\\"ostatus:conversation\\\",\\\"toot\\\":\\\"http://joinmastodon.org/ns#\\\",\\\"Emoji\\\":\\\"toot:Emoji\\\",\\\"focalPoint\\\":{\\\"@container\\\":\\\"@list\\\",\\\"@id\\\":\\\"toot:focalPoint\\\"},\\\"featured\\\":\\\"toot:featured\\\"}],\\\"id\\\":\\\"https://mastodon.social/users/Gargron/statuses/99670053839562591/activity\\\",\\\"type\\\":\\\"Announce\\\",\\\"actor\\\":\\\"https://mastodon.social/users/Gargron\\\",\\\"published\\\":\\\"2018-03-12T08:45:27Z\\\",\\\"to\\\":[\\\"https://www.w3.org/ns/activitystreams#Public\\\"],\\\"cc\\\":[\\\"https://mastodon.social/users/Noa89\\\",\\\"https://mastodon.social/users/Gargron/followers\\\"],\\\"object\\\":\\\"https://mastodon.social/users/Noa89/statuses/99668292355953925\\\",\\\"atomUri\\\":\\\"https://mastodon.social/users/Gargron/statuses/99670053839562591/activity\\\",\\\"signature\\\":{\\\"type\\\":\\\"RsaSignature2017\\\",\\\"creator\\\":\\\"https://mastodon.social/users/Gargron#main-key\\\",\\\"created\\\":\\\"2018-03-12T08:45:30Z\\\",\\\"signatureValue\\\":\\\"PxWbVG2+8ALQMLnPJqLiCfSOd+FGFb2O3EhwKv13z5Z/TPHOwYRb4ghCprUzeWLXigukCIDjseenBXzb4xA//UzErs594y54culgoha0mrL+gvnkg4QfzJ2p32kReHzK40OEvFiZFoUV5UBhsHvqUhx5s2b34l68VKHPqMxk01jJoA5tr2LphKxQnQHPjtpIo/MKKynlJCtLxxmCunK1z30CEEwzYyqkY9Z4txRmxIpoHsygAt6GuukrX/R6JntzUTcOhBw2648Ny+0Mj5beSIk2GPG7JvlBL2Z3flzB7ts6oHDSJVxtcfqU7yxTARyZYF/GbH3VjxKk9rujw5MUhQ==\\\"}}\"],\"retry\":true,\"queue\":\"default\",\"backtrace\":true,\"jid\":\"d54802549aadb871df136517\",\"created_at\":1520844342.6147585,\"enqueued_at\":1520860905.0932858,\"error_message\":\"failed to connect: No route to host - connect(2) for \\\"2001:bc8:3890:a100::1\\\" port 443 on https://mastodon.social/users/Noa89/statuses/99668292355953925\",\"error_class\":\"HTTP::ConnectionError\",\"failed_at\":1520844342.7385914,\"retry_count\":9,\"error_backtrace\":[\"/usr/local/www/mastodon/app/lib/request.rb:99:in `initialize'\"],\"retried_at\":1520854242.3667173}"}
2018-03-12T13:21:45.161Z 86844 TID-a3oqxw WARN: HTTP::ConnectionError: failed to connect: No route to host - connect(2) for "2001:bc8:3890:a100::1" port 443 on https://mastodon.social/users/Noa89/statuses/99668292355953925
2018-03-12T13:21:45.161Z 86844 TID-a3oqxw WARN: /usr/local/www/mastodon/app/lib/request.rb:99:in `initialize'

```

@nightpool Well, is it any worse than it was pre-2.3?  

A cache would probably do the trick.  I thought about finding some way to get the current retry count into there, to use that as the index into the Addrinfo array, but the ordering of addresses is not necessarily going to be the same on each call to getaddrinfo.
```

## What you have

- `/testbed/repo` is a git clone of `mastodon/mastodon` truncated just after the regression was
  reported.  `HEAD` is `f5f165a5ebad5493a0d127c89b92876ffb75b0ef` and the full history behind it is present.
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
