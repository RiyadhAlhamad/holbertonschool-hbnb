---
config:
  theme: neo-dark
  look: handDrawn
  layout: elk
---
flowchart TD
 subgraph subGraph0["Presentation Layer"]
        A["ServiceAPI &lt;&gt;"]
  end
 subgraph subGraph1["Business Logic Layer"]
        B["Facade"]
        C["User"]
        D["Place"]
        E["Review"]
        F["Amenity"]
  end
 subgraph subGraph2["Persistence Layer"]
        G["DBStorage"]
  end
    A --> B
    B --> C & D & E & F & G
