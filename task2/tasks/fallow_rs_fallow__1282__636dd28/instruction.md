# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
False positives dead code for vue pinia store members consumed via storeToRefs

First of all, thank you for this beautiful library

### What happened?

For vue dead code in stores i am getting false positives if members are consumed via storeToRefs call

### Reproduction

for example 
```ts

const {
    canCreateEvents,
    canEditFloorPlans,
    canSeeAnalytics,
    canSeeDigitalMenuCards,
    canSeeGuestbook,
    canSeeInventory,
    canSeeReservationRequests,
} = storeToRefs(usePermissionsStore());
```

### Expected behavior

_No response_

### Fallow version

2.97.0

### Operating system

Linux

### Configuration

```toml
{
    "$schema": "./node_modules/fallow/schema.json",
    "entry": [
        "eslint.config.js",
        "oxlint.config.ts",
        "packages/eslint-plugin/src/index.ts",
        "packages/floor-creator-v2/scripts/check-architecture-boundaries.mjs",
        "packages/floor-creator-v2/src/index.ts",
        "packages/floor-creator-v2/vitest.benchmark.config.ts",
        "packages/frontend/src/main.ts",
        "packages/frontend/src/router/index.ts",
        "packages/frontend/src/boot/**/*",
        "packages/frontend/src/features/guests/guest-data.ts",
        "packages/frontend/public/firebase-messaging-sw.js",
        "packages/frontend/tools/check-translations.ts",
        "packages/functions/seeds/scripts/*.ts",
        "packages/functions/test-helpers/vitest-setup.ts",
        "packages/functions/src/index.ts",
        "packages/functions/src/billing-runtime.ts",
        "packages/functions/src/features/events/helpers/event-logs.ts",
        "packages/functions/src/features/reservation-requests/helpers/reservation-request-transitions.ts",
        "packages/functions/src/legal.ts",
        "packages/functions/src/legal-light.ts",
        "packages/functions/src/plan.ts",
        "packages/functions/src/user-capabilities.ts",
        "packages/functions/src/utils/index.ts",
        "packages/functions/src/utils/inventory-utils.ts",
        "packages/functions/src/utils/widget-utils.ts",
        "packages/types/src/index.ts"
    ],
    "ignorePatterns": [
        "**/*.d.ts",
        "**/coverage/**",
        "**/dist/**",
        "**/dist-esbuild/**",
        "**/lib/**",
        "**/node_modules/**",
        "**/playwright-report/**",
        "**/test-utils/**",
        "**/test-results/**",
        ".firebase/**",
        ".fallow/**",
        ".idea/**",
        "docs/**",
        "firebase-export-*/**",
        "local-db/**",
        "packages/frontend/src/css/breakpoints.scss",
        "packages/frontend/src/css/mixins.scss",
        "packages/frontend/src/features/menu-cards/components/menu-form-shared.scss",
        "packages/frontend/src/features/venue/components/settings/_venue-settings.scss",
        "packages/frontend/src/styles/settings.scss"
    ],
    "ignoreDependencies": [
        "@firetable/floor-creator-v2",
        "@firetable/functions",
        "@firetable/types",
        "@shared-types/auth.js",
        "@shared-types/event.js",
        "@shared-types/firebase.js",
        "@shared-types/floor.js",
        "@shared-types/guest.js",
        "@shared-types/index.js",
        "@shared-types/organisation.js",
        "@shared-types/venue.js",
        "register-service-worker",
        "src",
        "workbox-core"
    ],
    "ignoreExportsUsedInFile": true,
    "publicPackages": [
        "@firetable/eslint-plugin",
        "@firetable/floor-creator-v2",
        "@firetable/functions",
        "@firetable/types"
    ],
    "production": {
        "deadCode": true,
        "dupes": true,
        "health": false
    },
    "includeEntryExports": true,
    "rules": {
        "boundary-violation": "error",
        "circular-dependencies": "error",
        "coverage-gaps": "error",
        "duplicate-exports": "error",
        "feature-flags": "error",
        "private-type-leaks": "off",
        "stale-suppressions": "error",
        "test-only-dependencies": "error",
        "type-only-dependencies": "error",
        "unlisted-dependencies": "error",
        "unresolved-imports": "error",
        "unused-class-members": "error",
        "unused-dependencies": "error",
        "unused-dev-dependencies": "error",
        "unused-enum-members": "error",
        "unused-exports": "error",
        "unused-files": "error",
        "unused-optional-dependencies": "error",
        "unused-types": "error"
    },
    "duplicates": {
        "mode": "semantic",
        "minTokens": 80,
        "minLines": 8,
        "threshold": 0,
        "ignoreImports": true,
        "ignore": [
            "**/*.spec.ts",
            "**/test-helpers/**",
            "**/seeds/**",
            "**/tools/**",
            "packages/frontend/src/i18n/**",
            "packages/functions/src/i18n/**",
            "packages/functions/src/legal/copy.ts",
            "packages/types/src/**",
            "packages/floor-creator-v2/src/entities/**",
            "packages/floor-creator-v2/src/editor/**",
            "packages/floor-creator-v2/src/rendering/renderers/**",
            "packages/floor-creator-v2/src/metadata/**",
            "packages/floor-creator-v2/src/typedefs.ts",
            "packages/floor-creator-v2/src/entity-registry-bootstrap.ts",
            "packages/floor-creator-v2/src/filters.ts",
            "packages/floor-creator-v2/src/input-manager.ts",
            "packages/floor-creator-v2/src/services/entity-property-handlers.ts",
            "packages/floor-creator-v2/src/services/handles/**",
            "packages/floor-creator-v2/src/services/scene-entity-operation-service.ts",
            "packages/frontend/src/features/billing/components/BillingDocumentsPanel.vue",
            "packages/frontend/src/features/billing/components/OrganisationBillingSection.vue",
            "packages/frontend/src/features/events/ai/poster-ai-service.ts",
            "packages/frontend/src/features/events/components/event-timeline/ReservationBlock.vue",
            "packages/frontend/src/features/events/composables/useReservationDrag.ts",
            "packages/frontend/src/features/events/composables/useReservationTransfers.ts",
            "packages/frontend/src/features/events/pages/PageAdminReservationRequests.vue",
            "packages/frontend/src/features/events/pages/PageManageEvent.vue",
            "packages/frontend/src/features/events/reservation-events.ts",
            "packages/frontend/src/features/floors/components/FloorEditorTableLayoutPanel.vue",
            "packages/frontend/src/features/floors/components/FloorEditorUI.vue",
            "packages/frontend/src/features/floors/composables/useFloorEditorTools.ts",
            "packages/frontend/src/features/inventory/db/db-stock-operations.ts",
            "packages/frontend/src/features/inventory/helpers/inventory-translations.ts",
            "packages/frontend/src/features/inventory/pages/PageAdminInventory.vue",
            "packages/frontend/src/features/inventory/types.ts",
            "packages/frontend/src/features/legal/pages/PageLegalDpa.vue",
            "packages/frontend/src/features/legal/pages/PageLegalTerms.vue",
            "packages/frontend/src/features/menu-cards/helpers/export-menu-card.ts",
            "packages/frontend/src/features/menu-cards/helpers/menu-card-enhancement.ts",
            "packages/frontend/src/features/public-reservation-manage/db.ts",
            "packages/frontend/src/features/system-admin/components/EmailCampaignsCampaignsTab.vue",
            "packages/frontend/src/features/system-admin/components/EmailCampaignsTemplatesTab.vue",
            "packages/frontend/src/features/venue/helpers/venue-translations.ts",
            "packages/frontend/src/features/widget/components/WidgetStepTime.vue",
            "packages/frontend/src/features/widget/db.ts",
            "packages/frontend/src/helpers/timezone-helpers.ts",
            "packages/frontend/src/router/route-names.ts",
            "packages/frontend/src/router/routes.ts",
            "packages/functions/src/features/events/helpers/demo-event-data-generator.ts",
            "packages/functions/src/features/inventory/helpers/build-movement-data.ts",
            "packages/functions/src/features/organisations/billing/callables/billing-checkout-session-idempotency-store.ts",
            "packages/functions/src/features/organisations/billing/callables/request-manual-billing.ts",
            "packages/functions/src/features/organisations/billing/helpers/billing-mutation-helpers.ts",
            "packages/functions/src/features/organisations/billing/services/billing-support-notification-service.ts",
            "packages/functions/src/features/organisations/billing/webhooks/stripe-webhook-projector.ts",
            "packages/functions/src/features/organisations/callables/trial-organisation-provisioning.ts",
            "packages/functions/src/features/reservation-requests/callables/cancel-reservation.ts",
            "packages/functions/src/features/reservation-requests/callables/handle-change-request.ts",
            "packages/functions/src/features/widget/callables/update-reservation.ts",
            "packages/functions/src/features/widget/callables/widget-utils.ts",
            "packages/functions/src/legal/types.ts",
            "packages/functions/src/paths.ts",
            "packages/functions/src/services/reservation-notification-service.ts"
        ]
    },
    "health": {
        "maxCyclomatic": 20,
        "maxCognitive": 15,
        "maxCrap": 70,
        "ignore": [
            "**/*.spec.ts",
            "**/test-helpers/**",
            "**/seeds/**",
            "**/tools/**",
            "**/public/firebase-messaging-sw.js"
        ],
        "suggestInlineSuppression": true
    },
    "overrides": [
        {
            "files": ["**/test-helpers/**"],
            "rules": {
                "unused-exports": "off",
                "unused-files": "off"
            }
        },
        {
            "files": ["packages/frontend/src/**/*.vue"],
            "rules": {
                "unused-types": "off"
            }
        },
        {
            "files": [
                "packages/frontend/src/features/venue/components/settings/*.vue",
                "packages/frontend/src/features/venue/pages/PageManageVenueSettings.vue"
            ],
            "rules": {
                "unresolved-imports": "off"
            }
        },
        {
            "files": ["packages/frontend/src/logger/BaseLogger.ts"],
            "rules": {
                "unused-class-members": "off"
            }
        }
    ],
    "regression": {
        "baseline": {
            "totalIssues": 0,
            "unusedFiles": 0,
            "unusedExports": 0,
            "unusedTypes": 0,
            "unusedDependencies": 0,
            "unusedDevDependencies": 0,
            "unusedOptionalDependencies": 0,
            "unusedEnumMembers": 0,
            "unusedClassMembers": 0,
            "unresolvedImports": 0,
            "unlistedDependencies": 0,
            "duplicateExports": 0,
            "circularDependencies": 0,
            "typeOnlyDependencies": 0,
            "testOnlyDependencies": 0,
            "boundaryViolations": 0
        }
    }
}
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `636dd2896aef22fa6c1f33f0de931508d4dab6e9`.  There
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
{"case_id": "fallow_rs_fallow__1282__636dd28",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
