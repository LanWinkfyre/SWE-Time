# Locate the commit that introduced this regression

A regression was reported against `doxygen/doxygen`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Trying to document function named "i_calloc()" produces unwanted links

When trying to document the following function:

```
/**
 * @ingroup module_index_allocators
 * @brief The default allocator.
 *
 * Allocates `(nmemb x size)` bytes of storage and initializes it to all bits zero.
 *
 * @param[in] nmemb The number of members to allocate.
 * @param[in] size The size of each member in bytes.
 * @return On success, a pointer to the allocated space. Otherwise a null pointer.
 */
void* i_calloc(std::size_t nmemb, std::size_t size);
```

Doxygen produces false links that point to this function.  
Nearly all function arguments as well as C++ keywords are mapped to this.  
Looks like doxygen creates a bunch of these:
```
<a class="el" href="group__module__index__allocators.html#ga14c058754ff52f9070c24631c36c91cd">const</a>
```
This happens only for `i_calloc()` and NOT for `i_malloc()`.
It also does NOT happen for the templated version of `i_calloc()`:
```
template <typename T>
T* i_calloc(std::size_t nmemb);
```
```

## What you have

- `/testbed/repo` is a git clone of `doxygen/doxygen` truncated just after the regression was
  reported.  `HEAD` is `195cfeb27bee80dcba54e84b4494b8176ce9be00` and the full history behind it is present.
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
