## Midterm Exam – IT3090E (Database Management Systems)  
**Date:** 23/04/2024 **Duration:** 75 min (closed book) **Student ID:** __________________ **Student Name:** __________________  

---

### Question 1 – ER Modeling & Relational Schema  
**Scenario:** *Bloodhound Coaches* operates daily services between depots, with intermediate stops. Prices are the sum of segment prices; special prices may exist between two towns, and children receive a 50 % discount. The system must support:

* Towns (some have depots) – depot telephone & street.  
* Routes (identified by a route number) – each runs between two depots and visits a sequence of stops.  
* Stops – belong to a town; a stop can be visited by many routes.  
* Segment price & travel time between any two consecutive stops (constant throughout the day).  
* Special price between two towns (override normal sum).  

#### 1.1 ER Diagram (textual description)

| Entity | Primary Key | Attributes |
|--------|--------------|------------|
| **Town** | town_id | name |
| **Depot** | depot_id | telephone, street, **FK** → Town |
| **Stop** | stop_id | **FK** → Town |
| **Route** | route_no | **FK** → Depot (origin), **FK** → Depot (destination) |
| **Route_Stop** (weak entity) | (route_no, stop_seq) | **FK** → Route, **FK** → Stop, price_to_next, time_to_next |
| **Special_Price** | (town_id₁, town_id₂) | price, applicable_to_children (boolean) |

*Relationships*  

* **Depot‑Town** – one‑to‑one (optional: a town may have a depot).  
* **Route‑Depot** – each route has exactly one origin depot and one destination depot.  
* **Route‑Stop** – many‑to‑many with ordering (`stop_seq`).  
* **Stop‑Town** – many stops belong to one town.  
* **Special_Price** – many‑to‑many between towns (symmetric).

#### 1.2 Relational Schema (derived from the ER model)

```sql
-- Town
Town( town_id PK, name );

-- Depot (optional for a town)
Depot( depot_id PK,
       town_id FK → Town.town_id,
       telephone,
       street );

-- Stop
Stop( stop_id PK,
      town_id FK → Town.town_id );

-- Route
Route( route_no PK,
       origin_depot_id FK → Depot.depot_id,
       dest_depot_id   FK → Depot.depot_id );

-- Route_Stop (ordered list of stops on a route)
Route_Stop(
    route_no   FK → Route.route_no,
    stop_seq   INT,               -- sequence number on the route
    stop_id    FK → Stop.stop_id,
    price_to_next   DECIMAL(8,2), -- price from this stop to the next stop
    time_to_next    TIME,
    PRIMARY KEY (route_no, stop_seq)
);

-- Special_Price (overrides normal sum)
Special_Price(
    town_id_1  FK → Town.town_id,
    town_id_2  FK → Town.town_id,
    price      DECIMAL(8,2),
    child_half BOOLEAN,
    PRIMARY KEY (town_id_1, town_id_2)
);
```

*Notes*  

* The price of a direct journey between two stops is obtained by summing `price_to_next` for the consecutive `Route_Stop` rows between the stops, unless a matching row exists in **Special_Price** (which takes precedence).  
* Children’s fare = `price * 0.5` when `child_half = TRUE`.  
* Queries such as “all route numbers that visit a given stop” use `SELECT route_no FROM Route_Stop WHERE stop_id = …`.

---

### Question 2 – Armstrong’s Axioms  

Relation **R(A B C D)**, FD set **F** = { AB → D;  BC → C;  AC → B;  AC → CD }  

Four additional FDs derivable from **F**:

1. **A C → D**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    