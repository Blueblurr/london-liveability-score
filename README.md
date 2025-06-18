# London Liveability Score

## 🧠 Project Idea
## 🎯 London Livability Heatmap for Renters
London rent prices are a bit of a joke—especially if you're a student or recent grad trying to get a foothold in the city. While platforms like Rightmove and Zoopla cover the basics (price, location, maybe some photos), they miss out on the more vibe-based factors that actually determine where someone wants to live.

This project aims to explore whether it's possible to algorithmically score areas of London based on:

Push factors: Crime stats, distance from Zone 1, affordability

Pull factors: Density of cafes, museums, pubs, bars, concert venues, theatres, etc.

Practical factors: Tube access, commuting tolerance, proximity to employment hotspots (e.g. Canary Wharf, City, Temple)

## ❌ What Listing Sites Don’t Tell You
Most aggregators don’t (or won’t) tell you things like:

1. Local crime rates

2. Nearby nightlife or cultural spots

3. General vibes (is this an area where young professionals actually live, or just students?)

**Why not?** 

Because:

-They don't want to discourage renters—data on crime or lack of amenities hurts listings.

-Business model conflict—their customers are landlords, not renters.

-Transient audience - you can't make renters subscribe if they'll only use it for the month or so it takes to find a listing.

## 💡 So What's the Point?
While building a full listing platform isn’t viable (Scraping SpareRoom, for example, is messy and likely against ToS), I can build a visualisation tool that combines public datasets into an intuitive livability heatmap for London postcodes.

This would be useful for:

-Recent grads starting their first job in London

-People looking to avoid student-heavy flatshares

-Those willing to compromise on commute time for quality of life and affordability

## 🔍 Key Data Layers
Data will be sourced from open APIs or public data only. Some planned layers:

### -📍 Amenities (Pull Factors)
Number of cafes

-Bars/pubs/clubs (nightlife category)

-Museums and galleries

-Theatres and cinemas

-Concert venues

### 🚨 Crime (Push Factors)
-Violent crime

-Burglary/theft

-Antisocial behaviour
(Filtered to crimes relevant to average residents — e.g., ignoring drug possession or bike theft)

### 🛤️ Practical
Commute radius to major job centres

Transport links (Tube, Overground)

### 💰 Price
Rent estimates based on area (average 1-bed or studio prices from public data)

## 🔧 Technical Direction
This is exploratory, but possibilities include:

Clustering methods to group similar postcodes

Generating a composite "livability score" per area

Ranking and heatmap visualisations

Possibly a basic ML model that predicts a score based on weighted input features

If this were a thesis, I'd title it something like:

  "Algorithmically synthesising quantitative and qualitative indicators to produce a 'liveability score' for London postcodes, tailored to cost‑conscious, commute‑tolerant young professionals."

## 🚫 Why No Listings Integration?
I considered integrating SpareRoom listings. But:

It violates their ToS.

Listings often include subjective or discriminatory tenant preferences (e.g. "no pets","students only", "no guests allowed", "must be a girl", etc.)

SpareRoom seems overrun with student house shares — not great for young professionals wanting peace, privacy, and cleanliness.

Instead, I’ll focus on publicly available data and treat listings as out-of-scope (for now).

## ✅ MVP Goals
Static map + scoring system

Overlay layers for crime, amenities, and price

Interactive postcode hover/highlight

Public dataset only, no scraping required

📓 Tracking Progress
Prototyping and ideation are being tracked on Notion. Updates coming soon.

🙌 Wish Me Luck
This is a passion project, and I’ll be refining the scope as I go. If you’ve got data suggestions, ideas, or want to collaborate—get in touch
