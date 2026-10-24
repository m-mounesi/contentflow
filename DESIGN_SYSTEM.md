# ContentFlow Design System

**Version:** 1.0  
**Design Direction:** Editorial Design + Developer Blog + Modern Magazine  
**Principles:** KISS, YAGNI, Consistency

---

## 1. Design Philosophy

ContentFlow combines three design approaches:

- **Editorial Design:** Strong typography, clear hierarchy, and comfortable reading.
- **Developer Blog:** Technical content, readable code blocks, and a developer-oriented aesthetic.
- **Modern Magazine:** Bold homepage hero, carefully designed article cards, and generous whitespace.

The result should feel modern, professional, content-focused, and consistent.

### Core Rules

1. Readability comes before decoration.
2. Reuse existing design tokens and components.
3. Do not introduce new colors, spacing values, shadows, or border radii without a clear reason.
4. Prefer simple HTML and CSS over unnecessary dependencies.
5. Do not add JavaScript or a CSS framework unless a real requirement justifies it.
6. All pages must feel like parts of the same website.

---

## 2. Color Palette

These colors are the single source of truth for the website.

| Token | Value | Purpose |
|---|---|---|
| `--color-bg` | `#F7F7F5` | Main page background |
| `--color-surface` | `#FFFFFF` | Cards and content surfaces |
| `--color-surface-soft` | `#F0F0ED` | Subtle backgrounds |
| `--color-ink` | `#171717` | Hero, footer, strong text |
| `--color-text` | `#242424` | Main body text |
| `--color-muted` | `#707070` | Secondary text and metadata |
| `--color-border` | `#E3E3DF` | Borders and dividers |
| `--color-accent` | `#6258E8` | Links and primary accents |
| `--color-accent-hover` | `#4E45CC` | Accent hover state |
| `--color-accent-soft` | `#EEEDFF` | Subtle accent backgrounds |
| `--color-code-bg` | `#191A22` | Code block background |
| `--color-code-text` | `#F2F2F5` | Code block text |
| `--color-danger` | `#B42318` | Error states |

### Color Rules

- Use the off-white background for the main site.
- Use white for article cards and reading surfaces.
- Reserve near-black for the homepage hero and footer.
- Use indigo as the primary accent.
- Do not introduce additional accent colors for individual pages.
- Code blocks always use the dark code palette.

---

## 3. Typography

### Font Families

**Primary font stack:**

`Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`

**Monospace font stack:**

`ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace`

Use system fonts. Do not load external fonts.

### Typography Rules

| Element | Guideline |
|---|---|
| Base font size | `16px` |
| Body line height | `1.7` |
| Article body line height | `1.8` |
| Homepage hero title | Responsive, approximately `42–76px` |
| Article title | Responsive, approximately `36–58px` |
| Section heading | Approximately `29–39px` |
| Card title | Approximately `21–22px` |
| Metadata | Approximately `11–13px` |
| Code | Monospace font |

Use negative letter spacing for large headings. Avoid excessively small body text.

---

## 4. Layout System

### Main Dimensions

| Property | Value |
|---|---|
| Main container maximum width | `1120px` |
| Article reading maximum width | `740px` |
| Desktop horizontal padding | `32px` |
| Mobile horizontal padding | `20px` |
| Header minimum height | `82px` desktop |
| Header minimum height | `70px` mobile |

### Spacing Scale

Use these spacing values consistently:

| Token | Value |
|---|---|
| `--space-1` | `4px` |
| `--space-2` | `8px` |
| `--space-3` | `12px` |
| `--space-4` | `16px` |
| `--space-5` | `24px` |
| `--space-6` | `32px` |
| `--space-7` | `48px` |
| `--space-8` | `64px` |

Do not invent arbitrary spacing values when an existing token works.

---

## 5. Border Radius and Shadows

### Border Radius

| Token | Value |
|---|---|
| `--radius-sm` | `8px` |
| `--radius-md` | `14px` |
| `--radius-lg` | `20px` |

### Shadows

**Default card shadow:**

`0 8px 28px rgba(23, 23, 23, 0.045)`

**Card hover shadow:**

`0 14px 36px rgba(23, 23, 23, 0.08)`

Use shadows sparingly. Borders and whitespace should do most of the visual work.

---

## 6. Page Design Rules

### 6.1 Homepage

The homepage combines editorial impact with a clean content layout.

**Hero section:**
- Dark background using `--color-ink`.
- Light text with an indigo-tinted heading highlight.
- One prominent headline.
- One short descriptive paragraph.
- One simple link to the article section.
- No unnecessary illustrations, gradients, or decorative animations.

**Article section:**
- Light background.
- Clear section heading.
- Three-column article grid on large screens.
- Two columns on medium screens.
- One column on mobile.
- White article cards with subtle borders and shadows.

### 6.2 Article Cards

Every article card should follow the same structure:

1. Category label.
2. Small index or secondary detail.
3. Article title.
4. Short excerpt.
5. Publication date.
6. Small directional link.

Keep card spacing, typography, borders, and hover behavior consistent.

### 6.3 Article Detail

The article detail page prioritizes reading.

- Use a light background.
- Center the reading column.
- Keep the content width at or below `740px`.
- Display breadcrumbs before the article header.
- Display the category, title, and publication metadata.
- Use comfortable paragraph spacing and line height.
- Style headings, lists, links, quotations, inline code, and code blocks consistently.
- Provide a link back to the article list.

Do not add a sidebar unless a real content requirement emerges.

### 6.4 Header

- Simple wordmark: `ContentFlow`.
- Light background.
- Minimal navigation.
- No sticky behavior in version 1.
- No image logo is required.

### 6.5 Footer

- Dark background using `--color-ink`.
- Light wordmark.
- One short descriptive line.
- Copyright notice.
- No unnecessary columns or widgets.

### 6.6 Empty States

When there are no published articles, show a clear message explaining that the journal has no published content yet.

Avoid blank pages and unnecessary decorative elements.

### 6.7 Pagination

- Keep pagination simple and horizontal.
- Use the primary accent for available links.
- Visually distinguish disabled navigation.
- Display the current page and total page count.

---

## 7. Responsive Design

Use these breakpoints:

| Breakpoint | Behavior |
|---|---|
| Above `900px` | Three-column article grid |
| `900px` and below | Two-column article grid |
| `640px` and below | Single-column grid and compact spacing |

Additional rules:

- Reduce heading sizes on smaller screens.
- Keep mobile page padding at `20px`.
- Prevent horizontal page overflow.
- Ensure links and controls remain usable on touch screens.

---

## 8. Code Styling

Code content should be easy to distinguish from prose.

- Use the monospace font stack.
- Use `--color-code-bg` as the code block background.
- Use `--color-code-text` for code text.
- Allow horizontal scrolling for long code lines.
- Style inline code with a subtle light background.
- Do not add a syntax-highlighting library in version 1.

---

## 9. Accessibility

- Use semantic HTML elements.
- Maintain a logical heading hierarchy.
- Provide visible keyboard focus states.
- Ensure links have meaningful labels.
- Do not communicate important information using color alone.
- Respect reduced-motion preferences.
- Preserve readable text sizes and contrast.

---

## 10. Technical Constraints

Version 1 uses:

- Django templates.
- One shared CSS file.
- Django's static files system.
- Existing views, models, and URL patterns.

Do not introduce:

- Bootstrap.
- Tailwind CSS.
- React or another frontend framework.
- JavaScript for purely visual effects.
- External font dependencies.
- Icon libraries.
- Additional packages solely for styling.

The design must work with the existing Django project without requiring database or model changes.

---

## 11. Design Consistency Rules

Whenever a new page or component is created:

1. Read this document first.
2. Reuse the existing color palette.
3. Reuse the spacing, radius, and shadow tokens.
4. Follow the typography and layout rules.
5. Reuse existing components where possible.
6. Keep responsive behavior consistent.
7. Avoid adding dependencies without a clear need.
8. Update this document deliberately if the design system genuinely needs to change.

**Final rule:** New pages should extend the ContentFlow design system, not invent a new one.