(define (problem instance) (:domain BridgeCrossing)
(:objects
    a b c d t - Locatable
    a b c d - Person
    t - Torch
    leftSide - Side
    rightSide - Side
)

(:init
    ( located a leftSide )
    ( located b leftSide )
    ( located c leftSide )
    ( located d leftSide )
    ( located t leftSide )
    (= ( travelTimeOfLocatable a ) 1)
    (= ( travelTimeOfLocatable b ) 2)
    (= ( travelTimeOfLocatable c ) 5)
    (= ( travelTimeOfLocatable d ) 10)
    (= ( travelTimeOfLocatable t ) 0)
)

(:goal (and
        ( located a rightSide )
        ( located b rightSide )
        ( located c rightSide )
        ( located d rightSide )
        ( located t rightSide )
    )
)

(:metric minimize ( total-time ))
)
