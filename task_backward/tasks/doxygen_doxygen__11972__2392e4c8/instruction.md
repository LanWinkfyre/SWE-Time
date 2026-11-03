# Locate the commit that introduced this regression

A regression was reported against `doxygen/doxygen`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Incorrect indentation for custom command following list

**Describe the bug**
HTML output doesn't seem to close a markdown list correctly if followed by a custom command 

**Screenshots**

If a list is followed by a built-in command (here "@&NoBreak;attention") the text is left-aligned after the list.
<img width="188" height="285" alt="Image" src="https://github.com/user-attachments/assets/c78c23a9-6568-43aa-a94b-5babcaff24a3" />

but for a custom command (from ALIAS="...") the text has been folded into the list

<img width="204" height="255" alt="Image" src="https://github.com/user-attachments/assets/172b2123-e9d8-497d-a4bf-6d1dee0eaa55" />

would expect it to look like this

<img width="181" height="264" alt="Image" src="https://github.com/user-attachments/assets/8eb2416e-0f4a-4c70-87f5-21d363e555ee" />

**To Reproduce**

```C

/** @file */


/**
 * @brief Some text in a title.
 * 
 * - an item
 * - another
 * 
 * @attention This or that
 * 
 */
void afunc() {}

/**
 * @brief Some text in a title.
 * 
 * - an item
 * - another
 * 
 * @custom This or that
 * 
 */
void bfunc() {}

/**
 * @brief Some text in a title.
 * 
 * - an item
 * - another
 * .
 * @custom This or that
 * 
 */
void cfunc() {}
```

Doxyfile

```
#

ALIASES                = "custom=\xrefitem custom \"Custom\" \"Custom Page\" "

```

**Workaround**

Terminate the list with `.` - see the doc comment for `cfunc`.

**Expected behavior**
Would expect the Custom text to be left aligned.

**Version**
Windows 11, x64 doxygen 1.16.1

**Additional context**

In the HTML you can see the `<dl>` gets tucked inside the last `<li>`

```html
<p>Some text in a title. </p>
<ul>
<li>an item</li>
<li><p class="startli">another</p>
<dl class="custom"><dt><b><a class="el" href="custom.html#_custom000001">Custom</a></b></dt><dd>This or that</dd></dl>
</li>
</ul>
```

compare the builtin version

```html
<p>Some text in a title. </p>
<ul>
<li>an item</li>
<li>another</li>
</ul>
<dl class="section attention"><dt>Attention</dt><dd>This or that </dd></dl>
```


A bisect gave:
```

## What you have

- `/testbed/repo` is a git clone of `doxygen/doxygen` truncated just after the regression was
  reported.  `HEAD` is `e02b26a8101beafedebc953503fd208931f4e38d` and the full history behind it is present.
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
