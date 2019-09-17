(define (domain BridgeCrossing)

(:types
  Side Locatable       - Object
  Torch Person         - Locatable
  LeftSide RightSide   - Side
)

(:functions
  ( travelTime ?p - Person ?l - Locatable )
)

(:durative-action TravelOne
  :parameters (
    ?p - Person
    ?t - Torch
    ?origin - Side
    ?destination - Side
  )
  :duration (= ? duration ( travelTime ?p1 ?t ))
  :precondition (and (
    (at start ( located ?p ?origin ))
    (at start ( located ?t ?origin ))
    )
  )
  :effect ( and
    (at start ( not ( located ?p ?origin )))
    (at start ( not ( located ?t ?origin )))
    (at end ( located ?p ?destination ))
    (at end ( located ?t ?destination ))
    )
)

(:durative-action Travel
  :parameters (
    ?p2 - Person
    ?p1 - Person
    ?t - Torch
    ?origin - Side
    ?destination - Side
  )
  :duration (= ? duration ( travelTime ?p1 ?p2 ))
  :precondition (and (
    (at start ( located ?p1 ?origin ))
    (at start ( located ?p2 ?origin ))
    (at start ( located ?t ?origin ))
    )
  )
  :effect ( and
    (at start ( not ( located ?p1 ?origin )))
    (at start ( not ( located ?p2 ?origin )))
    (at start ( not ( located ?t ?origin )))
    (at end ( located ?p1 ?destination ))
    (at end ( located ?p2 ?destination ))
    (at end ( located ?t ?destination ))
    )
)

(:predicates
  ( located ?l - Locatable ?a - Side )
)
)