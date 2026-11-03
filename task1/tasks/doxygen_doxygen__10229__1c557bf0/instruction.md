# Locate the commit that introduced this regression

A regression was reported against `doxygen/doxygen`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Documented members in unnamed and undocumented union/struct are not output

**Describe the bug**
When unnamed union or struct is undocumented but only its members are documented, these members are not output in HTML doc using 1.9.7.
And although the members are listed in treeview, there is no link target for them.

While I use 1.9.6, these members are output in HTML doc.

In the both cases, `HIDE_UNDOC_MEMBERS = YES` is configured in DoxyFile.

There is the case that unnamed union and struct itself is not documented, but want to document on its members.
In this case I have to configure `HIDE_UNDOC_MEMBERS = NO` as a workaround.
What is a best practice when dealing with unnamed union and struct?

```
class sampleClass
{
public:
    // Members are not output in "Public Attributes" with 1.9.7.
    union
    {
        //! Member1 in unnamed and uncommented union
        int union_unnamed_uncommented1;

        //! Member2 in unnamed and uncommented union
        int union_unnamed_uncommented2;
    };
```

**Expected behavior**
I would like to have outputs of unnamed union and struct if only their members are documented, but want to confirm what the behavior should ideally be.

**Screenshots**
doxygen 1.9.7 output:
![197_sampleClass](https://github.com/doxygen/doxygen/assets/79039413/53cb62b1-e446-4cb8-8075-4e5162aefbc6)

doxygen 1.9.6 output:
![196_sampleClass](https://github.com/doxygen/doxygen/assets/79039413/171e402b-e52e-4195-ab00-66520441bf23)


**To Reproduce**

Extract the attached [unnamedUnionStruct.zip](https://github.com/doxygen/doxygen/files/12328837/unnamedUnionStruct.zip) and create document.


**Version**
doxygen 1.9.7

The situation is a bit inconsistent now.
I did a bisect and got as result:


I think that either:
- the old, output, situation has to be reinstated (I think the correct situation)
- the mentioned members should not be shown in the treeview
```

## What you have

- `/testbed/repo` is a git clone of `doxygen/doxygen` truncated just after the regression was
  reported.  `HEAD` is `682b594f5b4334512dc2f3026be5c4e0d90fb6a1` and the full history behind it is present.
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
