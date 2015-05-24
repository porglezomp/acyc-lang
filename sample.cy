data List(a) = Cons(a, List(a)) | Nil

fib n = if n == 0 then 0
        else if n == 1 then 1
        else fib(n - 1) + fib(n - 2)

fib2 n = match n for
          case if n <= 0 = 0
          case 1 = 1
          case n = fib2(n - 1) + fib2(n - 2)

fib3 n = let fib4(n, a, b) =
                match n for
                 case if n <= 0 = a
                 case 1 = b10
                 case n = fib4(n-1, b, a+b)
            in
                fib4(n, 0, 1)

data List(a) = Cons(a, List(a)) | Nil

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