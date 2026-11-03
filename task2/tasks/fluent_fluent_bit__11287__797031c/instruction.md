# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
geoip2 :The lookup path does not match the data

## Bug Report

**Describe the bug**
cannot get subdivision from geoip2 filter

**To Reproduce**
```
pipeline:
    inputs:
        - name: dummy
          dummy: '{"remote_addr": "171.217.41.222"}'

    filters:
        - name: geoip2
          match: '*'
          database: GeoLite2-City.mmdb
          lookup_key: remote_addr
          # https://github.com/jclo/jgeoip
          record:
              - country      remote_addr %{country.names.zh-CN}
              - province     remote_addr %{subdivision.0.names.en}
              - city         remote_addr %{city.names.zh-CN}

    outputs:
        - name: stdout
          match: '*'

```
output:
```
{"remote_addr"=>"171.217.41.222", "country"=>"中国", "province"=>nil, "city"=>"成都"}
```
the province is incorrect.  The compelete data is :
```
{
  continent: {
    code: 'AS',
    geonameId: 6255147,
    names: {
      de: 'Asien',
      en: 'Asia',
      es: 'Asia',
      fr: 'Asie',
      ja: 'アジア',
      'pt-BR': 'Ásia',
      ru: 'Азия',
      'zh-CN': '亚洲'
    }
  },
  country: {
    geonameId: 1814991,
    isoCode: 'CN',
    names: {
      de: 'China',
      en: 'China',
      es: 'China',
      fr: 'Chine',
      ja: '中国',
      'pt-BR': 'China',
      ru: 'Китай',
      'zh-CN': '中国'
    }
  },
  maxmind: undefined,
  registeredCountry: {
    geonameId: 1814991,
    isoCode: 'CN',
    names: {
      de: 'China',
      en: 'China',
      es: 'China',
      fr: 'Chine',
      ja: '中国',
      'pt-BR': 'China',
      ru: 'Китай',
      'zh-CN': '中国'
    },
    isInEuropeanUnion: false
  },
  representedCountry: undefined,
  traits: {
    isAnonymous: false,
    isAnonymousProxy: false,
    isAnonymousVpn: false,
    isAnycast: false,
    isHostingProvider: false,
    isLegitimateProxy: false,
    isPublicProxy: false,
    isResidentialProxy: false,
    isSatelliteProvider: false,
    isTorExitNode: false,
    ipAddress: '171.217.41.222',
    network: '171.217.0.0/17'
  },
  city: {
    geonameId: 1815286,
    names: {
      de: 'Chengdu',
      en: 'Chengdu',
      es: 'Chengdú',
      fr: 'Chengdu',
      ja: '成都市',
      'pt-BR': 'Chengdu',
      ru: 'Чэнду',
      'zh-CN': '成都'
    }
  },
  location: {
    accuracyRadius: 10,
    latitude: 30.6667,
    longitude: 104.0667,
    timeZone: 'Asia/Shanghai'
  },
  postal: undefined,
  subdivisions: [
    {
      geonameId: 1794299,
      isoCode: 'SC',
      names: {
        de: 'Sichuan',
        en: 'Sichuan',
        es: 'Sichuan',
        fr: 'Sichuan',
        'pt-BR': 'Sujuão',
        ru: 'Сычуань',
        'zh-CN': '四川'
      }
    }
  ]
}
```

**Expected behavior**
```
{"remote_addr"=>"171.217.41.222", "country"=>"中国", "province"=>"Sichuan", "city"=>"成都"}
```

**Screenshots**
<!--- If applicable, add screenshots to help explain your problem. -->

**Your Environment**
<!--- Include as many relevant details about the environment you experienced the bug in -->
* Version used:
* Configuration: 4.2.0
* Environment name and version (e.g. Kubernetes? What version?): docker 4.2.0
* Server type and version:
* Operating System and version: mac m3 pro
* Filters and plugins:
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `797031cc30d2845b4dcb36cece6d6f2dd363d430`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `master`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "fluent_fluent_bit__11287__797031c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
