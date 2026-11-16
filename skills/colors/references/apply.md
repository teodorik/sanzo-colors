# Apply a palette

Inspect theme files, components, and the current design before editing. Preserve existing user changes. Use the framework and token conventions already in the project; do not add a dependency or broadly rewrite styles for a palette change.

Assign roles deliberately: background, surface, text, muted text, accent, on-accent, border, and focus where relevant. A vivid swatch may need only a small accent area. The historical combination does not prescribe these roles or area ratios.

Measure actual text/background pairs. For opaque sRGB, use the bundled helper. Normal text requires >=4.5:1; large text (24 CSS px regular or about 18.67 CSS px bold) requires >=3:1. Never round a failing ratio into a pass. Check important UI boundaries, focus indicators, and non-text information in context. Do not communicate state with color alone.

If the original palette cannot serve all roles accessibly, use an existing suitable neutral or propose an adaptation. Label every added or changed value and keep the original combination visible. Do not claim the adapted theme itself is an unchanged historical palette.

Check hover, focus, disabled, and selected states; overlays and gradients require contextual verification. Use relevant existing project checks and visually inspect when possible. Never claim a rendered result, measured contrast, or accessibility pass that was not verified.

Report the selected source and combination, changed files, key contrast ratios, adaptations, and remaining uncertainty. For a recommendation request, show the proposed roles without editing the project.
