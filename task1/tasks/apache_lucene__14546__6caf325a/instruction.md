# Locate the commit that introduced this regression

A regression was reported against `apache/lucene`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
TestForTooMuchCloning: too many calls to IndexInput.clone during TermRangeQuery: 7

### Description

```
TestForTooMuchCloning > test FAILED
    java.lang.AssertionError: too many calls to IndexInput.clone during TermRangeQuery: 7
        at __randomizedtesting.SeedInfo.seed([3B8D209D5C693E94:B3D91F47F295536C]:0)
        at org.junit.Assert.fail(Assert.java:89)
        at org.junit.Assert.assertTrue(Assert.java:42)
        at org.apache.lucene.index.TestForTooMuchCloning.test(TestForTooMuchCloning.java:88)
        at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:103)
        at java.base/java.lang.reflect.Method.invoke(Method.java:580)
        at com.carrotsearch.randomizedtesting.RandomizedRunner.invoke(RandomizedRunner.java:1763)
        at com.carrotsearch.randomizedtesting.RandomizedRunner$8.evaluate(RandomizedRunner.java:946)
        at com.carrotsearch.randomizedtesting.RandomizedRunner$9.evaluate(RandomizedRunner.java:982)
        at com.carrotsearch.randomizedtesting.RandomizedRunner$10.evaluate(RandomizedRunner.java:996)
        at org.apache.lucene.tests.util.TestRuleSetupTeardownChained$1.evaluate(TestRuleSetupTeardownChained.java:48)
        at org.apache.lucene.tests.util.AbstractBeforeAfterRule$1.evaluate(AbstractBeforeAfterRule.java:43)
        at org.apache.lucene.tests.util.TestRuleThreadAndTestName$1.evaluate(TestRuleThreadAndTestName.java:45)
        at org.apache.lucene.tests.util.TestRuleIgnoreAfterMaxFailures$1.evaluate(TestRuleIgnoreAfterMaxFailures.java:60)
        at org.apache.lucene.tests.util.TestRuleMarkFailure$1.evaluate(TestRuleMarkFailure.java:44)
        at org.junit.rules.RunRules.evaluate(RunRules.java:20)
        at com.carrotsearch.randomizedtesting.rules.StatementAdapter.evaluate(StatementAdapter.java:36)
        at com.carrotsearch.randomizedtesting.ThreadLeakControl$StatementRunner.run(ThreadLeakControl.java:390)
        at com.carrotsearch.randomizedtesting.ThreadLeakControl.forkTimeoutingTask(ThreadLeakControl.java:843)
        at com.carrotsearch.randomizedtesting.ThreadLeakControl$3.evaluate(ThreadLeakControl.java:490)
        at com.carrotsearch.randomizedtesting.RandomizedRunner.runSingleTest(RandomizedRunner.java:955)
        at com.carrotsearch.randomizedtesting.RandomizedRunner$5.evaluate(RandomizedRunner.java:840)
        at com.carrotsearch.randomizedtesting.RandomizedRunner$6.evaluate(RandomizedRunner.java:891)
        at com.carrotsearch.randomizedtesting.RandomizedRunner$7.evaluate(RandomizedRunner.java:902)
        at org.apache.lucene.tests.util.AbstractBeforeAfterRule$1.evaluate(AbstractBeforeAfterRule.java:43)
        at com.carrotsearch.randomizedtesting.rules.StatementAdapter.evaluate(StatementAdapter.java:36)
        at org.apache.lucene.tests.util.TestRuleStoreClassName$1.evaluate(TestRuleStoreClassName.java:38)
        at com.carrotsearch.randomizedtesting.rules.NoShadowingOrOverridesOnMethodsRule$1.evaluate(NoShadowingOrOverridesOnMethodsRule.java:40)
        at com.carrotsearch.randomizedtesting.rules.NoShadowingOrOverridesOnMethodsRule$1.evaluate(NoShadowingOrOverridesOnMethodsRule.java:40)
        at com.carrotsearch.randomizedtesting.rules.StatementAdapter.evaluate(StatementAdapter.java:36)
        at com.carrotsearch.randomizedtesting.rules.StatementAdapter.evaluate(StatementAdapter.java:36)
        at org.apache.lucene.tests.util.TestRuleAssertionsRequired$1.evaluate(TestRuleAssertionsRequired.java:53)
        at org.apache.lucene.tests.util.AbstractBeforeAfterRule$1.evaluate(AbstractBeforeAfterRule.java:43)
        at org.apache.lucene.tests.util.TestRuleMarkFailure$1.evaluate(TestRuleMarkFailure.java:44)
        at org.apache.lucene.tests.util.TestRuleIgnoreAfterMaxFailures$1.evaluate(TestRuleIgnoreAfterMaxFailures.java:60)
        at org.apache.lucene.tests.util.TestRuleIgnoreTestSuites$1.evaluate(TestRuleIgnoreTestSuites.java:47)
        at org.junit.rules.RunRules.evaluate(RunRules.java:20)
        at com.carrotsearch.randomizedtesting.rules.StatementAdapter.evaluate(StatementAdapter.java:36)
        at com.carrotsearch.randomizedtesting.ThreadLeakControl$StatementRunner.run(ThreadLeakControl.java:390)
        at com.carrotsearch.randomizedtesting.ThreadLeakControl.lambda$forkTimeoutingTask$0(ThreadLeakControl.java:850)
        at java.base/java.lang.Thread.run(Thread.java:1575)
```

### Gradle command to reproduce

./gradlew test --tests TestForTooMuchCloning.test -Dtests.seed=3B8D209D5C693E94 -Dtests.locale=kk-KZ -Dtests.timezone=America/Indiana/Marengo -Dtests.asserts=true -Dtests.file.encoding=UTF-8

 /cc @gf2121
```

## What you have

- `/testbed/repo` is a git clone of `apache/lucene` truncated just after the regression was
  reported.  `HEAD` is `d76d55b6396d84ef7bd7c4ab2e29eab6ef497323` and the full history behind it is present.
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
