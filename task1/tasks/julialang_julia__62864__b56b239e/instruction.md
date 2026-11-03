# Locate the commit that introduced this regression

A regression was reported against `JuliaLang/julia`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
ConcurrencyViolationError reachable by REPL completions



```julia
julia> using REPL; function f(inline; k=1); @nospecialize(inline); end;
       let s = "Base.uncompressed_ast(which(Core.kwcall, (NamedTuple{(:k,), Tuple{Int}}, typeof(f), Any))).inli"
       REPL.REPLCompletions.completions(s, length(s))
       end
ERROR: ConcurrencyViolationError("Vector has invalid state. Don't modify internal fields incorrectly, or resize without correct locks")
Stacktrace:
     [1] _growend_internal!(a::Vector{Any}, delta::Int64, len::Int64)
       @ Base array.jl:1199
     [2] _growend!(a::Vector{Any}, delta::Int64)
       @ Base array.jl:1239 [inlined]
     [3] push!(a::Vector{Any}, x::Core.CodeInstance)
       @ Base array.jl:1389 [inlined]
     [4] add_one_edge!(edges::Vector{Any}, edge::Core.CodeInstance)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/stmtinfo.jl:323
     [5] _add_edges_impl(edges::Vector{Any}, info::Compiler.MethodMatchInfo, mi_edge::Bool)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/stmtinfo.jl:265
     [6] _add_edges_impl(edges::Vector{Any}, info::Compiler.MethodMatchInfo)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/stmtinfo.jl:238 [inlined]
     [7] add_edges_impl(edges::Vector{Any}, info::Compiler.MethodMatchInfo)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/stmtinfo.jl:185
     [8] add_edges!(edges::Vector{Any}, info::Compiler.CallInfo)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/types.jl:711
     [9] compute_edges!(sv::Compiler.InferenceState{REPL.REPLCompletions.REPLInterpreter})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/typeinfer.jl:908
    [10] finishinfer!(me::Compiler.InferenceState{…}, interp::REPL.REPLCompletions.REPLInterpreter, cycleid::Int64, opt_cache::IdDict{…})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/typeinfer.jl:751
    [11] finish_nocycle(interp::REPL.REPLCompletions.REPLInterpreter, frame::Compiler.InferenceState{…}, time_before::UInt64)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/typeinfer.jl:303
    [12] typeinf(interp::REPL.REPLCompletions.REPLInterpreter, frame::Compiler.InferenceState{REPL.REPLCompletions.REPLInterpreter})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:5107
    [13] const_prop_call(interp::REPL.REPLCompletions.REPLInterpreter, mi::Core.MethodInstance, result::Compiler.MethodCallResult, arginfo::Compiler.ArgInfo, sv::Compiler.InferenceState{…}, concrete_eval_result::Nothing)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:1529
    [14] abstract_call_method_with_const_args(interp::REPL.REPLCompletions.REPLInterpreter, result::Compiler.MethodCallResult, f::Any, arginfo::Compiler.ArgInfo, si::Compiler.StmtInfo, match::Core.MethodMatch, sv::Compiler.InferenceState{…}, invokecall::Nothing)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:986
    [15] abstract_call_method_with_const_args(interp::REPL.REPLCompletions.REPLInterpreter, result::Compiler.MethodCallResult, f::Any, arginfo::Compiler.ArgInfo, si::Compiler.StmtInfo, match::Core.MethodMatch, sv::Compiler.InferenceState{…})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:954 [inlined]
    [16] (::Compiler.var"#handle1#abstract_call_gf_by_type##1"{…})(interp::REPL.REPLCompletions.REPLInterpreter, sv::Compiler.InferenceState{…})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:205
    [17] doworkloop(interp::REPL.REPLCompletions.REPLInterpreter, sv::Compiler.InferenceState{REPL.REPLCompletions.REPLInterpreter})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/inferencestate.jl:1532
    [18] typeinf(interp::REPL.REPLCompletions.REPLInterpreter, frame::Compiler.InferenceState{REPL.REPLCompletions.REPLInterpreter})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:5091
    [19] const_prop_call(interp::REPL.REPLCompletions.REPLInterpreter, mi::Core.MethodInstance, result::Compiler.MethodCallResult, arginfo::Compiler.ArgInfo, sv::Compiler.InferenceState{…}, concrete_eval_result::Nothing)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:1529
    [20] abstract_call_method_with_const_args(interp::REPL.REPLCompletions.REPLInterpreter, result::Compiler.MethodCallResult, f::Any, arginfo::Compiler.ArgInfo, si::Compiler.StmtInfo, match::Core.MethodMatch, sv::Compiler.InferenceState{…}, invokecall::Nothing)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:986
    [21] abstract_call_method_with_const_args(interp::REPL.REPLCompletions.REPLInterpreter, result::Compiler.MethodCallResult, f::Any, arginfo::Compiler.ArgInfo, si::Compiler.StmtInfo, match::Core.MethodMatch, sv::Compiler.InferenceState{…})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:954 [inlined]
    [22] (::Compiler.var"#handle1#abstract_call_gf_by_type##1"{…})(interp::REPL.REPLCompletions.REPLInterpreter, sv::Compiler.InferenceState{…})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:205
    [23] (::Compiler.var"#infercalls#abstract_call_gf_by_type##0"{…})(interp::REPL.REPLCompletions.REPLInterpreter, sv::Compiler.InferenceState{…})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:274
    [24] abstract_call_gf_by_type(interp::REPL.REPLCompletions.REPLInterpreter, func::Any, arginfo::Compiler.ArgInfo, si::Compiler.StmtInfo, atype::Any, vtypes::Vector{…}, sv::Compiler.InferenceState{…}, max_methods::Int64)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:369
    [25] abstract_call_known(interp::REPL.REPLCompletions.REPLInterpreter, f::Any, arginfo::Compiler.ArgInfo, si::Compiler.StmtInfo, vtypes::Vector{…}, sv::Compiler.InferenceState{…}, max_methods::Int64)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:3082
    [26] abstract_call(interp::REPL.REPLCompletions.REPLInterpreter, arginfo::Compiler.ArgInfo, si::Compiler.StmtInfo, vtypes::Vector{…}, sv::Compiler.InferenceState{…}, max_methods::Int64)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:3233
    [27] abstract_call(interp::REPL.REPLCompletions.REPLInterpreter, arginfo::Compiler.ArgInfo, si::Compiler.StmtInfo, vtypes::Vector{…}, sv::Compiler.InferenceState{…})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:3226 [inlined]
    [28] abstract_call(interp::REPL.REPLCompletions.REPLInterpreter, arginfo::Compiler.ArgInfo, sstate::Compiler.StatementState, sv::Compiler.InferenceState{…})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:3372 [inlined]
    [29] abstract_eval_call(interp::REPL.REPLCompletions.REPLInterpreter, e::Expr, sstate::Compiler.StatementState, sv::Compiler.InferenceState{…})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:3390
    [30] abstract_eval_statement_expr(interp::REPL.REPLCompletions.REPLInterpreter, e::Expr, sstate::Compiler.StatementState, sv::Compiler.InferenceState{…})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:3817
    [31] abstract_eval_basic_statement(interp::REPL.REPLCompletions.REPLInterpreter, stmt::Any, sstate::Compiler.StatementState, frame::Compiler.InferenceState{…}, result::Nothing)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:4284 [inlined]
    [32] abstract_eval_basic_statement(interp::REPL.REPLCompletions.REPLInterpreter, stmt::Any, sstate::Compiler.StatementState, frame::Compiler.InferenceState{…})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:4246 [inlined]
    [33] typeinf_local(interp::REPL.REPLCompletions.REPLInterpreter, frame::Compiler.InferenceState{…}, nextresult::Compiler.CurrentState)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:4827
    [34] typeinf(interp::REPL.REPLCompletions.REPLInterpreter, frame::Compiler.InferenceState{REPL.REPLCompletions.REPLInterpreter})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:5100
    [35] const_prop_call(interp::REPL.REPLCompletions.REPLInterpreter, mi::Core.MethodInstance, result::Compiler.MethodCallResult, arginfo::Compiler.ArgInfo, sv::Compiler.InferenceState{…}, concrete_eval_result::Nothing)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:1529
    [36] abstract_call_method_with_const_args(interp::REPL.REPLCompletions.REPLInterpreter, result::Compiler.MethodCallResult, f::Any, arginfo::Compiler.ArgInfo, si::Compiler.StmtInfo, match::Core.MethodMatch, sv::Compiler.InferenceState{…}, invokecall::Nothing)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:986
    [37] abstract_call_method_with_const_args(interp::REPL.REPLCompletions.REPLInterpreter, result::Compiler.MethodCallResult, f::Any, arginfo::Compiler.ArgInfo, si::Compiler.StmtInfo, match::Core.MethodMatch, sv::Compiler.InferenceState{…})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:954 [inlined]
    [38] (::Compiler.var"#handle1#abstract_call_gf_by_type##1"{…})(interp::REPL.REPLCompletions.REPLInterpreter, sv::Compiler.InferenceState{…})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:205
    [39] (::Compiler.var"#infercalls#abstract_call_gf_by_type##0"{…})(interp::REPL.REPLCompletions.REPLInterpreter, sv::Compiler.InferenceState{…})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:274
    [40] abstract_call_gf_by_type(interp::REPL.REPLCompletions.REPLInterpreter, func::Any, arginfo::Compiler.ArgInfo, si::Compiler.StmtInfo, atype::Any, vtypes::Vector{…}, sv::Compiler.InferenceState{…}, max_methods::Int64)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:369
    [41] abstract_call_unknown(interp::REPL.REPLCompletions.REPLInterpreter, ft::Any, arginfo::Compiler.ArgInfo, si::Compiler.StmtInfo, vtypes::Vector{…}, sv::Compiler.InferenceState{…}, max_methods::Int64)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:3220
    [42] abstract_call(interp::REPL.REPLCompletions.REPLInterpreter, arginfo::Compiler.ArgInfo, si::Compiler.StmtInfo, vtypes::Vector{…}, sv::Compiler.InferenceState{…}, max_methods::Int64)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:3230
    [43] (::Compiler.var"#infercalls#abstract_apply##0"{…})(interp::REPL.REPLCompletions.REPLInterpreter, sv::Compiler.InferenceState{…})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:2138
    [44] abstract_apply(interp::REPL.REPLCompletions.REPLInterpreter, argtypes::Vector{…}, si::Compiler.StmtInfo, vtypes::Vector{…}, sv::Compiler.InferenceState{…}, max_methods::Int64)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:2158
    [45] abstract_call_known(interp::REPL.REPLCompletions.REPLInterpreter, f::Any, arginfo::Compiler.ArgInfo, si::Compiler.StmtInfo, vtypes::Vector{…}, sv::Compiler.InferenceState{…}, max_methods::Int64)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:2962
    [46] abstract_call(interp::REPL.REPLCompletions.REPLInterpreter, arginfo::Compiler.ArgInfo, si::Compiler.StmtInfo, vtypes::Vector{…}, sv::Compiler.InferenceState{…}, max_methods::Int64)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:3233
    [47] abstract_call(interp::REPL.REPLCompletions.REPLInterpreter, arginfo::Compiler.ArgInfo, si::Compiler.StmtInfo, vtypes::Vector{…}, sv::Compiler.InferenceState{…})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:3226 [inlined]
    [48] abstract_call(interp::REPL.REPLCompletions.REPLInterpreter, arginfo::Compiler.ArgInfo, sstate::Compiler.StatementState, sv::Compiler.InferenceState{…})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:3372 [inlined]
    [49] abstract_eval_call(interp::REPL.REPLCompletions.REPLInterpreter, e::Expr, sstate::Compiler.StatementState, sv::Compiler.InferenceState{…})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:3390
    [50] abstract_eval_statement_expr(interp::REPL.REPLCompletions.REPLInterpreter, e::Expr, sstate::Compiler.StatementState, sv::Compiler.InferenceState{…})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:3817
    [51] abstract_eval_basic_statement(interp::REPL.REPLCompletions.REPLInterpreter, stmt::Any, sstate::Compiler.StatementState, frame::Compiler.InferenceState{…}, result::Nothing)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:4284 [inlined]
    [52] abstract_eval_basic_statement(interp::REPL.REPLCompletions.REPLInterpreter, stmt::Any, sstate::Compiler.StatementState, frame::Compiler.InferenceState{…})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:4246 [inlined]
    [53] typeinf_local(interp::REPL.REPLCompletions.REPLInterpreter, frame::Compiler.InferenceState{…}, nextresult::Compiler.CurrentState)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:4827
    [54] typeinf(interp::REPL.REPLCompletions.REPLInterpreter, frame::Compiler.InferenceState{REPL.REPLCompletions.REPLInterpreter})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:5100
    [55] const_prop_call(interp::REPL.REPLCompletions.REPLInterpreter, mi::Core.MethodInstance, result::Compiler.MethodCallResult, arginfo::Compiler.ArgInfo, sv::Compiler.InferenceState{…}, concrete_eval_result::Nothing)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:1529
    [56] abstract_call_method_with_const_args(interp::REPL.REPLCompletions.REPLInterpreter, result::Compiler.MethodCallResult, f::Any, arginfo::Compiler.ArgInfo, si::Compiler.StmtInfo, match::Core.MethodMatch, sv::Compiler.InferenceState{…}, invokecall::Nothing)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:986
    [57] abstract_call_method_with_const_args(interp::REPL.REPLCompletions.REPLInterpreter, result::Compiler.MethodCallResult, f::Any, arginfo::Compiler.ArgInfo, si::Compiler.StmtInfo, match::Core.MethodMatch, sv::Compiler.InferenceState{…})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:954 [inlined]
    [58] (::Compiler.var"#handle1#abstract_call_gf_by_type##1"{…})(interp::REPL.REPLCompletions.REPLInterpreter, sv::Compiler.InferenceState{…})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:205
    [59] (::Compiler.var"#infercalls#abstract_call_gf_by_type##0"{…})(interp::REPL.REPLCompletions.REPLInterpreter, sv::Compiler.InferenceState{…})
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:274
    [60] abstract_call_gf_by_type(interp::REPL.REPLCompletions.REPLInterpreter, func::Any, arginfo::Compiler.ArgInfo, si::Compiler.StmtInfo, atype::Any, vtypes::Vector{…}, sv::Compiler.InferenceState{…}, max_methods::Int64)
       @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:369
 ┌  [61] abstract_call_known(interp::REPL.REPLCompletions.REPLInterpreter, f::Any, arginfo::Compiler.ArgInfo, si::Compiler.StmtInfo, vtypes::Vector{…}, sv::Compiler.InferenceState{…}, max_methods::Int64)
 │     @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:3082
 ├  [62] abstract_call(interp::REPL.REPLCompletions.REPLInterpreter, arginfo::Compiler.ArgInfo, si::Compiler.StmtInfo, vtypes::Vector{…}, sv::Compiler.InferenceState{…}, max_methods::Int64)
 │     @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:3233
 ├  [63] abstract_call(interp::REPL.REPLCompletions.REPLInterpreter, arginfo::Compiler.ArgInfo, si::Compiler.StmtInfo, vtypes::Vector{…}, sv::Compiler.InferenceState{…})
 │     @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:3226 [inlined]
 ├  [64] abstract_call(interp::REPL.REPLCompletions.REPLInterpreter, arginfo::Compiler.ArgInfo, sstate::Compiler.StatementState, sv::Compiler.InferenceState{…})
 │     @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:3372 [inlined]
 ├  [65] abstract_eval_call(interp::REPL.REPLCompletions.REPLInterpreter, e::Expr, sstate::Compiler.StatementState, sv::Compiler.InferenceState{…})
 │     @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:3390
 ├  [66] abstract_eval_statement_expr(interp::REPL.REPLCompletions.REPLInterpreter, e::Expr, sstate::Compiler.StatementState, sv::Compiler.InferenceState{…})
 │     @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:3817
 ├  [67] abstract_eval_basic_statement(interp::REPL.REPLCompletions.REPLInterpreter, stmt::Any, sstate::Compiler.StatementState, frame::Compiler.InferenceState{…}, result::Nothing)
 │     @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:4284 [inlined]
 ├  [68] abstract_eval_basic_statement(interp::REPL.REPLCompletions.REPLInterpreter, stmt::Any, sstate::Compiler.StatementState, frame::Compiler.InferenceState{…})
 │     @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:4246 [inlined]
 ├  [69] typeinf_local(interp::REPL.REPLCompletions.REPLInterpreter, frame::Compiler.InferenceState{…}, nextresult::Compiler.CurrentState)
 │     @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:4827
 ├  [70] typeinf(interp::REPL.REPLCompletions.REPLInterpreter, frame::Compiler.InferenceState{REPL.REPLCompletions.REPLInterpreter})
 │     @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:5100
 ├  [71] const_prop_call(interp::REPL.REPLCompletions.REPLInterpreter, mi::Core.MethodInstance, result::Compiler.MethodCallResult, arginfo::Compiler.ArgInfo, sv::Compiler.InferenceState{…}, concrete_eval_result::Nothing)
 │     @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:1529
 ├  [72] abstract_call_method_with_const_args(interp::REPL.REPLCompletions.REPLInterpreter, result::Compiler.MethodCallResult, f::Any, arginfo::Compiler.ArgInfo, si::Compiler.StmtInfo, match::Core.MethodMatch, sv::Compiler.InferenceState{…}, invokecall::Nothing)
 │     @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:986
 ├  [73] abstract_call_method_with_const_args(interp::REPL.REPLCompletions.REPLInterpreter, result::Compiler.MethodCallResult, f::Any, arginfo::Compiler.ArgInfo, si::Compiler.StmtInfo, match::Core.MethodMatch, sv::Compiler.InferenceState{…})
 │     @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:954 [inlined]
 ├  [74] (::Compiler.var"#handle1#abstract_call_gf_by_type##1"{…})(interp::REPL.REPLCompletions.REPLInterpreter, sv::Compiler.InferenceState{…})
 │     @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:205
 ├  [75] doworkloop(interp::REPL.REPLCompletions.REPLInterpreter, sv::Compiler.InferenceState{REPL.REPLCompletions.REPLInterpreter})
 │     @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/inferencestate.jl:1532
 ├  [76] typeinf(interp::REPL.REPLCompletions.REPLInterpreter, frame::Compiler.InferenceState{REPL.REPLCompletions.REPLInterpreter})
 │     @ Compiler ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/Compiler/src/abstractinterpretation.jl:5091
 ├  [77] repl_eval_ex(ex::Any, context_module::Module; limit_aggressive_inference::Bool)
 │     @ REPL.REPLCompletions ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/stdlib/v1.14/REPL/src/REPLCompletions.jl:796
 ├  [78] repl_eval_ex(ex::Any, context_module::Module)
 │     @ REPL.REPLCompletions ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/stdlib/v1.14/REPL/src/REPLCompletions.jl:769 [inlined]
 ├  [79] complete_symbol!(suggestions::Vector{…}, prefix::Any, name::String, context_module::Module; complete_modules_only::Bool, shift::Bool)
 │     @ REPL.REPLCompletions ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/stdlib/v1.14/REPL/src/REPLCompletions.jl:190
 ├  [80] completions(string::String, pos::Int64, context_module::Module, shift::Bool, hint::Bool)
 │     @ REPL.REPLCompletions ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/stdlib/v1.14/REPL/src/REPLCompletions.jl:1275
 ╰────── repeated 2 times
   [101] completions(string::String, pos::Int64)
       @ REPL.REPLCompletions ~/.julia/juliaup/julia-nightly/Julia-1.14.app/Contents/Resources/julia/share/julia/stdlib/v1.14/REPL/src/REPLCompletions.jl:1123
   [102] top-level scope
       @ REPL[1]:3
Some type information was truncated. Use `show(err)` to see complete types.
```

Segfaults if repeated.
```

## What you have

- `/testbed/repo` is a git clone of `JuliaLang/julia` truncated just after the regression was
  reported.  `HEAD` is `c9c281e7938df9c5ec82ea6758966755fabb7127` and the full history behind it is present.
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
