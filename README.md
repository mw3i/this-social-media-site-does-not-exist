---
title: This Social Media Site Doesn't Exist
date: 2024-09-13
layout: doc.html 
---

# This Social Media Site Doesn't Exist

A snapshot of a social media site with LLM-generated users and content.

Disclaimer: Hopefully no one has already done this exact thing

**total cost**: 6$

**total time**: 8 hours

---

# How it works

A bunch of scripts in `data/` generate data tables for (in order):

- `profiles` (with sampled profile attributes and dalle-generated images)
- `posts` (from randomly selected users)
- `comments` (from randomly selected users for randomly selected posts)

And it's all stored in `data/db.sqlite`

Then, eleventy + liquid html build the pages in `frontend/` via sql queries (custom filter `frontend/_plugins`)

The result is stored in `_site`

# How to Run

**Option 1**: install all the python and nodejs dependencies manually, and then run `data/build` to generate the users, posts, and comments, and `frontend/serve` to serve the website.

**Option 2**:

- Install [podman](https://podman.io/docs/installation)
- Execute the `build` file to build a container w/ dependencies
- make an `env` file with your path to python and openai api key (see `env-example` for example)
- Execute the `run` file to launch the container, which executes `frontend/serve`

Regardless of which option you choose, you can then view the site at [0.0.0.0:8080](0.0.0.0:8080).

# Repo Org

- `data` has a bunch of data generation scripts
    - `build`: regenerate all the content
- `frontend` is an eleventy-generated static site
    - `build`: generate static site

# Future Directions:

- [ ] trace of users past posts in the post generation prompt. this could serve as a "personality trace" that can evolve from randomness over time (though there is no selection mechanism. we could add a selection mechanism by weighting based on likes)
- [ ] nested conversations
- [ ] put more parameters in `config` for easier experimentation
- [x] switch to sqlite3 for the data storage (as opposed to the json)
