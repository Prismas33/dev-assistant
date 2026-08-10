# Modular architecture by responsibility

## Decision rule

Create a module when a responsibility can change, be tested, or be replaced independently. Do not decide decomposition from a fixed line count.

## Expected boundaries

| Responsibility | Typical location |
| --- | --- |
| Route metadata and composition | `app/**/page.*`, `layout.*`, route entrypoint |
| Independent visual section | `features/<feature>/components/` |
| Shared visual primitive | `components/ui/` |
| Shared layout | `components/layout/` |
| Interaction state | `features/<feature>/hooks/` or `store/` |
| UI-triggered operation | `features/<feature>/actions/` or `mutations/` |
| Data read/composition | `features/<feature>/queries/` |
| Business rule/use case | `features/<feature>/services/` |
| Persistence/provider access | `features/<feature>/repositories/` or infrastructure client |
| Boundary validation | `features/<feature>/schemas/` |
| Domain contracts | `features/<feature>/types/` |
| Non-trivial transformation | feature `helpers/`; shared `lib/` only when transversal |
| Configuration/constants | explicitly named configuration/constant files |

Not every feature needs every directory. Create only layers backed by real responsibilities.

## Entrypoint rule

Entrypoints may receive route parameters, load or delegate data, choose metadata, wire dependencies, and compose imported modules. They must not contain several complete visual sections plus complex state, persistence, validation, and business rules.

```tsx
import { CommunityHero } from '@/features/community/components/community-hero'
import { CommunityHighlights } from '@/features/community/components/community-highlights'
import { getCommunityPageData } from '@/features/community/queries/get-community-page-data'

export default async function CommunityPage() {
  const data = await getCommunityPageData()

  return (
    <>
      <CommunityHero />
      <CommunityHighlights items={data.highlights} />
    </>
  )
}
```

## Review gate

- Does the file have one primary responsibility?
- Is the entrypoint limited to composition and light orchestration?
- Are independent visual sections components?
- Is complex state outside presentation components?
- Are data, validation, and business rules separated from UI?
- Are persistence and external SDKs isolated?
- Can responsibilities be tested and changed independently?
- Do extracted files represent real boundaries rather than artificial fragmentation?

If a relevant answer is no, reorganize before considering the implementation complete.
