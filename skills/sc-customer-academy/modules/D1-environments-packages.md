# D1. Environments, packages and who changes what

**Track 2 · 75 min · your development environment · Uses:** the toolkit's environment setup, clio, Creatio packages

## Why it matters

With Claude, business builders can change Creatio quickly. That's good only if IT can still answer three questions
at any time: **where** a change was made, **what** it consists of, and **how** it gets to production. In Creatio the
answer is packages: every change lives in a package, packages depend on other packages, and packages move between
environments. This module sets up the structure the business builders' work lands in.

## Lab

1. **Map your environments:** with Claude, list what you have (development, test, production) and who may change
   each. Agree the rule: builders work in development only; test and production change only by release.
2. **Read the package landscape** in development (read-only): which packages are installed, which are locked
   (product and installed apps), which are yours. Ask Claude to explain dependencies for one package.
3. **Create your team's package** with a clear name and its dependencies, and make it the place builders' changes
   go. Ask Claude how to make it the current package for new work.
4. **Find a business builder's change** from Track 1 (or make a small one) and confirm, with Claude, which package
   it landed in. If it landed anywhere else, that's the finding of the day: fix the setup.
5. **Locked packages:** ask Claude why installed-app packages are read-only, and when unlocking one is (rarely)
   acceptable. Write your team's rule.

## Check

- [ ] A written environment map with who changes what.
- [ ] Your team package exists with its dependencies, and a new change lands in it.
- [ ] You can explain, for one package, what it depends on and why.

## Watch out for

- **Changes landing in a package nobody chose** (an automatic or default package). Check the current package before
  the first change of every session.
- **Unlocking a product package to "just fix it"**: the fix is lost or conflicts on the next update.
- **Deleting a package removes everything in it.** Delete only by exact name, after listing it, and never a package
  you didn't create. (In one real incident, deleting by name removed two packages that shared a name.)

## For the facilitator

- Bring their IT's existing release process into the room; this module adapts to it, it doesn't replace it.
- If they have only one environment (production), stop: they need a development or sandbox environment first. That's
  a commercial question for the AE.
