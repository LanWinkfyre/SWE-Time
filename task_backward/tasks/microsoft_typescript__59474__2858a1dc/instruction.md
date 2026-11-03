# Locate the commit that introduced this regression

A regression was reported against `microsoft/TypeScript`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Typescript 5.5 does not infer event handler types in MUI

### 🔎 Search Terms

"inferred types event handler" 

### 🕗 Version & Regression Information

- This changed between versions 5.3.3 and 5.5.4

### ⏯ Playground Link

[Code Sandbox](https://codesandbox.io/p/sandbox/bold-ben-pdgszs?file=%2Fsrc%2FApp.tsx&layout=%257B%2522sidebarPanel%2522%253A%2522EXPLORER%2522%252C%2522rootPanelGroup%2522%253A%257B%2522direction%2522%253A%2522horizontal%2522%252C%2522contentType%2522%253A%2522UNKNOWN%2522%252C%2522type%2522%253A%2522PANEL_GROUP%2522%252C%2522id%2522%253A%2522ROOT_LAYOUT%2522%252C%2522panels%2522%253A%255B%257B%2522type%2522%253A%2522PANEL_GROUP%2522%252C%2522contentType%2522%253A%2522UNKNOWN%2522%252C%2522direction%2522%253A%2522vertical%2522%252C%2522id%2522%253A%2522clz8x9p7700073b6gibb1mmmu%2522%252C%2522sizes%2522%253A%255B100%252C0%255D%252C%2522panels%2522%253A%255B%257B%2522type%2522%253A%2522PANEL_GROUP%2522%252C%2522contentType%2522%253A%2522EDITOR%2522%252C%2522direction%2522%253A%2522horizontal%2522%252C%2522id%2522%253A%2522EDITOR%2522%252C%2522panels%2522%253A%255B%257B%2522type%2522%253A%2522PANEL%2522%252C%2522contentType%2522%253A%2522EDITOR%2522%252C%2522id%2522%253A%2522clz8x9p7600033b6gjw9e6rt5%2522%257D%255D%257D%252C%257B%2522type%2522%253A%2522PANEL_GROUP%2522%252C%2522contentType%2522%253A%2522SHELLS%2522%252C%2522direction%2522%253A%2522horizontal%2522%252C%2522id%2522%253A%2522SHELLS%2522%252C%2522panels%2522%253A%255B%257B%2522type%2522%253A%2522PANEL%2522%252C%2522contentType%2522%253A%2522SHELLS%2522%252C%2522id%2522%253A%2522clz8x9p7600043b6gla5v5hha%2522%257D%255D%252C%2522sizes%2522%253A%255B100%255D%257D%255D%257D%252C%257B%2522type%2522%253A%2522PANEL_GROUP%2522%252C%2522contentType%2522%253A%2522DEVTOOLS%2522%252C%2522direction%2522%253A%2522vertical%2522%252C%2522id%2522%253A%2522DEVTOOLS%2522%252C%2522panels%2522%253A%255B%257B%2522type%2522%253A%2522PANEL%2522%252C%2522contentType%2522%253A%2522DEVTOOLS%2522%252C%2522id%2522%253A%2522clz8x9p7700063b6ggzop0d8g%2522%257D%255D%252C%2522sizes%2522%253A%255B100%255D%257D%255D%252C%2522sizes%2522%253A%255B50%252C50%255D%257D%252C%2522tabbedPanels%2522%253A%257B%2522clz8x9p7600033b6gjw9e6rt5%2522%253A%257B%2522tabs%2522%253A%255B%257B%2522id%2522%253A%2522clz8x9p7600023b6g4u5y2cjf%2522%252C%2522mode%2522%253A%2522permanent%2522%252C%2522type%2522%253A%2522FILE%2522%252C%2522filepath%2522%253A%2522%252Fsrc%252FApp.tsx%2522%252C%2522state%2522%253A%2522IDLE%2522%257D%255D%252C%2522id%2522%253A%2522clz8x9p7600033b6gjw9e6rt5%2522%252C%2522activeTabId%2522%253A%2522clz8x9p7600023b6g4u5y2cjf%2522%257D%252C%2522clz8x9p7700063b6ggzop0d8g%2522%253A%257B%2522id%2522%253A%2522clz8x9p7700063b6ggzop0d8g%2522%252C%2522activeTabId%2522%253A%2522clz8x9p7600053b6gg66a2uqp%2522%252C%2522tabs%2522%253A%255B%257B%2522id%2522%253A%2522clz8x9p7600053b6gg66a2uqp%2522%252C%2522mode%2522%253A%2522permanent%2522%252C%2522type%2522%253A%2522UNASSIGNED_PORT%2522%252C%2522port%2522%253A0%252C%2522path%2522%253A%2522%252F%2522%257D%252C%257B%2522type%2522%253A%2522CHANGELOG%2522%252C%2522id%2522%253A%2522clz8xnww0001r3b6fa4jjtphv%2522%252C%2522mode%2522%253A%2522permanent%2522%257D%255D%257D%252C%2522clz8x9p7600043b6gla5v5hha%2522%253A%257B%2522tabs%2522%253A%255B%255D%252C%2522id%2522%253A%2522clz8x9p7600043b6gla5v5hha%2522%257D%257D%252C%2522showDevtools%2522%253Atrue%252C%2522showShells%2522%253Afalse%252C%2522showSidebar%2522%253Atrue%252C%2522sidebarPanelSize%2522%253A15%257D)

### 💻 Code

```ts
// Your code here

import "./styles.css";
import { IconButton } from '@mui/material'
import ContentCopyIcon from '@mui/icons-material/ContentCopy';

export default function App() {

  const handleCopyClick = (event: React.MouseEvent<HTMLElement>, id: string | null) => {
    event.stopPropagation();
    console.log('hello', id)
  }

  return (
    <div className="App">
      <IconButton onClick={(event) => handleCopyClick(event, 'id')}>
        <ContentCopyIcon />
      </IconButton>
    </div>
  );
}
```
### 🙁 Actual behavior

in `onClick={(event) => ...`, `event` is underlined with TS error 'Parameter 'event' implicitly has an 'any' type.ts(7006)'

Typing the event handler with `onClick={(event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => ...` makes this error go away

### 🙂 Expected behavior

I would expect the type of `event` to be inferred from the underlying `onClick` event handler. This was the previous behavior of Typescript.

Short of a fix to this, I would like to at least understand why this changed and why explicitly typing `event` improves type safety/robustness.

### Additional information about the issue
![image](https://github.com/user-attachments/assets/69c11b7d-e27c-41b5-8658-85188b2a1178)

ok after 8 steps, some bad, some good, this is what I got:

from what I understand 5.5.0-dev is the last "good" commit, and then comes the first bad
```

## What you have

- `/testbed/repo` is a git clone of `microsoft/TypeScript` truncated just after the regression was
  reported.  `HEAD` is `d7ff565b6c3057f844d007d5417ec84d5aafda87` and the full history behind it is present.
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
