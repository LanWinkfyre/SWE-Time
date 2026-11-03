# Locate the commit that introduced this regression

A regression was reported against `scipy/scipy`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
BUG: linalg solve behavior change breaking downstream tests

I bisected SciPy against a rather messy reproducer--it requires using some obscure project we have (https://github.com/lanl/ldrd_neat_ml) that started failing tests with SciPy `1.17.0`, and those tests in turn interact with https://github.com/marcotcr/lime (not well maintained I admit) and `scikit-learn`. So, apologies that this isn't cleaner yet--I asked a trainee to help with the root causing. 




The traceback, admittedly partially propagating through some projects we don't care about here, is pasted below the fold. I don't think it will be much help yet, but we're getting a bunch of `nan`s propagating through now.

<details>

```
_______________________________ test_build_lime_data[0-expected0] _______________________________
[gw4] darwin -- Python 3.12.3 /Users/treddy/python_venvs/py_312_ldrd_neat_dev/bin/python

important_col = 0, expected = [0, 0, 0]

    @pytest.mark.parametrize("important_col, expected", [
        # should be easy to predict the important
        # feature for the non-zero rows
        (0, [0, 0, 0]),
        (1, [1, 1, 1]),
        (2, [2, 2, 2]),
    ])
    def test_build_lime_data(important_col, expected):
        # very simple dataset to check the most basic
        # properties of the LIME data structure generation
        data = np.zeros(shape=(4, 3), dtype=np.float64)
        data[:-1, important_col] = 1.0
        y = np.asarray([1, 1, 1, 0])
        X = pd.DataFrame(data=data, columns=["1", "2", "3"])
        rf = RandomForestClassifier(random_state=0)
        rf.fit(X, y)
>       lime_actual = lib.build_lime_data(X=X, model=rf)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

neat_ml/tests/test_lib.py:144: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
../../../python_venvs/py_312_ldrd_neat_dev/lib/python3.12/site-packages/joblib/memory.py:607: in __call__
    return self._cached_call(args, kwargs, shelving=False)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../../python_venvs/py_312_ldrd_neat_dev/lib/python3.12/site-packages/joblib/memory.py:562: in _cached_call
    return self._call(call_id, args, kwargs, shelving)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../../python_venvs/py_312_ldrd_neat_dev/lib/python3.12/site-packages/joblib/memory.py:832: in _call
    output = self.func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
neat_ml/lib.py:792: in build_lime_data
    exp = explainer_lime.explain_instance(X.to_numpy()[index],
../../../python_venvs/py_312_ldrd_neat_dev/lib/python3.12/site-packages/lime/lime_tabular.py:452: in explain_instance
    ret_exp.score, ret_exp.local_pred) = self.base.explain_instance_with_data(
../../../python_venvs/py_312_ldrd_neat_dev/lib/python3.12/site-packages/lime/lime_base.py:183: in explain_instance_with_data
    used_features = self.feature_selection(neighborhood_data,
../../../python_venvs/py_312_ldrd_neat_dev/lib/python3.12/site-packages/lime/lime_base.py:134: in feature_selection
    return self.feature_selection(data, labels, weights,
../../../python_venvs/py_312_ldrd_neat_dev/lib/python3.12/site-packages/lime/lime_base.py:76: in feature_selection
    return self.forward_selection(data, labels, weights, num_features)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../../python_venvs/py_312_ldrd_neat_dev/lib/python3.12/site-packages/lime/lime_base.py:61: in forward_selection
    score = clf.score(data[:, used_features + [feature]],
../../../python_venvs/py_312_ldrd_neat_dev/lib/python3.12/site-packages/sklearn/base.py:654: in score
    return r2_score(y, y_pred, sample_weight=sample_weight)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../../python_venvs/py_312_ldrd_neat_dev/lib/python3.12/site-packages/sklearn/utils/_param_validation.py:218: in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
../../../python_venvs/py_312_ldrd_neat_dev/lib/python3.12/site-packages/sklearn/metrics/_regression.py:1281: in r2_score
    _check_reg_targets_with_floating_dtype(
../../../python_venvs/py_312_ldrd_neat_dev/lib/python3.12/site-packages/sklearn/metrics/_regression.py:208: in _check_reg_targets_with_floating_dtype
    y_type, y_true, y_pred, sample_weight, multioutput = _check_reg_targets(
../../../python_venvs/py_312_ldrd_neat_dev/lib/python3.12/site-packages/sklearn/metrics/_regression.py:115: in _check_reg_targets
    y_pred = check_array(y_pred, ensure_2d=False, dtype=dtype)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../../python_venvs/py_312_ldrd_neat_dev/lib/python3.12/site-packages/sklearn/utils/validation.py:1074: in check_array
    _assert_all_finite(
../../../python_venvs/py_312_ldrd_neat_dev/lib/python3.12/site-packages/sklearn/utils/validation.py:133: in _assert_all_finite
    _assert_all_finite_element_wise(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

X = array([nan, nan, nan, ..., nan, nan, nan])

    def _assert_all_finite_element_wise(
        X, *, xp, allow_nan, msg_dtype=None, estimator_name=None, input_name=""
    ):
        # Cython implementation doesn't support FP16 or complex numbers
        use_cython = (
            xp is np and X.data.contiguous and X.dtype.type in {np.float32, np.float64}
        )
        if use_cython:
            out = cy_isfinite(X.reshape(-1), allow_nan=allow_nan)
            has_nan_error = False if allow_nan else out == FiniteStatus.has_nan
            has_inf = out == FiniteStatus.has_infinite
        else:
            has_inf = xp.any(xp.isinf(X))
            has_nan_error = False if allow_nan else xp.any(xp.isnan(X))
        if has_inf or has_nan_error:
            if has_nan_error:
                type_err = "NaN"
            else:
                msg_dtype = msg_dtype if msg_dtype is not None else X.dtype
                type_err = f"infinity or a value too large for {msg_dtype!r}"
            padded_input_name = input_name + " " if input_name else ""
            msg_err = f"Input {padded_input_name}contains {type_err}."
            if estimator_name and input_name == "X" and has_nan_error:
                # Improve the error message on how to handle missing values in
                # scikit-learn.
                msg_err += (
                    f"\n{estimator_name} does not accept missing values"
                    " encoded as NaN natively. For supervised learning, you might want"
                    " to consider sklearn.ensemble.HistGradientBoostingClassifier and"
                    " Regressor which accept missing values encoded as NaNs natively."
                    " Alternatively, it is possible to preprocess the data, for"
                    " instance by using an imputer transformer in a pipeline or drop"
                    " samples with missing values. See"
                    " https://scikit-learn.org/stable/modules/impute.html"
                    " You can find a list of all estimators that handle NaN values"
                    " at the following page:"
                    " https://scikit-learn.org/stable/modules/impute.html"
                    "#estimators-that-handle-nan-values"
                )
>           raise ValueError(msg_err)
E           ValueError: Input contains NaN.

../../../python_venvs/py_312_ldrd_neat_dev/lib/python3.12/site-packages/sklearn/utils/validation.py:182: ValueError
```

</details>

Need to clean up the reproducer...
```

## What you have

- `/testbed/repo` is a git clone of `scipy/scipy` truncated just after the regression was
  reported.  `HEAD` is `012ca52084d830eab769e3fd4ac086192f1e3784` and the full history behind it is present.
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
