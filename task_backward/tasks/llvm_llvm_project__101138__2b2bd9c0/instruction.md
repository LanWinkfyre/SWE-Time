# Locate the commit that introduced this regression

A regression was reported against `llvm/llvm-project`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
clang-format: templated operator with std::enable_if_t followed by a comment causes formatting to be different.

This is very specific. You need to have a templated operator function with `std::enable_if_t` followed by a comment.

```cpp
// Correct.
template< typename T >
constexpr std::enable_if_t< std::is_integral_v< T >, bool >
operator|( const T& left, const T& right ) noexcept
{
	return left < 3 * right;
}

// Incorrect.
template< typename T >
constexpr std::enable_if_t< std::is_integral_v< T >, bool > // This comment breaks formatting.
operator|( const T& left, const T& right ) noexcept
{
	return left < 3 * right;
}
```

This gets formatted into:

```cpp
// Correct.
template< typename T >
constexpr std::enable_if_t< std::is_integral_v< T >, bool >
operator|( const T& left, const T& right ) noexcept
{
	return left < 3 * right;
}

// Incorrect.
template< typename T >
constexpr std::enable_if_t< std::is_integral_v< T >, bool >  // This comment breaks formatting.
operator|( const T & left, const T & right ) noexcept
{
	return left < 3 * right;
}
```

There is an extra space with parameters `const T & left` but this only happens if there is a commet for  `std::enable_if_t` 



Issue is here

`Previous` here is `comment`, not `TT_TemplateCloser` (as it is without the comment), so the check fails
```

## What you have

- `/testbed/repo` is a git clone of `llvm/llvm-project` truncated just after the regression was
  reported.  `HEAD` is `fcd6bd5587cc376cd8f43b60d1c7d61fdfe0f535` and the full history behind it is present.
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
