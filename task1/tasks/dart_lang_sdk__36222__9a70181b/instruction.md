# Locate the commit that introduced this regression

A regression was reported against `dart-lang/sdk`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
dart2js not setting default function field

I have the following program:

```dart
typedef int BinaryFunc(int x, int y);

class A {
  const A({this.foo = A.defaultFoo});

  static int defaultFoo(int x, int y) {
    return x + y;
  }

  final BinaryFunc foo;
}

class B<T> {
  T get item => _item;
  T _item;
}

class C extends B<A> {
  bar() {
    print(item.foo(1, 2));
  }
}

class Box {
  final B<Object> b;
  Box(B<Object> b) : this.b = b;

  update(Object o) {
    b._item = o;
  }
}

main() {
  var c = C();
  var box1 = Box(c);

  var b = B<int>();
  var box2 = Box(b);

  box2.update(3);
  box1.update(A());

  c.bar();
}
```



dart2js emits this code for the class A:

```
  T.A.prototype = {
    foo$2: function(arg0, arg1) {
      return this.foo.call$2(arg0, arg1);
    }
  };
```

but it never sets `this.foo` so when `c.bar()` is run, it crashes with:

 ```
TypeError: Cannot read property 'call$2' of undefined
          throw e;
          ^
TypeError: Cannot read property 'call$2' of undefined
    at A.foo$2 (out.js:1464:23)
    at main (out.js:1221:33)
    at action (/usr/local/google/home/het/Projects/dart/sdk/sdk/lib/_internal/js_runtime/lib/preambles/d8.js:275:31)
    at eventLoop (/usr/local/google/home/het/Projects/dart/sdk/sdk/lib/_internal/js_runtime/lib/preambles/d8.js:258:9)
    at self.dartMainRunner (/usr/local/google/home/het/Projects/dart/sdk/sdk/lib/_internal/js_runtime/lib/preambles/d8.js:276:5)
    at out.js:1534:7
    at out.js:1520:7
    at dartProgram (out.js:1531:5)
    at out.js:1538:3
```
```

## What you have

- `/testbed/repo` is a git clone of `dart-lang/sdk` truncated just after the regression was
  reported.  `HEAD` is `208f8b5441206e562b9c8dd3dfc13015cd4fdef5` and the full history behind it is present.
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
