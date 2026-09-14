# THE CONVERGENCE — asset batch for the starting quadrant

Everything here was generated through PixelLab (v3 characters, template and
custom animations, map objects, pixen icons, Wang and road autotiles, pixflux
backgrounds, portrait conversion, font and UI) from prompts written against
the compendium, and composed with our own tooling. 1,103 generations in
total; 1,830 of 5,000 remain.

## What the compendium says is about to happen

The current quadrant is where the histories meet, not where they began (§15).
The Republic's couriers and Farkeepers enter from UNITY; the Diefenbunker
Society has just come up through a five-hundred-ton door that cannot close
again (§11); the Lamplighter Nomads are the first to reach them (§13); the
Reapers hold territory and treat what moves through it as theirs (P01); the
communities the Republic calls Cannibals know their own ground and nothing of
the distant city funding the armed strangers (P04); Raiders, Rebels, Flame
Keepers and Iron Giants have their own claims on the road (§15, P02–P06).
The batch is built as that cast, with the objects, tiles and interface that
the situations need.

## People — 31 new characters, 64 px, 8 rotations (working frame 96 px)

| Character | Source | What carries it |
|---|---|---|
| Douglas Reed, Prime Administer | §10, §12, §23 | old civil-service jacket, a row of ancient enamel pins, a badge on a lanyard, a clipboard — the political class, generations on |
| Sarah Oconnel, mechanic | §10, §12, §23 | coveralls tied at the waist, welding goggles up, the torch — "doors open until we get the welders up" |
| Lt. Jimmy Butler, Enforcement Department | §10, §12, §23 | navy uniform, beret, radio, a C8 with the red leaf on the sight housing |
| Enforcement trooper; work crew on New World Day | §11, §14 | the C7A2 with olive furniture and the boxy optic; hard hat, headlamp, shovel — they came up ready to dig |
| Lamplighter sniper, marksman, nomad hauler, nomad elder | §8–9, §13–14, P09 | rag-and-net cloak that breaks the silhouette, a scoped bolt rifle or a DMR, and always the shuttered lantern — the light carried, no longer shown the same way |
| Reaper overseer; household woman; child; captive | P01, §3 (E01) | a police jacket with the badge scraped off and a white ownership mark; a bundle of firewood and a child's shoe; an oversized orange coverall; rope at the wrists and the mark on the chest |
| Haven courier | §19 (Haven) | slate-blue tunic under a hide poncho, a hand-painted settlement sign on the shoulder |
| Hunter, hearth keeper, lookout (the hill community) | P04 revised, §3 | cured hides, ash and ochre, a pipe spear, snare wire, a cook pot, a bird-bone whistle — practices, obligations, material conditions; nothing monstrous |
| Raider rover; bandit | P02, §15 | patchwork with pouches everywhere, bolt cutters, rope; a burlap mask and a pipe rifle |
| Rebel militiaman; speaker | P03 | a farmer's coat and hunting rifle with a settlement armband; a painted sign board and a tin lantern |
| Furnace warden; stoker | P05 | scorched apron, tongs, a caged lantern of coals, the ring of keys — warmth kept under guard |
| Frame pilot; working frame | P06 | harness and visor; a two-legged riveted salvage exoskeleton with the pilot in a caged cockpit — repaired structural mass, not enlarged anatomy |
| Mason, Forrester, Path Presser | §4–5 | a hod of cobbles; an axe and a log; a bundle of marker stakes and hobnailed boots |
| Farkeeper captain (mounted, banner) | §6 | slate blue over green on the pole |
| Draft horse; light horse | §6 | "different animals bring different strengths" |

## Motion

Walk for all 31 (8 directions); breathing idle for the twelve who carry
scenes; combat from the templates that exist for the rig — spear thrust,
claymore overhead swing, sabre cuts, punches, the Torch's flame thrust,
ready stances for the rifles — and deaths for six, because a life on these
roads can be lost (§16). Story motions from templates: the captive's sad walk
and getting up, the hauler's pull, the path presser's push, the Postman
picking up mail, the work crew digging.

Four custom-directed animations (south, 9 frames, ~30 generations each):
the Lamplighter kneels and shoulders the rifle; the Postman's deliberate
handover with the small bow (§4 — the work is completed when what was
entrusted to the road is deliberately delivered); Sarah welds; the hearth
keeper stirs.

Partial sets (7 of 8 directions after a retry): hunter walk, marksman ready,
raider death, torch death. The soldier's ready stance timed out at two
directions and is not shipped.

## Portraits

Character-to-portrait conversion, 64 px: Reed, Oconnel, Butler, the sniper,
the Admiral, the Anointer, the captain, Ada, the Postman. The three bunker
voices sit beside their verbatim testimonies in the codex.

## Objects, icons, tiles, plates

Twenty-seven map objects: the blast door, hatch, bullion-crate barricade,
comms array and decontamination shower of §14; the station shelter, post box,
ladder, cache crate, milestone and mail cart of §5; the cloaked lantern; the
Reaper marker pole; the hill gathering-place post; the furnace; the parked
frame; road materials in piles; the first-reply table (P07); the Ever-flame
brazier. Twenty-seven inventory icons including every named firearm of §14.
Nine tilesets at 32 px: grass→path, dirt→cobble, grass→snow, gravel→water,
moss→rock as Wang sets, and cobble, timber-corduroy, scrap-metal and worn-path
roads as 18-configuration autotiles — the road materials of §5 as the map's
own vocabulary. Ten story plates: a generated background at 400×224 with
generated sprites composed 1:1 and depth-sorted, one per situation.

A postal stencil font (TTF in `ui/font_postal`) and two dialogue panels.

## What was deliberately not made

No Greys — the compendium gives them a sound and nothing else. No execution
scene: P01 says it does not establish that it has happened. No named
Cannibal history, no single origin; three people with tools, not a
caricature. No mount for a Cannibal or Reaper — none is supplied. No
Lamplighter city. No new names anywhere.

## Files

    <faction>/<name>/<name>_rotations.png            S SW W NW N NE E SE
    <faction>/<name>/<anim>/<name>_<anim>_sheet.png  rows = directions, + .json meta, + _x3.gif preview
    portraits/<name>/                                 64 px bust
    objects/<name>/<name>.png   icons/<name>/<name>.png   tiles/<set>/tile_*.png (+ meta.json rules)
    plates/<name>/               backgrounds       story/<nn>_<name>.png (+ _x2)
    ui/font_postal/*.ttf         ui/dialogue_panel   ui/bunker_panel
    convergence_codex.html       the codex, self-contained
    manifest.json                character IDs (animate further without regenerating), costs
    content2.py                  every prompt, keyed to the compendium
    pl2.py batch2.py batch3.py batch3b.py plates.py codex.py   the pipeline
