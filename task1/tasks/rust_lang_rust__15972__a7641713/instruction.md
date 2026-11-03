# Locate the commit that introduced this regression

A regression was reported against `rust-lang/rust`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
regression: code is SIGSEGVing 

Previously valid code is now behaving wrong.

``` rust
  pub fn new<'a>(cx: &'a ExtCtxt, tts: &[TokenTree]) -> Parser<'a> {
    let sess = cx.parse_sess();
    let ttsvec = tts.iter().map(|x| (*x).clone()).collect();   // [1]
    // let ttsvec = Vec::from_slice(tts);   // [2]

    debug!("tts: {}", tts);
    debug!("ttsvec: {}", ttsvec);   // [3]

    let mut reader = box lexer::new_tt_reader(
        &sess.span_diagnostic, None, ttsvec) as Box<lexer::Reader>;

    let tok0 = reader.next_token();
    let token = tok0.tok;
    let span = tok0.sp;


    Parser {
      sess: sess,
      reader: reader,

      token: token,
      span: span,

      last_token: None,
      last_span: span,
    }
  }
```

Here's the problem description: parser cannot parse input, as it's hitting wrong tokens. Apparently, a bunch of tokens in input are lost. The problem is in line [1], which works as expected when replaced by line [2]. The problem is getting even worse, as line [3] SIGSEGVs the application.

If line [1] is replaced by line [2], the code fails further, as I described in https://github.com/rust-lang/rust/issues/15931. I think it relates to the same problem (parser reports bad token which isn't even in the input!). It kind of feels like memory corruption (in rust, heh).

Digging deeper, it seems that it doesn't crash at `debug!()` point, it's just `debug!()` somehow altering the program state to allow it to crash further on. gdb can't unwind the stack for some reason, lldb shows this:

```
  * frame #0: 0x000000010235f522 libsyntax-4e7c5e5c.dylib`cell::Cell$LT$T$GT$::get::h16703176363586027891 + 66
    frame #1: 0x0000000000000018
    frame #2: 0x000000010238e6c4 libsyntax-4e7c5e5c.dylib`rc::RcBoxPtr::strong::h13767585679411698615 + 84
    frame #3: 0x00000001023f64af libsyntax-4e7c5e5c.dylib`rc::RcBoxPtr::inc_strong::h7981967022436922026 + 95
    frame #4: 0x00000001023f6436 libsyntax-4e7c5e5c.dylib`rc::Rc$LT$T$GT$.Clone::clone::h3247237882429377366 + 54
    frame #5: 0x00000001023f59bd libsyntax-4e7c5e5c.dylib`ast::TokenTree...std..clone..Clone::clone::hc9d3937696cc261fCkl + 221
    frame #6: 0x00000001024c0dd7 libsyntax-4e7c5e5c.dylib`ext::tt::transcribe::tt_next_token::he37abde7b9ce15f4Rfb + 2679
    frame #7: 0x00000001024c010d libsyntax-4e7c5e5c.dylib`parse::lexer::TtReader$LT$$x27a$GT$.Reader::next_token::hea6b26d7f0c328024mG + 93
    frame #8: 0x0000000106a65e29 libmacro_platformtree.dylib`parser::Parser$LT$$x27a$GT$::bump::hb11efbf8fc1eeb58Xnc + 249
    frame #9: 0x0000000106a5a843 libmacro_platformtree.dylib`parser::Parser$LT$$x27a$GT$::parse_platformtree::h55536ab21adb63f1CJb + 1235
```



I will try to provide a smaller test case, but so far I had no luck, all the pieces extracted from the original crate seem to work as expected.

Please advise, we're kind of stuck with this breakage.
```

## What you have

- `/testbed/repo` is a git clone of `rust-lang/rust` truncated just after the regression was
  reported.  `HEAD` is `4e388859a2e12f4019a09224d626eb07b8333651` and the full history behind it is present.
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
