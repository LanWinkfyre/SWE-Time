# Locate the commit that introduced this regression

A regression was reported against `doxygen/doxygen`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
status RESOLVED severity *major* in component *documentation* for *---*
Reported in version *1.8.6* on platform *Other*
Assigned to: Dimitri van Heesch

On 2014-01-17 21:21:40 +0000, Reece H. Dunn wrote:

> For the standard Doxyfile and the code:
> 
> -----
> namespace cainteoir { namespace rdf
> {
> 	struct uri {};
> 
> 	class literal
> 	{
> 	public:
> 		uri type;
> 
> 		literal();
> 
> 		template<typename T>
> 		literal(const T &aValue);
> 
> 		template<typename T>
> 		literal(const T &aValue, const std::string &aLanguage);
> 
> 		template<typename T>
> 		literal(const T &aValue, const uri &aType);
> 	};
> }}
> -----
> 
> given either:
> 
>     /**
>     \fn    cainteoir::rdf::literal::literal(const T &aValue, const cainteoir::rdf::uri &aType)
>     \brief Create a datatype literal resource.
>     */
> 
> or:
> 
>     /**
>     \fn    cainteoir::rdf::literal::literal(const T &aValue, const uri &aType)
>     \brief Create a datatype literal resource.
>     */
> 
> the following warning is generated:
> 
> -----
> warning: no matching class member found for 
>   cainteoir::rdf::literal::literal(const T &aValue, const cainteoir::rdf::uri &aType)
> Possible candidates:
>   cainteoir::rdf::literal::literal()
>   'template < T >
>   cainteoir::rdf::literal::literal(const T &aValue)
>   'template < T >
>   cainteoir::rdf::literal::literal(const T &aValue, const std::string &aLanguage)
>   'template < T >
>   cainteoir::rdf::literal::literal(const T &aValue, const uri &aType)
> -----
> 
> This warning is not present in 1.8.6.
> 
> NOTE: Removing the line:
> 
>     uri type;
> 
> makes the following documentation work:
> 
> -----
>     /**
>     \fn    cainteoir::rdf::literal::literal(const T &aValue, const uri &aType)
>     \brief Create a datatype literal resource.
>     */
> -----

On 2014-01-17 21:33:18 +0000, Reece H. Dunn wrote:

> I have run a bisect which points to:
> 
> -----



> -----

On 2014-02-15 18:21:19 +0000, Dimitri van Heesch wrote:

> Confirmed. 

On 2014-04-21 10:09:17 +0000, Dimitri van Heesch wrote:


> doxygen version 1.8.7. Please verify if this is indeed the case. Reopen the
> bug if you think it is not fixed and please include any additional information 
> that you think can be relevant (preferrably in the form of a self-contained example).
```

## What you have

- `/testbed/repo` is a git clone of `doxygen/doxygen` truncated just after the regression was
  reported.  `HEAD` is `154e877cc2e8b10091d7e0068b6f6d5793cd29f3` and the full history behind it is present.
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
