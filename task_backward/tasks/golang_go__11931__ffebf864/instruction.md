# Locate the commit that introduced this regression

A regression was reported against `golang/go`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
cmd/compile: escape analysis bug involving interfaces

We started seeing this panic in our tests at ipfs.io. I didn't try go1.5beta1 but its in beta 2 and 3. (They work fine in 1.4.x)



([Full trace log](https://gist.githubusercontent.com/cryptix/c48c65f029f32925bbd0/raw/f886776739caabdc35a6723da532b5bfcdad7c50/gistfile1.txt))

It seems to come from [this](https://github.com/ipfs/go-ipfs/blob/master/p2p/peer/metrics.go#L60) map lookup but I can't figure out whats wrong with it. I wish I had a more minimal test case.


Confirmed. I see a slightly different error on OSX, but a panic non the less. The suspicious looking fault address is a side effect of the SIGSEGV handler on darwin freaking out if the fault address is higher than the 48th bit.

```
zapf(~/src/golang.org/x/crypto/ssh) % go test github.com/ipfs/go-ipfs/test/integration                                                                                   
unexpected fault address 0xb01dfacedebac1e
fatal error: fault
[signal 0xb code=0x1 addr=0xb01dfacedebac1e pc=0xc7b5]

goroutine 196 [running]:
runtime.throw(0x730e30, 0x5)
        /Users/dfc/go/src/runtime/panic.go:527 +0x96 fp=0xc8200b2cc8 sp=0xc8200b2cb0
runtime.sigpanic()
        /Users/dfc/go/src/runtime/sigpanic_unix.go:27 +0x2ba fp=0xc8200b2d18 sp=0xc8200b2cc8
runtime.mapaccess1_faststr(0x53bde0, 0xc82005b800, 0xc82057a750, 0x22, 0x20)
        /Users/dfc/go/src/runtime/hashmap_fast.go:262 +0x415 fp=0xc8200b2d78 sp=0xc8200b2d18
github.com/ipfs/go-ipfs/p2p/peer.(*metrics).LatencyEWMA(0xc82057c028, 0xc82057a750, 0x22, 0x0)
        /Users/dfc/src/github.com/ipfs/go-ipfs/p2p/peer/metrics.go:60 +0x70 fp=0xc8200b2dc0 sp=0xc8200b2d78
github.com/ipfs/go-ipfs/routing/kbucket.(*RoutingTable).Update(0xc8200e8000, 0xc82057a750, 0x22)
        /Users/dfc/src/github.com/ipfs/go-ipfs/routing/kbucket/table.go:69 +0x1f3 fp=0xc8200b2e50 sp=0xc8200b2dc0
github.com/ipfs/go-ipfs/routing/dht.(*IpfsDHT).Update(0xc82009a000, 0x19000c0, 0xc820556000, 0xc82057a750, 0x22)
        /Users/dfc/src/github.com/ipfs/go-ipfs/routing/dht/dht.go:252 +0x163 fp=0xc8200b2ed0 sp=0xc8200b2e50
github.com/ipfs/go-ipfs/routing/dht.(*netNotifiee).Connected(0xc82009a000, 0x1940308, 0xc820584000, 0x1980098, 0xc8200180c0)
        /Users/dfc/src/github.com/ipfs/go-ipfs/routing/dht/notif.go:23 +0x107 fp=0xc8200b2f48 sp=0xc8200b2ed0
github.com/ipfs/go-ipfs/p2p/net/mock.(*peernet).openConn.func1(0x19408a0, 0xc82009a000)
        /Users/dfc/src/github.com/ipfs/go-ipfs/p2p/net/mock/mock_peernet.go:172 +0x94 fp=0xc8200b2fb0 sp=0xc8200b2f48
runtime.goexit()
        /Users/dfc/go/src/runtime/asm_amd64.s:1696 +0x1 fp=0xc8200b2fb8 sp=0xc8200b2fb0
created by github.com/ipfs/go-ipfs/p2p/net/mock.(*peernet).notifyAll
        /Users/dfc/src/github.com/ipfs/go-ipfs/p2p/net/mock/mock_peernet.go:401 +0xc2
```

The same code passes with the race detector under 1.4.2 on the same host so for the moment it is possible that this is memory corruption unrelated to a data race.

/cc @rsc @randall77
```

## What you have

- `/testbed/repo` is a git clone of `golang/go` truncated just after the regression was
  reported.  `HEAD` is `b7205b92c0a5ae985a3530dc8ad17e7d3a7a807d` and the full history behind it is present.
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
