# dopecheddar

<p align="center">
<img alt="dopecheddar logo" width="200" src="https://github.com/cascio/dopecheddar/raw/master/dopecheddar.png"/>

A Python based automation tool for distributing electronic music content personally curated by Michael Cascio.

- [Why](#why)
- [How](#what)
</p>

## Why

Music has always been a source of happiness in my life and there is nothing I enjoy more than sharing songs with friends. In ~2011 I started an electronic music blog called dopecheddar, a platform where I share personally curated tracks that I discover on the internet. A problem I had was that I would listen to so much music during the day and would want to share the creations of so many talented artists with the world but did not have the time to devote to manually posting. Maybe I'm just lazy...

## How

Soundcloud is the music streaming platform that I use to discover a majority of the new electronic music artists that I listen to. Tumblr is the blogging platform that I use to manage dopecheddar as a website. Soundcloud and Tumblr both provide API functionality to interact with your accounts via code. This tool checks the dopecheddar Soundcloud account for recently favorited tracks and generates Tumblr posts for unique selections. All content published dopecheddar is saved to a Postgres database using the object-relational mapping magic of SQLAlchemy.