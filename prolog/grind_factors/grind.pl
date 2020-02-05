

grind(Query_Form, Ground_Form):-
    findall( Ground_Form, (Query_Form, not(Ground_Form)), GFList),
    forall(member(GF,GFList), assertz(GF)),
    (
        ([] = GFList) -> true ; grind(Query_Form, Ground_Form)
    ).

grind(Query_Form, Ground_Form, GroundedList):-
    grind(Query_Form, Ground_Form),
    findall(Ground_Form, Ground_Form, GroundedList).
