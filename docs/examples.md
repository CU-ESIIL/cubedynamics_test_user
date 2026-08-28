# UI Examples

This page contains small, copyable patterns that are compatible with a standard MkDocs + Material setup.

## Hoverable button

Use this for a small call-to-action with a subtle hover effect.

[Back to Home](index.md){ .md-button .oasis-hover-button }

```md
[Back to Home](index.md){ .md-button .oasis-hover-button }
```

## Responsive iframe embed

Use this wrapper to keep embedded content responsive.

<div class="oasis-embed">
  <iframe
    title="OpenStreetMap example embed"
    src="https://www.openstreetmap.org/export/embed.html?bbox=-105.3%2C39.9%2C-104.9%2C40.1&amp;layer=mapnik"
    loading="lazy"
    allowfullscreen>
  </iframe>
</div>

```html
<div class="oasis-embed">
  <iframe
    title="OpenStreetMap example embed"
    src="https://www.openstreetmap.org/export/embed.html?bbox=-105.3%2C39.9%2C-104.9%2C40.1&amp;layer=mapnik"
    loading="lazy"
    allowfullscreen>
  </iframe>
</div>
```

## Card grid

Use card grids to present parallel links or content categories.

<div class="grid cards" markdown>

- **Guide**

  ---

  Link short onboarding content.

- **Workflow**

  ---

  Summarize repeatable project steps.

- **Reference**

  ---

  Point to key files and definitions.

</div>

```md
<div class="grid cards" markdown>

- **Guide**

  ---

  Link short onboarding content.

- **Workflow**

  ---

  Summarize repeatable project steps.

- **Reference**

  ---

  Point to key files and definitions.

</div>
```

## Content tabs

Use tabs when two or three variants should live in one place.

=== "Python"

    ```python
    print("Hello from Python")
    ```

=== "R"

    ```r
    print("Hello from R")
    ```

## Admonition

Use callouts for important notes or caution points.

!!! tip
    Keep examples short and focused so future contributors can copy and adapt them quickly.
