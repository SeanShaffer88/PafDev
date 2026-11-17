# 19 — Accessibility

Accessibility is a property of the *package*, not just the base app.
PAL and the Installer are fixed tools — their UI is inherited and may
not be modified (AGENTS.md: never modify the Installer's own code) —
but the packager controls the metadata, the language chain, the splash
behaviour, help.html, and the icons, and each of those can include or
exclude users. Items below trace to the format documentation in
[`01`](01-format-spec.md)–[`06`](06-environment-variables.md); where
this repo's sources are silent, the entry says **Unverified** rather
than guessing.

## What you are given (do not break it)

- **The install wizard's language set.** If installer.ini has a
  `[Languages]` section, `ENGLISH=true` is required and every other
  language defaults to `false` ([`02`](02-installer-and-installer-ini.md)).
  A packager who adds the section carelessly ships an English-only
  wizard. Enable the languages the package actually supports.
- **Optional components pre-selected for non-English installs**
  (`OptionalSectionPreSelectedIfNonEnglishInstall`, default `true`) —
  language packs arrive selected for the users who need them. Leave the
  default unless you have a reason.
- **A keyboard-free path exists**: silent / Platform-driven installs
  need no wizard interaction at all.
- **A predictable destination**: the user picks a parent folder and the
  installer appends the app folder. Say so in help.html; predictability
  is a cognitive-accessibility feature.
- **The EULA as plain Unicode text** (`App\AppInfo\EULA.txt`) — readable
  by assistive technology as-is. Keep it that way (Unicode, not ANSI).
- **No launcher interaction is time-limited.** The one timed element is
  the splash screen (`SplashTime`, default 1500 ms), and users can turn
  it off (user config `DisableSplashScreen`, or the Platform option).
  Document that switch in help.html.
- **Warnings before install**: `[Dependencies]` declarations
  (`RequiresAdmin`, `Requires64bitOS`, `UsesDotNetVersion`) surface in
  the Platform *before* a user commits to a package that cannot run for
  them. Declaring them honestly is an accessibility duty, not metadata
  trivia.

## What you must do

- **Write the Description like it is the only description.** For a
  screen-reader user browsing the store, the ≤512-character
  `Description` in appinfo.ini ([`01`](01-format-spec.md)) may be all
  they get. Plain language, what the app does, no marketing filler.
  `Category` must be the exact English string even for non-English
  apps — it is a machine value, not display text.
- **Wire the language chain end-to-end.** Platform locale variables
  ([`06`](06-environment-variables.md)) → `[Language]` /
  `[LanguageStrings]` building `%PAL:LanguageCustom%` → `[LanguageFile]`
  fallback for launches outside the Platform — and then actually *pass*
  the variable to the app. A chain that stops one step early runs the
  app in its default language for exactly the users who needed it most.
  Mechanics: [`04`](04-launcher-ini-reference.md).
- **help.html discipline.** The template's help.html is semantic HTML
  with no CSS — it inherits the reader's fonts, sizes, and colours,
  which is the accessible default; do not add fixed colours or tiny
  fonts. Keep one `h1` then `h2`s in order; write link text that makes
  sense read aloud ("Download the manual", not "click here"); never put
  essential instructions only inside an image in `Other\Help\Images` —
  and give content images alt text. If you ship a translated help file,
  change its `lang` attribute to match.
- **Icons must survive 16×16.** The mandated icon set
  ([`01`](01-format-spec.md) §3) verifies presence, not legibility.
  Check the 16×16 rendering is recognisable, and make the 256px entry a
  real high-resolution rendering, not an upscale.
- **Choose `RunAsAdmin` values like a human will meet them.**
  `compile-force` produces a bare OS elevation prompt with no
  explanation — the worst option cognitively. Prefer `try` over `force`
  ([`12`](12-glossary-and-faq.md) FAQ), and explain in help.html why the
  app asks.
- **Beware silent aborts.** `SinglePortableAppInstance=true` aborts a
  second launch *silently* — no feedback at all, which is worst for
  screen-reader users. Only set it when the app truly cannot run twice,
  and say so in help.html.
- **Custom-code messages in plain language.** Any `MessageBox` your
  `Custom.nsh` shows is package UI. Write it so it makes sense read
  aloud, with the action it needs stated first. Whether PAL's own
  message boxes support copying their text (Ctrl+C) is **Unverified**
  in this repo — do not put information *only* in a message box; repeat
  it in help.html.
- **Do not strip the base app's accessibility features** — high-contrast
  themes, UI-automation support, language files — as "bloat" when
  trimming the package tree ([`07`](07-end-to-end-workflow.md) Phase 2).

## Accessibility checklist for packagers

- [ ] `Description` is plain language and self-contained; `Category` is
      the exact English string.
- [ ] `[Dependencies]` requirements declared honestly.
- [ ] `[Languages]`: `ENGLISH=true` present, supported languages
      enabled.
- [ ] Language chain tested: app starts in the Platform's language, and
      in the `[LanguageFile]` fallback language when launched directly.
- [ ] help.html: heading order sane, meaningful link text, no
      image-only instructions, alt text on content images, `lang`
      correct per file, `DisableSplashScreen` documented.
- [ ] Icon recognisable at 16×16; 256px entry is a genuine hi-res
      rendering.
- [ ] `RunAsAdmin` is the least surprising value that works; admin need
      explained in help.html.
- [ ] One full pass keyboard-only: install, first launch, settings
      change, exit — no mouse.
- [ ] One run under Windows high contrast: splash, help.html, and the
      app itself remain usable.
