# Locate the commit that introduced this regression

A regression was reported against `dotnet/runtime`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
System.IO.Packaging: ValidatedPartUri  violates Equals/GetHashCode contract vs System.Uri, breaking hash-based Uri collections

### Description

 These overrides violate the `object.Equals`/`GetHashCode` contract when a `ValidatedPartUri` is compared against, or co-located in a hash collection with, a plain `System.Uri` of the same value:

- `Equals` is **asymmetric**: `validatedPartUri.Equals(plainUri)` is `false` (the override guards with `obj is ValidatedPartUri`), but `plainUri.Equals(validatedPartUri)` is `true` (`System.Uri`'s value equality).
- `GetHashCode` is **inconsistent** with a value-equal plain `System.Uri`: the override returns `StringComparer.OrdinalIgnoreCase.GetHashCode(NormalizedPartUriString)`, which differs from `System.Uri.GetHashCode()` for the same URI.



### Reproduction

```csharp
using System;
using System.IO.Packaging;

Uri plain     = new Uri("/foo.xml", UriKind.Relative);   // System.Uri
Uri validated = PackUriHelper.CreatePartUri(plain);      // PackUriHelper.ValidatedPartUri : Uri

// This is how HashSet<Uri> / Dictionary<Uri,_> compare keys: the virtual object.Equals.
object a = validated, b = plain;
Console.WriteLine(a.Equals(b));   // False  -> ValidatedPartUri.Equals: `obj is ValidatedPartUri` is false
Console.WriteLine(b.Equals(a));   // True   -> System.Uri.Equals(object): value-equal ("/foo.xml")

Console.WriteLine(validated.GetHashCode() == plain.GetHashCode()); // False
```

Output:

```
False
True
False
```

> Note: if written as `validated.Equals(plain)` (both statically typed `Uri`), C# binds to the separate, non-overridden `System.Uri.Equals(Uri)` value-equality overload, which returns `True` and hides the asymmetry. You must go through `object.Equals` (as above) to observe what hash-based collections actually do.

### Impact

`System.Uri` equality/hashing is value-based and case-sensitive for relative URIs. Consumers that store part URIs in `HashSet<Uri>` / `Dictionary<Uri,_>` and **mix `ValidatedPartUri` (e.g. from `PackagePart.Uri`) with plain `System.Uri` (e.g. from `PackUriHelper.ResolvePartUri`, which returns `new Uri(resolvedUri.AbsolutePath, UriKind.Relative)`)** now get wrong lookup results, because the two types no longer hash to the same bucket and their `Equals` is asymmetric.

This is a real, observable regression in the **Open XML SDK** (`dotnet/open-xml-sdk`). 

1. `TestDataReferenceRelationshipsAreClonedCorrectly` — `ArgumentException: An item with the same key has already been added. Key: /PPT/SLIDES/SLIDE1.XML`. Its `PartUriHelper._reservedUri` (`Dictionary<Uri,int>`) is populated with keys of differing case/normalization (one path adds the original-case plain `Uri` from `ResolvePartUri`, another adds the upper-cased normalized `ValidatedPartUri`). 
2. `CanRoundTripWordprocessingDocumentWithAltChunks` and
3. `CanTransformWordprocessingDocumentWithAltChunksToFlatOpc` — `XmlException: Data at the root level is invalid`. `FlatOpcExtensions` builds a `HashSet<Uri>` of AltChunk part URIs from `ResolvePartUri` (plain `System.Uri`) and queries it with `part.Uri` (`ValidatedPartUri`). 

While the immediate fixes belong in Open XML SDK (key by normalized part-name strings rather than relying on `Uri` default equality), the underlying behavioral break is in this library and is likely to affect other consumers that treat part URIs as `Uri` keys.

### Suggested directions

- Reconsider whether `ValidatedPartUri` should override `Equals(object)`/`GetHashCode` at all given it derives from `System.Uri` and is routinely mixed with plain `System.Uri` instances in public scenarios.
- If case-insensitive part-name semantics are required, ensure the equality is **symmetric** and that `GetHashCode` stays **consistent with a value-equal `System.Uri`** (e.g. don't key off `NormalizedPartUriString` in a way that diverges from `System.Uri.GetHashCode`), or avoid handing `ValidatedPartUri` out where a plain `System.Uri` is expected.
- At minimum, document this as a breaking change for 11.0 so downstream consumers (Open XML SDK and others) can adjust their URI collections.

### Regression




### Configuration

- .NET 11 (`main`); `System.IO.Packaging` is out-of-band.

> [!NOTE]
> This issue was authored with assistance from GitHub Copilot (AI-generated content), reviewed by @rzikm.
```

## What you have

- `/testbed/repo` is a git clone of `dotnet/runtime` truncated just after the regression was
  reported.  `HEAD` is `b5d84ecbf4d92d63329e63025099a4a063a65285` and the full history behind it is present.
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
