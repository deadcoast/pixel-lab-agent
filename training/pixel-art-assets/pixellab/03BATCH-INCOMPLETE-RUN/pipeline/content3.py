"""03BATCH — "Hearth and Road": the world the cast stands in.
02BATCH built the starting quadrant's cast. This batch builds what they stand among: the environment of the top-down map
(old world left where it fell, the Republic's road furniture, the Farlands, Waylight's civic stone, the bunker inside),
the peoples not yet drawn (Farkeeper civilians, Waylight's mail society, the Republic's envoys, the bunker's archive,
the Smoke's driver), the party's running and hero motions, the faces for dialogue, and the interface a courier game needs.
Every key is checked against inventory.json — nothing here regenerates an existing asset.
Section refs: compendium §1–§22, proposals P01–P09, and the accepted design docs (WAYLIGHT-DESIGN, UNITY-DESIGN, the Smoke)."""

# ---------------------------------------------------------------- characters (v3, 64px, low top-down) ----
CHARS = {
 # §6, UNITY-DESIGN: the Farkeepers at home — the Farlands, famine remembered, the Ever-flame kept in the town hall, smoke spools as engineering
 "farkeeper/flame_tender": ("tall pale mountain woman who keeps a town hall's never-extinguished fire, long dark green wool robe with a hide mantle, a leather hood pushed back over grey-streaked braids, a long iron fire-hook and a leather bellows on a strap, a small hot coal in an iron clasp on a chain at the chest, soot on the sleeves, solemn face, dark green hide brown iron and one ember orange palette", "mannequin"),
 "farkeeper/spool_wright": ("wiry pale mountain engineer who tends the tall smoke-spool spires and their air ducts, leather smock over a wool tunic, a brass listening horn and a wooden duct-shutter key hung on a belt, a coil of thin rope and a tar pot, thick fingerless mittens, wind-reddened cheeks, close-cropped hair under a felt cap, hide brown brass and slate grey palette", "mannequin"),
 "farkeeper/matron": ("gaunt pale mountain grandmother who remembers the famine, heavy layered wool and a fringed hide shawl pinned with a bone brooch, a wooden meal-bowl carried in both hands with a small crust in it, a knotted cord belt with wooden tally beads, wrapped feet in hide shoes, deep-lined dignified face, dark wool grey hide brown and bone white palette", "mannequin"),
 "farkeeper/child": ("small pale mountain child in a hand-me-down wool coat far too big, sleeves rolled, a hide hood with fur trim, carrying a bundle of kindling twigs tied with cord, cheeks red from the cold, bright curious eyes, dark green wool and hide brown palette", "mannequin"),
 "farkeeper/stonecutter": ("broad pale mountain stonecutter, sleeveless hide jerkin over a wool shirt, arms dusted with grey stone powder, a heavy iron mallet and a pointed chisel, a leather apron with pockets of tools, a carved tracery fragment of dark stone under one arm, thick beard, hide brown stone grey and iron palette", "mannequin"),
 "farkeeper/shield_bearer": ("towering pale mountain warrior with a large round wooden shield rimmed in iron painted dark green with a slate blue centre, a bearded axe in the other hand, a hide and bronze scale coat, iron skull cap with a fur trim, fur-lined boots, a long braided beard with iron rings, stern watchful face, hide brown bronze dark green and slate blue palette", "mannequin"),
 # §1–§2, §4, WAYLIGHT-DESIGN: the mail society at home — the sorting hall, the letter wall, the outfitters, the couriers' hall, the home lamplighter
 "waylight/postmaster": ("stout older postmaster of a courier city, long slate-blue wool coat with brass buttons and a polished brass post-horn badge at the collar, half-moon spectacles, ink-stained fingers, a heavy ledger held open across one forearm and a brass hand-stamp in the other hand, neat grey hair, kind sharp face, slate blue brass and ledger cream palette", "mannequin"),
 "waylight/scribe": ("young public letter-writer of a courier city, slate-blue tunic under a paper-stained canvas apron, a wooden lap desk hung on a strap at the front with an ink pot and quills in loops, a small satchel of folded paper, cropped hair with a pencil behind the ear, earnest face, slate blue paper cream and ink black palette", "mannequin"),
 "waylight/lamplighter": ("home lamplighter of a courier city, a long hide coat over a slate-blue tunic, a tall brass-tipped lighting pole carried over one shoulder, a small brass oil can and a wick trimmer at the belt, a flat cap, a lit brass lantern in the other hand, calm weathered face, hide brown slate blue and warm brass palette", "mannequin"),
 "waylight/outfitter": ("outfitter of a courier city's gate hall, slate-blue vest over rolled shirtsleeves, a measuring cord around the neck, a leather pack-frame under one arm and a brass lantern held up in the other hand as if offering it, a belt hung with buckles and straps, thick forearms, warm practical face, slate blue leather brown and brass palette", "mannequin"),
 "waylight/trainee": ("teenage courier trainee of a courier city, running kit of a short slate-blue tunic and cropped trousers, a small canvas pack cinched tight, wrapped shins and soft running boots, a numbered cloth tag pinned to the chest, cropped hair, eager face, slate blue canvas tan and one white tag palette", "mannequin"),
 # §3, §15, P07–P08, UNITY-DESIGN: the Republic of Connection goes out to the settlements with a written promise and a registry
 "republic/envoy": ("envoy of a republic of couriers, a long formal slate-blue coat with a dark green Farkeeper sash across the chest, a polished brass post-horn brooch, a leather document case with a brass lock carried in both hands holding a rolled written promise with a wax seal, clean boots, a travel cloak folded over the shoulder, composed diplomatic face with tired eyes, slate blue dark green brass and parchment palette", "mannequin"),
 "republic/registrar": ("registrar of a republic of couriers who records each settlement's first reply, slate-blue coat with grey cuffs, a leather-bound register chained to the belt and a brass-nibbed pen, a small folding stool strapped to the back, wire spectacles, a wide-brimmed travel hat, patient bookish face, slate blue grey and brass palette", "mannequin"),
 # §3 the Smoke's capital the Farm, the-smoke-faction design: the only motors in the world, sunburned scalps, cut-pipe shingle, a lit ember
 "smoke/driver": ("post-apocalyptic tanker-truck driver of a fuel cult, raw sunburned red peeling bald scalp, a tar-black shingled vest of cut drum-steel plates, a cracked leather driving cap with goggles up, a rag around the neck, a lit cigarette, a heavy wrench through the belt and a jerrycan in one hand, oil-stained trousers and boots, squinting hard face, tar black rust and one orange ember palette", "mannequin"),
 # §10–14: the bunker's archive of old books and records; the first generation born to the open door
 "diefenbunker/archivist": ("middle-aged archivist of an underground bunker society, a grey cardigan over a pressed shirt with a laminated badge on a lanyard, cotton gloves, thick glasses, an armful of old cloth-bound books and a cardboard records box held against the chest, pale skin, soft careful face, grey cream and one small red pin palette", "mannequin"),
 "diefenbunker/child": ("small pale child of an underground bunker society, a cut-down grey coverall with a name tape, a knitted cap, a small rucksack, a hand-crank flashlight held up to the sky, squinting at daylight for the first time, wide amazed face, coverall grey and a small yellow flashlight palette", "mannequin"),
}

# ---------------------------------------------------------------- map objects (high top-down) ----
# (key, prompt, size) — size chosen by footprint: 64 props, 96 trees and vehicles, 128 buildings and bridges
OBJECTS = [
 # -- the old world, left where it fell (§5 roads that remember, WAYLIGHT-DESIGN layer 1)
 ("objects/wrecked_car", "a rusted burned-out old sedan car with no glass, flat tyres, a small tree growing out of the engine bay, pixel art game object, post-apocalyptic", 96),
 ("objects/wrecked_bus", "a long rusted old passenger bus tipped on its side, windows gone, moss on the roof, doors hanging open, pixel art game object, post-apocalyptic", 128),
 ("objects/power_pylon", "a tall steel lattice electricity pylon with snapped wires hanging from it, rust, a bird's nest in the crossarm, pixel art game object", 128),
 ("objects/power_pole", "a leaning wooden utility pole with a cross arm, glass insulators and a re-strung copper wire, pixel art game object", 96),
 ("objects/highway_sign", "a bent green highway sign on a rusted steel post, white lettering half legible, bullet holes, pixel art game object, post-apocalyptic", 64),
 ("objects/guardrail", "a length of buckled steel highway guardrail on wooden posts, rust, grass grown through, pixel art game object", 64),
 ("objects/overpass_stub", "a broken stub of a concrete highway overpass with the deck sheared off, rebar sticking out, shrubs growing on the slab, pixel art game object", 128),
 ("objects/cobra_lamp", "an old cobra-head street lamp post with a brass oil lantern hung from its head on a chain, lit, pixel art game object", 96),
 ("objects/water_tower", "an old steel water tower tank on four riveted legs repainted white with a brass band, a ladder and a downpipe, pixel art game object", 128),
 ("objects/wind_turbine", "a rebuilt white three-blade wind turbine on a lattice tower with a wooden switch house at the base and a cable, pixel art game object", 128),
 ("objects/solar_row", "a neat row of five salvaged solar panels on a timber rack angled toward the sun, cables to a small box, pixel art game object", 96),
 ("objects/shipping_container", "a rusted slate-blue shipping container with the doors chained shut and a painted brass post-horn stencil, pixel art game object", 96),
 ("objects/tyre_pile", "a pile of old car tyres stacked and sorted in a salvage yard, pixel art game object", 64),
 ("objects/billboard", "a tall old roadside billboard on two steel posts, the poster torn to shreds, a painted white route arrow added, pixel art game object, post-apocalyptic", 128),
 ("objects/gas_station_ruin", "a collapsed old fuel station canopy on two posts with the pumps rusted and the sign fallen, weeds, pixel art game object, post-apocalyptic", 128),
 ("objects/phone_box", "an old roadside telephone booth with no glass, converted into a tiny post box with a slate-blue painted door and a brass slot, pixel art game object", 64),
 # -- nature (§5, §19: the Darklands, the Farlands' cold, the hill country)
 ("objects/pine_tree", "a tall dark pine tree with a straight trunk and layered needle boughs, pixel art game object", 96),
 ("objects/dead_tree", "a dead leafless grey tree with twisted bare branches, bark peeling, pixel art game object", 96),
 ("objects/oak_tree", "a broad old oak tree with a wide round green canopy and a thick trunk, pixel art game object", 128),
 ("objects/birch_cluster", "a cluster of three slim white birch trees with pale yellow leaves, pixel art game object", 96),
 ("objects/snow_pine", "a dark pine tree heavy with snow on its boughs, pixel art game object", 96),
 ("objects/bush", "a round dense green bush with a few small red berries, pixel art game object", 64),
 ("objects/tall_grass", "a tuft of tall dry wild grass, pixel art game object", 64),
 ("objects/boulder", "a large grey granite boulder with lichen patches and a crack, pixel art game object", 64),
 ("objects/rock_outcrop", "a jagged grey rock outcrop rising from the ground with layered strata and moss at the base, pixel art game object", 128),
 ("objects/fallen_log", "a fallen mossy log with the roots torn up at one end, fungus on the side, pixel art game object", 96),
 ("objects/stump", "a cut tree stump with an axe left in it and wood chips around the base, pixel art game object", 64),
 ("objects/reeds", "a clump of green reeds and cattails at a water edge, pixel art game object", 64),
 ("objects/snowdrift", "a low drift of fresh snow with a wind-carved edge and a few footprints, pixel art game object", 64),
 ("objects/cairn", "a stack of flat grey stones piled into a waymarker cairn on a ridge, pixel art game object", 64),
 # -- the Republic's road furniture (§5 stations, storage, shelters; §4 crews; WAYLIGHT-DESIGN third pass)
 ("objects/timber_bridge", "a short timber plank bridge with log piers and rope handrails crossing a stream, pixel art game object", 128),
 ("objects/stone_bridge", "an old arched stone bridge with a low parapet and a brass lantern at each end, moss, pixel art game object", 128),
 ("objects/ford_stones", "a line of flat stepping stones across a shallow stream with a wooden marker stake at each bank, pixel art game object", 96),
 ("objects/lamp_post", "a slender iron lamp post with a lit brass oil lantern and a small slate-blue flag, pixel art game object", 64),
 ("objects/dark_lamp_post", "a slender iron lamp post with its brass lantern unlit and a dark cloth hood tied over it, pixel art game object", 64),
 ("objects/signpost", "a wooden signpost with four hand-painted arrow boards pointing different ways, settlement signs painted on each, pixel art game object", 64),
 ("objects/notice_board", "a wooden notice board on two posts with paper sheets pinned to it under a small shingle roof, pixel art game object", 64),
 ("objects/letter_wall", "a free-standing marble wall with a grid of dark pigeonhole slots for public mail, a few letters showing, a bench at the base, pixel art game object", 128),
 ("objects/well", "a stone well with a timber windlass frame, a bucket on a rope and a brass cup on a chain, pixel art game object", 64),
 ("objects/water_trough", "a long wooden water trough on legs with a hand pump at one end, pixel art game object", 64),
 ("objects/hitching_rail", "a wooden hitching rail with a coiled rope and a feed bag hung on it, pixel art game object", 64),
 ("objects/hay_shelter", "an open-sided hay shelter of four posts and a shingle roof with hay bales stacked under it, pixel art game object", 96),
 ("objects/weigh_beam", "a large brass balance weigh-beam on a timber frame with two hanging pans and a bale on one pan, pixel art game object", 96),
 ("objects/lantern_rail", "a wooden rail hung with a row of six lit brass lanterns outside an outfitter's hall, pixel art game object", 64),
 ("objects/way_column", "a tall white marble column on a stepped base with a lit brass lantern cage on top, pixel art game object", 128),
 ("objects/roman_pillar", "a fluted white stone pillar with a simple capital, standing alone on a square base, pixel art game object", 64),
 ("objects/statue_column", "a stone column topped by a statue of a cloaked courier holding a lantern high, pixel art game object", 128),
 ("objects/pillared_entrance", "a residential house entrance of two fluted stone pillars carrying a plain lintel, a slate-blue door behind, pixel art game object", 96),
 ("objects/clock_tower", "a square stone bell and clock tower on an old concrete stub, a brass clock face, a bell in the open top, pixel art game object", 128),
 ("objects/timber_house", "a small frontier timber house with a shingle roof, a stone chimney with smoke, a slate-blue door and a lit window, pixel art game object", 128),
 ("objects/stone_house", "a small house of pale dressed stone with a terracotta tile roof, a pillared porch and a brass lantern by the door, pixel art game object", 128),
 ("objects/courier_hall", "a long two-storey stone hall with five identical slate-blue doors in a row and a bell on a bracket, pixel art game object", 128),
 ("objects/sorting_hall", "a domed civic hall of pale stone with a wide arched entrance, a brass post-horn over the door, a row of solar panels on the flat roof beside the dome, pixel art game object", 128),
 ("objects/greenhouse", "a long greenhouse of mismatched salvaged window panes on a low stone sill with white glazing bars, crop rows inside, pixel art game object", 128),
 ("objects/allotment", "a rectangular vegetable allotment of planted rows with a beehive and a scarecrow, pixel art game object", 96),
 ("objects/paper_mill_wheel", "a wooden waterwheel on a stone mill wall with a chute feeding water onto it, pixel art game object", 96),
 # -- the Farlands (§6, UNITY-DESIGN: gothic-cathedral engineering; the Ever-flame; smoke spools; famine)
 ("objects/smoke_spool", "a tall sharp dark-stone gothic spire used as a chimney, pierced with narrow lancet vents, thin smoke spooling from the pinnacle, pixel art game object", 128),
 ("objects/everflame_hall", "a small dark-stone gothic hall with a steep slate roof, lancet windows glowing orange from a fire inside, a spire chimney with smoke, flying buttresses, pixel art game object", 128),
 ("objects/lancet_ruin", "a ruined dark-stone wall fragment with a tall pointed lancet window arch and broken tracery, moss, pixel art game object", 96),
 ("objects/drystone_wall", "a length of drystone wall of grey field stones with a wooden stile step over it, pixel art game object", 64),
 ("objects/famine_field", "a blighted crop field of withered grey-brown stalks in rows with a bare scarecrow, pixel art game object", 96),
 ("objects/peat_stack", "a neat stack of cut dark peat bricks drying under a hide cover, pixel art game object", 64),
 ("objects/farkeeper_longhouse", "a long low dark-stone house with a steep slate roof, a pointed arch door, a small spire chimney with smoke and a round shield hung by the door, pixel art game object", 128),
 ("objects/standing_stone", "a tall weathered standing stone leaning slightly, carved with a simple spiral, a small offering bowl at the base, pixel art game object", 64),
 # -- the bunker inside (§11, §14)
 ("objects/bunk_beds", "a steel military bunk bed stacked three high with grey wool blankets folded square and a footlocker, pixel art game object", 64),
 ("objects/ration_shelves", "a steel shelving unit stacked with old ration cans and cardboard boxes with faded labels, mostly empty, pixel art game object", 64),
 ("objects/generator", "an old diesel generator on a concrete pad with a fuel drum, cables and a control panel with a red light, pixel art game object", 96),
 ("objects/air_filter", "a large industrial air filtration unit of grey steel ducts and a round fan grille, warning stencil, pixel art game object", 96),
 ("objects/terminal_desk", "an old grey steel desk with a green-phosphor computer terminal, a rotary telephone and stacked folders, pixel art game object", 64),
 ("objects/cistern", "a large riveted steel water cistern tank on a concrete base with a brass tap and a gauge, pixel art game object", 96),
 ("objects/bunker_door", "a heavy grey steel bunker corridor door in a concrete frame with a wheel lock and a stencilled number, pixel art game object", 64),
 ("objects/records_cabinet", "a tall grey steel filing cabinet with one drawer open showing folders, a stack of old books on top, pixel art game object", 64),
 ("objects/map_table", "a large steel map table under a hanging lamp with an old paper map pinned flat and markers on it, pixel art game object", 96),
 # -- Reaper ground (§3, P01: taking made permanent; marks of ownership)
 ("objects/watchtower", "a tall timber watchtower of scaffold poles with a plank platform, a corrugated roof and a confiscated road sign bolted to the front, pixel art game object", 128),
 ("objects/palisade_wall", "a length of palisade wall of sharpened timber poles with a walkway behind and rags tied at the top, pixel art game object", 96),
 ("objects/palisade_gate", "a heavy timber palisade gate with iron bands, a crude white painted ownership mark, and a confiscated stop sign nailed above it, pixel art game object", 128),
 ("objects/stockade_cage", "a crude stockade cage of scrap rebar and timber with a chained door, an empty bowl inside, pixel art game object", 64),
 ("objects/loot_heap", "a heap of seized goods under a tarp: sacks, crates, a rolled carpet and a bicycle, a white painted mark on the tarp, pixel art game object", 64),
 ("objects/marked_storehouse", "a squat storehouse of corrugated sheet and timber with a padlocked door and a large white painted ownership mark across the front, pixel art game object", 128),
 # -- the hill community (§3, P04 revised)
 ("objects/hide_hut", "a low dome hut of bent saplings covered in stitched hides with a smoke hole and a hide door flap, pixel art game object", 96),
 ("objects/drying_rack", "a wooden rack hung with strips of drying meat and stretched hides over a low smoky fire, pixel art game object", 64),
 ("objects/snare_line", "a line of small snare traps of bent saplings and wire set along a game trail with a marker of feathers, pixel art game object", 64),
 # -- the claims on the road (P02 Raiders, P03 Rebels, P05 Flame Keepers, P06 Iron Giants)
 ("objects/caravan_wreck", "a looted caravan wagon tipped in a ditch with a broken wheel, spilled crates and cut harness straps, pixel art game object, post-apocalyptic", 96),
 ("objects/loot_sacks", "a pile of stuffed burlap sacks and a strongbox with the lock cut, a pair of bolt cutters left on top, pixel art game object", 64),
 ("objects/furniture_barricade", "a street barricade of stacked furniture, doors, a cart and sandbags with a white armband tied to a chair leg, pixel art game object", 96),
 ("objects/settlement_sign", "a tall wooden post with a hand-painted settlement sign board and a tin lantern hung beneath it, pixel art game object", 64),
 ("objects/coal_bunker", "a stone coal bunker with a heavy iron door chained and padlocked, a shovel leaning beside it, pixel art game object", 64),
 ("objects/hearth_house", "a squat stone hearth house with a wide chimney pouring smoke, a warm lit doorway and a guard's stool beside it, pixel art game object", 128),
 ("objects/gantry_crane", "a salvage-yard gantry crane of riveted steel beams on four legs with a chain hoist and a hanging car engine, pixel art game object", 128),
 ("objects/scrap_press", "a heavy hydraulic scrap press machine with a crushed car cube beside it, hoses and a lever, pixel art game object", 96),
 # -- the Smoke (§3 the Farm)
 ("objects/oil_drums", "a cluster of tar-black oil drums, one tipped and leaking a dark slick, pixel art game object", 64),
 ("objects/flare_stack", "a thin rust-brown lattice flare stack with a small orange flame burning at the top and a pipe run at the base, pixel art game object", 128),
 ("objects/pipeline", "a length of rusted oil pipeline on short steel trestles with a valve wheel and a patch weld, pixel art game object", 96),
 ("objects/fuel_bowser", "a small two-wheeled fuel bowser trailer, a tar-black tank with a hand pump and a coiled hose, pixel art game object", 64),
 ("objects/storage_tank", "a huge pale cylindrical oil storage tank with a ladder up the side, rust streaks and a square door cut into it for a dwelling, pixel art game object", 128),
 # -- the Lamplighters (§8–9, P09)
 ("objects/ridge_blind", "a sniper's hide of netting and dry brush stretched over a low frame among rocks, a bedroll inside, pixel art game object", 64),
 ("objects/nomad_cache", "a hollow under a flat rock lid with a wrapped bundle and a hooded lantern hidden inside, the lid pushed aside, pixel art game object", 64),
]

# ---------------------------------------------------------------- 8-direction objects (Pro, 20–40 gens each) ----
OBJECTS8 = {
 # the-smoke-faction design + vehicles doc V5: the only motor vehicle anyone will see; §3 the Farm
 "objects8/smoke_bowser": ("a squat post-apocalyptic fuel tanker war-truck: one enormous pale tar-streaked cylindrical tank with riveted bands on a small cab with oversized fat tyres, cut-pipe shingle plates over the cab, two round headlamps, a long hose arm curled over the tank with a flared nozzle, pixel art game vehicle", 96),
 # §4 Haulers and Donkey Caravans
 "objects8/caravan_wagon": ("a covered caravan wagon on four wooden wheels, canvas hood over a slate-blue painted body, crates and bales lashed on, a brass lantern on a hook at the front, shafts for a draft animal, pixel art game vehicle", 96),
}

# ---------------------------------------------------------------- inventory icons (pixen 32px) ----
ICONS = {
 # the courier's desk (§4)
 "icons/wax_seal": "game inventory icon of a stick of red sealing wax and a brass post-horn seal stamp, pixel art, isolated",
 "icons/ink_and_quill": "game inventory icon of a small ink pot with a quill pen, pixel art, isolated",
 "icons/ledger": "game inventory icon of a leather-bound ledger book with a brass clasp, pixel art, isolated",
 "icons/hand_stamp": "game inventory icon of a wooden-handled brass postmark hand stamp, pixel art, isolated",
 "icons/written_promise": "game inventory icon of a rolled parchment scroll tied with a slate-blue ribbon and a wax seal, pixel art, isolated",
 "icons/courier_badge": "game inventory icon of a polished brass letter-carrier badge with a post horn, pixel art, isolated",
 "icons/lamp_oil": "game inventory icon of a small brass oil can with a long spout, pixel art, isolated",
 "icons/paper_sheets": "game inventory icon of a small stack of cream paper sheets tied with string, pixel art, isolated",
 # the road (§5)
 "icons/bedroll": "game inventory icon of a rolled wool bedroll with leather straps, pixel art, isolated",
 "icons/rope": "game inventory icon of a coil of hemp rope, pixel art, isolated",
 "icons/matches": "game inventory icon of a small tin of matches with one match beside it, pixel art, isolated",
 "icons/compass": "game inventory icon of a brass pocket compass with the lid open, pixel art, isolated",
 "icons/spyglass": "game inventory icon of a brass telescope spyglass, pixel art, isolated",
 "icons/firewood": "game inventory icon of a bundle of split firewood tied with cord, pixel art, isolated",
 "icons/horseshoe": "game inventory icon of an iron horseshoe with nails, pixel art, isolated",
 "icons/feed_bag": "game inventory icon of a canvas feed bag of oats, pixel art, isolated",
 "icons/shovel": "game inventory icon of a steel shovel with a wooden handle, pixel art, isolated",
 "icons/pickaxe": "game inventory icon of a pickaxe with a wooden handle, pixel art, isolated",
 "icons/hammer_and_nails": "game inventory icon of a claw hammer and three nails, pixel art, isolated",
 "icons/bandage_roll": "game inventory icon of a roll of clean linen bandage with a safety pin, pixel art, isolated",
 "icons/dried_fish": "game inventory icon of two dried salted fish on a string, pixel art, isolated",
 "icons/bread_loaf": "game inventory icon of a round rustic bread loaf with a slice cut, pixel art, isolated",
 # the bunker (§11, §14)
 "icons/sbsn_card": "game inventory icon of a laminated grey identity card with a photo, a barcode and a small red maple leaf, pixel art, isolated",
 "icons/ration_can": "game inventory icon of an old olive-green military ration tin with a faded label, pixel art, isolated",
 "icons/radio_handset": "game inventory icon of a black military radio handset with a coiled cord, pixel art, isolated",
 "icons/flashlight": "game inventory icon of a yellow hand-crank flashlight, pixel art, isolated",
 "icons/gas_mask": "game inventory icon of an old grey rubber gas mask with round eye pieces, pixel art, isolated",
 "icons/clipboard": "game inventory icon of a clipboard with a form and a pen, pixel art, isolated",
 "icons/old_book": "game inventory icon of an old cloth-bound hardback book with a faded gold title, pixel art, isolated",
 "icons/rifle_cartridges": "game inventory icon of five brass rifle cartridges standing in a row, pixel art, isolated",
 # the Lamplighters, the hill people, the Farkeepers, the Smoke, the claims (§6, §8, P02–P06)
 "icons/rifle_scope": "game inventory icon of a black rifle telescopic scope, pixel art, isolated",
 "icons/ghillie_net": "game inventory icon of a folded bundle of camouflage netting and rags, pixel art, isolated",
 "icons/snare_wire": "game inventory icon of a coil of thin snare wire with a loop, pixel art, isolated",
 "icons/bone_whistle": "game inventory icon of a small carved bird-bone whistle on a cord, pixel art, isolated",
 "icons/ochre_pot": "game inventory icon of a small clay pot of red-orange ochre paint with a finger mark, pixel art, isolated",
 "icons/round_shield": "game inventory icon of a round wooden shield rimmed in iron painted dark green with a slate blue centre, pixel art, isolated",
 "icons/bearded_axe": "game inventory icon of a bearded axe with a long ash haft, pixel art, isolated",
 "icons/ever_coal": "game inventory icon of a single glowing ember coal in an iron clasp on a chain, pixel art, isolated",
 "icons/peat_brick": "game inventory icon of a dark cut peat brick, pixel art, isolated",
 "icons/jerrycan": "game inventory icon of a tar-black steel jerrycan with a spout, pixel art, isolated",
 "icons/pressure_gauge": "game inventory icon of a round brass pressure gauge with a cracked glass and a bent needle, pixel art, isolated",
 "icons/bolt_cutters": "game inventory icon of a pair of long-handled red bolt cutters, pixel art, isolated",
 "icons/burlap_mask": "game inventory icon of a burlap sack mask with cut eye holes, pixel art, isolated",
 "icons/armband": "game inventory icon of a white cloth armband with a hand-painted settlement sign, pixel art, isolated",
 "icons/key_ring": "game inventory icon of a heavy iron ring of old keys, pixel art, isolated",
 "icons/rivet_gun": "game inventory icon of a heavy pneumatic rivet gun with a hose, pixel art, isolated",
 "icons/hydraulic_hose": "game inventory icon of a coiled black hydraulic hose with brass couplings, pixel art, isolated",
}

# faction emblems (pixen 32px) — for UI, map markers and banners
EMBLEMS = {
 "emblems/republic": "game emblem icon of a brass post horn with a small lantern hanging from it on a slate blue round shield shape, pixel art, isolated",
 "emblems/waylight": "game emblem icon of a lit brass lantern above a white marble column on a slate blue round shield shape, pixel art, isolated",
 "emblems/farkeeper": "game emblem icon of a tall sharp dark spire with a curl of smoke and a small flame at its base on a dark green round shield shape, pixel art, isolated",
 "emblems/lamplighter": "game emblem icon of an iron lantern with a dark cloth hood tied over it showing one sliver of light, on a charcoal round shield shape, pixel art, isolated",
 "emblems/diefenbunker": "game emblem icon of a red maple leaf over a round grey steel door, on a navy round shield shape, pixel art, isolated",
 "emblems/reaper": "game emblem icon of a crude white painted ownership mark on a black round shield shape, pixel art, isolated",
 "emblems/smoke": "game emblem icon of a tar-black drop with a small orange flame at the top on a rust round shield shape, pixel art, isolated",
 "emblems/hill_community": "game emblem icon of an ochre hand print with three small bone beads on a hide brown round shape, pixel art, isolated",
 "emblems/raider": "game emblem icon of crossed bolt cutters and a rope loop on a patchwork brown round shape, pixel art, isolated",
 "emblems/rebel": "game emblem icon of a white armband with a painted house sign on a canvas brown round shape, pixel art, isolated",
 "emblems/flame_keeper": "game emblem icon of an iron key laid over a glowing hearth on a soot black round shape, pixel art, isolated",
 "emblems/iron_giant": "game emblem icon of a riveted steel claw gripping a gear on a rust grey round shape, pixel art, isolated",
}

# ---------------------------------------------------------------- tiles ----
TILESETS = {
 # key: (lower, upper, transition)
 "tiles/grass_to_mud": ("wet green lowland grass", "dark churned mud with puddles and wheel ruts", "muddy grass edge with trampled blades"),
 "tiles/dirt_to_ash": ("dry packed dirt", "grey ash and charred black ground with embers", "scorched dirt edge with soot"),
 "tiles/heather_to_peat": ("purple-brown heather moorland", "dark cut peat bog with standing water", "peat edge with tufts of heather"),
 "tiles/concrete_to_grate": ("smooth grey bunker concrete floor with painted lines", "steel floor grating over a dark channel", "riveted steel edge strip"),
 "tiles/flagstone_to_cobble": ("large pale flagstone paving", "grey cobblestone paving", "flagstone edge set into cobbles"),
}
ROADS = {
 "tiles/asphalt_roads": "an old cracked asphalt highway with faded lane paint, grass growing through the cracks, post-apocalyptic",
 "tiles/flagstone_roads": "a civic avenue of large pale dressed flagstones with a shallow gutter along the edge",
}
# building kits via tiles-pro (tile_feature "building") — probe one first to learn the cost, then the rest if affordable
BUILDINGS = {
 "kits/waylight_stone": ("pale dressed stone civic walls with a terracotta tile roof and slate-blue doors", "pale flagstone floor", "terracotta tile roof"),
 "kits/farkeeper_gothic": ("dark dressed stone walls with narrow pointed lancet windows", "dark slate flagstone floor", "steep dark slate roof"),
 "kits/bunker_steel": ("grey riveted steel bunker walls with stencilled numbers and pipe runs", "grey concrete floor with painted lines", "flat grey concrete roof"),
 "kits/frontier_timber": ("weathered timber plank walls with corrugated scrap patches", "rough plank floor", "shingle roof"),
}

# ---------------------------------------------------------------- story-plate backgrounds (pixflux background 400x224) ----
PLATES = {
 "plates/bunker_interior": "pixel art game background, a long underground bunker corridor of grey riveted steel and concrete, pipes and cables along the ceiling, caged lights, stencilled numbers, a green phosphor terminal glowing at a desk, stacked ration boxes, wide landscape, no people",
 "plates/sorting_hall": "pixel art game background, inside a domed civic mail hall of pale stone, tall pigeonhole walls full of letters, long sorting tables, brass lanterns, sacks of mail, sunlight through a high window, wide landscape, no people",
 "plates/waylight_forum": "pixel art game background, a sunlit stone forum of a courier city with a white marble column topped by a brass lantern, a colonnade, a fountain, a marble letter wall with pigeonholes, terracotta roofs and a dome behind, wide landscape, no people",
 "plates/unity_plaza": "pixel art game background, a plaza of a capital city where two styles meet: white marble pillars and a statue column on one side, dark pointed gothic spires with smoke spooling from their tips on the other, cobbles and flagstones, a brass brazier burning, wide landscape, no people",
 "plates/farlands_village": "pixel art game background, a cold mountain village of dark stone longhouses with steep slate roofs and tall sharp spire chimneys spooling thin smoke, a gothic hall with lancet windows glowing orange, snow on the ridges, wide landscape, no people",
 "plates/famine_field": "pixel art game background, a bleak highland field of withered grey crop rows under a low sky, a drystone wall, a bare scarecrow, a standing stone, a village with spire chimneys far off, wide landscape, no people",
 "plates/reaper_stockade": "pixel art game background, inside a warband stockade of sharpened timber palisades and scaffold watchtowers, confiscated road signs with white painted marks, a corrugated storehouse, a rebar cage, dusty afternoon light, wide landscape, no people",
 "plates/hearth_hall": "pixel art game background, inside a stone hearth hall where a great furnace roars behind an iron gate, chained coal bunkers, a rack of keys on the wall, warm orange light and long shadows, wide landscape, no people",
 "plates/scrap_yard": "pixel art game background, a salvage yard of sorted scrap: a gantry crane with a chain hoist, a hydraulic press, stacked crushed cars, an armored walking frame parked by a workshop shed with welding sparks, wide landscape, no people",
 "plates/tank_farm": "pixel art game background, a post-apocalyptic tank farm at dusk: huge pale cylindrical oil tanks with ladders, a thin lattice flare stack burning orange at the top, pipe runs on trestles, black scorched ground, tar-black drums, wide landscape, no people",
 "plates/river_crossing": "pixel art game background, an old arched stone bridge over a cold grey river in a wooded valley, brass lanterns at the bridge ends, a worn road leading to it, mist on the water, morning light, wide landscape, no people",
 "plates/snow_pass": "pixel art game background, a high snowy mountain pass with a narrow road between rock walls, snow-laden pines, a stone cairn, a milestone half buried in snow, grey sky and blowing snow, wide landscape, no people",
 "plates/burned_settlement": "pixel art game background, a small settlement after a fire: charred timber house frames, ash ground, a blackened well, a scorched notice board still standing, smoke drifting, grey morning, wide landscape, no people",
 "plates/old_highway": "pixel art game background, a cracked old asphalt highway with faded lane paint running through dry grassland, rusted cars pushed to the shoulder, a bent green highway sign, power pylons with snapped wires, late afternoon, wide landscape, no people",
}

# ---------------------------------------------------------------- UI (generate-ui-v2) and a second font ----
UI = {
 "ui/inventory_panel": ({"description": "pixel art RPG inventory panel of dark slate wood with a brass rivet border, a grid of 6 by 4 empty square item slots with brass corners, a small brass post-horn emblem at the top", "image_size": {"width": 512, "height": 384}, "seed": 7, "color_palette": "dark slate wood, brass and parchment"}),
 "ui/letter_panel": ({"description": "pixel art RPG reading panel shaped like an opened cream parchment letter with a red wax seal at the bottom, a slate-blue ribbon across one corner and worn folded edges, empty of text", "image_size": {"width": 512, "height": 384}, "seed": 7, "color_palette": "parchment cream, slate blue and red wax"}),
 "ui/map_frame": ({"description": "pixel art RPG map frame of worn brown leather with brass corner plates and a brass compass rose in one corner, empty parchment centre", "image_size": {"width": 512, "height": 384}, "seed": 7, "color_palette": "brown leather, brass and parchment"}),
 "ui/hud_bars": ({"description": "pixel art RPG HUD with three horizontal status bars stacked with brass end caps and dark slate frames: the top bar red, the middle bar tan, the bottom bar amber, small brass icons at the left of each", "image_size": {"width": 256, "height": 96}, "seed": 7, "color_palette": "dark slate, brass, red tan and amber"}),
 "ui/button_set": ({"description": "pixel art RPG button set: three rectangular buttons of dark slate wood with a brass edge in a row, one normal, one highlighted, one pressed, empty of text", "image_size": {"width": 384, "height": 96}, "seed": 7, "color_palette": "dark slate wood and brass"}),
 "ui/standing_meter": ({"description": "pixel art RPG horizontal meter with a brass needle pointer, the left end dark red and the right end slate blue, a dark wood frame with rivets", "image_size": {"width": 256, "height": 64}, "seed": 7, "color_palette": "dark wood, brass, dark red and slate blue"}),
 "ui/map_markers": ({"description": "pixel art set of small map marker pins in a row: a brass post horn, a lantern, a red warning mark, a tent, a house, a crossed swords mark, a question mark, each on a small round dark badge", "image_size": {"width": 256, "height": 48}, "seed": 7, "color_palette": "dark slate, brass, red and parchment"}),
}
FONTS = {
 "ui/font_bunker": {"description": "military stencil block capitals as sprayed on a bunker wall, grey with slight overspray, uniform width", "weight": "Bold", "glyph_px": 16, "seed": 7, "font_name": "Diefenbunker Stencil"},
}

# ---------------------------------------------------------------- portraits (character_to_portrait, 25 each) ----
PORTRAITS = ["party/tally", "party/merrow", "party/kell", "reaper/overseer", "lamplighter/nomad_elder", "cannibal/hearth_keeper", "rebel/speaker", "smoke/gauger", "republic/envoy", "farkeeper/flame_tender"]

# ---------------------------------------------------------------- animations ----
HORSE = {"farkeeper/captain", "animals/draft_horse", "animals/light_horse", "waylight/donkey", "farkeeper/rifle_rider", "farkeeper/recon_rider"}
# template anims for characters that have none (the 01BATCH side set)
SIDE_WALK = ["diefenbunker/soldier", "diefenbunker/salvager", "lamplighter/nomad", "waylight/mail_worker", "waylight/hauler", "waylight/donkey"]
# runs — the party and the animals; a courier game is played at a run
RUN = ["party/postman", "party/tally", "party/merrow", "party/kell", "party/ada", "animals/draft_horse", "animals/light_horse", "farkeeper/rifle_rider"]
# walks for every new character
NEW_WALK = list(CHARS.keys())
# idles: new scene-carriers, then existing characters that only have a walk
IDLE = ["farkeeper/flame_tender", "farkeeper/spool_wright", "farkeeper/matron", "waylight/postmaster", "waylight/scribe", "republic/envoy", "republic/registrar", "diefenbunker/archivist", "smoke/driver",
        "lamplighter/nomad_elder", "rebel/speaker", "lamplighter/marksman", "diefenbunker/enforcement_trooper", "flamekeeper/stoker", "cannibal/lookout", "reaper/household_woman", "reaper/child"]
# template story/combat beats (name, template)
TEMPLATE = [("party/tally", "stance", "fight-stance-idle-8-frames"), ("party/kell", "crouch", "crouching"), ("farkeeper/shield_bearer", "swing", "throw-object"), ("farkeeper/shield_bearer", "hit", "taking-punch"),
            ("waylight/trainee", "run", "running-8-frames"), ("diefenbunker/child", "pickup", "picking-up"), ("farkeeper/child", "pickup", "picking-up"), ("waylight/lamplighter", "reach", "throw-object"),
            ("republic/envoy", "bow", "picking-up"), ("waylight/postmaster", "drink", "drinking")]
# custom v3 hero beats, south only, ~30 each
CUSTOM = [("party/ada", "read", "opens a letter with both hands, holds it up and reads aloud to a crowd, one hand rising to gesture, then lowers the letter"),
          ("party/merrow", "treat", "kneels on one knee, unrolls the tool wrap, binds a bandage around an unseen patient's arm and checks the pulse at the wrist"),
          ("party/tally", "fire", "levers the cut-down rifle one-handed at the hip, fires with a flash and recoil, levers again, then glances down at the bandolier to count"),
          ("party/kell", "map", "unslings a map tube from the back, pulls out a rolled canvas map, unrolls it wide with both hands and studies it, looks up along the road"),
          ("diefenbunker/douglas_reed", "address", "steps forward, raises one hand palm out to address a crowd, speaks with small emphatic gestures of the clipboard, then lowers the hand"),
          ("farkeeper/flame_tender", "tend", "kneels, feeds a log into a fire with the iron hook, works the bellows twice so sparks rise, then stands and bows the head to the flame"),
          ("republic/envoy", "offer", "opens the document case, draws out the sealed scroll and holds it out with both hands toward the viewer, waits, then withdraws it slowly")]
