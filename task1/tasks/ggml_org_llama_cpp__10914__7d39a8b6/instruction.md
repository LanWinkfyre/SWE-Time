# Locate the commit that introduced this regression

A regression was reported against `ggml-org/llama.cpp`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[llama-server] Duplicated text being produced during streaming generation with stop strings

### Name and Version


built with cc (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0 for x86_64-linux-gnu

### Operating systems

Linux

### GGML backends

CUDA

### Hardware

i7-12700KF
RTX A6000

### Models

Magnum-v4-72B-IQ4_XS.gguf - extra newlines and usually the last token of the preceding paragraph
Magnum-v4-123B-IQ3_XXS.gguf - just extra newlines
L3.3-70B-Euryale-v2.3-IQ4_XS.gguf - extra newlines and usually the last token of the preceding paragraph
Llama-3.3-70B-Instruct-IQ4_XS.gguf - extra newlines and usually the last token of the preceding paragraph

All imatrix quants made by bartowski and uploaded to HF.

### Problem description & steps to reproduce

It's a bit of a weird problem to describe, but it happens when doing streaming inference via llama-server using SillyTavern as a frontend. I can best describe it as "extra newlines and sometimes the final token of the previous paragraph is being added in between paragraphs".

I am *not* requesting logprobs with the request from SillyTavern.







### Relevant log output

Prompt here is "Write me a 3 paragraph story about something."

Magnum-v4-72B-IQ4_XS.gguf:
```
Here is a 3 paragraph story:

:

The old house at the end of Maple Street had been abandoned for as long as anyone could remember. Its paint was peeling, the windows were boarded up, and the yard was overgrown with weeds. Neighborhood kids whispered that it was haunted, and dared each other to run up and touch the front door.



One summer evening, a young girl named Lily was walking home from a friend's house when she noticed a light flickering in one of the upstairs windows of the old house. Curious, she crept up the creaky front steps and peered through a gap in the boards covering the window. To her surprise, she saw an old woman sitting in a rocking chair, knitting by the light of a single candle. The woman looked up and their eyes met. Lily gasped and stumbled backwards, her heart pounding.

.

The next day, Lily gathered her courage and knocked on the front door of the old house. The door swung open and the woman from the window beckoned her inside. Lily hesitantly stepped into the dusty foyer. The woman introduced herself as Agatha and invited Lily to sit and chat. As they talked, Lily realized Agatha was lonely, having lived alone in the house for decades. From that day on, Lily visited Agatha every afternoon, and the two became the closest of friends. The old house was no longer abandoned or scary - it was a place of warmth, laughter and companionship.
```

Magnum-v4-123B-IQ3_XXS.gguf:
```
Here is a 3 paragraph story for you:



The old house at the end of Maple Street had been abandoned for years. Its windows were boarded up, the paint was peeling, and the yard was overgrown with weeds. Neighborhood kids whispered that it was haunted, but no one dared to go inside.



One summer day, a curious 12-year-old boy named Tommy decided to explore the old house. He crept up the creaky front steps and pried open the door. Inside, he found the house filled with cobwebs and dust. As he made his way through the dark hallways, he heard a strange noise coming from the attic.



Tommy's heart raced as he climbed the stairs to the attic. There, in the dim light filtering through a small window, he saw an old rocking chair moving back and forth. Sitting in the chair was the ghost of an old woman, her translucent form humming a tune. Tommy froze in fear, but the ghostly woman just smiled and beckoned him closer. She told Tommy the story of her life in the house and how she had died there, alone. From that day on, Tommy and the ghost became friends, and he would visit her whenever he could, listening to her stories and keeping her company in the old, abandoned house.
```

L3.3-70B-Euryale-v2.3-IQ4_XS.gguf:
```
In the quaint town of Willow Creek, nestled between rolling hills and dense forests, there lived a young girl named Lily. She was a curious and adventurous soul, with a heart full of wonder and a mind full of questions. Lily spent her days exploring the woods, discovering hidden streams and secret meadows, and her nights gazing up at the starry sky, dreaming of far-off lands and magical creatures. She was a gentle soul, loved by all who knew her, and her presence brought joy and light to the quiet town.

.

One day, while wandering deeper into the forest than she had ever gone before, Lily stumbled upon a hidden glade. In the center of the clearing stood an enormous tree, its trunk twisted and gnarled with age, its branches reaching up towards the sky like giant arms. The air was filled with the sweet scent of blooming flowers, and the soft chirping of birds could be heard from the treetops. Lily felt a strange sense of peace and belonging as she approached the tree, as if she had finally found a place where she truly belonged. She reached out a hand to touch the trunk, and as she did, the tree began to glow with a soft, ethereal light.

.

As the light enveloped her, Lily felt herself being transported to a world beyond her wildest dreams. She found herself standing in a lush, vibrant forest, surrounded by towering trees and sparkling fountains. A soft, melodious voice spoke to her, telling her that she had been chosen to be the guardian of this magical world, to protect it from harm and to keep its beauty and wonder alive. Lily was both thrilled and terrified at the prospect, but she knew that she was ready for the challenge. With a sense of purpose and determination, she accepted the role, and as she did, the tree's glow faded, leaving her back in the hidden glade, but forever changed by the experience. From that day on, Lily spent her days exploring the magical world, learning its secrets and protecting its beauty, and her nights back in Willow Creek, sharing her stories and spreading joy and wonder to all who would listen.
```

Llama-3.3-70B-Instruct-IQ4_XS.gguf:
```
As the sun set over the rolling hills, a sense of peace settled over the small village of Willowdale. The air was filled with the sweet scent of blooming wildflowers, and the sound of birds singing their evening songs. In the midst of this serene landscape, a young girl named Emily sat on the edge of a tranquil lake, her feet dangling in the cool water. She had always loved coming to this spot, where she could escape the hustle and bustle of daily life and connect with nature. With a fishing rod in hand, Emily waited patiently for a bite, her eyes fixed on the gentle ripples that disturbed the lake's surface.

.

As the stars began to twinkle in the night sky, Emily felt a tug on her line, and her heart skipped a beat with excitement. She carefully reeled in the catch, her hands moving slowly and deliberately to avoid breaking the line. As the fish emerged from the water, Emily gasped in delight - it was a beautiful rainbow trout, its scales shimmering in the fading light. She gently lifted the fish out of the water and placed it in a nearby bucket, feeling a sense of pride and accomplishment at her successful catch. As she sat back down on the lake's edge, Emily couldn't help but feel grateful for this moment of solitude, surrounded by the beauty and wonder of the natural world.

.

As the night wore on, Emily decided to build a small fire on the lake's shore, using some dry wood and kindling she had brought with her. The flames crackled and danced, casting a warm glow over the surrounding landscape. Emily sat back, feeling the warmth of the fire on her face, and watched as the stars twinkled above. She felt a deep sense of connection to the world around her, and a sense of peace that she had not felt in a long time. As she sat there, listening to the sound of the water lapping against the shore, Emily knew that this was a moment she would never forget, a moment of perfect tranquility and joy in the midst of a busy and often chaotic world. And as she drifted off to sleep, lulled by the sound of the water and the warmth of the fire, Emily felt her heart fill with a sense of wonder and awe at the beauty of the world around her.
```


I encountered a similar bug and I believe that it has the same cause: when streaming with stop strings the server generates duplicate tokens that include those strings.

An example without the bug (`"stop": ["\n"]`):
```
❯ curl -Ss --data '{"prompt": "Alice: Hi, Bob!\nBob: Hi,", "n_predict": 8, "cache_prompt": true, "stop": ["\n"], "stream": true}' http://127.0.0.1:8080/completion | head -n 3

data: {"index":0,"content":" Alice","tokens":[30505],"stop":false,"id_slot":-1,"tokens_predicted":1,"tokens_evaluated":11}

data: {"index":0,"content":"!","tokens":[0],"stop":false,"id_slot":-1,"tokens_predicted":2,"tokens_evaluated":11}
```
The server properly generates the output ` Alice!`.

But if you add `Alice:` to the stop strings, here's what it generates:
```
❯ curl -Ss --data '{"prompt": "Alice: Hi, Bob!\nBob: Hi,", "n_predict": 8, "cache_prompt": true, "stop": ["\n", "Alice:"], "stream": true}' http://127.0.0.1:8080/completion | head -n 3

data: {"index":0,"content":" Alice","tokens":[30505],"stop":false,"id_slot":-1,"tokens_predicted":1,"tokens_evaluated":11}

data: {"index":0,"content":" Alice!","tokens":[4999],"stop":false,"id_slot":-1,"tokens_predicted":2,"tokens_evaluated":11,"timings":{"prompt_n":1,"prompt_ms":24.626,"prompt_per_token_ms":24.626,"prompt_per_second":40.60748802079103,"predicted_n":2,"predicted_ms":12.734,"predicted_per_token_ms":6.367,"predicted_per_second":157.0598397989634}}
```
Now it generates ` Alice Alice!`.
```

## What you have

- `/testbed/repo` is a git clone of `ggml-org/llama.cpp` truncated just after the regression was
  reported.  `HEAD` is `d408bb9268a988c5a60a5746d3a6430386e7604d` and the full history behind it is present.
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
