# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Next.js plugin: metadata export in app/not-found.tsx flagged as unused

### What happened?

The Next.js plugin exempts framework-read exports on `app/**/page.tsx` and `layout.tsx` (the metadata surface and, since 3.x, route segment config like `revalidate`), but a static `metadata` export on `app/not-found.tsx` is still reported as an unused export. Next.js does consume it: the rendered 404 shell carries the title from that export.

The file itself is detected as a plugin entry point, so this looks like `not-found.tsx` missing from the special-file list that allowlists the metadata exports, rather than the file being unknown to the plugin.

### Reproduction

Three files, no install needed:

```jsonc
// package.json
{
    "name": "next-metadata-repro",
    "private": true,
    "dependencies": { "next": "16.0.0", "react": "19.0.0", "react-dom": "19.0.0" }
}
```

```tsx
// app/layout.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = { title: 'Repro' };

const RootLayout = ({ children }: { children: React.ReactNode }): React.ReactElement => (
    <html lang="en">
        <body>{children}</body>
    </html>
);

export default RootLayout;
```

```tsx
// app/page.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = { title: 'Home' };

const Home = (): React.ReactElement => <main>home</main>;

export default Home;
```

```tsx
// app/not-found.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = { title: 'Page not found' };

const NotFound = (): React.ReactElement => <main>not found</main>;

export default NotFound;
```

Run `npx fallow@3.7.1 dead-code`:

```
  3 entry points detected (3 plugin)

── Unused Code ─────────────────────────────────────

● Unused exports (1)
  app/not-found.tsx
    :3 metadata
```

The identical `metadata` exports in `layout.tsx` and `page.tsx` are correctly left alone; only the `not-found.tsx` one is flagged.

### Expected behavior

The metadata surface (`metadata`, `generateMetadata`, `viewport`, `generateViewport`) on every special file that supports it, including `not-found.tsx`, is treated as a framework-consumed entry-point export, matching the existing handling on `page.tsx` and `layout.tsx`. Worth a sweep over the other special files (`error.tsx`, `loading.tsx`, `default.tsx`, and friends) while in there, so the allowlist matches Next's actual per-file export surface.

### Fallow version

3.7.1, also reproduces on 2.86.0, so it predates the 3.x route-segment-config fix and was never covered by it.

### Operating system

macOS 15 (also seen on ubuntu-latest in CI)

### Configuration

None (no `.fallowrc.json`, default settings). Severity does not matter; it reproduces as `warn` and `error` alike.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `29308d1c2e3a4ec957e2115bd906175abf6656a8`.  There
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
{"case_id": "fallow_rs_fallow__1987__29308d1",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
