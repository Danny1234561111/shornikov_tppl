from interpreter import Interpreter
from interpreter import Parser
kk=Interpreter()
res =kk.eval( """
            BEGIN
                y := 2;
                BEGIN
                    a := 3;
                    a := a;
                    b := 10 + a + 10 * y / 4;
                    c := a - b+b;
                    BEGIN
                        p := 7*b;
                    END;
                END;
                BEGIN
                    p := 7*15;
                END;
                x := 11;
            END.
            """)
print(res)
