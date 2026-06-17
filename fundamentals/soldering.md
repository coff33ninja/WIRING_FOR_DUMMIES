# Soldering Basics — Fundamental Reference

## What It Is

Soldering joins metal components using **solder** — a low-melting-point metal alloy (usually 60% tin, 40% lead, or lead-free). You heat both the component lead AND the PCB pad, then melt solder onto them. The solder flows into the joint and solidifies, creating a mechanical and electrical connection.

**It is not glue.** The solder must bond with both surfaces (wetting). You don't just melt solder on top of a cold joint.

## What You Need

### Essential

| Tool | What it does | Don't skimp on |
|------|-------------|----------------|
| Soldering iron | Heats the joint | Temperature-controlled (30–80W) |
| Solder | Fills the joint | Rosin-core, 0.8mm or 0.5mm diameter |
| Sponge or brass wool | Cleans the tip | Brass wool is better (doesn't thermally shock tip) |
| Tip | Transfers heat | Fine conical or chisel tip for through-hole |

### Nice to Have

| Tool | When you need it |
|------|-----------------|
| Helping hands (alligator clips) | Holding wires while soldering |
| Fume extractor or fan | Any indoor soldering (solder fumes are toxic) |
| Desoldering pump / wick | Fixing mistakes |
| Flux pen | Oxidized pads or leads (helps solder flow) |
| Third hand with magnifier | Small SMD components |

## Safety

- **Lead is toxic.** Wash hands after soldering. Don't eat or drink while soldering.
- **Fumes are harmful.** Even rosin-core solder produces irritating smoke. Use a fan or fume extractor.
- **Iron is hot (300–400°C).** Burns happen fast. Use a stand, not the table.
- **Safety glasses.** Solder can splatter. Hot solder in the eye is a bad day.

## Step by Step: Through-Hole Soldering

### 1. Prepare

Insert the component lead through the PCB hole. Bend the lead slightly outward (45°) to hold it in place while you solder. Flip the board over.

### 2. Clean and Tin the Tip

Wipe the iron tip on a wet sponge or brass wool. Melt a tiny amount of solder onto the tip — this is **tinning** and improves heat transfer.

### 3. Heat Both Surfaces

Touch the iron tip so it contacts **both** the component lead AND the PCB pad simultaneously. Count 1–2 seconds.

### 4. Apply Solder

Touch the solder wire to the joint (NOT the iron tip). If the joint is hot enough, the solder will melt and flow into the gap. Feed just enough to fill the hole.

### 5. Remove and Inspect

Remove the solder wire, then remove the iron. Don't move the board for 2–3 seconds. The joint should look like a shiny volcano cone:

```
   ┌──┐
   │  │  ← Smooth, shiny cone
  ─┴──┴─ ← PCB pad
```

**Good joint:** Smooth, shiny, fills the hole completely, visible fillet on top and bottom.

**Bad joint:** Dull gray, cracked, blob-shaped, didn't flow through.

### 6. Trim

Cut the excess lead flush with the solder joint.

## Common Problems and Fixes

| Problem | Cause | Fix |
|---------|-------|-----|
| Solder balls / splatter | Too much solder, or dirty tip | Clean tip, use less solder |
| Dull gray joint | Moved while cooling, or cold joint | Reheat until shiny |
| Solder blob bridging pads | Too much solder | Desolder wick to remove excess |
| Component won't stay | Not enough heat, or lead not bent | Add flux, use higher temp, bend lead |
| Solder won't flow | Cold iron, dirty tip, or oxidized surface | Clean tip, check temp (300°C+), add flux |
| Lifted pad | Too much heat, or pulled on component | Use lower temp, be gentler, use flux |

## Wire-to-Wire Soldering

### Tinning Wires

1. Strip ~5mm of insulation
2. Twist the strands together
3. Apply iron and solder to the exposed wire until solder wicks into the strands
4. Pre-tinned wires are easier to join

### Joining Two Tinned Wires

```
──══──    ──══──    ──═════──
 Wire 1    Wire 2    Soldered
 (tinned)  (tinned)  (hold together, heat)
```

Lay the tinned wires parallel. Touch iron to both simultaneously. When the solder on both melts, they merge. Remove iron, hold steady until cool.

## Desoldering

### Desoldering Pump (Solder Sucker)

1. Heat the joint until solder is fully molten
2. Position pump tip next to the joint
3. Press the release button — the vacuum sucks up the molten solder

### Desoldering Wick (Braid)

1. Lay the wick over the joint
2. Press iron onto the wick (not directly on the joint)
3. The wick absorbs molten solder by capillary action
4. Cut off the used portion

## Temperature Guide

| Solder type | Temperature |
|-------------|-------------|
| Lead-based (63/37 or 60/40) | 300–350°C |
| Lead-free (SAC305) | 350–380°C |
| Small SMD components | Lower end (300°C) |
| Large ground planes | Higher end (370–400°C) |
| Desoldering | 350–380°C |

## What NOT to Do

| Don't | Why |
|-------|-----|
| Touch the tip to the solder first | You're melting solder on the tip, not in the joint. The joint stays cold. |
| Blow on the joint to cool it | Creates a cold, brittle joint. Let it cool naturally for 2–3 seconds. |
| Use plumbing solder | Contains acid flux that corrodes electronics. Use rosin-core solder only. |
| Use too much solder | Causes bridges and blobs. A little goes a long way. |
| Leave the iron on for 10+ seconds | Lifts PCB pads and damages components. 2–4 seconds is enough. |
| Store the iron without tinning | The tip oxidizes and becomes unusable. Always tin before putting away. |

## Quick Reference

1. Heat the joint (both pad and lead), not the solder
2. Feed solder into the joint, not the iron
3. Joint should be shiny and form a volcano cone
4. 2–4 seconds per joint — if it takes longer, something is wrong
5. Clean the tip frequently
6. Use flux when solder won't flow
7. Lead-free = higher temp, shorter dwell time
8. Always wash hands after soldering

## See Also

- [74hc595-shift-register](/projects/74hc595-shift-register)
- [relay-module](/projects/relay-module)
- [esp32-fan-controller](/projects/esp32-fan-controller)
