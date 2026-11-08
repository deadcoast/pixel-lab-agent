I've saved the lantern plan to `APPROACH.md`. I didn't set up any PIXL production state, make any art, or contact PixelLab.

**What the reference does:**
- It's a 32×32 image built from three colours: a dark navy outline, a teal fill and cream "eyes".
- The partial transparency and anti-aliasing are the same thing here. There are 30 semi-transparent teal pixels in one column just outside each side of the outline.
- The left column is fainter (opacity about 38%) than the right (about 63%). It might suggest light coming from the right, but that's my guess.
- Every other edge, including the top, bottom and corners, is fully solid with no softening. That's what makes the anti-aliasing "selective".
- PIXL's image check flagged an alpha "failure" only because it expects every pixel to be fully solid or fully clear by default. With your brief, that flag isn't a problem.

**The plan:**
- **What a lantern must pass:**
  - Some pixels are partly transparent, and they're clearly placed on purpose.
  - Some chosen edges are softened while the rest stay hard. A lantern with no softening fails, and so does one softened evenly on every edge.
  - It reads as a lantern at actual size.
  - It visually matches the reference, which you'd judge yourself.
- **No palette check**, since you didn't impose one.
- **Things I'm only trying, not requiring:** the reference's exact colours, opacity levels and 32×32 size, plus a transparent background and light from the right. The PixelLab prompt marks each of these as a proposal.
- **One sample first:** generate a single lantern using the reference as the style guide. If it comes back with no soft pixels, or with every edge softened, I'd add the soft pixels by hand only on the chosen edges and keep both versions.
- Then look at it on light, dark and mid-tone backgrounds, because semi-transparent pixels look different on each one.

When I re-read the whole first draft, it limited transparency to edges, and two sections contradicted each other about which option was closest to the reference. I fixed both. I also downgraded a few rules I had added myself to proposals, such as a required transparent background. The first draft is kept as `APPROACH.draft1.md`.

**Decision for you:** where should the lantern's partial transparency go?
- **(A) See-through glass panes.** This is my recommendation, together with softening the lantern's vertical sides the way the reference softens its sides. Glass is the natural see-through part of a lantern, though the reference doesn't show anything like it.
- **(B) Solid glass with a soft glow just outside the frame.** This is closest to how the reference does it.
- **Both.**

Separately, it would help to know whether your game engine expects straight or premultiplied transparency (two ways of storing it in the image file). It isn't needed to start, but it should be confirmed before any art is accepted.
