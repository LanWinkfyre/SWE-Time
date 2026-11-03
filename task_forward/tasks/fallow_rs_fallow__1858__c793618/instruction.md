# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Follow-up: `unused-class-members` false positives remain in 3.4.2 — root cause is not Playwright-specific

### What happened?

### Context

Follow-up to #1791 ("function returning `.extend(...)`", fixed in 3.3.0) and the `mergeTests(...)`-in-a-function follow-up (228 → 218 findings, reportedly fixed in 3.4.2: "Playwright page-object methods used through `mergeTests()` wrapping helpers are now credited... Members reached through local subclasses, factory results, and opaque destructures are properly credited").

After upgrading `3.3.0` → `3.4.2`, our `unused-class-members` count did **not** meaningfully drop (218 → 217). Bisecting from scratch (not assuming the cause was still `mergeTests`) found a different, more general root cause that has nothing to do with Playwright, `mergeTests`, or function-wrapped fixtures: **a class-typed property read off a separately-constructed instance (`factory.someProp`), when placed as a value inside a *new* object literal, loses its member-usage credit** — at any nesting depth, in plain TypeScript, with zero Playwright/fixture involvement.

This is presumably why the "factory results... properly credited" line in the 3.4.2 changelog didn't fix our case: our factories return object literals whose properties are populated from *other* factory instances' properties/getters, not directly instantiated with `new` at the object-literal call site.

### Environment

- fallow: `3.4.2`
- node: `v24.16.0`
- typescript: `^6.0.3`
- OS: Windows 11

### Reproduction

### Reproduction (no Playwright required)

File tree (all names/data synthetic):

```
src/pages/orders-page.ts
src/fixtures/orders-invoker-factory.ts
tests/plain.spec.ts
```

**`src/pages/orders-page.ts`**

```ts
export class OrdersPage {
	async placeOrder(orderId: string): Promise<void> {
		console.log(`placing order ${orderId}`);
	}

	async cancelOrder(orderId: string): Promise<void> {
		console.log(`cancelling order ${orderId}`);
	}
}
```

**`src/fixtures/orders-invoker-factory.ts`**

```ts
import { OrdersPage } from "../pages/orders-page";

export class OrdersInvokerFactory {
	readonly ordersPage: OrdersPage = new OrdersPage();
}

// Plain function, no Playwright / .extend() / mergeTests() involved at all.
export function createOrdersUi() {
	const factory = new OrdersInvokerFactory();
	return {
		orders: factory.ordersPage, // <-- the trigger: property-read-of-a-separate-instance, re-wrapped in a new object literal
	};
}
```

**`tests/plain.spec.ts`**

```ts
import { createOrdersUi } from "../src/fixtures/orders-invoker-factory";

async function run() {
	const ui = createOrdersUi();
	await ui.orders.placeOrder("SYN-001");
	await ui.orders.cancelOrder("SYN-001");
}

void run();
```

### Steps to reproduce

1. Create the three files above in a fresh fallow project (no `@playwright/test` dependency needed).
2. Run:
   ```
   fallow dead-code --unused-class-members
   ```

### Expected behavior

### Expected result

No findings — `placeOrder` and `cancelOrder` are both called from `tests/plain.spec.ts`.

### Actual result (fallow 3.4.2)

```
unused-class-member:src/pages/orders-page.ts:2:OrdersPage.placeOrder
unused-class-member:src/pages/orders-page.ts:6:OrdersPage.cancelOrder
```

### Bisection

| Shape of `createOrdersUi()`'s return value | Result on 3.4.2 |
|---|---|
| `return { orders: new OrdersPage() }` (direct construction inside the literal) | ✅ resolves correctly |
| `const orders = new OrdersPage(); return { orders };` (local variable, then wrapped) | ✅ resolves correctly |
| `const factory = new OrdersInvokerFactory(); return factory.ordersPage;` (property read, **not** re-wrapped in a new object literal) | ✅ resolves correctly |
| `const factory = new OrdersInvokerFactory(); return { orders: factory.ordersPage };` (property read, wrapped 1 level deep) | ❌ still flagged |
| Same as above but 2 levels deep (`{ invoke: { orders: factory.ordersPage } }`, consumed as `ui.invoke.orders.placeOrder()`) | ❌ still flagged (nesting depth doesn't matter, consistent with the original bug report) |
| `factory.ordersPage` implemented as a `get ordersPage()` accessor instead of a `readonly` field | ❌ still flagged (same either way) |
| Whole scenario wrapped in a Playwright `base.extend(...)` fixture instead of a plain function | ❌ still flagged (same either way — **this confirms the bug is not Playwright-specific**) |

So the precise trigger is: **an object-literal property whose initializer is a member-expression read (`x.y`) of a separately constructed instance, where the read type is itself a project class.** Constructing directly (`new X()`) or aliasing through a local `const` both credit correctly; reading the same value off another object and re-literal-wrapping it does not.

### Real-world impact

Our actual Page-Object-Model classes are wired through per-feature "invoker/asserter factory" classes with `get` accessors (for lazy construction), and a plain function assembles those into the nested object literal a Playwright fixture then exposes:

```ts
export class BicsPortalUiInvokerFactory {
	get dashboardInvoker(): DashboardInvoker {
		return (this._dashboardInvoker ??= new DashboardInvoker(/* ... */));
	}
	// ...
}

export function createBicsPortalUi(page: Page): BicsPortalUi {
	const invokerFactory = new BicsPortalUiInvokerFactory(page, domHandlerFactory);
	return {
		invoke: {
			dashboard: invokerFactory.dashboardInvoker, // <-- exact shape of the repro above
			// ...
		},
		// ...
	};
}
```

This factory-with-getters + object-literal-assembly pattern is how essentially every Page Object class in our suite is exposed, independent of the `mergeTests`/function-wrapping issue already reported. It's why upgrading to 3.4.2 only moved our count from 218 to 217 findings — the fix that shipped doesn't cover this shape. `fallow inspect --symbol` on one of the affected classes confirms fallow does resolve the **class** as used/reachable (`"is_used": true, "reason": "Used by 2 file(s)"`), so this is specifically a member-level (not file/export-level) resolution gap.

### Suggested fix

Extend `unused-class-members` receiver-type resolution to follow a member-expression initializer (`someOtherInstance.someProperty`) the same way it already follows a direct `new ClassX()` initializer or a local `const` alias, when that value becomes an object-literal property — including when the property on the source object is a `get` accessor rather than a field.


### Fallow version

3.4.2

### Operating system

Windows

### Configuration

```toml
### `.fallowrc.json` used


{
	"entry": ["tests/**/*.spec.ts", "src/fixtures/**/*-fixture.ts"],
	"rules": {
		"unused-class-members": "error"
	}
}
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `c7936189eb0040a97190baafb7522d9a9e392ded`.  There
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
{"case_id": "fallow_rs_fallow__1858__c793618",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
