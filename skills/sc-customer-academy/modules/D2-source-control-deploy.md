# D2. Source control, deployment and rollback

**Track 2 · 90 min · your development and test environments · Uses:** clio package commands, git

## Why it matters

A package in development is only half the job. To run Creatio like software you need its source in version control,
a repeatable way to install it in test and production, and a way back when something goes wrong. clio gives you the
commands; this module turns them into your release routine, and teaches Claude to follow it.

## Lab

1. **Pull the team package** from development into a local folder with clio, with Claude explaining each command
   before it runs. Look at what's inside (objects, pages, data, descriptor).
2. **Put it in git:** a repository for your Creatio packages, a first commit, and a short README: what the package
   is, its dependencies, how to install it.
3. **Make a change** in development (a business builder's B4 change is perfect), pull again, and read the git diff
   with Claude. This is the review step: someone other than the builder reads it.
4. **Install to test** with clio. Claude says what it will do and you confirm. Then test the change in test as a user.
5. **Rollback rehearsal:** with Claude, write the rollback for this release (install the previous version from git,
   or remove the change) and try it in test.
6. **Write your routine** in ten lines: pull, commit, review, install to test, test, approve, install to production
   (by whom, when), rollback.

## Check

- [ ] The package is in git with a README, and a reviewed change is committed.
- [ ] The change was installed in test and checked there.
- [ ] A rollback was rehearsed in test, and the routine is written.

## Watch out for

- **Building directly in test or production** "because it's quicker": everything starts in development.
- **Mixing a package pulled from the server with a local workspace copy** of the same package can overwrite server
  changes. Keep one source of truth per package.
- **Compiles and restarts** affect everyone on that environment. Claude asks first; schedule them for production.
- **A green install isn't a tested release:** test as a user before approving.

## For the facilitator

- Use their git host and naming. If they already have CI, show where clio commands fit; don't build a pipeline in the session.
- Production installs are their IT's call; never run one in the course.
