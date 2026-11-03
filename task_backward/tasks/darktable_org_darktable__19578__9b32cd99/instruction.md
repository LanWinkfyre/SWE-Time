# Locate the commit that introduced this regression

A regression was reported against `darktable-org/darktable`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Crash on current master

With current master I get a crash when doing:
- on darkroom copy part history, select one module
- move to next image (press space)
- do a paste part, press ok
- All good... (sometimes it crashes here)
- Now do an undo Ctrl-Z
- And darktable crash with a memory corruption

I have tracked this down into Lua... Don't make sense to me, but with the following hack I don't have a crash anymore:

```
diff --git a/src/lua/call.c b/src/lua/call.c
index 3ea1b71ef3..7578c6b352 100644
--- a/src/lua/call.c
+++ b/src/lua/call.c
@@ -296,6 +296,7 @@ static void alien_job_destroy(void *data_ptr)
 
 static gboolean alien_job_dispatch (GSource* source, GSourceFunc callback, gpointer user_data)
 {
+  if(1) return TRUE;
   gpointer message;
   message = g_async_queue_try_pop (darktable.lua_state.alien_job_queue);
   if(message == NULL)
@@ -730,4 +731,3 @@ int dt_lua_init_call(lua_State *L)
 // vim: shiftwidth=2 expandtab tabstop=2 cindent
 // kate: tab-indents: off; indent-width 2; replace-tabs on; indent-mode cstyle; remove-trailing-spaces modified;
 // clang-format on
```

I won't have time to work on that on the next 48h, so beware of this issue.

@wpferguson : Maybe you have an idea about what is going wrong?

@TurboGit git bisect returns
```

## What you have

- `/testbed/repo` is a git clone of `darktable-org/darktable` truncated just after the regression was
  reported.  `HEAD` is `73ced28ae0d86504808d3bd2d9a0f8b5e084c448` and the full history behind it is present.
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
