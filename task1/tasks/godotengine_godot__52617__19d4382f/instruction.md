# Locate the commit that introduced this regression

A regression was reported against `godotengine/godot`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Godot 4.0: Crash if script contains certain invalid syntax [] =

### Godot version



### System information

Linux Mint 20 - Lenovo Thinkpad & Kubuntu 21.0 - Ideapad

### Issue description

If a script contains the invalid syntax [] = (a guess someone was taking at array append syntax) and then is saved, the godot editor crashes. Attempting to load the project again will cause the editor to crash promptly.
Correcting the syntax back to .append(..) corrects the problem and the project can be loaded.

Additionally the editor does not identify the offending code as invalid by marking it in a red line.

Here is a sample of the offending code:
```
class DialogNode:
	var page_id: int
	var language: String
	
class DialogContents:
	var content : Array
	
	func add_content(content: DialogContent):
		self.content[] = content

class DialogContent:
	var type : String
	var text : String
	
	func _init(text: String, type: String = 'dialog'):
		self.set_text(text)
		self.set_type(type)
	
	func get_type():
		return type
	
	func get_text():
		return text
	
	func set_type(type: String):
		self.type = type
	
	func set_text(text: String):
		self.text = text
```


### Steps to reproduce

Using the minimal reproduction project:

1. Open Node2D.gd
2. Change line 11: `self.content.append(content)` into `self.content[] = content`
3. Save
4. The editor should crash
5. Subsequently attempting to load the project now will also crash
6. Reverting the change from a different editor will enable the project to load

### Minimal reproduction project

[ScriptBug.zip](https://github.com/godotengine/godot/files/7150356/ScriptBug.zip)



Stacktrace:
```
#0  0x00007f42eb0dbd22 in raise () from /usr/lib/libc.so.6
#1  0x00007f42eb0c5862 in abort () from /usr/lib/libc.so.6
#2  0x0000000003dac704 in handle_crash (sig=11) at platform/linuxbsd/crash_handler_linuxbsd.cpp:120
#3  <signal handler called>
#4  0x000000000427f4f1 in GDScriptCompiler::_parse_expression (this=0x7f427effbb48, codegen=..., r_error=@0x7f427effa2a4: OK, p_expression=0x0, p_root=false, p_initializer=false, p_index_addr=...)
    at modules/gdscript/gdscript_compiler.cpp:208
#5  0x00000000042868b4 in GDScriptCompiler::_parse_expression (this=0x7f427effbb48, codegen=..., r_error=@0x7f427effa2a4: OK, p_expression=0x7f427400ac40, p_root=true, p_initializer=false, p_index_addr=...)
    at modules/gdscript/gdscript_compiler.cpp:942
#6  0x000000000428d4c9 in GDScriptCompiler::_parse_block (this=0x7f427effbb48, codegen=..., p_block=0x7f4274009b40, p_add_locals=true) at modules/gdscript/gdscript_compiler.cpp:1789
#7  0x000000000428eb29 in GDScriptCompiler::_parse_function (this=0x7f427effbb48, p_script=0x7f4274013ed0, p_class=0x7f4274008e30, p_func=0x7f4274009840, p_for_ready=false)
    at modules/gdscript/gdscript_compiler.cpp:1931
#8  0x0000000004293e40 in GDScriptCompiler::_parse_class_blocks (this=0x7f427effbb48, p_script=0x7f4274013ed0, p_class=0x7f4274008e30, p_keep_state=false) at modules/gdscript/gdscript_compiler.cpp:2394
#9  0x00000000042943f9 in GDScriptCompiler::_parse_class_blocks (this=0x7f427effbb48, p_script=0x7f4274003cf0, p_class=0x7f4274007a20, p_keep_state=false) at modules/gdscript/gdscript_compiler.cpp:2490
#10 0x0000000004294b62 in GDScriptCompiler::compile (this=0x7f427effbb48, p_parser=0x7f427effbba8, p_script=0x7f4274003cf0, p_keep_state=false) at modules/gdscript/gdscript_compiler.cpp:2561
#11 0x000000000420e299 in GDScript::reload (this=0x7f4274003cf0, p_keep_state=false) at modules/gdscript/gdscript.cpp:842
#12 0x00000000041a0a9b in GDScriptCache::get_full_script (p_path=..., r_error=@0x7f427effbff4: OK, p_owner=...) at modules/gdscript/gdscript_cache.cpp:211
#13 0x000000000421b0f6 in ResourceFormatLoaderGDScript::load (this=0x9293b60, p_path=..., p_original_path=..., r_error=0x7f42740019f4, p_use_sub_threads=false, r_progress=0x7f42740019e8, 
    p_cache_mode=ResourceFormatLoader::CACHE_MODE_REUSE) at modules/gdscript/gdscript.cpp:2341
#14 0x0000000006f68c1c in ResourceLoader::_load (p_path=..., p_original_path=..., p_type_hint=..., p_cache_mode=ResourceFormatLoader::CACHE_MODE_REUSE, r_error=0x7f42740019f4, p_use_sub_threads=false, 
    r_progress=0x7f42740019e8) at core/io/resource_loader.cpp:194
#15 0x0000000006f693c6 in ResourceLoader::_thread_load_function (p_userdata=0x7f42740019b8) at core/io/resource_loader.cpp:221
#16 0x0000000006f6c7c7 in ResourceLoader::load (p_path=..., p_type_hint=..., p_cache_mode=ResourceFormatLoader::CACHE_MODE_REUSE, r_error=0x0) at core/io/resource_loader.cpp:576
#17 0x00000000045844c9 in EditorFileSystem::_scan_new_dir (this=0x9b51440, p_dir=0x7f4274001660, da=0x7f4274002e60, p_progress=...) at editor/editor_file_system.cpp:818
#18 0x00000000045828c8 in EditorFileSystem::_scan_filesystem (this=0x9b51440) at editor/editor_file_system.cpp:294
#19 0x00000000045859bd in EditorFileSystem::_thread_func (_userdata=0x9b51440) at editor/editor_file_system.cpp:324
#20 0x0000000006cc84c8 in Thread::callback (p_self=0x9b51660, p_settings=..., p_callback=0x45859a0 <EditorFileSystem::_thread_func(void*)>, p_userdata=0x9b51440) at core/os/thread.cpp:72
#21 0x0000000006cc979a in std::__invoke_impl<void, void (*)(Thread*, Thread::Settings const&, void (*)(void*), void*), Thread*, Thread::Settings, void (*)(void*), void*> (
    __f=@0x2117d988: 0x6cc8440 <Thread::callback(Thread*, Thread::Settings const&, void (*)(void*), void*)>, __args=@0x2117d968: 0x9b51440, __args=@0x2117d968: 0x9b51440, __args=@0x2117d968: 0x9b51440, 
    __args=@0x2117d968: 0x9b51440) at /usr/bin/../lib64/gcc/x86_64-pc-linux-gnu/11.1.0/../../../../include/c++/11.1.0/bits/invoke.h:61
#22 0x0000000006cc9611 in std::__invoke<void (*)(Thread*, Thread::Settings const&, void (*)(void*), void*), Thread*, Thread::Settings, void (*)(void*), void*> (
    __fn=@0x2117d988: 0x6cc8440 <Thread::callback(Thread*, Thread::Settings const&, void (*)(void*), void*)>, __args=@0x2117d968: 0x9b51440, __args=@0x2117d968: 0x9b51440, __args=@0x2117d968: 0x9b51440, 
    __args=@0x2117d968: 0x9b51440) at /usr/bin/../lib64/gcc/x86_64-pc-linux-gnu/11.1.0/../../../../include/c++/11.1.0/bits/invoke.h:96
#23 0x0000000006cc958d in std::thread::_Invoker<std::tuple<void (*)(Thread*, Thread::Settings const&, void (*)(void*), void*), Thread*, Thread::Settings, void (*)(void*), void*> >::_M_invoke<0ul, 1ul, 2ul, 3ul, 4ul> (this=0x2117d968) at /usr/bin/../lib64/gcc/x86_64-pc-linux-gnu/11.1.0/../../../../include/c++/11.1.0/bits/std_thread.h:253
#24 0x0000000006cc94f5 in std::thread::_Invoker<std::tuple<void (*)(Thread*, Thread::Settings const&, void (*)(void*), void*), Thread*, Thread::Settings, void (*)(void*), void*> >::operator() (
    this=0x2117d968) at /usr/bin/../lib64/gcc/x86_64-pc-linux-gnu/11.1.0/../../../../include/c++/11.1.0/bits/std_thread.h:260
#25 0x0000000006cc9169 in std::thread::_State_impl<std::thread::_Invoker<std::tuple<void (*)(Thread*, Thread::Settings const&, void (*)(void*), void*), Thread*, Thread::Settings, void (*)(void*), void*> > >::_M_run (this=0x2117d960) at /usr/bin/../lib64/gcc/x86_64-pc-linux-gnu/11.1.0/../../../../include/c++/11.1.0/bits/std_thread.h:211
#26 0x00007f42eb49f3c4 in std::execute_native_thread_routine (__p=0x2117d960) at /build/gcc/src/gcc/libstdc++-v3/src/c++11/thread.cc:82
#27 0x00007f42eb5fc259 in start_thread () from /usr/lib/libpthread.so.0
#28 0x00007f42eb19d5e3 in clone () from /usr/lib/libc.so.6
```
```

## What you have

- `/testbed/repo` is a git clone of `godotengine/godot` truncated just after the regression was
  reported.  `HEAD` is `5f69218edc4f4af574c7a65f077e2e0bf1f28365` and the full history behind it is present.
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
