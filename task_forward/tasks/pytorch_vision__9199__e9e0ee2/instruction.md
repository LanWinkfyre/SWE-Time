# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/vision`.  The report is quoted verbatim below.

## Report

```
Different label background color for `draw_bounding_boxes`

### 🚀 The feature

Add a `label_background_colors` parameter to the `draw_bounding_boxes` util to allow independent control of label background colors, separate from the box colors.

```py
image = draw_bounding_boxes(
    image,
    boxes,
    colors=box_colors,
    labels=label_texts,
    label_colors=text_colors,
    label_background_colors=background_colors,  # New parameter
    fill_labels=True, # Must be True for label_background_colors to take effect
)
```

This would work similarly to the existing `label_colors` parameter, but control the background fill color of label text boxes instead of the text color itself. When `fill_labels=False`, the `label_background_colors` param would be ignored since no background is rendered.

### Motivation, pitch

The newest `fill_labels` flag added in the 0.23 release is a welcome improvement, no doubt.

The rationale is to also use the same background color as the one set for the box color itself is likely the most obvious and useful one as well. 

However, it would be awesome to have the possibility to set a different label background color for the fill. An example would be the necessity of detecting subclasses as well as classes (and the color would already be taken by the class).

Worked example:

Let's say we're analyzing chest X-rays and detecting abnormalities in different organ regions. We can use box colors to represent the organ type:

```py
organ_colors = ["lightblue", "lightblue", "red", "lightblue"]  # blue=lung, red=heart
image = draw_bounding_boxes(
    image,
    boxes,
    colors=organ_colors,
)
```

Now we want to label the specific abnormality types detected in each region:

```py
organ_colors = ["lightblue", "lightblue", "red", "lightblue"]
abnormalities = ["nodule", "mass", "enlarged", "effusion"]
image = draw_bounding_boxes(
    image,
    boxes,
    colors=organ_colors,
    labels=abnormalities,
)
```

Finally, we want to encode severity levels using text color - for the sake of argument, this is best predicted/decoded as a color, and not text. We've filled out our labels already with the abnormalities, but we can use the text color feature for this. The problem is that this starts to render badly in Pillow:

```py
organ_colors = ["lightblue", "lightblue", "red", "lightblue"]
abnormalities = ["nodule", "mass", "enlarged", "effusion"]
severity_colors = ["green", "orange", "yellow", "red"]  # green=low, red=critical
image = draw_bounding_boxes(
    image,
    boxes,
    colors=organ_colors,
    labels=abnormalities,
    label_colors=severity_colors,
)
```

As you can see, it's now hard to make sense of all of these:

<img width="640" height="480" alt="Image" src="https://github.com/user-attachments/assets/0f47be8a-67a4-4d65-9f71-583277691663" />

### Alternatives

You could argue that you could combine all the information into the label text instead:

```py
organ_colors = ["lightblue", "lightblue", "red", "lightblue"]
abnormality_and_severity_types = ["nodule-green", "mass-orange", "enlarged-yellow", "effusion-red"]
# severity_colors = ["green", "orange", "yellow", "red"]

image = draw_bounding_boxes(
    image,
    boxes,
    colors=organ_colors,
    labels=abnormality_and_severity_types,
    # label_colors=severity_colors,
)
```

<img width="640" height="480" alt="Image" src="https://github.com/user-attachments/assets/60942d19-2793-441d-bf0d-51bdb0ecaba1" />

But equally valid would be having the option to choose an independent background color for the label text (e.g., black or white) while keeping the text appropriately colored for better visibility and semantic meaning.

### Additional context

Do you feel like this addition would be too over the top and would not fit the majority of use cases? In part, I could see it that way, too. However, I do have real real-life use case for this as well, and  I tend to believe this feature would significantly improve readability in multi-dimensional classification.

I'm happy to implement this feature myself since it's relatively straightforward - essentially adding a `label_background_colors` parameter alongside the existing `label_colors`. However, I wanted to gauge interest first to ensure this aligns with the project's overall vision (I'll see myself out).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `e9e0ee24fb9b9ec08e8ebcddd363b1bee289ffa6`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `main`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "pytorch_vision__9199__e9e0ee2",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
