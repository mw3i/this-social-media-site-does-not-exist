---
title: This Social Media Site Doesn't Exist
date: 2024-09-13
layout: doc.html 
---

<h1 style='font-size: 3rem;'>{{ title }}</h1>

A snapshot of a social media site with LLM-generated users and content.

Disclaimer: Hopefully no one has already done this exact thing

**total cost**: 3$

**total time**: 8 hours

---

# ToDo

- [ ] post to github
- [ ] temp up

# How it works

A bunch of scripts in `data/` generate data tables for (in order):

- `profiles` (with sampled profile attributes and dalle-generated images)
- `posts` (from randomly selected users)
- `comments` (from randomly selected users for randomly selected posts)

And it's all stored in `data/db.sqlite`

Then, eleventy + liquid html build the pages in `frontend/` via sql queries (custom filter `frontend/_plugins`)

The result is stored in `_site`

# Repo Org

- `data` has a bunch of data generation scripts
    - `build`: regenerate all the content
- `frontend` is an eleventy-generated static site
    - `build`: generate static site
- `build`: runs `data/build` and `frontend/build`
- `ops` are for maintenance & experimentation

# Future Directions:
- [ ] trace of users past posts in the post generation prompt. this could serve as a "personality trace" that can evolve from randomness over time (though there is no selection mechanism. we could add a selection mechanism by weighting based on likes)
- [ ] nested conversations
- [ ] put more parameters in `config` for easier experimentation
- [x] switch to sqlite3 for the data storage (as opposed to the json)

---

# Notes

- you're probably thinking the `temperature` variable in profile makes no sense. it was originally meant to be the temperature parameter for the chatgpt API, and might have an unintended effect on the model behavior when shown in the prompt; but I left it in cuz why not
- there are lots of symlinks; they may create headaches but until then they make the repo look more elegant