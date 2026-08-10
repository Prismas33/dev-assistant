# Setup questions

Ask only for information that is both missing from the repository and necessary for the requested setup.

## Core context

1. What is the project name, or should it remain `TBD`?
2. What kind of product is it?
3. What problem does it solve?
4. Who is it for?
5. What scope is required for the first usable version?

## Technical context

Ask only when the answer affects immediate work:

- frontend/runtime/framework;
- backend/API;
- database and migrations;
- authentication and authorization;
- hosting/environments;
- external integrations;
- test and deployment expectations.

Do not default silently to Next.js, Node.js, PostgreSQL, Supabase, Firebase, a payment provider, or a hosting provider. Use `TBD` until the user or an accepted project decision chooses them.

## Setup flow

1. Inspect existing files and extract known answers.
2. Classify the request as documentation-only or full technical setup.
3. Ask only blocking questions.
4. State the proposed responsibility split.
5. Create all applicable missing templates merge-safely.
6. Fill known content and mark genuine open decisions as `TBD`.
7. Create the first diary entry.
8. Run the documentation validator.
9. Report created, preserved, unresolved, and unvalidated items.
