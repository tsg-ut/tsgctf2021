# Intended solutions
The idea of the problem is inspired by std::vec of TSGCTF 2020. In C++'s foreach, changing the object that is iterated leads to undefined behavior. So how about other languages?

In C#'s foreach, it also leads [undefined behavior](https://docs.microsoft.com/en-us/dotnet/api/system.collections.generic.list-1.foreach?view=net-5.0#remarks). So I researched the source code of dotnet core in order to make the PoC.

Reading the source code and I found the line that throw the exception [here](https://github.com/dotnet/runtime/blob/87b928ab37d2b1fa2b7aeec93a76190e23a0bf61/src/libraries/System.Private.CoreLib/src/System/Collections/Generic/List.cs#L1136).  `_version` is how many times the list object is changed but its type is int so it can be overflow! So my intended solution is like below.

```
for (ulong i = 0; i < (1UL<<32)-2UL; ++i) {
                    a.Clear();
                }
                a.Add(9);
                a.Add(10);
```

# Unintended sols during contest

During the contest, only one team sent my intended solution and the others sent one of two unintended solutions described below.

## create another class instance

One of the unintended solutions that was received during contest is that create another instance of Program() and modify the list in field outside it's method.

## Using GetType() to create instances of arbitrary class 

The other is that using GetType(), which is the method of Object(), to create instances what is needed to get flag. 
