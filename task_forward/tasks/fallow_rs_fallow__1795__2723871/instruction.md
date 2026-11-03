# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Follow-up: `unused-class-members` false positives remain in 3.3.0 for `mergeTests(...)` wrapped in a function

### What happened?

Follow-up to #1791 ("`unused-class-members` false positives when a Playwright fixture is exported as a function returning `.extend(...)` instead of a `const`"), which is fixed in 3.3.0 — thank you. However, after upgrading I'm still seeing a large number of `unused-class-members` findings (218 in our repo, down from 228).

I bisected the remainder with a minimal repro: 3.3.0 correctly resolves a function that returns `base.extend(...)`, but **not** a function that returns `mergeTests(...)`. Since `mergeTests` is how we compose our API and UI fixtures into one E2E fixture, this is exactly the pattern used everywhere in our test suite, so the fix didn't move the needle on our largest source of false positives.

### Environment

- fallow: `3.3.0`
- node: `v24.16.0`
- `@playwright/test`: `^1.60.0`
- typescript: `^6.0.3`
- OS: Windows 11

### Reproduction

All names/data below are synthetic. File tree:

```
src/pages/orders-page.ts
src/pages/billing-page.ts
src/fixtures/orders/orders-base-fixture.ts
src/fixtures/orders/orders-fixture.ts
src/fixtures/billing/billing-base-fixture.ts
src/fixtures/billing/billing-fixture.ts
src/fixtures/checkout/checkout-fixture.ts
tests/checkout.spec.ts
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

**`src/pages/billing-page.ts`**

```ts
export class BillingPage {
	async openInvoice(invoiceId: string): Promise<void> {
		console.log(`opening invoice ${invoiceId}`);
	}
}
```

**`src/fixtures/orders/orders-base-fixture.ts`**

```ts
import { test as base } from "@playwright/test";
import { OrdersPage } from "../../pages/orders-page";

export type OrdersUi = {
	invoke: {
		orders: OrdersPage;
	};
};

export type OrdersUiFixtures = {
	ordersUi: OrdersUi;
};

export const ordersBaseFixture = base.extend<OrdersUiFixtures>({
	ordersUi: async ({}, use) => {
		await use({ invoke: { orders: new OrdersPage() } });
	},
});
```

**`src/fixtures/orders/orders-fixture.ts`**

```ts
import { ordersBaseFixture } from "./orders-base-fixture";

export function ordersUiTest() {
	return ordersBaseFixture.extend({});
}
```

**`src/fixtures/billing/billing-base-fixture.ts`**

```ts
import { test as base } from "@playwright/test";
import { BillingPage } from "../../pages/billing-page";

export type BillingFixtures = {
	billing: BillingPage;
};

export const billingBaseFixture = base.extend<BillingFixtures>({
	billing: async ({}, use) => {
		await use(new BillingPage());
	},
});
```

**`src/fixtures/billing/billing-fixture.ts`**

```ts
import { billingBaseFixture } from "./billing-base-fixture";

export function billingTest() {
	return billingBaseFixture.extend({});
}
```

**`src/fixtures/checkout/checkout-fixture.ts`**

```ts
import { mergeTests } from "@playwright/test";
import { billingTest } from "../billing/billing-fixture";
import { ordersUiTest } from "../orders/orders-fixture";

// Function returning mergeTests(...) - this is the part that's still unresolved.
export function checkoutTest() {
	const merge = mergeTests(billingTest(), ordersUiTest());
	return merge;
}
```

**`tests/checkout.spec.ts`**

```ts
import { checkoutTest } from "../src/fixtures/checkout/checkout-fixture";

checkoutTest()(
	"places and cancels an order, opens an invoice",
	async ({ ordersUi, billing }) => {
		await ordersUi.invoke.orders.placeOrder("SYN-001");
		await ordersUi.invoke.orders.cancelOrder("SYN-001");
		await billing.openInvoice("SYN-INV-001");
	},
);
```

### Steps to reproduce

1. Create the files above in a fresh Playwright + fallow project.
2. Run:
   ```
   fallow dead-code --unused-class-members
   ```


### Expected behavior

### Expected result

No findings — `placeOrder`, `cancelOrder`, and `openInvoice` are all called from `checkout.spec.ts`.

### Actual result (fallow 3.3.0)

```
unused-class-member:src/pages/billing-page.ts:2:BillingPage.openInvoice
unused-class-member:src/pages/orders-page.ts:2:OrdersPage.placeOrder
unused-class-member:src/pages/orders-page.ts:6:OrdersPage.cancelOrder
```

### What I checked to isolate this from the already-fixed case

| Fixture shape | Result on 3.3.0 |
|---|---|
| `export const x = base.extend(...)`, used as `x(title, cb)` | ✅ resolves correctly |
| `export function x() { return base.extend(...) }`, used as `x()(title, cb)` | ✅ resolves correctly (this was the original bug, now fixed) |
| `export const x = mergeTests(a, b)`, used as `x(title, cb)` | ✅ resolves correctly |
| `export function x() { return mergeTests(a, b) }`, used as `x()(title, cb)` | ❌ still flagged (this issue) |

So specifically: `mergeTests(...)` resolves fine as a direct `const`, and a plain `.extend(...)` resolves fine wrapped in a function — but `mergeTests(...)` wrapped in a function does not, regardless of whether `a`/`b` are themselves consts or function-wrapped fixtures.

### Real-world impact

Our actual composition looks like this (synthetic names, same shape as the repro above):

```ts
export function apiTest() {
	return apiBaseFixture.extend({ /* ... */ });
}

export function uiTest(user: Role = Role.User) {
	return uiBaseFixture.extend({ /* ... */ });
}

export function e2eTest() {
	const merge = mergeTests(apiTest(), uiTest());
	return merge;
}
```

```ts
// spec file
e2eTest()("cancels an order", async ({ shopUi }) => {
	await shopUi.invoke.orders.openOrdersPage();
	await shopUi.invoke.orders.cancelOrder({ /* ... */ });
});
```

Nearly every one of our end-to-end specs goes through `e2eTest()`, since that's the fixture that gives access to both API setup and UI page objects. As a result the fix in 3.3.0 didn't reduce our false-positive count much: we went from 228 to 218 `unused-class-members` findings, and the remaining ones are still overwhelmingly the UI Page-Object-Model classes reached exclusively through `e2eTest()`.

### Suggested fix

Extend whatever resolution was added for "function returning `.extend(...)`" to also follow a function's `return` through a `mergeTests(...)` call (including when its arguments are themselves function calls, e.g. `mergeTests(fnA(), fnB())`).

### Fallow version

3.3.0

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

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2723871c33b6fb591227b2b09bf3a99b3af47da1`.  There
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
{"case_id": "fallow_rs_fallow__1795__2723871",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
