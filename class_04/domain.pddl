(define (domain BridgeCrossing)

(:types
  Side Locatable       - Object
  Torch Person         - Locatable
  LeftSide RightSide   - Side
)

(:predicates 
  ( located ?l - Locatable ?s - Side )
)

(:functions
  ( travelTimeOfLocatable ?l - Locatable )
)

(:durative-action TravelOne
  :parameters (
    ?p - Person
    ?t - Torch
    ?origin - Side
    ?destination - Side
  )
  :duration (= ?duration ( travelTimeOfLocatable ?p ))
  :condition ( and
      (at start ( located ?p ?origin ))
      (at start ( located ?t ?origin ))
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
  :duration (= ?duration ( travelTimeOfLocatable ?p1 ))
  :condition (and
      (at start ( > (travelTimeOfLocatable ?p1) (travelTimeOfLocatable ?p2)))
      (at start ( located ?p1 ?origin ))
      (at start ( located ?p2 ?origin ))
      (at start ( located ?t ?origin ))
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

)