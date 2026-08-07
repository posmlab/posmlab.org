# The PoSM Lab website

Our website, http://posmlab.org, is a [GitHub Pages](https://pages.github.com/) site built with [Jekyll](https://jekyllrb.com/) and [Bootstrap](http://getboostrap.com), based on the Drummond Lab's Jekyll Bootstrap "lab" theme (itself pulled from [Trevor Bedford's site](http://bedford.io) in 2015 and heavily modified).

# Editing the site

Here's a step-by-step guide to making modifications to the site, focused initially on adding typical content. You'll need a working Unix-like environment and working knowledge of Git, [Markdown](https://daringfireball.net/projects/markdown/syntax), HTML, and Unix commands. You'll need a working Ruby installation, with gems for Jekyll, GitHub Pages, and their dependencies installed. For now, if you need help getting set up, ask someone who's already up and running.

## Clone the repository

If you have write access to the [posmlab GitHub organization](https://github.com/posmlab), you have access to the website repository.

To clone the repository, making a local copy on your machine:

	git clone git@github.com:posmlab/posmlab.org.git

Enter your local repository:

	cd posmlab.org

The repository currently has a single branch, `gh-pages`, which is both the working branch and the branch GitHub Pages deploys from — there's no separate `staging`/`master` split, so changes pushed to `gh-pages` go live directly.

## Overview of the structure

Let's assume you're familiar with HTML pages. A site is a collection of HTML pages. For our site (and many others), there are page types, like a paper page, or a lab member page, which are the same in design but different in content. In the web-accessible site, these are indeed different pages. However, as you might hope, they are _generated_ from a single template file filled in with information from many paper- or member-specific data files. This generation is done every time the site changes; it's handled by GitHub Pages, the service we use.

The template files are weird-looking HTML files residing in the `_includes/themes/lab` folder.

## How to add content

For most common actions---adding a lab member, paper, project, or news item---you'll be making a new Markdown file in the proper location, naming it properly, and filling in the required fields. In almost all cases, you can (and should!) copy an existing item, change the name, and change its content, rather than trying to write a Markdown document from scratch.

For example, suppose you want to add a news item, which will appear on the front page, announcing that a new paper has been published. Go into the `news/_posts` folder. Copy one of the existing items into a new file named with today's date (it matters!) and a brief title:

	cp 2024-01-31-viscoelastic-materials-published.md 2026-08-07-new-paper-published.md

The date is used by the generator; it's inelegant and perhaps there's a way to do it differently, but that's how it is for now. Now edit the new file to make the content what you want. Just open it in your favorite editor and type away. By the time you're done, hopefully you have something like this:

	---
	layout: news
	title: "New paper published!"
	author: "Mark Ilton"
	author_handle: milton
	image: /assets/images/news/default-news.png
	category: news
	tags: [paper]
	---
	Our [paper] on some exciting new soft matter physics is out!

	[paper]: /papers/paper/some-paper-nickname

Now add it to the repository:

	git add news/_posts/2026-08-07-new-paper-published.md

And, when you're happy with it, commit and push:

	git commit -m "announcing new paper"
	git push

The same basic process is used to add papers, projects, team members, and blog posts — see `CLAUDE.md` for the frontmatter fields each content type expects.

## Updating the public site

Preview the site locally before pushing. Generate the pages and start the private webserver:

	rake preview

...and then open the local test site, http://127.0.0.1:4000. Look at anything you've changed and make sure it's good to go.

Then commit and push to GitHub:

	git add <your files>
	git commit -m "describe your change"
	git push

Changes won't be immediate, so wait a minute or two while GitHub's servers regenerate the site and publish it. Check to make sure the public site looks the way you intend.

## Changing look and feel

Fonts, colors, spacing, and similar stylings are separate from the template pages. Like most sites circa 2023, we use Cascading Style Sheets (CSS).

### To-dos

See Issues on [the site](https://github.com/posmlab/posmlab.org/issues).


## License

[MIT](http://opensource.org/licenses/MIT)
