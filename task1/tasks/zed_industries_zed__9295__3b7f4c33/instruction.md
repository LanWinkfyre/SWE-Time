# Locate the commit that introduced this regression

A regression was reported against `zed-industries/zed`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Wayland: BorrowMutError

### Check for existing issues

- [X] Completed

### Describe the bug / provide steps to reproduce it

Launch Zed built from latest git commit on Wayland and move mouse over the window.

### Environment

Ubuntu 24.04
GNOME Wayland

### If applicable, add mockups / screenshots to help explain present your vision of the feature

_No response_

### If applicable, attach your `~/Library/Logs/Zed/Zed.log` file to this issue.

```
Thread "main" panicked with "already borrowed: BorrowMutError" at crates/gpui/src/platform/linux/wayland/client.rs:301:56
   0: Zed::init_panic_hook::{closure#0}
             at code/zed/crates/zed/src/main.rs:598:29
   1: <alloc::boxed::Box<F,A> as core::ops::function::Fn<Args>>::call
             at /rustc/07dca489ac2d933c78d3c5158e3f43beefeb02ce/library/alloc/src/boxed.rs:2029:9
      std::panicking::rust_panic_with_hook
             at /rustc/07dca489ac2d933c78d3c5158e3f43beefeb02ce/library/std/src/panicking.rs:783:13
   2: std::panicking::begin_panic_handler::{{closure}}
             at /rustc/07dca489ac2d933c78d3c5158e3f43beefeb02ce/library/std/src/panicking.rs:657:13
   3: std::sys_common::backtrace::__rust_end_short_backtrace
             at /rustc/07dca489ac2d933c78d3c5158e3f43beefeb02ce/library/std/src/sys_common/backtrace.rs:171:18
   4: rust_begin_unwind
             at /rustc/07dca489ac2d933c78d3c5158e3f43beefeb02ce/library/std/src/panicking.rs:645:5
   5: core::panicking::panic_fmt
             at /rustc/07dca489ac2d933c78d3c5158e3f43beefeb02ce/library/core/src/panicking.rs:72:14
   6: core::cell::panic_already_borrowed
             at /rustc/07dca489ac2d933c78d3c5158e3f43beefeb02ce/library/core/src/cell.rs:761:5
   7: <core::cell::RefCell<gpui::platform::linux::wayland::client::CursorState>>::borrow_mut
             at /rustc/07dca489ac2d933c78d3c5158e3f43beefeb02ce/library/core/src/cell.rs:1051:25
      <gpui::platform::linux::wayland::client::WaylandClient as gpui::platform::linux::client::Client>::set_cursor_style
             at code/zed/crates/gpui/src/platform/linux/wayland/client.rs:301:56
   8: <gpui::window::WindowContext>::reset_cursor_style
             at code/zed/crates/gpui/src/window.rs:1042:13
      <gpui::window::WindowContext>::dispatch_mouse_event
             at code/zed/crates/gpui/src/window.rs:1181:13
      <gpui::window::WindowContext>::dispatch_event
             at code/zed/crates/gpui/src/window.rs:1169:13
   9: <gpui::window::Window>::new::{closure#7}::{closure#0}
             at code/zed/crates/gpui/src/window.rs:481:46
      <gpui::app::AppContext as gpui::Context>::update_window::<bool, <gpui::window::Window>::new::{closure#7}::{closure#0}>::{closure#0}
             at code/zed/crates/gpui/src/app.rs:1263:26
      <gpui::app::AppContext>::update::<core::result::Result<bool, anyhow::Error>, <gpui::app::AppContext as gpui::Context>::update_window<bool, <gpui::window::Window>::new::{closure#7}::{closure#0}>::{closure#0}>
             at code/zed/crates/gpui/src/app.rs:354:22
      <gpui::app::AppContext as gpui::Context>::update_window::<bool, <gpui::window::Window>::new::{closure#7}::{closure#0}>
             at code/zed/crates/gpui/src/app.rs:1254:9
      <gpui::app::async_context::AsyncAppContext as gpui::Context>::update_window::<bool, <gpui::window::Window>::new::{closure#7}::{closure#0}>
             at code/zed/crates/gpui/src/app/async_context.rs:70:14
      <gpui::window::AnyWindowHandle>::update::<gpui::app::async_context::AsyncAppContext, bool, <gpui::window::Window>::new::{closure#7}::{closure#0}>
             at code/zed/crates/gpui/src/window.rs:2605:9
      <gpui::window::Window>::new::{closure#7}
             at code/zed/crates/gpui/src/window.rs:481:22
  10: <alloc::boxed::Box<dyn core::ops::function::FnMut<(gpui::interactive::PlatformInput,), Output = bool>> as core::ops::function::FnMut<(gpui::interactive::PlatformInput,)>>::call_mut
             at /rustc/07dca489ac2d933c78d3c5158e3f43beefeb02ce/library/alloc/src/boxed.rs:2022:9
      <gpui::platform::linux::wayland::window::WaylandWindowState>::handle_input
             at code/zed/crates/gpui/src/platform/linux/wayland/window.rs:240:16
  11: <gpui::platform::linux::wayland::client::WaylandClientState as wayland_client::event_queue::Dispatch<wayland_client::protocol::wl_pointer::WlPointer, ()>>::event
             at code/zed/crates/gpui/src/platform/linux/wayland/client.rs:862:17
  12: wayland_client::event_queue::queue_callback::<wayland_client::protocol::wl_pointer::WlPointer, (), gpui::platform::linux::wayland::client::WaylandClientState>
             at .cargo/registry/src/index.crates.io-6f17d22bba15001f/wayland-client-0.31.2/src/event_queue.rs:656:5
  13: <wayland_client::event_queue::EventQueue<gpui::platform::linux::wayland::client::WaylandClientState>>::dispatching_impl
             at .cargo/registry/src/index.crates.io-6f17d22bba15001f/wayland-client-0.31.2/src/event_queue.rs:478:13
      <wayland_client::event_queue::EventQueue<gpui::platform::linux::wayland::client::WaylandClientState>>::dispatch_pending
             at .cargo/registry/src/index.crates.io-6f17d22bba15001f/wayland-client-0.31.2/src/event_queue.rs:384:9
      <gpui::platform::linux::wayland::client::WaylandClient>::new::{closure#1}
             at code/zed/crates/gpui/src/platform/linux/wayland/client.rs:190:23
      <core::cell::RefCell<calloop::sources::DispatcherInner<calloop_wayland_source::WaylandSource<gpui::platform::linux::wayland::client::WaylandClientState>, <gpui::platform::linux::wayland::client::WaylandClient>::new::{closure#1}>> as calloop::sources::EventDispatcher<()>>::process_events::{closure#0}
             at .cargo/registry/src/index.crates.io-6f17d22bba15001f/calloop-0.12.4/src/sources/mod.rs:327:61
      <calloop_wayland_source::WaylandSource<gpui::platform::linux::wayland::client::WaylandClientState>>::loop_callback_pending::<<core::cell::RefCell<calloop::sources::DispatcherInner<calloop_wayland_source::WaylandSource<gpui::platform::linux::wayland::client::WaylandClientState>, <gpui::platform::linux::wayland::client::WaylandClient>::new::{closure#1}>> as calloop::sources::EventDispatcher<()>>::process_events::{closure#0}>
             at .cargo/registry/src/index.crates.io-6f17d22bba15001f/calloop-wayland-source-0.2.0/src/lib.rs:245:19
      <calloop_wayland_source::WaylandSource<gpui::platform::linux::wayland::client::WaylandClientState> as calloop::sources::EventSource>::process_events::<<core::cell::RefCell<calloop::sources::DispatcherInner<calloop_wayland_source::WaylandSource<gpui::platform::linux::wayland::client::WaylandClientState>, <gpui::platform::linux::wayland::client::WaylandClient>::new::{closure#1}>> as calloop::sources::EventDispatcher<()>>::process_events::{closure#0}>
             at .cargo/registry/src/index.crates.io-6f17d22bba15001f/calloop-wayland-source-0.2.0/src/lib.rs:154:9
      <core::cell::RefCell<calloop::sources::DispatcherInner<calloop_wayland_source::WaylandSource<gpui::platform::linux::wayland::client::WaylandClientState>, <gpui::platform::linux::wayland::client::WaylandClient>::new::{closure#1}>> as calloop::sources::EventDispatcher<()>>::process_events
             at .cargo/registry/src/index.crates.io-6f17d22bba15001f/calloop-0.12.4/src/sources/mod.rs:326:9
  14: <calloop::loop_logic::EventLoop<()>>::dispatch_events
             at .cargo/registry/src/index.crates.io-6f17d22bba15001f/calloop-0.12.4/src/loop_logic.rs:445:31
      <calloop::loop_logic::EventLoop<()>>::dispatch::<core::option::Option<core::time::Duration>>
             at .cargo/registry/src/index.crates.io-6f17d22bba15001f/calloop-0.12.4/src/loop_logic.rs:559:9
  15: <calloop::loop_logic::EventLoop<()>>::run::<<gpui::platform::linux::platform::LinuxPlatform as gpui::platform::Platform>::run::{closure#0}, core::option::Option<core::time::Duration>>
             at .cargo/registry/src/index.crates.io-6f17d22bba15001f/calloop-0.12.4/src/loop_logic.rs:596:13
      <gpui::platform::linux::platform::LinuxPlatform as gpui::platform::Platform>::run
             at code/zed/crates/gpui/src/platform/linux/platform.rs:129:9
  16: <gpui::app::App>::run::<Zed::main::{closure#3}>
             at code/zed/crates/gpui/src/app.rs:142:9
      Zed::main
             at code/zed/crates/zed/src/main.rs:119:5
  17: <fn() as core::ops::function::FnOnce<()>>::call_once
             at /rustc/07dca489ac2d933c78d3c5158e3f43beefeb02ce/library/core/src/ops/function.rs:250:5
      std::sys_common::backtrace::__rust_begin_short_backtrace::<fn(), ()>
             at /rustc/07dca489ac2d933c78d3c5158e3f43beefeb02ce/library/std/src/sys_common/backtrace.rs:155:18
  18: std::rt::lang_start::<()>::{closure#0}
             at /rustc/07dca489ac2d933c78d3c5158e3f43beefeb02ce/library/std/src/rt.rs:166:18
  19: core::ops::function::impls::<impl core::ops::function::FnOnce<A> for &F>::call_once
             at /rustc/07dca489ac2d933c78d3c5158e3f43beefeb02ce/library/core/src/ops/function.rs:284:13
      std::panicking::try::do_call
             at /rustc/07dca489ac2d933c78d3c5158e3f43beefeb02ce/library/std/src/panicking.rs:552:40
      std::panicking::try
             at /rustc/07dca489ac2d933c78d3c5158e3f43beefeb02ce/library/std/src/panicking.rs:516:19
      std::panic::catch_unwind
             at /rustc/07dca489ac2d933c78d3c5158e3f43beefeb02ce/library/std/src/panic.rs:142:14
      std::rt::lang_start_internal::{{closure}}
             at /rustc/07dca489ac2d933c78d3c5158e3f43beefeb02ce/library/std/src/rt.rs:148:48
      std::panicking::try::do_call
             at /rustc/07dca489ac2d933c78d3c5158e3f43beefeb02ce/library/std/src/panicking.rs:552:40
      std::panicking::try
             at /rustc/07dca489ac2d933c78d3c5158e3f43beefeb02ce/library/std/src/panicking.rs:516:19
      std::panic::catch_unwind
             at /rustc/07dca489ac2d933c78d3c5158e3f43beefeb02ce/library/std/src/panic.rs:142:14
      std::rt::lang_start_internal
             at /rustc/07dca489ac2d933c78d3c5158e3f43beefeb02ce/library/std/src/rt.rs:148:20
  20: main
  21: __libc_start_call_main
             at ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16
  22: __libc_start_main_impl
             at ./csu/../csu/libc-start.c:360:3
  23: _start
```
```

## What you have

- `/testbed/repo` is a git clone of `zed-industries/zed` truncated just after the regression was
  reported.  `HEAD` is `a56a260778748c1309c5a30d37a917f10e56c39d` and the full history behind it is present.
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
