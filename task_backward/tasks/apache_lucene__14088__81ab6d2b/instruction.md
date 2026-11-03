# Locate the commit that introduced this regression

A regression was reported against `apache/lucene`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
TestSimpleExplanationsWithFillerDocs > testBQ23 FAILED AssertionError: FINISHED

Reproduces readily.

```
 Reproduce with: gradlew :lucene:core:test --tests "org.apache.lucene.search.TestSimpleExplanationsWithFillerDocs.testBQ23" -Ptests.jvms=6 "-Ptests.jvmargs=-XX:TieredStopAtLevel=1 -XX:+UseParallelGC -XX:ActiveProcessorCount=1" -Ptests.seed=E91A208A2114E608 -Ptests.locale=so-SO -Ptests.timezone=CET -Ptests.nightly=true -Ptests.gui=false -Ptests.file.encoding=UTF-8 -Ptests.vectorsize=128 -Ptests.forceintegervectors=true
```

```
TestSimpleExplanationsWithFillerDocs > testBQ23 FAILED
    java.lang.AssertionError: FINISHED
        at __randomizedtesting.SeedInfo.seed([E91A208A2114E608:46D11100E2CE0DDC]:0)
        at org.apache.lucene.tests.search.AssertingScorer.score(AssertingScorer.java:121)
        at org.apache.lucene.tests.search.AssertingScorable.score(AssertingScorable.java:35)
        at org.apache.lucene.tests.search.AssertingScorable$WrappedScorer.score(AssertingScorable.java:66)
        at org.apache.lucene.tests.search.AssertingScorable.score(AssertingScorable.java:35)
        at org.apache.lucene.tests.search.AssertingScorable$WrappedScorer.score(AssertingScorable.java:66)
        at org.apache.lucene.tests.search.QueryUtils$3.collect(QueryUtils.java:365)
        at org.apache.lucene.tests.search.AssertingLeafCollector$AssertingDocIdStream.lambda$forEach$0(AssertingLeafCollector.java:119)
        at org.apache.lucene.tests.search.AssertingLeafCollector$AssertingDocIdStream.lambda$forEach$0(AssertingLeafCollector.java:119)
        at org.apache.lucene.search.DenseConjunctionBulkScorer$DocIdStreamView.forEach(DenseConjunctionBulkScorer.java:182)
        at org.apache.lucene.tests.search.AssertingLeafCollector$AssertingDocIdStream.forEach(AssertingLeafCollector.java:114)
        at org.apache.lucene.tests.search.AssertingLeafCollector$AssertingDocIdStream.forEach(AssertingLeafCollector.java:114)
        at org.apache.lucene.search.LeafCollector.collect(LeafCollector.java:106)
        at org.apache.lucene.tests.search.AssertingLeafCollector.collect(AssertingLeafCollector.java:49)
        at org.apache.lucene.tests.search.AssertingLeafCollector.collect(AssertingLeafCollector.java:49)
        at org.apache.lucene.search.DenseConjunctionBulkScorer.scoreWindowUsingBitSet(DenseConjunctionBulkScorer.java:151)
        at org.apache.lucene.search.DenseConjunctionBulkScorer.score(DenseConjunctionBulkScorer.java:84)
        at org.apache.lucene.search.ReqExclBulkScorer.score(ReqExclBulkScorer.java:66)
        at org.apache.lucene.tests.search.AssertingBulkScorer.score(AssertingBulkScorer.java:82)
        at org.apache.lucene.search.IndexSearcher.searchLeaf(IndexSearcher.java:850)
        at org.apache.lucene.search.IndexSearcher.search(IndexSearcher.java:639)
        at org.apache.lucene.tests.search.QueryUtils.checkSkipTo(QueryUtils.java:350)
        at org.apache.lucene.tests.search.QueryUtils.check(QueryUtils.java:139)
        at org.apache.lucene.tests.search.QueryUtils.check(QueryUtils.java:131)
        at org.apache.lucene.tests.search.CheckHits.checkHitCollector(CheckHits.java:106)
        at org.apache.lucene.tests.search.BaseExplanationTestCase.qtest(BaseExplanationTestCase.java:110)
        at org.apache.lucene.search.TestSimpleExplanationsWithFillerDocs.qtest(TestSimpleExplanationsWithFillerDocs.java:118)
        at org.apache.lucene.search.TestSimpleExplanations.testBQ23(TestSimpleExplanations.java:481)
        at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:103)
        at java.base/java.lang.reflect.Method.invoke(Method.java:580)
        at com.carrotsearch.randomizedtesting.RandomizedRunner.invoke(RandomizedRunner.java:1758)
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
        at java.base/java.lang.Thread.run(Thread.java:1583)

```

git bisect tells me this /cc @jpountz
```

## What you have

- `/testbed/repo` is a git clone of `apache/lucene` truncated just after the regression was
  reported.  `HEAD` is `c0fc70016e1d79da96aa57d2799d5c9ded8cbb8d` and the full history behind it is present.
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
