# Technical Pixel-Art Systems Research for an AI-Driven Game Asset and Rendering Pipeline

## Evidence audit and corrections to the proposed framework

The four areas in the brief are technically useful, but the research does **not** support every game-specific attribution as originally stated. For an AI agent, this distinction matters: undocumented assumptions should not become “facts” that the agent later reproduces as engine requirements.

| Proposed claim                                                                      | Research finding                                                                                                                                                                                                                                                                                                     |                    Confidence | What the AI agent should retain                                                                           |
|-------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------:|-----------------------------------------------------------------------------------------------------------|
| *Noita* treats world pixels as simulated material cells                             | Strongly documented. Nolla describes the game as a falling-sand system based on “complex cellular automata”; its GDC presentation specifically covers scaling that simulation and coupling it to destructible rigid bodies. citeturn16search0turn20view4                                                         |                 **Very high** | Per-cell simulation, material rules, dirty chunks, spatially phased multithreading, rigid-body conversion |
| *Noita* uses 64×64 chunks and a four-phase checkerboard-like threading scheme       | Explicitly described by Petri Purho/Nolla: 64×64 chunks, dirty rectangles, four update rounds, and cross-shaped exclusive update domains extending 32 pixels from a chunk. citeturn20view0                                                                                                                        |                 **Very high** | This is one of the most valuable directly documented architectural patterns                               |
| Every *Noita* pixel separately stores density, flammability, melting point, etc.    | **Not established.** The material rules are documented, but that does not imply every cell duplicates every material property. citeturn20view4turn20view5                                                                                                                                                        | **Low for the storage claim** | Store immutable material properties in a material table and only mutable state per cell                   |
| *Noita* couples changing pixel material to rigid bodies                             | Explicitly documented: rigid-body pixels know their body membership and local position, and damaged shapes can be recalculated or split. citeturn20view3                                                                                                                                                          |                 **Very high** | Occupancy grid ↔ contour/components ↔ rigid body bridge                                                   |
| *Metal Slug Attack Reloaded* specifically uses hierarchical skeletal sprite mapping | I found **no first-party technical source establishing this**. SNK describes the title as retaining the franchise's detailed 2D pixel-art presentation, but does not document this runtime animation architecture. citeturn14search0                                                                              |                **Unverified** | Treat modular hierarchical sprite rigs as a useful *general technique*, not as confirmed SNK technology   |
| Modern large sprites primarily solve an old “sprite-sheet memory cap”               | Too simplistic. Modern engines still face texture memory and maximum texture-size constraints, but modularization is also about reuse, animation authoring, batching, variants, and reducing duplicated raster data. Sprite atlases can reduce GPU draw calls. citeturn18view5                                    |                      **High** | Optimize storage **and** render state, draw calls, transforms, texture locality, authoring                |
| *Arco* specifically uses the described sub-pixel color-shifting method              | *Arco*'s official material confirms Franek Nowotniak as its pixel artist, but I found no primary technical description identifying this exact technique. citeturn17search0turn17search3                                                                                                                          |                **Unverified** | Use *Arco* as visual reference, not as proof of implementation                                            |
| *Owlboy*'s artist works with “sub-pixelling”                                        | Directly supported. Simon Stafsnes Andersen discusses choosing colors that pair effectively for anti-aliasing and “sub-pixelling,” and describes studying sprite animation frame-by-frame to understand contortions and shading. citeturn19view0turn19view2                                                      |                      **High** | Palette-aware edge transitions, cluster manipulation, shading-based motion cues                           |
| *Eastward* is purely 2D with normal maps                                            | **Incorrect.** Lead programmer Tommo Zhou explicitly describes *Eastward* as “a 3D game with a 2D perspective.” Assets are separated by structure, rebuilt in a 3D environment, and hand-painted with bump-map information; the custom engine also uses shader textures and lighting. citeturn19view3turn19view5 |                 **Very high** | Treat *Eastward* as a 2D/3D hybrid or 2.5D pixel-lighting reference                                       |
| Normal mapping automatically makes 2D sprites cast physically correct shadows       | Incorrect. A normal map changes **surface response to light**; shadow casting requires an occluder representation, depth/height information, shadow geometry, or another visibility calculation. Modern 2D renderers expose normal maps separately from shadow/lighting systems. citeturn15search1                |                 **Very high** | Keep normal response and occlusion/shadow casting as separate systems                                     |

The most important architectural conclusion is therefore that these are **four different forms of “pixel manipulation,” operating at four different levels**:

| Level                | System                    | Pixel is treated as…                                                                  |
|----------------------|---------------------------|---------------------------------------------------------------------------------------|
| Simulation           | Falling-sand CA           | A stateful world cell                                                                 |
| Object animation     | Modular sprite rig        | A texel belonging to a transformable part                                             |
| Perceptual animation | Sub-pixel / micro-shading | A discrete sample whose temporal color/occupancy creates apparent fractional movement |
| Rendering            | Normal-mapped lighting    | A surface sample with color, orientation, masks, and potentially depth                |

An AI agent should never collapse these into one generic “pixel animation” mechanism. They have radically different state representations, update frequencies, authoring requirements, and failure modes.

## Cellular automata, material simulation, and destructible pixel worlds

The *Noita* architecture is the best-documented of the four examples. Petri Purho's GDC session explicitly covers scaling a falling-sand simulation into a large continuous world and integrating it with destructible rigid-body physics. Nolla's technical explanation describes the world as complex cellular automata in which simple local pixel rules combine to produce emergent behavior. citeturn16search0turn20view4

The essential insight is that **the rendered pixel is not the fundamental object**. The fundamental object is a *simulation cell*. Its appearance is a consequence of its material and state.

A practical cell representation for an AI-generated engine should look closer to this:

```cpp
struct Cell {
    uint16_t materialId;       // Index into shared MaterialDefinition table
    int16_t  temperature;      // Mutable only if thermal simulation is required
    uint16_t lifetime;         // Fire, steam, temporary reaction, etc.
    uint16_t bodyId;           // 0 = CA/free material; otherwise rigid-body owner
    uint8_t  flags;            // burning, active, updated, electrically charged...
    uint8_t  variant;          // visual/noise variant
};

struct MaterialDefinition {
    MaterialClass behavior;    // Empty, Static, Powder, Liquid, Gas...
    float density;
    float ignitionTemperature;
    float meltingTemperature;
    float boilingTemperature;
    uint16_t meltProduct;
    uint16_t burnProduct;
    uint16_t freezeProduct;
    uint32_t behaviorFlags;    // flammable, corrosive, conductive...
};
```

This is a better architecture than storing density, melting point, flammability, and all other immutable properties independently in every cell. The published *Noita* material examples establish that density and reaction behavior affect updates, but do not establish redundant copies of those properties in each cell. citeturn20view4turn20view5 The shared-definition design above is therefore a **recommended implementation derived from the documented behavior**, rather than a claim about Nolla's exact memory layout.

### Local movement rules

Purho gives remarkably simple examples. Liquids attempt to move downward and then laterally; density comparisons allow different liquids to displace one another. Gas behavior can invert the preference, trying upward movement before lateral movement. Fire can sample neighboring pixels for ignition; oil can burn, while an interaction with water can produce steam. citeturn20view3turn20view5

That maps cleanly to an agent-readable behavioral abstraction:

```text
POWDER:
    try down
    try down-left/down-right in randomized order
    otherwise remain

LIQUID:
    try down
    try diagonal-down
    try lateral spread
    permit swap when destination density < source density

GAS:
    try up
    try diagonal-up
    try lateral diffusion

STATIC_SOLID:
    normally no movement update
    react to heat/chemistry/damage
    optionally convert into POWDER/COLLAPSING_SOLID

FIRE:
    decrement lifetime
    sample neighbor(s)
    if target flammable -> ignite
    if reaction(fire, target) exists -> execute reaction
    expire -> replacement material / empty
```

The important phrase here is **“try”**. A falling-sand simulator is normally a conflict-resolution system as much as it is a physics system. Two cells may desire the same destination, update order can bias flow, and moving a cell twice in one simulation tick changes the apparent speed. *Noita*'s optimization discussion explicitly identifies duplicate cross-chunk updates as something that must be prevented. citeturn20view0

For deterministic behavior, give each update a seeded pseudorandom value derived from stable state rather than arbitrary thread execution order:

\[
r = H(\text{worldSeed}, x, y, \text{tick}, \text{materialId})
\]

where \(H\) is a deterministic integer hash. The agent can use `r & 1` to choose whether left or right gets priority. This removes permanent directional bias without making the outcome dependent on thread scheduling.

### Bottom-up scanning and update-order artifacts

Nolla reports updating falling material from the bottom upward. Purho explains the practical reason: otherwise a vertical column may effectively advance only from its lowest portion instead of propagating movement consistently through the column during the pass. citeturn20view0

A robust implementation should additionally reverse horizontal scan direction periodically:

```cpp
if ((tick & 1) == 0) {
    for (y = bottom; y >= top; --y)
        for (x = left; x <= right; ++x)
            updateCell(x, y);
} else {
    for (y = bottom; y >= top; --y)
        for (x = right; x >= left; --x)
            updateCell(x, y);
}
```

Without reversal or randomized tie-breaking, sand and fluids can develop visible left/right drift simply because one side is tested earlier.

### Active chunks and dirty rectangles

This is where *Noita* becomes particularly valuable as an engine case study. The documented implementation divides the world into **64×64 chunks**. Each chunk tracks a **dirty rectangle**, allowing the simulator to skip inactive cells rather than traversing the entire world every frame. citeturn20view0

Conceptually:

```text
World
 ├─ Chunk[0,0]  64×64 cells
 │    ├─ state: ACTIVE / SLEEPING
 │    └─ dirtyRect: xMin, yMin, xMax, yMax
 ├─ Chunk[1,0]
 ├─ Chunk[2,0]
 ...
```

When a cell moves from \((x_0,y_0)\) to \((x_1,y_1)\), mark both old and new neighborhoods dirty:

\[
R_{\text{dirty}} \leftarrow
R_{\text{dirty}}
\cup N(x_0,y_0)
\cup N(x_1,y_1)
\]

where \(N\) should be enlarged by the maximum radius of rules that can affect neighbors during the next simulation step.

This changes complexity from approximately

\[
O(W H)
\]

per simulation tick to approximately

\[
O(N_{\text{active}})
\]

plus chunk-management overhead, where \(N_{\text{active}}\) is the number of cells contained in currently dirty regions. That distinction becomes enormous when a level contains millions of mostly static rock pixels.

A useful agent rule is:

```text
Never scan an inert region merely because it exists.
Wake simulation regions because:
    material entered;
    material exited;
    temperature crossed a reaction threshold;
    explosion/damage occurred;
    nearby body moved;
    reaction generated an active material.
Put them back to sleep after N stable ticks.
```

### Parallelism without pixel locks

The particularly distinctive *Noita* technique is not simply “checkerboard threading.” According to Purho's explanation, naïvely assigning 64×64 chunks to threads fails because cells can leave their home chunk and enter another worker's region. Per-cell atomics or locks would solve correctness but impose synchronization costs. Instead, Nolla processes chunks in a checker-like spatial pattern over **four rounds**. During one round, a worker's cells can move in their 64×64 region plus a 32-pixel extension in each cardinal direction, creating an exclusive cross-shaped domain. The phases ensure another worker is not simultaneously writing that region. citeturn20view0

Formally, this is best understood as **spatial domain decomposition with phase-separated write ownership**.

An agent should encode the invariant rather than blindly copying “four phases”:

\[
D_i^{write} \cap D_j^{write} = \varnothing
\quad \text{for all concurrently executed jobs } i \ne j
\]

If the maximum cell displacement per simulation step changes, the spacing between concurrently processed chunks must change as well. A four-color pattern that is safe for one movement radius is not automatically safe for a larger radius.

A generic scheduler can therefore calculate:

```text
halo = maximum_cross_chunk_write_distance
phaseSpacing = ceil((chunkSize + 2*halo) / chunkSize)

schedule chunk groups such that concurrent write domains do not overlap
```

This is the **transferable mechanic** hidden inside Noita's implementation. “Four passes” is a particular solution; exclusive write domains are the general rule.

### Chemistry should be table-driven

Avoid a sprawling sequence such as:

```cpp
if (material == OIL && neighbor == FIRE) ...
else if (material == WATER && neighbor == LAVA) ...
else if (...)
```

An AI-friendly engine should treat reactions as data:

```json
{
  "reactants": ["water", "hot_surface"],
  "conditions": {
    "min_temperature": 100
  },
  "outputs": [
    {"material": "steam", "probability": 1.0}
  ],
  "heat_delta": -20
}
```

Then:

\[
\text{Reaction} =
f(M_a,M_b,T_a,T_b,P,\text{randomSeed})
\]

This allows an AI asset/gameplay agent to invent materials without changing engine source.

The actual *Noita* examples demonstrate precisely why this composition matters: fire, water, oil, steam, burning solids, freezing, melting, vegetation growth, and decomposition can interact through small rules rather than bespoke scripted encounters. citeturn20view5turn20view0

### Destruction and the rigid-body bridge

*Noita* does not force every solid object to remain either a cellular material forever or a conventional rigid body forever. Purho describes rigid-body pixels as storing body membership and a location within that body. When pixels belonging to a body are destroyed, its shape can be recalculated; if destruction cuts the object into pieces, multiple bodies can result. Large structural regions can also be carved into shapes and turned into falling rigid bodies. citeturn20view3

The generalized pipeline is:

```text
SIMULATION MASK
      │
      ├── identify unsupported/collapsing region
      │
      ▼
CONNECTED COMPONENT EXTRACTION
      │
      ▼
BOUNDARY / CONTOUR GENERATION
      │
      ▼
POLYGON SIMPLIFICATION
      │
      ▼
RIGID-BODY COLLIDER
      │
      ▼
PHYSICS TRANSFORM
      │
      ▼
RASTERIZE BODY OCCUPANCY BACK INTO PIXEL WORLD
```

**Marching Squares** is a natural boundary extractor here. Each square formed by four neighboring occupancy samples becomes a 4-bit configuration:

\[
c =
b_0
+2b_1
+4b_2
+8b_3,\qquad b_i\in\{0,1\}
\]

giving sixteen local cases. A lookup table determines which boundary segment crosses the cell. For scalar fields, the crossing can be interpolated along each edge; for a binary pixel occupancy field, a fixed halfway crossing is often sufficient.

The important complication is ambiguous saddle configurations. Research on the asymptotic decider addresses the topology ambiguity that occurs when a local cell permits multiple possible contour connections. citeturn16search1turn16search3 For gameplay collision derived from binary pixels, an engine can either use a fixed connectivity convention or apply an asymptotic-decider-style rule when continuity matters.

Do **not** immediately create one collision edge for every boundary pixel. Pixel terrain will generate excessive tiny collider segments. After contour extraction:

\[
P_{\text{raw}}
\rightarrow
P_{\text{simplified}}
\rightarrow
P_{\text{physics}}
\]

Apply a polygon simplifier with an error tolerance below the size at which players can perceive collision mismatch. Sharp gameplay-relevant corners can be tagged as protected so simplification cannot erase them.

The strongest architecture for an AI agent is therefore:

```text
Cellular simulation:
    authoritative for powders, liquids, gases, chemistry

Rigid-body solver:
    authoritative for coherent moving chunks

Conversion layer:
    turns qualifying pixel components into bodies
    and damaged bodies back into/recalculates pixel topology
```

That hybrid is substantially more powerful than attempting to make one solver handle everything.

## Modular multi-joint sprite rigs for massive pixel-art actors

The suggested technique is valid, but the *Metal Slug Attack Reloaded* attribution should be removed from the agent's factual knowledge base. SNK's own franchise material verifies that the title continues the series' detailed 2D pixel-art presentation, but I found no first-party development material establishing that its large units are specifically produced by the proposed hierarchical skeletal mapping system. citeturn14search0

The **general mechanism**, however, is thoroughly established by modern 2D animation runtimes. Spine, for example, defines attachments as visible images or meshes placed into slots that follow bone transformations in position, rotation and scale. It distinguishes rectangular atlas-region attachments from deformable mesh attachments. citeturn18view3 Slots separately determine which attachment is active and establish draw order, making it possible to swap parts without changing the underlying bone hierarchy. citeturn18view4

For strict pixel art, the most useful version is usually not conventional soft mesh skinning but a **hierarchical cutout rig**.

```text
BossRoot
 ├─ chassis
 │   ├─ turret_mount
 │   │   ├─ turret
 │   │   │   └─ cannon
 │   │   └─ antenna
 │   ├─ left_tread
 │   └─ right_tread
 ├─ front_armor
 ├─ rear_armor
 └─ effects_socket
```

Each node stores:

```json
{
  "parent": "turret_mount",
  "pivot_px": [11, 18],
  "local_position": [7.0, -4.0],
  "rotation_deg": 0.0,
  "scale": [1.0, 1.0],
  "attachment": "turret_idle_0",
  "draw_order": 12
}
```

The world transform is the ordinary parent-child transform:

\[
M_i^{world}
=

M_{parent}^{world}
\,T(x_i,y_i)
\,R(\theta_i)
\,S(s_{xi},s_{yi})
\,M_i^{attachment}
\]

This is more general than saying “parts use coordinate offsets.” Coordinate offsets are only the translation component. High-quality rigs also require pivots, rotations, draw ordering, attachment swaps, visibility, and sometimes scale.

### Cutout versus deformable rigs

There are three useful classes for a pixel-art game:

| Rig style         | Mechanism                                                                | Pixel-art suitability                                        |
|-------------------|--------------------------------------------------------------------------|--------------------------------------------------------------|
| **Rigid cutout**  | Each component is an undeformed sprite transformed around a pivot        | Excellent for machines, armor, weapons, segmented creatures  |
| **Weighted mesh** | Vertices of a textured mesh receive weighted bone transforms             | Excellent for painted HD 2D; risky for strict pixel clusters |
| **Hybrid**        | Rigid sprite parts + frame-swapped joints/faces + occasional deformation | Usually best for sophisticated pixel art                     |

Spine's own runtime distinction mirrors this separation: region attachments are rectangular image regions, while mesh attachments can contain deformable vertices and bone weights. citeturn18view3

For strict pixel art, mesh deformation creates a fundamental problem. Pixel art encodes structure into **clusters**. Stretching a cluster geometrically can turn a deliberate 2×3 highlight into irregular samples after rasterization. Consequently, an AI agent should default to rigid attachments and only enable deformation when the visual pipeline intentionally re-rasterizes the result at the game's virtual resolution.

### Why modular rigs save storage

Consider a hypothetical boss rendered as a unique 500×500 RGBA8 image for every frame:

\[
500 \times 500 \times 4
=

1{,}000{,}000\text{ bytes/frame}
\]

At sixty unique frames:

\[
60{,}000{,}000\text{ bytes}
\approx57.2\text{ MiB}
\]

before texture compression, packing, mipmaps, metadata, or platform-specific representation.

Suppose instead it contains twenty 64×64 components, each requiring eight unique raster states:

\[
20\times64\times64\times8\times4
=

2{,}621{,}440\text{ bytes}
\approx2.5\text{ MiB}.
\]

That is only an **illustrative storage comparison**, not data about *Metal Slug*. The key reason for the reduction is that rigid transformation data substitutes for repeated copies of unchanged pixels.

Even better, reusable components can share texture regions:

```text
tread:
    frame_0
    frame_1
    frame_2
    frame_3

turret:
    idle
    recoil
    damaged

jaw:
    closed
    half
    open
```

The runtime then produces many composite poses from a relatively small image vocabulary.

### Atlas everything that can batch together

Modularity can actually make rendering *slower* if every tiny sprite forces a separate draw call or material change. Current Unity documentation explicitly recommends sprite atlases to reduce draw calls by combining multiple textures into one texture. citeturn18view5 Spine similarly maps region attachments into atlas regions and materials. citeturn18view3

Therefore:

```text
BAD:
part A -> texture A -> material A -> draw
part B -> texture B -> material B -> draw
part C -> texture C -> material C -> draw

BETTER:
part A ┐
part B ├─ same atlas + same shader/material -> batch
part C ┘
```

The AI agent should optimize for:

\[
\text{cost} \approx
C_{\text{transform}}
+
C_{\text{vertices}}
+
C_{\text{draw calls}}
+
C_{\text{texture switches}}
\]

not merely sprite-sheet byte count.

### Pivot discipline is critical

Pixel rigs fail visually when pivots are inconsistent. Asset metadata should define pivots in **logical pixel coordinates**, not arbitrary normalized values:

```text
upper_arm pivot = shoulder socket
forearm pivot   = elbow socket
jaw pivot       = jaw hinge
cannon pivot    = turret bearing
```

Modern pixel-perfect tooling similarly exposes pixel-unit pivots; Unity's current Pixel Perfect workflow explicitly supports pivot placement using pixel units. citeturn15search4

For interchangeable pieces, standardize sockets:

```json
{
  "socket": "left_shoulder",
  "position_px": [12, 7],
  "accepted_tags": ["arm", "weapon_arm"],
  "mirrorable": true
}
```

The AI art agent can then generate a replacement part only if its socket coordinate and expected parent orientation satisfy the rig contract.

### Preserve floating-point animation, snap at rendering

Do **not** force all internal bone transforms to integers. Interpolation, easing, inverse kinematics, recoil, and hierarchical rotation benefit from continuous coordinates.

Instead:

\[
p_{anim}\in\mathbb{R}^2
\]

during animation, then quantize the final rendered position:

\[
p_{pixel}
=

\operatorname{round}(p_{screen}/s)\,s
\]

where \(s\) is the number of physical display pixels per logical art pixel.

This distinction is crucial:

```text
simulation/animation transform = float
final virtual-pixel placement  = quantized
```

Point sampling produces the hard pixel appearance expected from unfiltered pixel sprites; current Unity documentation distinguishes point filtering from bilinear/trilinear filtering, with bilinear filtering creating blur. citeturn15search25

Rotation is harder. Even if the pivot is snapped, arbitrary rotation does not preserve the original pixel grid. Unity's Pixel Perfect documentation likewise notes the trade-off between sharper point-filtered rotated imagery and filtering intended to reduce shimmering. citeturn15search16

An AI agent should choose a rotation strategy explicitly:

| Rotation requirement                                                | Preferred solution                                                       |
|---------------------------------------------------------------------|--------------------------------------------------------------------------|
| Machine part can rotate freely and slight pixel crawl is acceptable | Continuous rotation + nearest-neighbor rasterization                     |
| Pixel purity is more important                                      | Quantized angles                                                         |
| Hero object needs perfect silhouettes                               | Hand-drawn rotational variants                                           |
| Organic joint bends                                                 | Attachment swaps / bespoke in-between frames                             |
| Lots of rotation but strict virtual aesthetic                       | Render rig to low-res intermediate target, then nearest-neighbor upscale |

### Use animation composition instead of one giant clip

A large boss should be driven by independent channels:

```text
Locomotion:
    tread loop              phase = continuous

Body:
    chassis bob             phase = locomotion * 0.5

Weapon:
    aim angle               procedural
    recoil                  event-triggered curve

Damage:
    armor state             attachment swap
    sparks                  independent FX emitter

Secondary motion:
    antenna sway            delayed parent motion
    exhaust flap            periodic

Face/jaw:
    hand-drawn frame swaps
```

This gives the illusion of a highly animated object even when only a fraction of its pixels change at any one moment.

The architecture resembles what slots and attachments in established 2D skeletal systems are designed to support: attachments follow bones, one attachment can be selected from alternatives, and slot draw order can itself be animated. citeturn18view3turn18view4

For your AI agent, the important abstraction is therefore not “make a huge sprite skeletal.” It is:

> **Identify regions whose motion can be represented losslessly as transforms; identify regions whose visual topology actually changes; transform the first class and redraw/frame-swap only the second.**

That rule minimizes raster workload without sacrificing handcrafted pixel clusters.

## Sub-pixel animation, cluster handoff, and micro-shading motion

“Sub-pixel animation” in pixel-art terminology should not be confused with literal LCD subpixel rendering or ordinary GPU anti-aliasing. A low-resolution sprite cannot physically occupy half a logical pixel if it remains on a strict integer raster. Instead, the artist manipulates **temporal pixel coverage, color, clusters, and shading** so the viewer perceives a movement smaller or smoother than a one-pixel silhouette jump.

The *Owlboy* evidence is useful here. Simon Stafsnes Andersen explicitly discusses choosing palette colors according to whether they pair effectively for anti-aliasing and “sub-pixelling.” He also describes learning animation by stepping through existing sprite sequences and studying how body contortions and shading changed from frame to frame. citeturn19view0turn19view2 That supports sub-pixelling as a deliberate pixel-art craft technique. The same evidence was **not** found for *Arco*; its official press material verifies Franek Nowotniak's pixel-art role but does not disclose this particular implementation. citeturn17search0

### Edge-color migration

Suppose a bright object ends at logical pixel \(x\):

```text
Background = .
Object     = #
AA shade   = +

Frame A: ....###....
Frame B: ....##+....
Frame C: ...+###....
Frame D: ...###.....
```

No mathematical “half pixel” exists in the final raster. But the intermediate color changes the apparent center of mass of the edge.

A useful computational model is fractional coverage. Let an ideal high-resolution edge cover fraction \(\alpha\) of a logical cell. A conventional filtered representation would produce

\[
C(\alpha)
=

(1-\alpha)C_{bg}+\alpha C_{object}.
\]

Strict pixel art normally should **not** blindly use that RGB result. Instead, choose an approved palette color:

\[
C_{pixel}
=

\underset{c\in P_{edge}}{\arg\min}
\ d\!\left(c,C(\alpha)\right),
\]

where \(P_{edge}\) is the artist-approved edge ramp and \(d\) is a perceptual color-distance function.

The AI agent thereby gets the *coverage cue* of anti-aliasing without introducing arbitrary colors.

This aligns with Andersen's observation that palette choices need to be made with later anti-aliasing and sub-pixelling relationships in mind; those techniques depend on colors functioning together rather than being selected independently. citeturn19view0

### Cluster handoff

A stronger pixel-art technique is to avoid interpreting pixels individually and reason in **clusters**.

For a feature shifting right:

```text
Initial:
.##..

Transition:
.###.

Final:
..##.
```

The temporary width increase acts as a handoff. The trailing cluster has not disappeared before the leading pixel establishes the new location.

A one-pixel-wide feature might instead use value:

```text
A:   .#...
B:   .+*..
C:   ..#..
```

where `+` and `*` are palette-approved lower-coverage or shading colors.

Agent rule:

```text
For displacement < 1 logical pixel:
    preserve major silhouette if possible;
    change edge clusters or internal shading first;
    move the hard silhouette only when accumulated motion reaches the next cell.
```

### Internal shading drift

This is especially effective for breathing, muscle contraction, cloth bulge, facial motion, and slow rotation.

```text
Frame A:
  ####
 #++##
 ##..#
  ###

Frame B:
  ####
 ##++#
 #...#
  ###

Frame C:
  ####
 ###++
 #...#
  ###
```

The silhouette barely changes, but the highlight migrates. Human vision interprets moving shading as changing volume.

This gives your agent a useful hierarchy:

\[
\text{perceived motion}
=

w_s\Delta\text{silhouette}
+
w_i\Delta\text{internal clusters}
+
w_c\Delta\text{color/value}
+
w_t\Delta\text{timing}.
\]

A visible movement does **not** require every term to change.

### Outline pressure

For very small sprites, one dark outline pixel can represent both boundary and depth. Change its value before its coordinate:

```text
rest:      DARK
leaning:   MID-DARK
handoff:   MID
moved:     new outline pixel becomes DARK
```

This makes the contour appear to approach or retreat gradually.

Andersen's workflow reinforces the importance of deliberately coordinated shade colors rather than treating each color in isolation. citeturn19view0

### Dither phase shifting

Fractional coverage can also be represented spatially:

```text
25%:
#...
....
....
....

50%:
#.#.
....
#.#.
....

75%:
###.
#.#.
###.
....
```

For moving texture or translucency, the phase of a dither matrix can shift between frames.

This technique must be tightly constrained. Uncontrolled phase changes become **temporal noise** or “pixel boil.” Therefore the agent needs:

```text
dither animation allowed only when:
    affected region > minimum cluster size;
    pattern phase is intentionally controlled;
    change supports a directional motion/light cue;
    frequency is below the threshold that reads as random flicker.
```

### Palette-index animation is better than arbitrary RGB animation

Represent ramps explicitly:

```json
{
  "skin_highlight": [12, 13, 14, 15],
  "cloth_red": [31, 32, 33, 34],
  "outline_warm": [4, 5, 6],
  "metal_specular": [48, 49, 50]
}
```

Then an animated micro-shift can operate on indices:

\[
i_{t+1}
=

\operatorname{clamp}(i_t+\Delta i, i_{min}, i_{max})
\]

instead of performing an unconstrained RGB blend.

This gives an AI agent explicit knowledge that:

```text
dark_red_1 -> dark_red_2 -> red_mid
```

is legal, while

```text
dark_red_1 -> arbitrary interpolation RGB(127,58,71)
```

may violate the art direction.

### A computational sub-pixel frame generator

For an AI pipeline, a very powerful approach is to generate a *candidate* intermediate frame using supersampling while retaining the final low-resolution pixel aesthetic.

Pipeline:

```text
original logical sprite
        │
        ▼
construct 4× or 8× binary/material coverage representation
        │
        ▼
apply fractional transform Δx, Δy
        │
        ▼
measure coverage of every original logical pixel
        │
        ▼
map coverage to approved palette ramp
        │
        ▼
apply pixel-cluster constraints
        │
        ▼
human/AI art cleanup
```

For logical cell \(p\),

\[
\alpha_p =
\frac{\text{covered supersamples in }p}
     {\text{total supersamples in }p}.
\]

Then map the result to a discrete ramp:

\[
q =
\operatorname{round}(\alpha_p(K-1))
\]

and:

\[
C_p=P[q].
\]

This is **not a claim that Owlboy or Arco uses this algorithm**. It is a computational method for teaching an AI agent to generate traditional-looking sub-pixel candidates systematically.

It should then apply cluster constraints:

```text
Reject candidate if:
    creates isolated 1-pixel noise not intentionally permitted;
    destroys identifying facial feature;
    changes palette outside approved ramp;
    creates edge AA on an edge that should remain hard;
    produces more temporal flicker than geometric motion;
    changes sprite volume without corresponding pose change.
```

### Motion cadence matters more than raw frame count

The misconception to avoid is:

> “Smooth animation = more unique frames.”

Pixel animation frequently derives weight from **unequal frame durations**.

For example:

```text
anticipation     80 ms
compression      50 ms
launch           33 ms
airborne         100 ms
impact           33 ms
settle           50 ms
rest             120 ms
```

A tiny shading change held for 100 ms can communicate weight better than several evenly spaced interpolations.

The agent should therefore represent an animation frame as:

```json
{
  "image": "idle_03",
  "duration_ms": 120,
  "tags": ["settle"],
  "subpixel_features": {
    "shoulder_highlight": "ramp_down",
    "head_outline": "pressure_right"
  }
}
```

not merely as `frameIndex`.

### Do not confuse sub-pixel art with runtime bilinear filtering

Current engine documentation makes the distinction operationally important. Unity describes point filtering as preserving block-like texels, while bilinear filtering blurs neighboring samples; its Pixel Perfect Camera similarly exposes a trade-off between sharper point filtering and filtered modes intended to reduce shimmering. citeturn15search25turn15search16

For handcrafted sub-pixelling:

```text
sprite sampling     = nearest / point
logical coordinates = integer at final raster
fractional effect   = encoded in authored colors/clusters
```

Otherwise the GPU's interpolation destroys the controlled decisions the artist made.

## Normal-mapped pixel lighting, bump data, and 2.5D rendering

The *Eastward* case needs a substantial correction because the actual technique is more interesting than the simplified description. Lead programmer Tommo Zhou states that *Eastward* is **a 3D game presented with a 2D perspective**. Pixpil separates assets according to natural structure, such as building roof and wall components, rebuilds those assets in a 3D environment, and hand-paints bump information so they respond correctly to the game's lighting. The custom engine also uses shader textures and lighting systems to support atmosphere, weather, fog, and changes in time. citeturn19view3turn19view5

Thus the better model is:

```text
pixel diffuse art
        +
structural layer separation
        +
surface/bump information
        +
3D/depth-aware placement
        +
dynamic lighting shaders
        =
2D-looking scene with richer spatial lighting
```

This is more powerful than putting a normal map on a completely flat screen-space sprite.

Modern engines expose related architecture directly. Unity supports normal and mask maps as secondary textures on 2D sprites, with the textures sharing the sprite's UV correspondence. citeturn15search1 Godot likewise supports normal-map information in its 2D CanvasItem rendering system. These engine facilities show that per-pixel surface-direction lighting is a standard transferable technique even though *Eastward* itself uses a custom pipeline. citeturn15search1

### Asset channel layout

A sophisticated AI-authored sprite material can use:

\[
\mathcal A =
\{D,N,H,M,E,O\}
\]

where:

| Channel | Meaning                      | Required?                       |
|---------|------------------------------|---------------------------------|
| \(D\)   | Diffuse/base pixel color     | Yes                             |
| \(N\)   | Surface normal direction     | For directional lighting        |
| \(H\)   | Approximate height/elevation | Optional but powerful           |
| \(M\)   | Lighting/material mask       | Recommended                     |
| \(E\)   | Emissive mask/color          | For lamps, screens, lava        |
| \(O\)   | Occlusion/shadow metadata    | When real shadowing is required |

A compact packed representation might use:

```text
Texture A: RGBA = diffuse + alpha
Texture B: RGB  = normal
Texture C:
    R = height
    G = light-response mask
    B = emission strength
    A = material class / free channel
```

Unity's current 2D system similarly treats normal maps and mask maps as secondary sprite textures, and requires them to remain aligned with the main sprite's sampling coordinates. citeturn15search1

### Normal encoding

A normal is a unit vector:

\[
N=(n_x,n_y,n_z),\qquad \|N\|=1.
\]

Texture channels normally cannot directly encode negative values, so a conventional signed-to-unsigned encoding is:

\[
C=
\frac{N+1}{2}.
\]

At runtime:

\[
N=
\operatorname{normalize}(2C-1).
\]

Thus a surface facing straight “out of” the sprite plane:

\[
N=(0,0,1)
\]

encodes approximately as:

\[
C=(0.5,0.5,1).
\]

Engine coordinate conventions vary; in particular, the vertical normal channel can require inversion depending on texture-space orientation. Therefore every AI-generated normal-map pipeline needs a **normal-direction validation fixture** rather than assuming channel direction.

Store a test sprite containing:

```text
flat
left slope
right slope
up slope
down slope
convex sphere
concave bowl
```

Move one point light clockwise around it. Incorrect green-channel orientation becomes immediately obvious.

### Point-light vector

For fragment position

\[
P=(p_x,p_y,p_z)
\]

and light position

\[
L=(l_x,l_y,l_z),
\]

calculate:

\[
\vec{\ell}
=

\frac{L-P}{\|L-P\|}.
\]

For purely 2D screen-space objects, \(p_z\) may be a constant. A 2.5D system should instead derive it from layer elevation or a height map:

\[
p_z=z_{layer}+\lambda H(u,v).
\]

This is precisely where *Eastward*'s 3D reconstruction approach becomes important: a light can respond to meaningful scene depth rather than treating every roof, wall, floor, and character as lying on exactly the same plane. The developer explicitly describes rebuilding separated assets into a 3D environment before processing their bump-light response. citeturn19view3turn19view5

### Diffuse response

The basic Lambertian term is:

\[
L_d=
\max(0,N\cdot\vec{\ell}).
\]

Add distance attenuation:

\[
a(d)=
\left[
\max\left(0,1-\frac dR\right)
\right]^p
\]

for a stylized finite-radius light, where \(R\) is radius and \(p\) controls falloff.

Then:

\[
I =
I_{ambient}
+
C_L\,S_L\,L_d\,a(d)\,M
\]

where \(C_L\) is light color, \(S_L\) its strength, and \(M\) a material/light-response mask.

Finally:

\[
C_{out}=D\cdot I+E.
\]

That produces ordinary smooth dynamic lighting—but ordinary smooth lighting often looks wrong on intentionally quantized pixel art.

### Quantize the lighting, not necessarily the artwork

A very effective pixel-art shader constrains the lighting scalar:

\[
Q(I)=
\frac{
\operatorname{round}(I(K-1))
}{
K-1
}.
\]

With \(K=4\), for example, continuously changing illumination becomes four discrete light bands.

Then:

\[
C_{out}=D\cdot Q(I)+E.
\]

An even stronger art-directed method is **palette-ramp lighting**:

```json
{
  "brick_red": {
    "shadow": 41,
    "dark": 42,
    "base": 43,
    "light": 44,
    "hot": 45
  }
}
```

Instead of multiplying `brick_red` by arbitrary light values, calculate a lighting band:

\[
b=
\operatorname{clamp}
\left(
\operatorname{round}(I(K-1)),
0,K-1
\right)
\]

and select `brick_red[b]`.

This preserves palette authorship while still allowing lights to move dynamically.

### Preserve baked pixel shading

If the diffuse image already contains beautifully hand-painted highlights and shadows, applying a full-strength normal map can “double shade” it.

The agent should know three material modes:

```text
UNLIT_BASE:
    diffuse is mostly flat albedo;
    shader provides most volume.

AUTHORED_SHADE:
    diffuse already contains strong volume;
    normal light is restricted to subtle modulation.

HYBRID:
    hand-authored broad shading;
    normal map adds local dynamic-light direction.
```

For `AUTHORED_SHADE`:

\[
C =
D\left[
1+
k(L_d-\bar L)
\right]
\]

with a deliberately small \(k\), rather than completely replacing the image's original light structure.

This is especially appropriate when the pixel artwork itself contains carefully constructed ramps and dithering. *Eastward*'s team describes its lighting-support textures as individually hand-worked, reinforcing that the auxiliary maps belong to the art pipeline rather than being treated as an automatic postprocess. citeturn19view5

### Normal maps do not create occlusion shadows

This is the single most important technical correction to the original normal-map description.

The normal term:

\[
\max(0,N\cdot L)
\]

answers:

> “How directly is this surface element facing the light?”

It does **not** answer:

> “Is there another object between this surface and the light?”

That second question requires a visibility term \(V\):

\[
C_{lit}
=

D
\left(
A+
V\,L_d\,a(d)
\right).
\]

where:

\[
V=
\begin{cases}
0 & \text{occluded}\\
1 & \text{visible}
\end{cases}
\]

or a filtered fractional value.

A complete pixel-lighting system therefore separates:

```text
normal map -> local surface orientation
height/depth -> relative elevation
shadow caster -> occlusion geometry
light mask -> material response
diffuse sprite -> authored base color
```

For a top-down pixel game, shadow casters can be polygons around walls, simplified masks, signed-distance fields, or true 3D geometry. In a 2.5D architecture like the one *Eastward*'s developer describes, structural depth itself can participate in these lighting relationships. citeturn19view3turn19view5

### Keep all companion textures pixel-aligned

Normal-map pixels must correspond exactly to diffuse pixels. Unity's sprite secondary-texture documentation explicitly requires secondary textures to align with the main sprite because they share the sprite's UV coordinates. citeturn15search1

Therefore an AI asset validator should require:

```text
diffuse.width  == normal.width
diffuse.height == normal.height
diffuse pivot  == normal pivot
atlas rect     == corresponding normal atlas rect
animation frame boundaries identical
transparent padding consistent
```

If the diffuse atlas receives padding but the normal atlas does not, edge sampling can fetch an unrelated normal from the adjacent sprite.

### Keep pixel sampling intentional

Current Unity documentation describes point filtering as producing block-like, unfiltered texels while bilinear and trilinear modes introduce interpolation and blur. citeturn15search25 For a strict pixel-art material stack, diffuse, normal, masks, and height channels should normally use corresponding point-sampled coordinates at the intended virtual resolution.

A useful render pipeline is therefore:

```text
Game world
   ↓
virtual-resolution geometry
   ↓
diffuse + normal + mask lighting
   ↓
low-resolution lighting target
   ↓
optional palette/light-band quantization
   ↓
nearest-neighbor integer upscale
   ↓
display
```

This prevents a high-resolution light buffer from creating smooth, sub-logical-pixel gradients over artwork whose pixels are intentionally discrete.

One modern-engine caveat is worth encoding into the agent's performance knowledge: Unity's current URP documentation warns that adding sprite normal maps introduces an additional depth pre-pass for each layer batch, including a full-size render texture, so sophisticated 2D lighting is not automatically free. citeturn15search1

## Unified AI-agent asset schema and implementation mechanics

The most useful outcome of this research is not four disconnected tutorials but a **machine-readable ontology** that tells the agent what kind of pixel behavior it is creating.

A recommended top-level asset definition is:

```json
{
  "asset_id": "boss_excavator_01",
  "pixel_grid": {
    "logical_ppu": 16,
    "sampling": "nearest",
    "integer_upscale_required": true
  },

  "animation": {
    "mode": "hybrid_rig",
    "pixel_snap": "final_transform",
    "allow_arbitrary_rotation": false,
    "subpixel_style": "palette_cluster"
  },

  "lighting": {
    "mode": "normal_mapped_quantized",
    "normal_strength": 0.45,
    "light_bands": 5,
    "receives_dynamic_light": true,
    "casts_shadow": true
  },

  "simulation": {
    "mode": "none"
  }
}
```

A destructible terrain asset would instead use:

```json
{
  "asset_id": "wooden_support",
  "simulation": {
    "mode": "cellular_material",
    "material": "wood",
    "can_burn": true,
    "can_collapse": true,
    "rigid_body_conversion": true
  },

  "lighting": {
    "mode": "world_material"
  }
}
```

The core AI-agent decision tree should be:

```text
Does this pixel need independent physical behavior?
    YES -> Cellular material representation.
    NO  -> Continue.

Does this visual region preserve its shape while moving?
    YES -> Rigid sprite attachment / bone transform.
    NO  -> Continue.

Does topology change only at known poses?
    YES -> Attachment swap / hand-authored frame.
    NO  -> Continue.

Is the desired motion smaller than a logical pixel?
    YES -> Cluster/sub-pixel transition.
    NO  -> Ordinary frame or transform motion.

Must changing lights reveal surface orientation?
    YES -> Normal/bump information.

Must the object block a light source?
    YES -> Separate shadow/occlusion representation.
```

This prevents common architecture mistakes such as using skeletal deformation where frame swapping is better, adding full cellular simulation to decorative dust, or expecting normal maps to solve shadow occlusion.

### Agent representation for pixel clusters

Individual texels are too low-level for intelligent art generation. Define connected or semantically related clusters:

```json
{
  "cluster_id": "helmet_highlight",
  "semantic": "specular_highlight",
  "pixels": [[8,3],[9,3],[9,4]],
  "palette_ramp": "steel_light",
  "protected": false,
  "animation_behavior": "surface_follow"
}
```

Other cluster semantics:

```text
silhouette
outline
internal_shadow
highlight
eye
mouth
joint
material_transition
dither
emission
damage_mask
```

Then an animation operation can say:

```json
{
  "operation": "subpixel_shift",
  "cluster": "helmet_highlight",
  "direction": [1, 0],
  "fraction": 0.35,
  "preserve_silhouette": true
}
```

rather than instructing the agent to “change some pixels.”

### Agent representation for modular rigs

```json
{
  "bone": "cannon",
  "parent": "turret",
  "pivot_px": [4, 9],

  "constraints": {
    "rotation_min": -25,
    "rotation_max": 40,
    "rotation_quantization_deg": 5
  },

  "attachments": [
    "cannon_normal",
    "cannon_recoil",
    "cannon_damaged"
  ],

  "pixel_rules": {
    "snap_translation": true,
    "allow_mesh_deform": false
  }
}
```

Spine's documented separation of bones, slots, attachments, draw order, atlas-backed images, and deformable meshes provides a useful established conceptual model for this kind of runtime representation. citeturn18view3turn18view4

### Agent representation for cellular materials

```json
{
  "material": "oil",
  "class": "liquid",

  "physics": {
    "density": 0.8,
    "gravity_response": 1.0,
    "lateral_spread": 4
  },

  "thermal": {
    "flammable": true,
    "ignition_temperature": 220,
    "burn_product": "smoke"
  },

  "reactions": {
    "fire": "ignite",
    "lava": "ignite"
  }
}
```

The engine interprets that data through a stable behavior library rather than asking the AI to generate arbitrary executable simulation code every time it creates a substance. That design captures the compositional strength demonstrated by *Noita*'s simple liquid, density, fire, steam, and static-to-collapsing-material interactions. citeturn20view3turn20view5

### Agent representation for lighting

```json
{
  "material": "brick_red",

  "maps": {
    "diffuse": "brick_red_D.png",
    "normal": "brick_red_N.png",
    "height": "brick_red_H.png",
    "mask": "brick_red_M.png"
  },

  "normal_convention": {
    "x": "right",
    "y": "up",
    "z": "toward_camera"
  },

  "lighting": {
    "diffuse_model": "lambert",
    "quantization_bands": 4,
    "normal_strength": 0.5,
    "preserve_authored_shading": 0.8
  }
}
```

The Eastward pipeline provides especially strong justification for putting this information in the **asset authoring stage**: Pixpil describes dividing assets by structural component, reconstructing them spatially, and hand-painting bump information before engine import. citeturn19view5

### Pixel-art invariants

An AI agent should have hard validation rules rather than merely aesthetic prompts.

| Invariant                     | Validation                                                                                                              |
|-------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| No accidental smoothing       | Texture sampling is nearest unless explicitly authorized                                                                |
| Stable logical grid           | Output dimensions and pivots are integer logical-pixel compatible                                                       |
| Controlled palette            | Every sprite color belongs to approved palette/ramp or explicitly permitted dynamic-light output                        |
| No accidental isolated pixels | Connected-component / neighbor test flags new singleton clusters                                                        |
| Normal alignment              | Diffuse, normal, height, mask share dimensions, pivot and atlas region                                                  |
| Rig socket consistency        | Parent/child attachment coordinates match standardized sockets                                                          |
| No double update in CA        | One cell/material entity cannot perform two movement updates during the same tick unless behavior explicitly permits it |
| Thread safety                 | Concurrent CA jobs cannot own overlapping writable cells                                                                |
| Determinism                   | Same seed + same input sequence generates same simulation result where deterministic mode is required                   |
| Shadow separation             | `casts_shadow=true` requires actual occlusion representation; normal texture alone is insufficient                      |
| Temporal consistency          | Pixel changes between frames must be attributable to motion, shading, FX, damage, or intentional texture variation      |

A simple frame-to-frame pixel metric is useful:

\[
D_t=
\frac{
|\{p:I_t(p)\ne I_{t-1}(p)\}|
}{
|\text{sprite pixels}|
}.
\]

But low \(D_t\) is not automatically good. The agent should divide changes by semantic class:

\[
D_t =
D_{silhouette}+
D_{shade}+
D_{detail}+
D_{FX}.
\]

For a subtle breathing idle, large \(D_{silhouette}\) is suspicious; a small \(D_{shade}\) may be exactly what is wanted. For an explosion, the opposite constraint applies.

### Runtime ordering

For a game combining all four systems, the simulation/render frame should have a deliberate order:

```text
INPUT / GAMEPLAY
       ↓
CELLULAR EVENTS
    heat, damage, fluid injection
       ↓
CELLULAR AUTOMATA UPDATE
    phased active-chunk simulation
       ↓
STRUCTURAL ANALYSIS
    newly unsupported regions
    component splitting
       ↓
RIGID BODY PHYSICS
       ↓
RIG / CHARACTER ANIMATION
       ↓
FINAL PIXEL-SNAP TRANSFORMS
       ↓
VISIBILITY / SHADOW CASTERS
       ↓
NORMAL-MAPPED LIGHTING
       ↓
LIGHT / PALETTE QUANTIZATION
       ↓
VIRTUAL-RESOLUTION FRAME
       ↓
INTEGER / NEAREST UPSCALE
```

The exact physics ordering can vary by engine, but the invariants are important: cellular state must not race rigid-body ownership; final sprite snapping should occur after continuous animation evaluation; and pixel-light quantization should occur before the final nearest-neighbor upscale.

## Recommended implementation blueprint and research conclusions

The research suggests that the best production system is not to imitate any one referenced game wholesale. It is to combine the strongest **verified architectural ideas** while keeping each subsystem independently switchable.

The recommended stack is:

| System                  | Recommended implementation                                                       | Why                                                                                                                                                                                                    |
|-------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| World destruction       | Chunked cellular automata with dirty regions                                     | Directly grounded in *Noita*'s documented scalable approach. citeturn20view0turn16search0                                                                                                          |
| CA threading            | Spatially disjoint phased jobs with halo/write-radius constraints                | Generalizes *Noita*'s four-round checker-like solution. citeturn20view0                                                                                                                             |
| Material behavior       | Shared material prototypes + per-cell mutable state + data-driven reaction table | Captures the documented emergent-rule model without wasteful per-cell duplication. citeturn20view4turn20view5                                                                                      |
| Structural destruction  | Connected components + contour extraction + simplified rigid-body shapes         | Matches the documented need to recalculate/split destructible bodies and provides a principled Marching-Squares-style implementation. citeturn20view3turn16search1                                 |
| Huge actors             | Hybrid rigid-part skeletal rig                                                   | Well-supported general 2D skeletal architecture; game-specific Metal Slug attribution remains unverified. citeturn18view3turn18view4                                                               |
| Raster storage          | Atlas reusable part states rather than baking every composite frame              | Established sprite-atlas workflow reduces redundant texture state and draw-call pressure. citeturn18view5                                                                                           |
| Pixel-perfect rigging   | Float animation state → quantized final transform                                | Retains interpolation internally while protecting final raster placement; nearest/point filtering maintains hard texel boundaries. citeturn15search25turn15search4                                 |
| Organic micro-animation | Cluster handoff + palette-based sub-pixelling + shading drift                    | Directly compatible with Owlboy artist Simon Andersen's discussion of palette pairing for AA/sub-pixelling. citeturn19view0turn19view2                                                             |
| Dynamic light           | Diffuse + hand-painted/derived normal/bump + mask + optional height              | *Eastward*'s lead programmer explicitly describes shader lighting, structural separation, 3D reconstruction and hand-painted bump data. citeturn19view3turn19view5                                 |
| Pixel-light aesthetic   | Low-res light evaluation and/or quantized/palette-ramp output                    | Prevents continuously shaded lighting from overwhelming discrete pixel-art ramps                                                                                                                       |
| Shadows                 | Separate caster/depth/occlusion system                                           | A normal stores surface orientation, not line-of-sight visibility                                                                                                                                      |
| Final presentation      | Virtual render target → nearest-neighbor integer upscale                         | Keeps all simulation, shading and animation decisions tied to one logical grid; contemporary engine tooling continues to distinguish point and smoothing filters. citeturn15search10turn15search25 |

The **single most useful instruction to place in the AI agent's system knowledge** is:

> **Treat a pixel according to the abstraction that owns it. A simulation pixel is a material cell; an animation pixel belongs to an authored cluster or attachment; a lighting pixel is a sampled surface with orientation; a displayed pixel is the final quantized result. Never substitute one abstraction for another merely because all four eventually appear as square pixels on screen.**

A second high-value rule is:

> **Preserve continuous internal state where it provides useful physics or animation, but deliberately quantize at the artistic boundary.** Bone motion may be floating point while its rendered placement snaps to the virtual grid. Light intensity may be continuous while its final result selects among four palette bands. Ideal sub-pixel displacement may be fractional while its output becomes a discrete palette-and-cluster transition. Cellular calculations may have continuous temperatures and probabilities while material occupancy remains one logical cell at a time.

And the third is:

> **Use hand-authored discrete state changes wherever geometry alone cannot preserve pixel topology.** A rotating cannon may be transformed; a bending elbow may require a replacement sprite. A rigid armor plate may use a bone; a jaw changing silhouette may use keyed attachments. A tiny torso lean may be communicated through highlight migration before the actual silhouette moves. Established skeletal systems explicitly support attachment swapping and independent draw ordering for precisely this kind of compositional animation. citeturn18view3turn18view4

The research also changes how the four games should appear in your agent's knowledge base:

```yaml
references:

  noita:
    evidence_strength: very_high
    verified_lessons:
      - cellular_automata_material_world
      - simple_local_material_rules
      - density_based_liquid_displacement
      - fire_water_steam_interactions
      - static_to_collapsing_material_conversion
      - rigid_body_pixel_membership
      - destructible_body_recalculation_and_splitting
      - chunk_size_64x64
      - dirty_rect_updates
      - four_phase_checker_like_parallel_update
    sources:
      - Nolla/Petri Purho GDC 2019
      - Petri Purho/Nolla technical interview

  metal_slug_attack_reloaded:
    evidence_strength_for_skeletal_claim: unverified
    verified_lessons:
      - detailed_2d_pixel_art_presentation
    transferable_but_not_game_verified:
      - hierarchical_cutout_sprite_rig
      - modular_attachment_animation
      - atlas_part_reuse
      - independent_secondary_loops

  arco:
    evidence_strength_for_subpixel_claim: unverified
    verified_lessons:
      - pixel_art_by_franek_nowotniak
    use_as:
      - visual_reference_only_for_micro_animation
    do_not_assert:
      - documented_subpixel_shading_pipeline

  owlboy:
    evidence_strength: high_for_artist_workflow
    verified_lessons:
      - palette_colors_selected_for_anti_aliasing
      - explicit_use_of_sub_pixelling_terminology
      - frame_by_frame_study_of_contortion_and_shading

  eastward:
    evidence_strength: very_high
    verified_lessons:
      - 3d_game_with_2d_perspective
      - shader_textures
      - custom_lighting
      - structural_asset_layer_separation
      - assets_rebuilt_in_3d_environment
      - bump_information_hand_painted_per_asset
    correction:
      - not_a_purely_flat_2d_normal_map_pipeline
```

That distinction will keep an AI-generated development pipeline from propagating attractive but unsupported reverse-engineering claims as fact.

The deepest common principle across these techniques is **controlled discretization**. *Noita* discretizes physical matter into cells and gets continuous-looking material phenomena from local rules. Modular rigs discretize a giant character into reusable independently transformable parts. Sub-pixelling discretizes fractional perceptual motion into carefully chosen temporal changes in pixel clusters and palette values. Normal-mapped pixel lighting discretizes surface orientation and, when art-directed correctly, can re-quantize continuous illumination back into authored pixel-light bands. The games and tools differ, but the engineering pattern is the same: **maintain richer information behind the image, then decide deliberately how that information is projected onto the pixel grid.** citeturn16search0turn20view4turn18view3turn19view0turn19view3
