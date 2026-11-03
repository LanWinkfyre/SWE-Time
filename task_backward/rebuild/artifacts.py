"""Changelog-style files that are commit messages stored as tracked content.

Hiding commit messages at the git-plumbing layer turned out to be worthless for
repositories that keep a changelog in the tree.  In the first hard-batch round the
only solved case was solved by reading

    Misc/NEWS.d/next/Library/2019-01-09-23-43-08.bpo-35493.kEcRGE.rst

which names the upstream issue in the filename alone, and another agent ran
``git log -- RELEASES.md``.  Both are ordinary tracked files, so every rule about
``git log`` formats leaves them fully readable.

Rewriting history to drop them would change the SHAs that are the answers, so these
files are instead made invisible: absent from the working tree via sparse-checkout,
filtered out of git's output by the shim next to this module, and refused outright by
the guard hook.  The commit graph and every SHA stay exactly as upstream.

Matching is deliberately narrow.  A stem-plus-extension test keeps a source file
named ``changes.c`` readable while catching ``CHANGES``, ``CHANGES.rst`` and friends.
"""

from __future__ import annotations

import fnmatch
import re
from collections.abc import Iterable

# Basename stems that mean "human-readable log of what changed".
STEMS = frozenset(
    {
        "NEWS",
        "CHANGELOG",
        "CHANGELOGS",
        "CHANGES",
        "CHANGE",
        "CHANGELOG-PRE",
        "RELEASE",
        "RELEASES",
        "RELEASENOTES",
        "RELEASE-NOTES",
        "RELEASE_NOTES",
        "RELEASENOTES-PRE",
        "RELNOTES",
        "HISTORY",
        "WHATSNEW",
        "WHATS-NEW",
        "WHATS_NEW",
        "UPGRADING",
        "UPGRADE-NOTES",
    }
)

# Extensions a changelog is plausibly written in.  An empty extension counts, which is
# how bare ``NEWS`` and ``CHANGELOG`` are caught.
DOC_SUFFIXES = frozenset({"", ".MD", ".RST", ".TXT", ".HTML", ".ADOC", ".ORG", ".IN", ".D", ".OLD", ".1"})

# Trailing digits and separators keep versioned changelogs such as ``NEWS2x.txt`` and
# ``CHANGELOG-1.0.md`` in scope.  The extension check below is what keeps a source file
# named ``changes.c`` out of it, so widening the stem here is safe.
#
# ``ARCHIVE`` is a word rather than a version, so the digit-and-separator tail cannot reach
# it.  node retires old entries to ``doc/CHANGELOG.ARCHIVE.md`` and grafana to
# ``.changelog-archive/``; an archived changelog indexes exactly the same commits as a
# current one, only for older releases, which is the half of history a cutoff leaves visible.
_STEM_ALTERNATION = "|".join(sorted(map(re.escape, STEMS), key=len, reverse=True))
STEM_RE = re.compile("(?:" + _STEM_ALTERNATION + r")[0-9X_.-]*(?:ARCHIVES?[0-9X_.-]*)?")

# A release-notes page under a documentation root whose name carries a dotted version:
# flutter's ``docs/unsorted_wiki/Release-Notes-Flutter-1.9.1.md`` and
# ``Release-Notes---Changes-in-1.2.1.md``, each a per-version list of the PRs that landed.
# The stem alternation cannot reach those on its own -- ``---CHANGES-IN-`` is neither digits
# nor separators -- and the dotted version is what separates them from a prose page about
# releasing, such as a ``Release-Notes-Template.md``.
#
# The upgrade stems are excluded.  A migration guide names the versions it moves between --
# flutter's ``docs/platforms/android/Upgrading-Flutter-projects-to-Gradle-4.1-and-Android-
# Studio-Gradle-plugin-3.0.1.md`` -- and says nothing about which commit changed a behaviour,
# so including them would hide documentation for no gain.
_RELEASE_PAGE_STEMS = STEMS - {"UPGRADING", "UPGRADE-NOTES"}
DOC_RELEASE_STEM_RE = re.compile(
    "(?:" + "|".join(sorted(map(re.escape, _RELEASE_PAGE_STEMS), key=len, reverse=True))
    + r")[0-9A-Z_.-]*?[0-9]+\.[0-9]+[0-9A-Z_.-]*")

# The same page with the version written *first*: rails keeps
# ``guides/source/5_2_release_notes.md``, one per release, and links each entry to the commit
# that made it -- step (4) found a gold SHA in one of them, all forty characters of it, in a
# visible file.  Every stem rule above requires the changelog word at the start of the stem
# and ``guides`` is not a documentation root, so the whole family (19 pages) was readable.
#
# A leading version is the entire rule, and no documentation root is required, because the
# leading digit is already the discriminator: across both trees of all 25 repositories the
# only basenames carrying a release word after a digit-and-separator prefix are these.
# Requiring it is what keeps the near misses visible -- ClickHouse's
# ``docs/changelog_entry_guidelines.md``, llvm's ``clang/docs/ReleaseNotesTemplate.txt``,
# elasticsearch's ``ReleaseNotesGeneratorTest.index.md``, rust's ``changelog_update.md``:
# prose *about* changelogs, none of which names a commit.
VERSIONED_RELEASE_STEM_RE = re.compile(
    r"[0-9][0-9X_.-]*(?:"
    + "|".join(sorted(map(re.escape, _RELEASE_PAGE_STEMS), key=len, reverse=True))
    + r")[0-9X_.-]*")



# Whole directories of changelog fragments.  ``*`` crosses "/" under fnmatch, which is
# what we want: every fragment below the directory is hidden.
#
# ``api/next`` is go's: the files below it are the API promises a release adds, one per
# proposal, named by issue number.  It is not under a documentation root and ``api`` alone
# is far too common, so the pair has to be spelled out.
DIRECTORY_GLOBS = (
    "MISC/NEWS.D/*",
    "*/MISC/NEWS.D/*",
    "WHATSNEW/*",
    "*/WHATSNEW/*",
    "CHANGELOG.D/*",
    "*/CHANGELOG.D/*",
    "CHANGES.D/*",
    "*/CHANGES.D/*",
    "NEWSFRAGMENTS/*",
    "*/NEWSFRAGMENTS/*",
    "API/NEXT/*",
    "*/API/NEXT/*",
    # A repository's own collection of changelogs, at the root: kubernetes keeps
    # ``CHANGELOG/CHANGELOG-1.30.md`` and an index ``CHANGELOG/README.md``, numpy keeps
    # towncrier fragments in ``changelog/13578.deprecation.rst``, grafana retires old entries
    # to ``.changelog-archive/``.  Top level only, and deliberately: the same name nested
    # somewhere is the *tooling* that builds a changelog -- ClickHouse's ``utils/changelog/``
    # holds python, grafana's ``.github/actions/changelog/`` an action -- and hiding a
    # generator hides source, which is a judgement for a human rather than for this table.
    "CHANGELOG/*",
    "CHANGELOG-ARCHIVE/*",
    ".CHANGELOG-ARCHIVE/*",
    # Debian packaging keeps the release history of the packaged software in
    # ``debian/changelog``, spelled lower-case by policy, which is what puts it past the
    # capitalization convention the extensionless branch of ``is_hidden`` relies on.  Found
    # in julia, node (``tools/gflags/``) and dotnet, so the depth has to be free.
    "DEBIAN/CHANGELOG",
    "*/DEBIAN/CHANGELOG",
)

# Documentation roots.  A changelog directory below one of these is release notes whose
# own filenames say nothing -- ``doc/source/release/1.13.0-notes.rst``,
# ``docs/releases/1.11.txt`` -- so the directory is the only thing that identifies them.
DOC_ROOTS = frozenset({"DOC", "DOCS", "DOCUMENTATION"})

# Fragment directories that are recognizable from the directory name alone, but only
# unambiguous under a documentation root.  go keeps its release notes as
# ``doc/next/6-stdlib/99-minor/os/12345.md``; ``next`` is an ordinary word and hiding it
# anywhere else would take source directories with it.
DOC_FRAGMENT_DIRS = frozenset({"NEXT"})

# vim keeps its per-release patch list in ``runtime/doc/version9.txt`` -- a numbered
# documentation page, one per major release, that lists every patch and what it fixed.  The
# digit is the entire rule: prometheus ships ``VERSION`` = "2.43.0-rc.0" and, earlier,
# ``version/VERSION``, which name no commit and must stay visible.  The documentation root
# is what keeps ``src/version.c`` readable -- vim's really does carry the patch list, but it
# is source, and hiding source is a judgement for a human rather than for this table.
DOC_VERSIONED_STEM_RE = re.compile(r"VERSION[0-9][0-9X_.-]*")


# Stems that also occur as ordinary directory names: llvm/utils/release,
# lldb/test/API/functionalities/history, rust-analyzer's xtask/src/release.  Requiring a
# documentation root above them is what keeps that code readable.


# An extensionless changelog is spelled in capitals by convention -- NEWS, ChangeLog,
# Misc/HISTORY -- while the directories and data files that collide with a stem are
# lower-case: llvm/utils/release, lldb/test/API/functionalities/history,
# systemd's test/fuzz-corpus/dhcp-server/release.  Requiring a leading capital when there
# is no extension separates the two without a repository-specific exception list.


def _stem_splits(basename: str) -> list[tuple[str, str]]:
    """The (stem, suffix) readings of a basename, most specific first.

    The last dot is what a version needs: kubernetes ships ``CHANGELOG-1.10.md`` and neovim
    ``runtime/doc/news-0.10.txt``, and partitioning on the first dot reads those as suffix
    ``.10.md`` -- not a document extension, so the whole family stayed visible through the
    first hard batch.  The first dot is still needed for ``NEWS.d``, and keeping both
    readings rather than replacing one with the other means this change can only hide more,
    never less.
    """
    first, dot, tail = basename.partition(".")
    if not dot:
        return [(basename, "")]
    head, _, last = basename.rpartition(".")
    return [(head, "." + last), (first, dot + tail)]


def _doc_changelog_dir(components: list[str]) -> bool:
    """True for a changelog directory sitting inside a documentation tree."""
    for index, component in enumerate(components[:-1]):
        if component in DOC_ROOTS:
            return any(STEM_RE.fullmatch(later) or later in DOC_FRAGMENT_DIRS
                       for later in components[index + 1:-1])
    return False


def _under_doc_root(components: list[str]) -> bool:
    return any(component in DOC_ROOTS for component in components[:-1])


def _doc_versioned_page(components: list[str], stem: str, suffix: str) -> bool:
    """True for ``runtime/doc/version9.txt``: a numbered page under a documentation root.

    A suffix is required rather than optional.  The extensionless branch below leans on a
    leading capital to separate files from directories named after a stem, and there is no
    observed extensionless carrier of this shape to pay for that complication with.
    """
    return bool(suffix and suffix in DOC_SUFFIXES
                and DOC_VERSIONED_STEM_RE.fullmatch(stem)
                and _under_doc_root(components))


def _doc_release_page(components: list[str], stem: str, suffix: str) -> bool:
    """True for ``docs/unsorted_wiki/Release-Notes-Flutter-1.9.1.md``."""
    return bool(suffix and suffix in DOC_SUFFIXES
                and DOC_RELEASE_STEM_RE.fullmatch(stem)
                and _under_doc_root(components))


def _versioned_release_page(stem: str, suffix: str) -> bool:
    """True for rails' ``guides/source/5_2_release_notes.md``.

    A suffix is required for the same reason as in ``_doc_versioned_page``: the
    extensionless branch of ``is_hidden`` leans on a leading capital, which a name starting
    with a digit can never have, and no extensionless carrier of this shape was observed.
    """
    return bool(suffix and suffix in DOC_SUFFIXES
                and VERSIONED_RELEASE_STEM_RE.fullmatch(stem))


def is_hidden(path: str) -> bool:
    """True when ``path`` names a changelog-style artifact that must stay invisible."""
    if not path:
        return False
    normalized = path.replace("\\", "/").strip()
    while normalized.startswith("./"):
        normalized = normalized[2:]
    normalized = normalized.strip("/")
    if not normalized:
        return False
    upper = normalized.upper()
    for pattern in DIRECTORY_GLOBS:
        if fnmatch.fnmatchcase(upper, pattern):
            return True
    components = upper.split("/")
    if _doc_changelog_dir(components):
        return True
    for stem, suffix in _stem_splits(components[-1]):
        if _doc_versioned_page(components, stem, suffix):
            return True
        if _doc_release_page(components, stem, suffix):
            return True
        if _versioned_release_page(stem, suffix):
            return True
        if not STEM_RE.fullmatch(stem) or suffix not in DOC_SUFFIXES:
            continue
        if suffix:
            return True
        basename = normalized.rsplit("/", 1)[-1]
        if basename[:1].isupper():
            return True
    return False


# Patterns for .git/info/sparse-checkout.  Negations there are gitignore-style, so the
# stems are spelled out rather than derived; keep this in sync with STEMS.
def _ci(text: str) -> str:
    """A gitignore pattern matching ``text`` case-insensitively.

    Sparse-checkout patterns are matched literally and repositories spell these files
    ``ChangeLog``, ``CHANGELOG`` and ``Changelog`` interchangeably, so every letter
    becomes a character class rather than guessing at the spellings.
    """
    return "".join(f"[{char.lower()}{char.upper()}]" if char.isalpha() else char for char in text)


def sparse_checkout_lines(rescue: Iterable[str] = ()) -> list[str]:
    """Everything, minus the changelog artifacts, plus `rescue` back.

    Written with --no-cone semantics so that negation is honoured.  A pattern without a
    slash matches the basename at any depth, which is what hides ``Lib/idlelib/NEWS2x.txt``;
    the directory entries need their own lines because a stem match alone would not catch
    a fragment named ``2019-01-09.bpo-1.rst``.

    The stem/suffix pairs are spelled out rather than written as ``NEWS.*``: a bare ``.*``
    would also hide a source file named ``changes.c``.  ``prepare_case`` compares these
    patterns against ``is_hidden`` over every tracked file and refuses to run if the two
    disagree in either direction, so any repository that breaks an assumption here fails
    loudly instead of leaking.

    ``rescue`` is what that comparison found and this pattern language cannot express.  A
    gitignore pattern without a slash matches a *directory* of that name as well as a file,
    and git then prunes everything below it: ``News`` hides grafana's
    ``public/app/core/components/AppChrome/News/NewsDrawer.tsx`` and ``HISTORY`` hides
    julia's ``stdlib/REPL/src/History/*.jl``.  There is no file-only form of a gitignore
    pattern, and a depth limit would be a guess, so the caller re-lists the tree, asks
    ``is_hidden`` which files the patterns removed and should not have, and passes them here
    to be re-included by exact anchored path.  Only paths ``is_hidden`` calls visible are
    accepted -- a rescue that named a hidden file would be a leak with a helpful name --
    which is what keeps this exact rather than a second matcher to keep in sync.
    """
    lines = ["/*"]
    suffixes = sorted({suffix.lower() for suffix in DOC_SUFFIXES})
    archive = _ci("archive")
    for stem in sorted(STEMS):
        body = _ci(stem)
        # Extensionless: first letter fixed upper-case, matching is_hidden's convention
        # rule, so that a lower-case directory named after a stem is not pruned.
        capitalized = stem[0] + _ci(stem[1:])
        for suffix in suffixes:
            head = body if suffix else capitalized
            lines.append(f"!{head}{_ci(suffix)}")
            # Versioned changelogs: NEWS2x.txt, CHANGELOG-1.0.md.  `STEM_RE` accepts any of
            # `[0-9X_.-]` before the digits, and glob syntax has no repetition, so each
            # separator needs its own line: grafana ships `CHANGELOG_ARCHIVE.md`, which is
            # what proved the underscore is not hypothetical.
            for separator in ("", "-", ".", "_"):
                lines.append(f"!{head}{separator}[0-9]*{_ci(suffix)}")
            # An archived changelog.  One line rather than one per separator: the word
            # `ARCHIVE` is itself the discriminator, and a `*` before it covers every
            # separator `STEM_RE` allows, including none and including a version in between.
            # Wider than the matcher in principle -- `changelog_archive_tool.md` would match
            # here and not there -- and that is the safe direction: an over-removal comes
            # back through `rescue`, while a changelog this missed would sit on disk in
            # plain sight, which is exactly how `CHANGELOG_ARCHIVE.md` survived until step
            # (5)'s self-check.
            lines.append(f"!{head}*{archive}*{_ci(suffix)}")
            if not suffix:
                continue
            # grafana's `.changelog-archive/CHANGELOG.01.md` and node's
            # `doc/CHANGELOG.ARCHIVE.md`: a dot rather than a hyphen before the tail.
            lines.append(f"!{head}.[0-9]*{_ci(suffix)}")
            lines.append(f"!{head}.{archive}*{_ci(suffix)}")
            if stem in _RELEASE_PAGE_STEMS:
                # The version written first: rails' `guides/source/5_2_release_notes.md`.
                # Glob syntax has no repetition, so the digit-and-separator prefix that
                # `VERSIONED_RELEASE_STEM_RE` requires can only be approximated by `[0-9]*`.
                # Approximating *wider* is the safe direction: a name this matches and
                # `is_hidden` does not is restored by the rescue pass, while a name
                # `is_hidden` hides and this missed would be a changelog left on disk.
                lines.append(f"![0-9]*{body}{_ci(suffix)}")
                lines.append(f"![0-9]*{body}[0-9]*{_ci(suffix)}")
    # Directories of changelog fragments, and changelog directories under a doc root.
    for directory in ("Misc/NEWS.d", "whatsnew", "newsfragments", "changelog.d",
                      "changes.d", "api/next"):
        lines.append(f"!**/{_ci(directory)}/")
        lines.append(f"!{_ci(directory)}/")
    # The root-level changelog collection, anchored with a leading slash because the same
    # names nested deeper are generators rather than changelogs -- see DIRECTORY_GLOBS.
    for directory in ("changelog", "changelog-archive", ".changelog-archive"):
        lines.append(f"!/{_ci(directory)}/")
    lines.append(f"!**/{_ci('debian')}/{_ci('changelog')}")
    lines.append(f"!/{_ci('debian')}/{_ci('changelog')}")
    for root in sorted(DOC_ROOTS):
        for stem in sorted(STEMS) + sorted(DOC_FRAGMENT_DIRS):
            lines.append(f"!**/{_ci(root)}/**/{_ci(stem)}/")
        # Numbered documentation pages: vim's runtime/doc/version9.txt.  Scoped to the doc
        # root rather than written as a bare basename pattern, because `is_hidden` requires
        # that root and a pattern that did not would disagree with it on `Version9` in a
        # source directory -- which `prepare_case` would then refuse to run on.
        for suffix in suffixes:
            if suffix:
                lines.append(f"!**/{_ci(root)}/**/{_ci('version')}[0-9]*{_ci(suffix)}")
        # Per-version release-notes pages: flutter's Release-Notes-Flutter-1.9.1.md.  The
        # dotted version is required in both places, so the glob and DOC_RELEASE_STEM_RE
        # accept the same names.
        for stem in sorted(_RELEASE_PAGE_STEMS):
            for suffix in suffixes:
                if suffix:
                    lines.append(f"!**/{_ci(root)}/**/{_ci(stem)}"
                                 f"*[0-9].[0-9]*{_ci(suffix)}")
    # Last match wins, so the rescues go at the end.  Anchored with a leading slash: these
    # are exact paths, not names, and a bare `News/NewsDrawer.tsx` would re-include that
    # path at any depth.
    for path in sorted(set(rescue)):
        if is_hidden(path):
            raise ValueError(f"refusing to re-include a hidden path: {path}")
        lines.append("/" + path.lstrip("/"))
    return lines
