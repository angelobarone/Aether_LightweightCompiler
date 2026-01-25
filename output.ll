; ModuleID = "main_module"
target triple = "x86_64-pc-linux-gnu"
target datalayout = ""

declare i64 @"print"(i64 %".1")

define i64 @"main"()
{
entry:
  %"a" = alloca i64
  store i64 10, i64* %"a"
  %"b" = alloca i64
  store i64 5, i64* %"b"
  %"a.1" = load i64, i64* %"a"
  %"b.1" = load i64, i64* %"b"
  %"addtmp" = add i64 %"a.1", %"b.1"
  %"multmp" = mul i64 %"addtmp", 2
  %"res" = alloca i64
  store i64 %"multmp", i64* %"res"
  %"res.1" = load i64, i64* %"res"
  %"calltmp" = call i64 @"print"(i64 %"res.1")
  %"i" = alloca i64
  store i64 0, i64* %"i"
  %"__repeat_counter_0" = alloca i64
  store i64 0, i64* %"__repeat_counter_0"
  br label %"while_cond"
while_cond:
  %"__repeat_counter_0.1" = load i64, i64* %"__repeat_counter_0"
  %"cmptmp" = icmp slt i64 %"__repeat_counter_0.1", 3
  %"bool_cast" = zext i1 %"cmptmp" to i64
  %".8" = icmp ne i64 %"bool_cast", 0
  br i1 %".8", label %"while_body", label %"while_after"
while_body:
  %"i.1" = load i64, i64* %"i"
  %"calltmp.1" = call i64 @"print"(i64 %"i.1")
  %"i.2" = load i64, i64* %"i"
  %"addtmp.1" = add i64 %"i.2", 1
  store i64 %"addtmp.1", i64* %"i"
  %"__repeat_counter_0.2" = load i64, i64* %"__repeat_counter_0"
  %"addtmp.2" = add i64 %"__repeat_counter_0.2", 1
  store i64 %"addtmp.2", i64* %"__repeat_counter_0"
  br label %"while_cond"
while_after:
  ret i64 0
}
