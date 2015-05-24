# data List(a) = Cons(a, List(a)) | Nil


main () = fib2 400

fib2 n = fibhelper(n, 0, 1)
fibhelper (n, a, b) = if n == 0 then a
                      else if n == 1 then b
                      else fibhelper(n - 1, b, a + b)
fib n = if n == 0 then 0
        else if predEq (n, 1) then n
        else add (fib sub (n, 1), fib(n - 2))
predEq (a, b) = (a == b)
sub (a, b) = a - b
double n = add (n, n)
add (a, b) = a + b
square n = n * n
cube n = square n * n
qux n = n + 1 - 3 * square n
baz n = n + 1
bar n = n
foo n = 1

# fib2 n = match n for
#          case if n <= 0 = 0
#          case 1 = 1
#          case n = fib2(n - 1) + fib2(n - 2)

# fib3 n = let fib4(n, a, b) =
#                match n for
#                 case if n <= 0 = a
#                 case 1 = b10
#                 case n = fib4(n-1, b, a+b)
#            in
#                fib4(n, 0, 1)

# fib3(0) = 0
# fib3(1) = 1
# fib3(n) = fib3(n - 1) + fib3(n - 2)

# main : () -> String
# main() = format("fib({}) = {}", 3, fib(3))

# .isIn elem . Nil = False
# .isIn elem . Cons(x, xs) = if elem == x then True
#                           else elem .isIn xs

# print(x .isIn theSet)
# a :dot b