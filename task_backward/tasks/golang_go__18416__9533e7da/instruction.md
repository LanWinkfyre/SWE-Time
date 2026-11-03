# Locate the commit that introduced this regression

A regression was reported against `golang/go`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
runtime: Windows: pprof output is broken in cgo packages for go test -cpuprofile

Old issue: #16891

I'm concerned that even with embedded symbols in 1.8, this will still be an issue.

Please answer these questions before submitting your issue. Thanks!
1. What version of Go are you using (`go version`)?
   `1.7 windows/386`
2. What operating system and processor architecture are you using (`go env`)?
   Windows, 386
3. What did you do?
   If possible, provide a recipe for reproducing the error.
   A complete runnable program is good.
   A link on play.golang.org is best.  
   run `go test` on a package with the `-cpuprofile` flag.
4. What did you expect to see?  
   Using output from 1.6.3, I get the following result from `pprof top10`:

```
(pprof) top10
2470ms of 2880ms total (85.76%)
Dropped 61 nodes (cum <= 14.40ms)
Showing top 10 nodes out of 91 (cum >= 40ms)
      flat  flat%   sum%        cum   cum%
    1440ms 50.00% 50.00%     1720ms 59.72%  <redacted>
     540ms 18.75% 68.75%      540ms 18.75%  runtime.cgocall
     210ms  7.29% 76.04%      210ms  7.29%  runtime.osyield
      50ms  1.74% 77.78%      190ms  6.60%  <redacted>
      50ms  1.74% 79.51%      100ms  3.47%  runtime.mallocgc
      40ms  1.39% 80.90%       40ms  1.39%  runtime.heapBitsForObject
      40ms  1.39% 82.29%       40ms  1.39%  runtime.heapBitsSetType
      40ms  1.39% 83.68%       80ms  2.78%  runtime.mapaccess2
      30ms  1.04% 84.72%       30ms  1.04%  runtime.scanobject
      30ms  1.04% 85.76%       40ms  1.39%  runtime.typedmemmove
```
1. What did you see instead?  
   Using output from 1.7, I get the following result from `pprof top10`

```
(pprof) top10
2.87s of 2.87s total (  100%)
      flat  flat%   sum%        cum   cum%
     2.87s   100%   100%      2.87s   100%  [traffic.test.exe]
```

The issue seems to be related to use of the `github.com/google/gopacket/pcap` package, which binds to `libpcap` via CGo

I tested with a bare CGo sample, and also a control.

# Control results:
```
$ go tool pprof cgo_17_bug_control.test.exe cpu.prof
Entering interactive mode (type "help" for commands)
(pprof) top10
1650ms of 2040ms total (80.88%)
Dropped 4 nodes (cum <= 10.20ms)
Showing top 10 nodes out of 27 (cum >= 50ms)
      flat  flat%   sum%        cum   cum%
     370ms 18.14% 18.14%      370ms 18.14%  sync/atomic.AddUint32
     310ms 15.20% 33.33%      310ms 15.20%  sync/atomic.CompareAndSwapUint32
     210ms 10.29% 43.63%     1360ms 66.67%  math/rand.(*lockedSource).Int63
     210ms 10.29% 53.92%      210ms 10.29%  math/rand.(*rngSource).Int63
     130ms  6.37% 60.29%      440ms 21.57%  sync.(*Mutex).Lock
     120ms  5.88% 66.18%     1480ms 72.55%  math/rand.(*Rand).Int63
     120ms  5.88% 72.06%      500ms 24.51%  sync.(*Mutex).Unlock
      70ms  3.43% 75.49%      370ms 18.14%  runtime.newstack
      60ms  2.94% 78.43%     1610ms 78.92%  scratch/cgo_17_bug_control.grind
      50ms  2.45% 80.88%       50ms  2.45%  runtime.casgstatus
(pprof)
```

# Bug results:
```
$ go tool pprof cgo_17_bug.test.exe cpu.prof
Entering interactive mode (type "help" for commands)
(pprof) top10
1.33s of 1.33s total (  100%)
      flat  flat%   sum%        cum   cum%
     1.33s   100%   100%      1.33s   100%  [cgo_17_bug.test.exe]
(pprof)

```

# Control:
## impl
```
package cgo_17_bug_control

import (
	"math/rand"
)

func grind(in int) (out int) {
	for i := 0; i < 1000; i++ {
		out += in + rand.Int()
	}
	return
}
```
## test
```
package cgo_17_bug_control

import (
	"testing"
)

func BenchmarkGrind(b *testing.B) {
	for i := 0; i < b.N; i++ {
		grind(i)
	}
}
```

# Bug
## impl
```
package cgo_17_bug

// #include <stdlib.h>
//
// unsigned int grind(unsigned int in) {
// 	unsigned int out = 0;
// 	for (int i = 0; i < 1000; i++) {
// 		out += in + rand();
// 	}
// 	return out;
// }
import "C"

func grind(in uint) (out uint) {
	return uint(C.grind(C.uint(in)))
}
```
## test
```
package cgo_17_bug

import (
	"testing"
)

func BenchmarkGrind(b *testing.B) {
	for i := 0; i < b.N; i++ {
		grind(uint(i))
	}
}
```

git-bisect result:
```

## What you have

- `/testbed/repo` is a git clone of `golang/go` truncated just after the regression was
  reported.  `HEAD` is `17190343e3db72a3f299e5a4359ae6bc3e5ed194` and the full history behind it is present.
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
