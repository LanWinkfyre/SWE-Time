# Locate the commit that introduced this regression

A regression was reported against `doxygen/doxygen`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
status ASSIGNED severity *normal* in component *general* for *---*
Reported in version *1.8.13* on platform *Other*
Assigned to: Dimitri van Heesch

On 2018-05-14 09:01:46 +0000, Marcin Kasperski wrote:

    Summary
    =========
    
    Doxygen fails to parse default values with backslashes, like
    
         string someFunc(const string& splitOn = " \n");
    
    (it seems any backslash inside default value suffices, I saw it on "\t\r\n",
    "\n" and some similar)
    
    The problem appears in 1.8.13 but was not present in 1.8.11
    
    Detailed example
    ======================
    
    
    // doxygen 1.18.13 fails to parse parameters with default values containing
    backslash.
    // In older versions they worked correctly.
    //
    // To test:
    //     doxygen -g test
    //     doxygen test
    //
    // Problems:
    //
    // - the following warnings are reported:
    //
    //     problem.hxx:31: warning: argument 'value' of command @param is not
    found in the argument list of ThisFails()
    //     problem.hxx:37: warning: argument 'value' of command @param is not
    found in the argument list of ThisFailsToo(const string &arg1)
    //     problem.hxx:37: warning: argument 'arg2' of command @param is not
    found in the argument list of ThisFailsToo(const string &arg1)
    //
    // - in generated docs, doxygen claims the following signatures:
    //
    //    string ThisFails ( )
    //
    //    string ThisFailsToo ( const string &      arg1)
    
    
    /**
       @file
    **/
    
    #include <string>
    using std::string;
    
    /**
       @param value Some value
    **/
    string
    ThisWorks(const string& value);
    
    /**
       @param value Some value
    **/
    string
    ThisWorksToo(const string& value = "abc def");
    
    /**
       @param value Some value
    **/
    string
    ThisFails(const string& value = " \r\n");
    
    /**
       @param value Some value
       @param arg1 Some arg1
       @param arg2 Some arg2
    **/
    string
    ThisFailsToo(const string& arg1, const string& value = " \r\n", const
    string& arg2="");

On 2018-05-14 09:27:37 +0000, Marcin Kasperski wrote:

    The problem appears also on tip ( SHA:


On 2018-05-14 09:37:45 +0000, Marcin Kasperski wrote:

    I bisected this over doxygen sources, and:
    
    


    

On 2018-05-14 12:55:45 +0000, albert wrote:

    Thanks for the work on the bisection to the commit.
    
    I've just pushed a proposed patch to github (pull request 724,


On 2018-05-14 15:46:59 +0000, Marcin Kasperski wrote:

    Patch seems to help.

On 2018-06-10 10:03:45 +0000, albert wrote:

    Code has been integrated in master on github.
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
