"""The Convergence batch — every asset keyed to the compendium (section refs in comments)."""

# ---------------------------------------------------------------- characters (v3, 64px unless noted) ----
CHARS = {
 # §10–14 the Diefenbunker Society: Canadian-origin descendants, hundreds of years underground, work gear, old pins, C8/C7/C22
 "diefenbunker/douglas_reed": ("older man, Diefenbunker Prime Administer, grey hair combed back, tired administrator's face with reading glasses, a faded dark-blue civil service jacket with a row of small ancient enamel pins on the lapel and a laminated badge on a lanyard, pressed trousers, polished old shoes, a clipboard of papers under one arm, pale skin from a life underground, muted navy grey and one small red pin palette", "mannequin"),
 "diefenbunker/sarah_oconnel": ("woman mechanic from an underground bunker society, grease-stained grey coveralls with the sleeves tied at the waist over a dark tank top, welding goggles pushed up into short practical hair, heavy leather gauntlets, tool belt with wrenches, a welding torch in one hand and its hose over the shoulder, pale skin, sharp weary face, grey coverall gunmetal and a small copper flame palette", "mannequin"),
 "diefenbunker/jimmy_butler": ("bunker enforcement lieutenant, dark navy uniform with a department shoulder patch and rank bars, black beret, tactical vest of old canvas webbing, radio handset clipped at the chest, black C8 carbine with a red maple leaf etched on the sight housing held across the body, pale clean-shaven young face, alert, navy black and gunmetal with one red leaf palette", "mannequin"),
 "diefenbunker/enforcement_trooper": ("bunker enforcement trooper, dark navy fatigues, olive-drab C7 rifle with a green plastic stock and a boxy optical sight, old combat helmet with a chin strap, canvas webbing, knee pads, pale skin, navy olive drab and gunmetal palette", "mannequin"),
 "diefenbunker/work_crew": ("bunker work-crew digger on New World Day, grey coveralls with reflective strips, yellow hard hat with a headlamp, dust mask around the neck, heavy gloves, a shovel over the shoulder and a coil of rope, pale skin, hopeful young face, grey safety-yellow and dust palette", "mannequin"),
 # §8–9, §13–14 Lamplighters: crafty, elusive, precision fire; the Society's precision rifles; the cloaked torch
 "lamplighter/sniper": ("post-apocalyptic exiled marksman, long dark hooded cloak of layered rags and netting that breaks the silhouette, hood up, a scoped bolt-action precision rifle with a long heavy barrel slung on the back, a shuttered iron lantern hooked at the belt with the shutter closed, dark travel clothes, soft-soled boots, bedroll and pack, patient watchful face in shadow, charcoal moss-green and dust palette, no bright colour", "mannequin"),
 "lamplighter/marksman": ("post-apocalyptic exiled rifleman, dark weathered cloak thrown back over one shoulder, semi-automatic marksman rifle with a scope held ready, a small shuttered lantern at the hip, grey scarf over the lower face, dark wide-brimmed hat, worn travel gear, charcoal grey and dust brown palette", "mannequin"),
 "lamplighter/nomad_hauler": ("post-apocalyptic exiled wanderer carrying a huge dark pack, heavy hooded cloak of dark canvas, walking staff with an iron ferrule, a covered lantern hanging from the pack frame, worn boots wrapped in cloth, weary determined face, charcoal and dark leather palette", "mannequin"),
 "lamplighter/nomad_elder": ("old exiled wanderer woman, long grey hair in a braid, dark hooded cloak patched many times, a tall staff, a small brass lantern with a dark cloth hood tied over it hanging from the staff, layered dark travel clothes, weathered kind face, charcoal dust brown and one dim brass palette", "mannequin"),
 # §3, P01 Reaper territory: confiscated civic/military clothing made uniform through marks of ownership; households; captives
 "reaper/overseer": ("post-apocalyptic warband overseer, a confiscated dark police duty jacket with the old badge scraped off and a crude painted white ownership mark on the chest and sleeve, black peaked cap, leather gloves, a coiled whip and a ring of keys at the belt, a short club, heavy boots, hard flat face, black charcoal with white paint marks palette", "mannequin"),
 "reaper/household_woman": ("post-apocalyptic townswoman living under a warband, plain patched brown dress and a grey shawl, headscarf, worn shoes, carrying a bundle of firewood and a small child's shoe in the other hand, drawn anxious face, dust brown grey and faded orange scrap of cloth palette", "mannequin"),
 "reaper/child": ("small post-apocalyptic child in an oversized faded orange rain coat rolled at the sleeves, bare knees, worn sandals, holding a wooden toy horse, short messy hair, wide serious eyes, faded orange and dust palette", "mannequin"),
 "reaper/captive": ("post-apocalyptic captive prisoner, gaunt, torn undershirt and ragged trousers, bare feet, rope binding the wrists in front, a crude painted ownership mark on the chest, hollow cheeks, matted hair, bruised, grey and dust palette, hunched", "mannequin"),
 "waylight/haven_courier": ("post-apocalyptic frontier courier from a small settlement, faded slate-blue postal tunic under a hide poncho, a hand-painted wooden settlement sign patch sewn on the shoulder, canvas mail sack, fingerless gloves, straw hat, dusty boots, freckled earnest face, slate blue hide brown and one painted white sign palette", "mannequin"),
 # P04 Cannibals (revised): learned local practices, obligations, material conditions — human, specific, no monster costume
 "cannibal/hunter": ("post-apocalyptic hunter from an isolated hill community, lean and strong, layered cured hides and a fur collar, face and forearms marked with pale ash paint, hair in tight braids with bone toggles, a spear made from a sharpened steel pipe, a coil of snare wire and hooks at the belt, bare feet wrapped in hide, wary intelligent face, ash bone ochre and hide brown palette", "mannequin"),
 "cannibal/hearth_keeper": ("old woman elder of an isolated hill community, layered hides and a heavy woven shawl, necklaces of small bones and river stones, grey hair bound with sinew, carrying a blackened iron cook pot and a long ladle, ochre marks on the cheeks, weathered proud face, ash ochre and hide brown palette", "mannequin"),
 "cannibal/lookout": ("wiry young lookout from an isolated hill community, bare torso with ash paint stripes, hide breechcloth and leg wraps, a sling and a pouch of stones, a bird-bone whistle on a cord, crouched alert posture, shaved head with a single braid, ash bone and ochre palette", "mannequin"),
 # P02 Raiders: mobile, improvised, equipment adapted for travel and theft; Bandits separately
 "raider/rover": ("post-apocalyptic raider scavenger, patchwork jacket of many salvaged fabrics with pouches sewn everywhere, aviator goggles, a red bandana over the nose, a long-handled bolt cutter across the back, a coil of rope, a crowbar at the belt, fingerless gloves, mismatched boots, lean grinning face, dusty multicolour patchwork palette", "mannequin"),
 "raider/bandit": ("post-apocalyptic bandit, ragged long coat, a sack over the shoulder, a crude pipe rifle, a burlap mask with cut eye holes pulled up on the forehead, dirty scarf, torn gloves, hunched wary stance, dust grey and brown palette", "mannequin"),
 # P03 Rebels: local loyalties, settlement signs, practical regional dress
 "rebel/militiaman": ("post-apocalyptic settlement militiaman, farmer's canvas coat and woollen cap, a hunting rifle with a scratched wooden stock, a white armband with a hand-painted local settlement sign, a hatchet at the belt, muddy boots, stubborn weathered face, canvas brown wool grey and white armband palette", "mannequin"),
 "rebel/speaker": ("post-apocalyptic settlement spokeswoman, practical regional dress of a thick wool skirt and a leather jerkin, a knitted shawl, a hand-painted wooden sign board held under one arm, a tin lantern in the other hand, grey-streaked hair tied back, fierce open face, wool grey leather brown and one painted sign palette", "mannequin"),
 # P05 Flame Keepers: industrial, custodial; warmth kept under guard
 "flamekeeper/furnace_warden": ("post-apocalyptic furnace warden, heavy scorched leather apron over a wool coat, long iron tongs, a caged iron lantern holding glowing coals, a heavy ring of keys at the belt, soot-blackened gloves and face, a brass-fitted leather cap, watchful guarded expression, soot black leather brown and one glowing coal orange palette", "mannequin"),
 "flamekeeper/stoker": ("post-apocalyptic furnace stoker, bare muscular arms streaked with soot, a coal shovel, a heavy leather vest and thick trousers, a wet headwrap, boots with steel toes, a small brass token on a cord at the neck, soot black and leather brown palette", "mannequin"),
 # P06 Iron Giants: human-operated armored working frames; restoration culture
 "irongiant/frame_pilot": ("post-apocalyptic salvage-frame pilot, a padded harness with buckles over a mechanic's jumpsuit, a welding visor raised on the head, heavy insulated gloves, a hydraulic hose coupling at the belt, knee and shin guards, oil-stained, calm technical face, oil grey rust and brass fittings palette", "mannequin"),
 "irongiant/working_frame": ("a human-operated armored salvage walking frame, a bulky two-legged industrial exoskeleton of riveted repaired steel plates with a caged open cockpit in the chest where a small pilot sits, two heavy hydraulic claw arms, exposed pistons and hoses, a lifting hook, rust patches and fresh welds, rust grey and brass palette, post-apocalyptic machine", "mannequin"),
 # §4 Waylighter road crews: Masons, Forresters, Path Pressers
 "waylight/mason": ("post-apocalyptic road mason, slate-blue tunic with rolled sleeves under a leather apron, a wooden hod full of grey cobblestones on one shoulder, a mallet at the belt, knee pads, dusty boots, broad friendly face, slate blue leather brown and grey stone palette", "mannequin"),
 "waylight/forrester": ("post-apocalyptic forester, slate-blue tunic under a thick checked wool shirt, a long-handled felling axe over one shoulder and a fresh log balanced on the other, leather gloves, a coil of rope, wool cap, bearded weathered face, slate blue wool green and raw timber palette", "mannequin"),
 "waylight/path_presser": ("post-apocalyptic route-marker walker, slate-blue tunic and a long dust coat, a bundle of painted wooden marker stakes strapped to the back and a mallet in hand, heavy hobnailed boots, a rolled map at the belt, wide-brimmed hat, sun-lined face, slate blue dust brown and painted white stakes palette", "mannequin"),
 # §6 Farkeeper captain, mounted, banner
 "farkeeper/captain": ("towering mountain warrior captain on a heavy dark horse, pale skin, iron skull cap with a fur trim, hide and wool coat with a dark green sash, a tall banner pole with a slate blue over dark green banner held upright, a long rifle in a saddle scabbard, fur boots in the stirrups, hide brown iron grey dark green and slate blue palette", "horse"),
 # §6 horses: different animals bring different strengths in speed, toughness, travel
 "animals/draft_horse": ("heavy draft horse, dark bay with a black mane and feathered hooves, broad chest, plain leather harness and a pack saddle, patient head, dark bay and leather brown palette", "horse"),
 "animals/light_horse": ("fast light riding horse, dun coloured with a dark dorsal stripe, lean build, a light saddle and bridle, alert ears, dun and leather brown palette", "horse"),
}

# ---------------------------------------------------------------- map objects (high top-down, 64px) ----
OBJECTS = {
 "objects/station_shelter": "a small roadside courier station: a lean-to shelter of timber and corrugated scrap with a bench inside, a brass lantern hanging from the post, and a slate-blue painted post-horn sign, post-apocalyptic, pixel art game object",
 "objects/ladder": "a wooden ladder leaning against a rock ledge, weathered, pixel art game object",
 "objects/cache_crate": "a half-buried wooden cache crate with an iron hasp and a small brass plate, tarp over one corner, pixel art game object",
 "objects/milestone": "a squat carved stone road marker with a small brass plate on its face, moss at the base, pixel art game object",
 "objects/cloaked_lantern": "an iron hand lantern with a dark cloth hood tied over it so only a sliver of light escapes at the bottom, set on the ground, pixel art game object",
 "objects/letter_bundle": "a bundle of folded letters tied with string, one wax seal visible, pixel art game object",
 "objects/blast_door": "an enormous circular steel bunker blast door standing half open in a concrete tunnel mouth, rust streaks broken free of the seals, hydraulic pistons, painted stencil markings, pixel art game object",
 "objects/bunker_hatch": "a round steel bunker hatch in a concrete collar set into the ground, wheel lock, warning stripes, pixel art game object",
 "objects/bullion_crate_barricade": "a barricade of massive steel bank bullion crates stacked two high across a tunnel, riveted, stencilled, sandbags at the base, pixel art game object",
 "objects/comms_array": "an old military shortwave radio communications array: a rack of grey steel radio equipment with dials and a coiled cable running up to a tall antenna mast, pixel art game object",
 "objects/decon_shower": "an industrial radiation decontamination shower array in a concrete tunnel: a frame of steel pipes with shower heads and a drain grate, warning signs, pixel art game object",
 "objects/reaper_marker": "a warband territory marker: a scrap-metal pole with confiscated road signs bolted on and a crude white painted ownership mark, rags tied at the top, pixel art game object",
 "objects/furnace": "a large iron furnace with a glowing door, a stack of coal and a brass gauge, tended and well kept, pixel art game object",
 "objects/highleaf_bale": "a bale of dried green-gold leaf bound with twine on a wooden pallet, pixel art game object",
 "objects/road_roller": "a hand-pulled stone road roller on a wooden frame with a pull bar, pixel art game object",
 "objects/cobble_pile": "a neat pile of dressed grey cobblestones on a wooden pallet, pixel art game object",
 "objects/timber_stack": "a stack of cut timber logs and split planks bound with rope, pixel art game object",
 "objects/scrap_pile": "a pile of flattened rusty car panels and metal sheets sorted for road building, pixel art game object",
 "objects/everflame_brazier": "a tall iron brazier on a carved stone base with a bright flame that never goes out, pixel art game object",
 "objects/campfire": "a small campfire ring of stones with a cooking pot on a tripod, pixel art game object",
 "objects/nomad_tent": "a low dark canvas nomad tent with a hooded lantern hanging at the entrance, pixel art game object",
 "objects/hill_totem": "a gathering-place marker of an isolated hill community: a weathered post hung with river stones, small bones and strips of hide, ochre hand prints, pixel art game object",
 "objects/salvage_frame_parked": "a parked human-operated armored salvage walking frame, bulky riveted steel, hydraulic claw arms lowered, cage cockpit empty, pixel art game object",
 "objects/mail_cart": "a two-wheeled wooden mail cart painted slate blue with a brass post horn emblem, full of sacks, pixel art game object",
 "objects/wire_fence_gate": "a gate in a wire fence made from salvaged bed frames and road signs, pixel art game object",
 "objects/first_reply_table": "a long wooden table in a settlement square with an opened bundle of letters spread on it, a lantern and cups, pixel art game object",
}

# ---------------------------------------------------------------- inventory icons (pixen 32px) ----
ICONS = {
 "icons/letter_sealed": "game inventory icon of a folded letter sealed with a small brass post-horn seal, pixel art, isolated",
 "icons/letter_brass": "game inventory icon of an important letter with a polished brass clasp and slate blue ribbon, pixel art, isolated",
 "icons/cargo_crate": "game inventory icon of a small wooden cargo crate with rope handles, pixel art, isolated",
 "icons/cobblestone": "game inventory icon of three grey cobblestones, pixel art, isolated",
 "icons/timber": "game inventory icon of two cut timber planks, pixel art, isolated",
 "icons/scrap_metal": "game inventory icon of a bent rusty metal sheet with rivet holes, pixel art, isolated",
 "icons/highleaf": "game inventory icon of a small bundle of hand-rolled green-gold leaf smokes tied with string, pixel art, isolated",
 "icons/c8_carbine": "game inventory icon of a compact black military carbine rifle with an optical sight, side view, pixel art, isolated",
 "icons/c7_rifle": "game inventory icon of a military rifle with olive-green furniture and a boxy optical sight, side view, pixel art, isolated",
 "icons/c22_pistol": "game inventory icon of a modern black semi-automatic service pistol, side view, pixel art, isolated",
 "icons/c14_timberwolf": "game inventory icon of a long bolt-action precision sniper rifle with a large scope and bipod, side view, pixel art, isolated",
 "icons/c3a1_rifle": "game inventory icon of a bolt-action sniper rifle with a heavy barrel and a traditional wooden stock and scope, side view, pixel art, isolated",
 "icons/c20_dmr": "game inventory icon of a semi-automatic marksman rifle with a scope and a long magazine, side view, pixel art, isolated",
 "icons/longbow": "game inventory icon of a tall yew longbow with an arrow, pixel art, isolated",
 "icons/claymore": "game inventory icon of a huge two-handed claymore sword, pixel art, isolated",
 "icons/spear": "game inventory icon of an ash spear with an iron head, pixel art, isolated",
 "icons/cloaked_torch": "game inventory icon of a small iron lantern with a dark cloth hood tied over it, pixel art, isolated",
 "icons/mail_satchel": "game inventory icon of a leather mail satchel with a brass buckle, pixel art, isolated",
 "icons/ration": "game inventory icon of a wrapped bread ration and dried meat, pixel art, isolated",
 "icons/water_flask": "game inventory icon of a dented tin water flask with a leather strap, pixel art, isolated",
 "icons/saddle": "game inventory icon of a worn leather horse saddle, pixel art, isolated",
 "icons/map_tube": "game inventory icon of a rolled canvas map in a leather tube, pixel art, isolated",
 "icons/welding_torch": "game inventory icon of a welding torch with a hose, pixel art, isolated",
 "icons/red_leaf_pin": "game inventory icon of a small enamel pin with a red maple leaf, pixel art, isolated",
 "icons/coal_lantern": "game inventory icon of a caged iron lantern holding glowing coals, pixel art, isolated",
 "icons/tally_stick": "game inventory icon of a notched wooden tally stick, pixel art, isolated",
}

# ---------------------------------------------------------------- tiles: roads that remember (§5) ----
TILESETS = {
 # key: (lower, upper, transition)
 "tiles/dirt_to_cobble": ("packed dirt road with wheel ruts", "hand-laid grey cobblestone paving", "loose cobbles set into the dirt"),
 "tiles/grass_to_snow": ("dry wild grass with dust", "fresh snow with footprints", "grass poking through thin snow"),
 "tiles/gravel_to_water": ("cold grey river water with ripples", "wet gravel shore with pebbles", "foam at the water line"),
 "tiles/moss_to_rock": ("dark moss and pine needles on a forest floor", "grey mountain rock with lichen", "moss creeping over rock"),
}
ROADS = {
 "tiles/timber_roads": "corduroy road of timber logs laid side by side across a muddy track, bark and rope lashings, post-apocalyptic frontier",
 "tiles/scrap_roads": "road paved with flattened rusty car panels and metal sheets riveted together, post-apocalyptic frontier",
 "tiles/worn_path_roads": "a bare earth footpath worn into grass by many feet, no paving, post-apocalyptic frontier",
}

# ---------------------------------------------------------------- story plates: backgrounds (pixflux background) ----
PLATES = {
 "plates/new_world_day": "pixel art game background, an enormous circular steel bunker blast door standing open in a concrete hillside tunnel mouth at dawn, rust streaks, hydraulic pistons, steam drifting out, a cracked concrete apron in front, dead grass and a grey sky, wide landscape, no people",
 "plates/reaper_town": "pixel art game background, a post-apocalyptic town street under warband control, boarded windows, confiscated road signs bolted to poles with white painted marks, a wooden platform, orange rags on wires, dusty evening light, wide landscape, no people",
 "plates/road_station": "pixel art game background, a lonely roadside courier station on a worn dirt path through dry grassland, a timber lean-to shelter with a hanging brass lantern, a brass post box on a stone post, hills and a long low sunset, wide landscape, no people",
 "plates/hill_camp": "pixel art game background, an isolated hill community camp in a rocky gully at dusk, hide tents, a smoky cook fire, drying racks, a weathered post hung with stones and bones, cliffs behind, wide landscape, no people",
 "plates/unity_gate": "pixel art game background, the gate of a walled stone city at first light, two tall dark openwork gothic spires flanking a pointed archway with a single brass lantern, a cobbled avenue lined with marble pillars, smoke rising from tall sharp spires behind, wide landscape, no people",
 "plates/nomad_ridge": "pixel art game background, a windy ridge at night above a dark valley, scrub and boulders, a hooded lantern glowing faintly beside a bedroll, a distant line of lights along a road far below, stars, wide landscape, no people",
}

PORTRAITS = ["diefenbunker/douglas_reed", "diefenbunker/sarah_oconnel", "diefenbunker/jimmy_butler", "lamplighter/sniper", "reaper/admiral", "smoke/anointer", "farkeeper/captain", "party/ada"]
