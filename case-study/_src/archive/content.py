"""Single source of truth for the case study copy. All three versions render from this file.

Edit the text here, then run: python3 case-study/_src/build.py

Research evidence: every item links to a public source. `says` is a paraphrase in my words.
To show a verbatim excerpt (for example from a Reddit thread you have read yourself), add
"quote": "the excerpt" to the item. The components render it in quotation marks above `says`.
Reddit item template:
    {"source": "r/movies", "who": "u/name", "date": "Jan 1, 2025", "url": "https://...",
     "quote": "Short excerpt.", "says": "One line on why it matters."},
"""

META = {
    'title': 'From Ratings to Decisions.',
    'subtitle': 'Reimagining Rotten Tomatoes around the moment that matters: deciding what to watch.',
    'tags': ['Product Design', 'Research', 'Information Architecture'],
    'author': 'Cynthia Lu',
    'project': 'Reimagining the Rotten Tomatoes movie detail experience',
    'example': 'La La Land',
    'context': 'Product design take-home for Prelim',
    'date': 'November 2026',
    'scope': 'Movie detail page, desktop 1440',
    'disclaimer': 'Independent concept. Not affiliated with Rotten Tomatoes, Fandango or the film’s rights holders. '
                  'Rotten Tomatoes marks, La La Land imagery and quoted reviews belong to their owners.',
    'placeholders': 'Interface copy is real Rotten Tomatoes content captured in November 2026. Streaming prices, '
                    'audience star values, helpful counts and ad creatives are placeholders.',
    'prototype': '../../interactive/index.html',
    'prototype_note': 'Working HTML prototype built from an earlier iteration, so its hero differs from the final Figma frame.',
}

CHAPTERS = [
    ('00', 'Opening', 'opening'),
    ('01', 'The Disconnect', 'disconnect'),
    ('02', 'The Product Reality', 'reality'),
    ('03', 'Information Architecture', 'architecture'),
    ('04', 'Key Design Decisions', 'decisions'),
    ('05', 'The Redesigned Experience', 'experience'),
    ('06', 'Reflection', 'reflection'),
]

OPENING = {
    'headline': 'Rotten Tomatoes has everything a moviegoer needs to know about a film. '
                'Yet finding what actually helps them make a decision can feel surprisingly difficult.',
    'question': 'How might we make Rotten Tomatoes better at helping people decide what to watch?',
}

DISCONNECT = {
    'headline': 'Is Rotten Tomatoes actually broken?',
    'lead': 'The redesign began with a question rather than an assumption. Two sources shaped the answer: '
            'what people say about the site, and what the page does when you use it.',
    'voices_label': 'What users are saying',
    'voices_note': 'Public comments from Hacker News, 2013 to 2024, paraphrased and linked. '
                   'A small, self-selecting sample, read for themes rather than proof.',
    'themes': [
        {
            'title': 'Ratings don’t tell the whole story.',
            'body': 'Users question whether a single Tomatometer percentage adequately communicates movie quality.',
            'icon': 'tomato',
            'evidence': [
                {'source': 'Hacker News', 'who': 'curun1r', 'date': 'Oct 16, 2015',
                 'url': 'https://news.ycombinator.com/item?id=10397489',
                 'says': 'Reads the score as how many people a film pleases, not how good it is.'},
                {'source': 'Hacker News', 'who': 'mrob', 'date': 'Sep 7, 2017',
                 'url': 'https://news.ycombinator.com/item?id=15195877',
                 'says': 'Finds the Average Rating more useful, and says the site doesn’t make it obvious.'},
            ],
        },
        {
            'title': 'Critics and audiences see movies differently.',
            'body': 'Differences between professional critics and audience opinions are meaningful, '
                    'but users need context to understand them.',
            'icon': 'popcorn',
            'evidence': [
                {'source': 'Hacker News', 'who': 'mrbombastic', 'date': 'Dec 23, 2024',
                 'url': 'https://news.ycombinator.com/item?id=42493120',
                 'says': 'Finds the two scores most valuable when they diverge.'},
                {'source': 'Hacker News', 'who': 'aleksiy123', 'date': 'Sep 7, 2023',
                 'url': 'https://news.ycombinator.com/item?id=37421836',
                 'says': 'Points out that the two percentages are calculated differently, so they aren’t directly comparable.'},
            ],
        },
        {
            'title': 'A score can influence perception.',
            'body': 'Some users feel that Rotten Tomatoes scores have become overly prominent in movie marketing.',
            'icon': 'certified-fresh',
            'evidence': [
                {'source': 'Hacker News', 'who': 'CM30', 'date': 'Sep 7, 2017',
                 'url': 'https://news.ycombinator.com/item?id=15195566',
                 'says': 'Discusses a New York Times report on studios objecting to a Rotten score beside the ticket button.'},
                {'source': 'Hacker News', 'who': 'mcpackieh', 'date': 'Sep 7, 2023',
                 'url': 'https://news.ycombinator.com/item?id=37423537',
                 'says': 'Describes the premise of the site as a simple number read in a second.'},
            ],
        },
        {
            'title': 'Movie discovery and streaming availability matter.',
            'body': 'Users also rely on Rotten Tomatoes to find movies and understand where to watch them.',
            'icon': 'splat',
            'evidence': [
                {'source': 'Hacker News', 'who': 'rixrax', 'date': 'Dec 25, 2018',
                 'url': 'https://news.ycombinator.com/item?id=18755536',
                 'says': 'Wants scores visible while browsing Netflix, and keeps a second device nearby to look them up.'},
                {'source': 'Hacker News', 'who': 'ryanianian', 'date': 'Jul 19, 2019',
                 'url': 'https://news.ycombinator.com/item?id=20482498',
                 'says': 'Uses Reelgood because it puts scores, a trailer and a deep link to the film in one place.'},
            ],
        },
    ],
    'pull': {
        'text': 'so much time ‘deciding’ what to watch, that it gets too late to watch.',
        'who': 'gedrap', 'source': 'Hacker News', 'date': 'Nov 2, 2013',
        'url': 'https://news.ycombinator.com/item?id=6657537',
    },
    'builders_label': 'People keep building the missing link themselves',
    'builders_note': 'For more than a decade, people have shipped their own tools that join a score to a place to watch.',
    'builders': [
        {'year': '2011', 'name': 'Rotten Tomatoes reviews overlaid on Netflix', 'url': 'https://news.ycombinator.com/item?id=3393106'},
        {'year': '2012', 'name': 'A Better Queue: Netflix + Rotten Tomatoes', 'url': 'https://news.ycombinator.com/item?id=4054008'},
        {'year': '2018', 'name': 'Trailer Nite: find something to watch tonight', 'url': 'https://news.ycombinator.com/item?id=17013946'},
        {'year': '2021', 'name': 'Tomatotree.tv: find your next series with Rotten Tomatoes', 'url': 'https://news.ycombinator.com/item?id=28051563'},
    ],
    'audit_label': 'My heuristic evaluation',
    'audit_note': 'Observed on the live page, desktop Chrome at 1440×900, signed out, November 2, 2026. '
                  'Positions measured on my 1:1 Figma recreation.',
    'issues': [
        {'title': 'Information hierarchy',
         'body': 'Important movie information competes with secondary content.',
         'detail': 'The two scores start around 720px. When a 970×250 ad is served, they fall entirely below the fold.'},
        {'title': 'Content competition',
         'body': 'Advertisements, recommendations, videos, and movie information compete for attention.',
         'detail': 'Six ad placements, three separate video modules, and a floating pill that can’t be closed.'},
        {'title': 'Decision-making friction',
         'body': 'Users need to navigate different sections to find ratings, synopsis, reviews, and viewing options.',
         'detail': 'Ratings at 706px, reviews at 1,649px, the full synopsis at 4,376px.'},
    ],
    'conclusion': 'The problem wasn’t a lack of information. It was how that information competed for attention.',
}

REALITY = {
    'headline': 'Redesigning the experience means understanding what must remain.',
    'lead': 'A movie page is also a business surface. Three constraints set the boundaries of the redesign.',
    'business': {
        'n': '1', 'title': 'A business built around monetization',
        'body': 'Rotten Tomatoes is owned by Fandango, and its experience supports several commercial activities at once. '
                'The redesign has to accommodate advertising and partnerships rather than assume they can simply disappear.',
        'paths': [
            {'name': 'Advertising', 'body': 'Display ads and sponsored placements.', 'image': 'final-ad-leader'},
            {'name': 'Distribution', 'body': 'Streaming availability, rentals, purchases, and ticketing.', 'image': 'final-where'},
        ],
    },
    'context': {
        'n': '2', 'title': 'A pre-viewing decision context',
        'body': 'Rotten Tomatoes is often used before watching a movie. '
                'So the page should prioritize evaluating a movie and finding a way to watch it.',
        'journey': [
            {'step': 'Discover', 'q': 'What’s this?', 'on': False},
            {'step': 'Evaluate', 'q': 'Is it worth my time?', 'on': True},
            {'step': 'Validate', 'q': 'Do others agree?', 'on': False},
            {'step': 'Watch', 'q': 'Where can I see it?', 'on': True},
        ],
    },
    'ratings': {
        'n': '3', 'title': 'Two rating systems define the product',
        'body': 'The two scores answer different questions, so neither can stand in for the other. Both need to stay prominent.',
        'meters': [
            {'name': 'Tomatometer', 'score': '91%', 'count': '472 reviews', 'icon': 'tomato',
             'def': 'Critics’ positive review percentage. Fresh at 60% and above.', 'asks': 'Did critics approve?'},
            {'name': 'Popcornmeter', 'score': '82%', 'count': '50,000+ ratings', 'icon': 'popcorn',
             'def': 'Audience rating percentage. A rating of 3.5 stars or higher counts as positive.', 'asks': 'Did audiences enjoy it?'},
        ],
    },
    'conclusion': 'The redesign needed to preserve the dual-perspective rating experience while making it easier to understand and act on.',
}

ARCHITECTURE = {
    'headline': 'Prioritizing the movie decision.',
    'lead': 'Every element on the page was ranked by how directly it helps someone decide. '
            'The layout moves from content-heavy to decision-oriented.',
    'tiers': [
        {'id': 'P0', 'name': 'Core movie information', 'bill': 'Starring',
         'items': ['Movie title', 'Tomatometer and Popcornmeter', 'Genre, runtime, release date, and rating', 'Synopsis']},
        {'id': 'P1', 'name': 'Decision support', 'bill': 'Supporting',
         'items': ['Critics Reviews', 'Audience Reviews', 'Trailer', 'Where to Watch']},
        {'id': 'P2', 'name': 'Engagement', 'bill': 'Featuring',
         'items': ['Watchlist', 'Write a Review', 'Share']},
        {'id': 'P3', 'name': 'Discovery', 'bill': 'With',
         'items': ['Related Movies', 'What to Watch', 'Additional clips and videos']},
    ],
    'chart_label': 'Where each element sits on the page',
    'chart_note': 'Top of each module in px, measured on the 1440-wide Figma frames of the original and the redesign.',
    # (label, tier, y in the original, y in the redesign)
    'moves': [
        ('Ratings', 'P0', 706, 228),
        ('Rent or stream action', 'P1', 890, 824),
        ('Where to Watch', 'P1', 1026, 964),
        ('Full synopsis', 'P0', 4376, 1097),
        ('Critics Reviews', 'P1', 1649, 1320),
        ('Audience Reviews', 'P1', 2037, 2184),
        ('Cast & Crew', 'P3', 2615, 3173),
        ('Videos', 'P3', 2875, 3490),
        ('More Like This', 'P3', 3185, 3890),
    ],
    'page_old': 6074,
    'page_new': 5226,
}

DECISIONS = {
    'headline': 'Key design decisions',
    'lead': 'Four decisions, each traced from a problem to what changed.',
    'labels': ['Problem', 'Insight', 'Design decision', 'Design outcome'],
    'items': [
        {
            'n': '01', 'id': 'decision-first', 'title': 'Put the movie decision first',
            'problem': 'Title, scores and actions were split across the hero, a card below it and a sticky bar, while ads and a video rail held the first screen.',
            'insight': 'The first screen has to answer “is this worth my time?” even when it also carries an ad.',
            'decision': 'Consolidate title, ratings, metadata and primary actions in one hero. Keep ratings visible when advertising is present, and keep the trailer as a cinematic element, with muted playback and visible controls.',
            'outcome': 'In the same 1440×900 frame, both scores, the rental action and Watchlist now sit above the fold, beneath a 90px ad slot.',
            'hypothesis': 'Exploring autoplay: whether muted playback helps or distracts is untested.',
            'statement': 'Ratings should do more than summarize reception. They should help users understand why a movie is worth considering.',
        },
        {
            'n': '02', 'id': 'two-voices', 'title': 'Give Critics and Audience different voices',
            'problem': 'Both review types shared one carousel card. Above the fold, the two pinned audience reviews were the same off-topic joke, marked Verified.',
            'insight': 'Critics are read for authority, audiences for volume. Identical cards flatten that difference.',
            'decision': 'Stack the two vertically and let each set its own rhythm, instead of forcing both into matching side-by-side cards.',
            'outcome': 'Critics read like a newspaper page. Audience reads like a fast, dense feed.',
            'voices': [
                {'name': 'Critics Reviews', 'dir': 'Newspaper-inspired editorial typography',
                 'points': ['Editorial credibility', 'Publication and critic identity', 'Original review excerpts', 'Critic ratings and links to full reviews']},
                {'name': 'Audience Reviews', 'dir': 'A streamlined, information-dense review feed',
                 'points': ['Quick scanning of multiple opinions', 'Star ratings and verification status', 'Review content prioritized over reviewer identity', 'Compact and readable list presentation']},
            ],
            'statement': 'Different sources deserve different reading experiences.',
        },
        {
            'n': '03', 'id': 'transparent', 'title': 'Make ratings more transparent',
            'problem': 'The fresh and rotten split and the average score were hidden behind an icon that didn’t look clickable. Reviews couldn’t be filtered on the page.',
            'insight': 'If people doubt a single percentage, the answer is to show the evidence behind it, not a bigger number.',
            'decision': 'Open each review section into a drawer that keeps the page in place, with filters for critics and a rating breakdown for audiences.',
            'outcome': 'Both scores can be inspected without leaving the movie page.',
            'voices': [
                {'name': 'For Critics', 'dir': 'Expanded Critics Reviews',
                 'points': ['Filters for Top Critics, Fresh, and Rotten', 'Publication identity and review excerpts', 'Access to full reviews']},
                {'name': 'For Audience', 'dir': 'Expanded Audience Reviews',
                 'points': ['Average rating', 'Star-rating distribution', 'Verified user reviews', 'Helpful feedback indicators']},
            ],
            'note': 'Star distribution and helpful counts are illustrative placeholders.',
            'statement': 'Make ratings more transparent, not just more prominent.',
        },
        {
            'n': '04', 'id': 'next-step', 'title': 'Make watching the natural next step',
            'problem': 'The main button said STREAM NOW but led to renting or buying on Fandango. Where to Watch held a single logo.',
            'insight': 'The moment someone decides to watch is also where user intent and commercial distribution meet.',
            'decision': 'Name the real action and price in the hero, place Where to Watch directly beneath it, and keep the rental action in the sticky header once the hero scrolls away.',
            'outcome': 'The button says what it actually does, and every provider sits directly beneath the hero.',
            'note': 'Prices shown are placeholders.',
            'statement': 'Once users decide a movie is worth watching, finding where to watch it should be effortless.',
        },
    ],
}

EXPERIENCE = {
    'headline': 'A more focused movie experience.',
    'lead': 'The complete redesigned movie detail page, then a closer look at each part.',
    'sections': [
        {'name': 'Hero and ratings', 'image': 'final-hero', 'y': 164, 'h': 800},
        {'name': 'Where to Watch', 'image': 'final-where', 'y': 964, 'h': 93},
        {'name': 'Movie overview', 'image': 'final-overview', 'y': 1057, 'h': 215},
        {'name': 'Critics Reviews', 'image': 'final-critics', 'y': 1320, 'h': 816},
        {'name': 'Audience Reviews', 'image': 'final-audience-ad', 'y': 2184, 'h': 831},
        {'name': 'Cast and Crew', 'image': 'final-cast', 'y': 3173, 'h': 317},
        {'name': 'Related Movies and additional media', 'image': 'final-media', 'y': 3490, 'h': 858},
        {'name': 'End credits', 'image': 'final-credits', 'y': 4348, 'h': 800},
    ],
    'interactions': [
        {'name': 'Sticky navigation', 'video': 'clip-sticky', 'body': 'Scores and the rental action stay reachable once the hero scrolls away.'},
        {'name': 'Critics Reviews, expanded', 'video': 'clip-critics', 'body': 'Filter by Top Critics, Fresh and Rotten.'},
        {'name': 'Audience Reviews, expanded', 'video': 'clip-audience', 'body': 'Average rating, distribution and verified reviews.'},
        {'name': 'Rent, then choose a provider', 'video': 'clip-watch', 'body': 'The action leads straight to Where to Watch.'},
    ],
    'interactions_note': 'Screen recordings of the working HTML prototype.',
}

REFLECTION = {
    'headline': 'Bringing Rotten Tomatoes back to the decision that matters.',
    'closing': [
        'The redesign brings Rotten Tomatoes closer to its most important job: helping people make more informed movie decisions.',
        'By prioritizing ratings, giving critics and audience reviews distinct reading experiences, and making the path to watching more direct, the experience becomes more focused while respecting the commercial realities of the platform.',
    ],
    'columns': [
        {'title': 'What the redesign addresses',
         'items': ['Scores and actions reach the first screen', 'Critics and audiences get their own reading experience', 'Both scores can be inspected in place', 'The path from deciding to watching is direct']},
        {'title': 'What remains unvalidated',
         'items': ['No usability testing has been run yet', 'Whether muted autoplay helps or distracts', 'Whether advertisers and partners accept the new placements', 'Whether moving ratings up changes what people decide']},
        {'title': 'What could come next',
         'items': ['Test the page with real moviegoers', 'Design the mobile experience in depth', 'Extend poster-derived color across the catalog', 'Connect live streaming prices and availability']},
    ],
}

# Measured from the two 1440-wide Figma frames. Boxes are (x, y, w, h) in page px.
ZONES_OLD = {
    'ads': [(170, 0, 1100, 100), (186, 1507, 728, 142), (954, 1327, 300, 290), (186, 4234, 728, 142), (170, 5676, 1100, 110), (561, 816, 317, 60)],
    'video': [(186, 552, 1084, 136), (186, 2875, 728, 310), (186, 3667, 728, 310)],
    'recs': [(954, 722, 300, 605), (186, 3185, 728, 482)],
    'core': [(186, 706, 728, 250), (186, 1026, 728, 239), (186, 1265, 728, 242), (186, 1649, 728, 388), (186, 2037, 728, 322), (186, 4376, 728, 1276)],
}
PAGE_W = 1440
FOLD = 900
