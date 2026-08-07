# Notes

## Goals

* Must have
	* Site is available
	* Modern tools
	* Modern look and feel
	* Source code available
	* Blog
	* Trusted users can update
	* Separation of content and style
		* Themes separate
* Nice to have
	* Mobile-friendly
	* Tags for papers
	* Share
	* Search
	* Analytics

## Approach

* GitHub Pages
* Jekyll + Bootstrap (and Jekyll Bootstrap)
* Sass support for CSS
* Google Fonts

## Directory structure

Each of the major content areas is structured like a blog: an `index.html` (or `index.md`) that lists/renders the collection, plus an `_posts/` folder of dated Markdown files. For example:

	papers/
		index.html
		_posts/
			2018-08-09-cascading-power-limits.md
			2024-01-31-viscoelastic-materials.md
	projects/
		index.md
		_posts/
			2018-08-09-high-speed-mechanics.md
	team/
		index.html
		_posts/
			2018-08-01-mark-ilton.md
	news/
		index.html
		_posts/
			2018-08-10-posm-lab-logo.md
	blog/
		index.html
		_posts/
			2026-06-27-optimizing-free-knot-spline-approximation.md

See `CLAUDE.md` for the required frontmatter fields for each content type.

Team members use an `alum: true/false` field to distinguish current lab members from alumni on the team page.

## Issues / to-do

Issues are tracked at GitHub [github-issues].

[github-issues]: https://github.com/posmlab/posmlab.org/issues

## Hosting

Custom domain (posmlab.org) via [GitHub Pages]. Currently deploying from the `gh-pages` branch to the default `posmlab.github.io/posmlab.org` URL; the custom domain will be wired up (via the `CNAME` file) once we're ready to cut over.

[GitHub Pages]: https://pages.github.com/
