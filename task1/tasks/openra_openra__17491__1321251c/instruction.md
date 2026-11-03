# Locate the commit that introduced this regression

A regression was reported against `OpenRA/OpenRA`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Render initialization fails when launching with Graphics.PreferGLES=false

Running bleed with this argument `Graphics.PreferGLES=false` results in an renderer intialization failure (judging by the console output). On Windows 7 this causes two game windows to appear - one of them is stuck and doesn't render anything, the other one runs the game fine. Closing one of the windows also terminates the other. On Ubuntu 19.10 this straight up crashes the game regardless if  `Graphics.PreferGLES` is `true` or `false`.



Double window:
![изображение](https://user-images.githubusercontent.com/1355810/71322779-0bed7700-24d4-11ea-9ffb-40811f3b5230.png)

Console output on Windows:

<details>

```
Platform is Windows
Engine version is {DEV_VERSION}
Using SDL 2 with OpenGL ES renderer
Desktop resolution: 1920x1200
Using resolution: 1024x768
Using window scale 1,00
OpenGL version: OpenGL ES 3.0 335.23
Renderer initialization failed. Check graphics.log for details.
Using SDL 2 with OpenGL renderer
Desktop resolution: 1920x1200
Using resolution: 1024x768
Using window scale 1,00
OpenGL version: 3.2.0
Using default sound device
```

</details>

`graphics.log` on Windows:

<details>

```
GL Info Log:
0(88) : error C7011: implicit cast from "int" to "float"
0(90) : error C7011: implicit cast from "ivec2" to "vec2"

System.InvalidProgramException: Compile error in shader object 'D:\ivaylo\code\OpenRA\glsl\combined.frag'
   at OpenRA.Platforms.Default.Shader.CompileShaderObject(Int32 type, String name)
   at OpenRA.Platforms.Default.Shader..ctor(String name)
   at OpenRA.Platforms.Default.Sdl2GraphicsContext.CreateShader(String name)
   at OpenRA.Renderer..ctor(IPlatform platform, GraphicSettings graphicSettings)
   at OpenRA.Game.Initialize(Arguments args)
```

</details>

Console output on Ubuntu:

<details>

```
Platform is Linux
Engine version is {DEV_VERSION}
Using SDL 2 with OpenGL ES renderer
Desktop resolution: 1366x768
Using resolution: 1140x700
Using window scale 1,00
OpenGL version: OpenGL ES 3.2 Mesa 19.2.1
Renderer initialization failed. Check graphics.log for details.
Using SDL 2 with OpenGL ES renderer
Desktop resolution: 1366x768
Using resolution: 1140x700
Using window scale 1,00
OpenGL version: OpenGL ES 3.2 Mesa 19.2.1
Renderer initialization failed. Check graphics.log for details.
Exception of type `System.InvalidOperationException`: Failed to initialize platform-integration library. Check graphics.log for details.
  at OpenRA.Game.Initialize (OpenRA.Arguments args) [0x0015d] in <14184c368a4f41a18d3c747f4b307929>:0 
  at OpenRA.Game.InitializeAndRun (System.String[] args) [0x00006] in <14184c368a4f41a18d3c747f4b307929>:0 
  at OpenRA.Program.Main (System.String[] args) [0x00044] in <14184c368a4f41a18d3c747f4b307929>:0 
```
</details>

`graphics.log` on Ubuntu:

<details>

```
GL Info Log:
0:88(6): error: could not implicitly convert operands to relational operator
0:88(6): error: if-statement condition must be scalar boolean
0:90(2): error: initializer of type ivec2 cannot be assigned to variable of type vec2

System.InvalidProgramException: Compile error in shader object '/home/ivaylo/code/OpenRA/glsl/combined.frag'
  at OpenRA.Platforms.Default.Shader.CompileShaderObject (System.Int32 type, System.String name) [0x00137] in <5016eaa07668473294ead7b0a84676ea>:0 
  at OpenRA.Platforms.Default.Shader..ctor (System.String name) [0x00034] in <5016eaa07668473294ead7b0a84676ea>:0 
  at OpenRA.Platforms.Default.Sdl2GraphicsContext.CreateShader (System.String name) [0x00006] in <5016eaa07668473294ead7b0a84676ea>:0 
  at OpenRA.Platforms.Default.ThreadedGraphicsContext+<>c__DisplayClass22_0.<RenderThread>b__9 (System.Object name) [0x00000] in <5016eaa07668473294ead7b0a84676ea>:0 
  at OpenRA.Platforms.Default.ThreadedGraphicsContext+Message.Execute () [0x000ad] in <5016eaa07668473294ead7b0a84676ea>:0 
--- End of stack trace from previous location where exception was thrown ---

  at OpenRA.Platforms.Default.ThreadedGraphicsContext+Message.Result () [0x00033] in <5016eaa07668473294ead7b0a84676ea>:0 
  at OpenRA.Platforms.Default.ThreadedGraphicsContext.RunMessage (OpenRA.Platforms.Default.ThreadedGraphicsContext+Message message) [0x00007] in <5016eaa07668473294ead7b0a84676ea>:0 
  at OpenRA.Platforms.Default.ThreadedGraphicsContext.Send[T] (System.Func`2[T,TResult] method, System.Object state) [0x00024] in <5016eaa07668473294ead7b0a84676ea>:0 
  at OpenRA.Platforms.Default.ThreadedGraphicsContext.CreateShader (System.String name) [0x00000] in <5016eaa07668473294ead7b0a84676ea>:0 
  at OpenRA.Renderer..ctor (OpenRA.IPlatform platform, OpenRA.GraphicSettings graphicSettings) [0x0009e] in <14184c368a4f41a18d3c747f4b307929>:0 
  at OpenRA.Game.Initialize (OpenRA.Arguments args) [0x001ff] in <14184c368a4f41a18d3c747f4b307929>:0 
GL Info Log:
0:88(6): error: could not implicitly convert operands to relational operator
0:88(6): error: if-statement condition must be scalar boolean
0:90(2): error: initializer of type ivec2 cannot be assigned to variable of type vec2

System.InvalidProgramException: Compile error in shader object '/home/ivaylo/code/OpenRA/glsl/combined.frag'
  at OpenRA.Platforms.Default.Shader.CompileShaderObject (System.Int32 type, System.String name) [0x00137] in <5016eaa07668473294ead7b0a84676ea>:0 
  at OpenRA.Platforms.Default.Shader..ctor (System.String name) [0x00034] in <5016eaa07668473294ead7b0a84676ea>:0 
  at OpenRA.Platforms.Default.Sdl2GraphicsContext.CreateShader (System.String name) [0x00006] in <5016eaa07668473294ead7b0a84676ea>:0 
  at OpenRA.Platforms.Default.ThreadedGraphicsContext+<>c__DisplayClass22_0.<RenderThread>b__9 (System.Object name) [0x00000] in <5016eaa07668473294ead7b0a84676ea>:0 
  at OpenRA.Platforms.Default.ThreadedGraphicsContext+Message.Execute () [0x000ad] in <5016eaa07668473294ead7b0a84676ea>:0 
--- End of stack trace from previous location where exception was thrown ---

  at OpenRA.Platforms.Default.ThreadedGraphicsContext+Message.Result () [0x00033] in <5016eaa07668473294ead7b0a84676ea>:0 
  at OpenRA.Platforms.Default.ThreadedGraphicsContext.RunMessage (OpenRA.Platforms.Default.ThreadedGraphicsContext+Message message) [0x00007] in <5016eaa07668473294ead7b0a84676ea>:0 
  at OpenRA.Platforms.Default.ThreadedGraphicsContext.Send[T] (System.Func`2[T,TResult] method, System.Object state) [0x00024] in <5016eaa07668473294ead7b0a84676ea>:0 
  at OpenRA.Platforms.Default.ThreadedGraphicsContext.CreateShader (System.String name) [0x00000] in <5016eaa07668473294ead7b0a84676ea>:0 
  at OpenRA.Renderer..ctor (OpenRA.IPlatform platform, OpenRA.GraphicSettings graphicSettings) [0x0009e] in <14184c368a4f41a18d3c747f4b307929>:0 
  at OpenRA.Game.Initialize (OpenRA.Arguments args) [0x001ff] in <14184c368a4f41a18d3c747f4b307929>:0 
```

</details>
```

## What you have

- `/testbed/repo` is a git clone of `OpenRA/OpenRA` truncated just after the regression was
  reported.  `HEAD` is `bb85146544b85b4be8a3514cfed06f68d4b42f46` and the full history behind it is present.
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
