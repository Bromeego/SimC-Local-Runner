---
version: "1.0"
name: simc-local-runner
description: |
  A local technical workbench for SimulationCraft: quiet, precise, and
  reassuringly private. The interface pairs warm paper surfaces in light mode
  with charcoal laboratory surfaces in dark mode. Ember orange is reserved for
  the action that starts a run, active state, and small pieces of operational
  emphasis. Large utilitarian headings give the app confidence; monospace type
  identifies profiles, build data, report metadata, and other machine-shaped
  details. Rounded panels and restrained depth keep a powerful Docker-backed
  workflow approachable without making it feel playful or cloud-hosted.

colors:
  dark:
    canvas: "#111315"
    canvas-deep: "#0d0f10"
    surface: "#181b1e"
    surface-subtle: "#15181a"
    surface-raised: "#202428"
    ink: "#f1eee9"
    body: "#c7c2bb"
    muted: "#99958f"
    faint: "#7f7c77"
    hairline: "#34383c"
    hairline-strong: "#4b5055"
    accent: "#f08a4b"
    accent-strong: "#ff9c60"
    on-accent: "#25150d"
    danger: "#ff7b73"
    focus: "rgba(240, 138, 75, 0.34)"
  light:
    canvas: "#f0efec"
    canvas-deep: "#e7e5e1"
    surface: "#f9f8f5"
    surface-subtle: "#e9e7e2"
    surface-raised: "#fdfbf7"
    ink: "#222426"
    body: "#4f5356"
    muted: "#6d706f"
    faint: "#7d7e7b"
    hairline: "#cfcdc7"
    hairline-strong: "#aaa8a2"
    accent: "#b8451c"
    accent-strong: "#9f3511"
    on-accent: "#fff8f1"
    danger: "#a8322d"
    focus: "rgba(184, 69, 28, 0.24)"

typography:
  display:
    fontFamily: "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: "clamp(36px, 4vw, 48px)"
    fontWeight: 760
    lineHeight: 0.98
    letterSpacing: "-0.035em"
  display-error:
    fontFamily: "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: "clamp(35px, 7vw, 74px)"
    fontWeight: 760
    lineHeight: 0.98
    letterSpacing: "-0.035em"
  heading:
    fontFamily: "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: 20px
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.035em"
  body:
    fontFamily: "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: 14px
    fontWeight: 700
    lineHeight: 1.4
  helper:
    fontFamily: "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.45
  eyebrow:
    fontFamily: "ui-monospace, SFMono-Regular, Consolas, monospace"
    fontSize: 11px
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: "0.16em"
    textTransform: uppercase
  code:
    fontFamily: "ui-monospace, SFMono-Regular, Consolas, monospace"
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.55
  metadata:
    fontFamily: "ui-monospace, SFMono-Regular, Consolas, monospace"
    fontSize: 11px
    fontWeight: 400
    lineHeight: 1.5

rounded:
  none: 0px
  control: 12px
  panel: 18px
  progress: 3px
  full: 9999px

spacing:
  xxs: 4px
  xs: 8px
  sm: 12px
  md: 16px
  lg: 20px
  xl: 24px
  xxl: 34px
  section: 48px

components:
  panel-primary:
    backgroundColor: "{colors.*.surface}"
    textColor: "{colors.*.ink}"
    border: "1px solid {colors.*.hairline}"
    rounded: "{rounded.panel}"
    padding: "clamp(24px, 3vw, 34px)"
  panel-secondary:
    backgroundColor: "{colors.*.surface-subtle}"
    textColor: "{colors.*.ink}"
    border: "1px solid {colors.*.hairline}"
    rounded: "{rounded.panel}"
    padding: 24px
  button-primary:
    backgroundColor: "{colors.*.accent-strong}"
    textColor: "{colors.*.on-accent}"
    typography: "{typography.label}"
    rounded: "{rounded.control}"
    padding: "11px 18px"
    minHeight: 46px
  button-secondary:
    backgroundColor: "{colors.*.surface}"
    textColor: "{colors.*.body}"
    border: "1px solid {colors.*.hairline}"
    rounded: "{rounded.control}"
    padding: "9px 13px"
    minHeight: 40px
  text-input:
    backgroundColor: "{colors.*.surface-raised}"
    textColor: "{colors.*.ink}"
    border: "1px solid {colors.*.hairline}"
    rounded: "{rounded.control}"
    padding: "10px 12px"
    minHeight: 46px
  text-area:
    backgroundColor: "{colors.*.surface-raised}"
    textColor: "{colors.*.ink}"
    typography: "{typography.code}"
    border: "1px solid {colors.*.hairline}"
    rounded: "{rounded.control}"
    padding: 15px
    minHeight: 164px
  drop-zone:
    backgroundColor: "{colors.*.surface-raised}"
    textColor: "{colors.*.body}"
    border: "1px dashed {colors.*.hairline-strong}"
    rounded: "{rounded.control}"
    padding: 18px
    minHeight: 164px
  report-row:
    backgroundColor: "{colors.*.surface}"
    textColor: "{colors.*.body}"
    typography: "{typography.metadata}"
    rounded: "{rounded.control}"
    padding: "13px 14px"
  status-popover:
    backgroundColor: "{colors.*.surface}"
    textColor: "{colors.*.ink}"
    border: "1px solid {colors.*.hairline-strong}"
    rounded: "{rounded.panel}"
    padding: 18px
  focus-ring:
    borderColor: "{colors.*.accent}"
    boxShadow: "0 0 0 4px {colors.*.focus}"
---

# SimC Local Runner design system

This file describes how the app should look, feel, and behave. It is written for
people and coding agents making interface changes. The implementation in
[`app/static/app.css`](app/static/app.css) remains the source of truth for
current token values.

## 1. Visual theme and atmosphere

The product should feel like a well-kept local instrument:

- **Technical, not intimidating.** Docker and simulation details are visible
  when useful, but the primary path stays obvious.
- **Quietly premium.** Quality comes from spacing, typography, alignment, and
  state design—not decoration.
- **Local and trustworthy.** Copy should reinforce that profiles remain on the
  user's machine.
- **Warm, not playful.** Cream, charcoal, and ember orange soften the tool
  without turning it into a game interface.
- **Dense only where earned.** Forms and report metadata may be compact; primary
  decisions need room to breathe.

Use a dark-first workbench in dark mode and a warm-paper workbench in light
mode. Avoid pure black and pure white as large default surfaces.

## 2. Color palette and roles

### Semantic use

| Role | Rule |
| --- | --- |
| Canvas | A low-contrast vertical field with a faint ember glow near the upper-right |
| Primary surface | The simulation form and other focused work areas |
| Subtle surface | Guidance, report archive, and supporting content |
| Raised surface | Inputs, drop zones, expanded rows, and nested technical blocks |
| Ember accent | The run action, active disclosure, focus, and small technical emphasis |
| Danger | Destructive actions and validation failures only |
| Border | Structural separation; never the loudest element |

Accent color is scarce. A typical viewport should have one dominant orange
object: the **Run simulation** button. Small labels and active states may echo
it, but large orange panels, gradients, or repeated orange buttons are outside
the system.

Maintain readable contrast in both themes. Do not use `muted` text for required
instructions, errors, or primary labels.

## 3. Typography rules

The UI uses two voices:

1. **System sans** for headings, explanations, labels, and controls.
2. **System monospace** for profiles, versions, digests, report names, timing,
   technical eyebrows, and other machine-generated facts.

Headlines are large, compact, and left-aligned. The main headline may wrap into
two deliberate lines and uses a nearly solid line height. Body copy is calmer
and should generally stay below 60 characters per line.

Do not introduce a web font for a small utility app unless there is a measured
need. Fast local rendering and platform familiarity are part of the character.

### Hierarchy

| Content | Style |
| --- | --- |
| Page promise | Display |
| Panel title | Heading |
| Section signal | Eyebrow in uppercase monospace |
| Field name | Label |
| Explanation | Body or helper |
| Profile and build data | Code or metadata |

Use sentence case for headings, buttons, and labels. Preserve upstream names
such as `HecticAddCleave` and `DungeonSlice`.

## 4. Component styling

### Buttons

- Primary buttons are solid ember, high contrast, and reserved for starting a
  run or recovering from an error.
- Secondary buttons are surface-colored with a hairline border.
- Destructive buttons begin neutral; danger color appears on hover/focus or
  inside a confirmation pattern.
- Pressed controls move down by `1px`.
- Disabled run controls lose the accent and retain a clear waiting cursor.

### Inputs

- Text inputs and selects are 46px minimum height.
- Labels sit 8px above controls; helper text sits 7px below.
- Focus uses an accent border plus a 4px translucent ring.
- Placeholder text is muted but remains readable.
- Code-like input uses monospace and generous line height.

### Panels and cards

- Large page regions use an 18px radius and a single hairline border.
- Nested controls and report rows use a 12px radius.
- Avoid card-on-card-on-card nesting. One nested surface level is normally
  enough.
- Supporting cards should be slightly quieter than the primary form.

### Status and disclosures

- The engine status stays compact in the header; deeper data lives in a
  popover.
- Native `details` and `summary` are preferred for optional explanations.
- Active summaries use the accent; inactive summaries use body color.
- Progress is indeterminate unless real progress data exists. Never display a
  fabricated percentage.

### Empty and error states

- Empty states use a dashed hairline and calm, instructive copy.
- Error pages keep the same design language and reveal raw technical details in
  an optional disclosure.
- Do not expose unescaped process output.

## 5. Layout principles

The desktop shell is capped at `1380px` with 24px side gutters and a 24px grid
gap. The main workspace uses a wide work panel and a narrower supporting
sidebar:

```text
┌───────────────────────────────────┬─────────────────┐
│ New simulation                    │ Encounter guide │
│                                   ├─────────────────┤
│ Form, profile source, run action  │ Reports         │
└───────────────────────────────────┴─────────────────┘
```

The primary column is approximately 1.65 parts to the sidebar's 0.75 parts. The
sidebar may remain sticky only while both columns fit comfortably.

Within the form:

- use a two-column control grid on wide screens;
- keep the report name full width;
- separate profile input from encounter settings with a hairline;
- give upload and paste sources comparable visual weight; and
- place the run action at the natural end of the form.

Alignment matters more than symmetry. Text should align to control edges and
supporting descriptions should sit close to the object they explain.

## 6. Depth, elevation, and motion

Depth is restrained:

- primary panels use one broad, low-opacity shadow;
- secondary panels normally have no shadow;
- popovers receive the strongest elevation;
- raised inputs are communicated mostly through surface contrast and border.

The canvas may use one faint radial ember glow over a vertical background
gradient. Do not add decorative blobs, glassmorphism, noisy textures, or
multiple competing glows.

Motion lasts roughly `160ms` for control feedback and about `500ms` for initial
panel entry. Use a decelerating curve for panels. Respect
`prefers-reduced-motion`; all content must remain understandable without
animation.

## 7. Do's and don'ts

### Do

- Make the profile-to-report path obvious at a glance.
- Reuse semantic CSS variables across both themes.
- Keep exact build and report details in monospace.
- Pair every control with visible text; keep icons optional.
- Preserve generous focus rings and 44px-or-larger touch targets.
- Explain limits and local storage in plain language.
- Test empty, loading, success, error, and long-content states.

### Don't

- Do not imitate World of Warcraft's ornamental fantasy UI.
- Do not fill the page with orange or use it decoratively.
- Do not introduce neon gradients, glass cards, or dashboard clutter.
- Do not hide critical security or storage behavior behind a tooltip.
- Do not use pill shapes for every control.
- Do not add animations that imply progress the system cannot measure.
- Do not make dark mode pure black or light mode clinical white.
- Do not add an icon library for one or two symbols.

## 8. Responsive behavior

### Wide — above 980px

- Show the two-column workspace.
- Keep the guide and report archive stacked in a sticky sidebar.
- Use the two-column form grid.

### Medium — 701px to 980px

- Stack the primary work panel above the sidebar.
- Place guide and reports side by side when space permits.
- Keep the two-column form grid.

### Narrow — 700px and below

- Use 14px page gutters.
- Stack all workspace, sidebar, form, and profile-source columns.
- Turn the profile-source divider from vertical to horizontal.
- Make the primary action full width.
- Remove the brand subtitle before removing the brand name.
- Let report lists grow naturally rather than creating a small inner scroller.

### Very narrow — 480px and below

- Give header actions their own row.
- Present the engine popover as an inset, fixed sheet beneath the header.

Never rely on hover. Disclosures, copy actions, and destructive actions must
work with touch and keyboard input.

## 9. Agent prompt guide

When generating or changing an interface, use this short brief:

> Build a precise local technical workbench for SimulationCraft. Use charcoal
> or warm-paper canvases, layered low-contrast surfaces, ember orange only for
> the decisive action and active state, large compact system-sans headings, and
> monospace for profiles and build metadata. Prefer 12px controls, 18px panels,
> hairline borders, quiet shadows, excellent focus states, and restrained
> motion. Keep the profile-to-report flow obvious. Avoid fantasy ornament,
> glassmorphism, neon gradients, excessive pills, and generic dashboard cards.

Before finishing a UI change, verify:

- light and dark themes;
- keyboard focus order and visibility;
- 320px, 700px, 980px, and wide desktop layouts;
- reduced-motion behavior;
- long report names, digests, and error output;
- empty, running, completed, and failed states; and
- the Docker/security boundary in any new explanatory copy.

## Provenance

This project-specific design document follows the plain-text design-system
approach collected by
[`VoltAgent/awesome-design-md`](https://github.com/VoltAgent/awesome-design-md).
Its rules and tokens are derived from this repository's own interface rather
than copied from another product's brand.
