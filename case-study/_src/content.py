"""All the copy for the case study, from Figma "Case Study" → A · Plates (292:1290).

Edit the text here, then run: python3 case-study/_src/build.py

Images: every `image` below is a file name in assets/img, without the .webp extension.
Videos: every `video` below is a name from _src/make_media.py. After adding or replacing an
upload in assets/video, run: python3 case-study/_src/make_media.py
"""

META = {
    'title': 'Rotten Tomatoes Redesign',
    'author': 'Cynthia Lu',
    'context': 'Product design take-home for Prelim, November 2026',
    'disclaimer': 'Independent concept. Not affiliated with Rotten Tomatoes, Fandango or the film’s rights holders. '
                  'Rotten Tomatoes marks, La La Land imagery and quoted reviews belong to their owners.',
}

LINKS = {
    'prototype': '../../design-explorations/B-prototype/index.html',
    'figma': 'https://www.figma.com/design/e40l8Q1wHbuS1qlspq4L4r/-Public-Rotten-Tomatoes-Redesign',
    'original': 'https://www.rottentomatoes.com/m/la_la_land',
}

NAV = [
    ('Intro', 'intro'),
    ('Research', 'research'),
    ('Limitations', 'limitations'),
    ('Design Decisions', 'decisions'),
    ('Reflection', 'reflection'),
]

INTRO = {
    'body': "Rotten Tomatoes has plenty of information about a movie, but finding what actually helps people decide "
            "whether to watch it isn't always easy. I wanted to rethink the movie page while keeping its core value "
            "and business model intact.",
    'buttons': [('Interactive Prototype', 'prototype', True), ('Figma Link', 'figma', False)],
    'caption_links': [('Original website', 'original'), ('Interactive Redesign', 'prototype')],
    # Scrolling wipes from `original` to `redesign`, in a frame shaped like the recordings (1908×1080).
    'original': {'image': 'old-first', 'alt': 'Original Rotten Tomatoes page, first screen'},
    'redesign': {'video': 'rt-hero', 'alt': 'Scrolling through the redesigned Rotten Tomatoes page'},
    'statement': 'Rotten Tomatoes has everything a moviegoer needs to know about a film. However, finding what '
                 'actually helps them make a decision can feel surprisingly difficult.',
    'question': 'How might we make Rotten Tomatoes better at helping people decide what to watch?',
}

RESEARCH = {
    'n': '01', 'label': 'Research',
    'lead': 'I combined heuristic evaluation with Reddit discussions to understand where the existing experience '
            'falls short and what users find confusing.',
    'heuristic': {
        'title': 'Heuristic evaluation',
        'body': 'The heuristic evaluation revealed two major issues: the ratings were easy to miss because of poor '
                'information hierarchy, and ads often competed with editorial content.',
        'issues': [
            'The first screen lacks a clear visual hierarchy. The Tomatometer and Popcornmeter are difficult to find, '
            'even though they are essential to helping users decide whether to watch a movie.',
            'Ads are mixed in with movie content, making it harder for users to focus on the information they came to see.',
        ],
        'images': [
            ('old-hierarchy', 'Original first screen: a red box marks the scores at the very bottom, below a large hero and partly covered by a floating ad'),
            ('old-ads-mixed', 'Original page: red boxes mark a tall ad, a banner ad and a floating ad placed among the photos and Movie Info'),
        ],
    },
    'community': {
        'title': 'Community discussions',
        'body': 'Community discussions pointed to confusion around the rating system, particularly the difference '
                'between Critics and Audience reviews and what the scores actually mean.',
        # Add the thread link as `url` to turn a username into a link.
        'cards': [
            {'title': 'Users are unclear about the difference between Critics and Audience reviews',
             'quotes': [
                 {'text': 'Why would there be such a difference? Which one should you trust more?', 'by': 'u/summernights64', 'url': ''},
             ]},
            {'title': 'Users want more transparency in movie scores',
             'quotes': [
                 {'text': "The 'Average rating' is hidden under 'see score details' for some reason, though I found it "
                          "to be a more reliable parameter than the percentage rating.", 'by': 'u/0iam', 'url': ''},
                 {'text': 'It only shows the completely useless percent.', 'by': 'u/Level-Pineapple3503', 'url': ''},
             ]},
        ],
    },
}

LIMITATIONS = {
    'n': '02', 'label': 'Limitations',
    'title': 'What needs to be preserved?',
    'decision': {
        'title': 'Support pre-viewing decision',
        'body': "I chose to focus on the main use case, which is the pre-viewing decision: someone has a particular "
                "movie in mind and wants to decide whether it's worth watching before finding where to stream or rent it.",
    },
    'journey': [
        {'step': 'Idea', 'q': 'What movie?', 'on': False},
        {'step': 'Evaluate / validate', 'q': 'Is it worth my time?', 'on': True},
        {'step': 'Decide', 'q': 'Where to watch?', 'on': False},
    ],
    'business': {
        'title': 'Be mindful of the business model',
        'body': 'Rotten Tomatoes is also an advertising and distribution business owned by Fandango. Ads and viewing '
                'options therefore need to remain part of the experience.',
    },
    'value': {
        'title': 'Make sure RT’s core value stands out',
        'body': 'Throughout the redesign, I wanted to keep its two signature rating systems at the center.',
    },
    'icons': ['splat', 'tomato', 'popcorn', 'spilled'],
}

DECISIONS = {
    'n': '04', 'label': 'Design Decisions',
    'title': 'Key Design Decisions',
    'image': 'still-hero-poster',
    'items': [
        {
            'n': '01', 'title': 'Reorganizing the first impression',
            'rows': [
                {'video': 'hero-interactions', 'alt': 'Redesigned hero with the trailer, ratings and rental action', 'text': [
                    'I wanted users to get a sense of whether a movie is worth watching as soon as they land on the '
                    'page. In the original layout, secondary videos took up much of the first screen, while the '
                    'Tomatometer and Popcornmeter were difficult to find.',
                    "I moved the ratings, essential movie information, and primary actions higher in the hierarchy, "
                    "removed secondary videos, and added a quote from a Top Critic to give users an immediate sense "
                    "of the film's reception.",
                    'I also wanted the page to feel more connected to the movie itself. I used a dark background '
                    'inspired by its poster and made the trailer the visual centerpiece, creating a more immersive '
                    'introduction to the film.',
                ]},
            ],
        },
        {
            'n': '02', 'title': 'Separating advertising from editorial content',
            'rows': [
                {'video': 'ads', 'alt': 'Scrolling past dedicated ad space on the redesigned page', 'text': [
                    "Since advertising is part of Rotten Tomatoes' business model, removing it wasn't a realistic "
                    "solution. The real issue was how easily ads blended into the editorial experience.",
                    "I reserved dedicated space for advertising so it wouldn't overlap with essential movie "
                    "information. I also used differences in container width, background, corner radius, and spacing "
                    "to make the distinction clearer while keeping ads within the page.",
                ]},
            ],
        },
        {
            'n': '03', 'title': 'Giving critics and audiences different voices',
            'rows': [
                {'image': 'x-side-by-side', 'alt': 'Early exploration: Critics and Audience Reviews side by side in matching cards',
                 'tag': 'One of early explorations', 'tile': True, 'text': [
                    'I initially explored a side-by-side layout with similar visual treatments for both review types. '
                    'However, I realized that readers look for different things in each section, so I chose a vertical '
                    'layout with distinct visual treatments.',
                ]},
                {'video': 'critics-reviews', 'alt': 'Filtering Critics Reviews and opening the expanded panel', 'text': [
                    "For Critics Reviews, the source is an important part of the review's credibility. I drew "
                    "inspiration from newspaper layouts, giving more prominence to the publication and original review excerpt.",
                ]},
                {'video': 'audience-reviews', 'alt': 'Reading Audience Reviews and writing a review', 'text': [
                    'For Audience Reviews, the opinions themselves matter more than who wrote them. I used a familiar '
                    'discussion-style layout that puts comments first, gives them more room, and makes space for user interaction.',
                ]},
            ],
        },
        {
            'n': '04', 'title': 'Making reviews more transparent',
            'rows': [
                {'video': 'rating-ratio', 'alt': 'Average rating and rating distribution in the Audience Reviews panel', 'text': [
                    'A single Audience Score can hide very different rating patterns. Two movies could both score 82%, '
                    'even though one receives consistently high ratings while the other has a much wider spread.',
                    'I added the average rating and rating distribution to the Audience Reviews panel, allowing users '
                    'to see the sentiment behind the percentage.',
                ]},
                {'video': 'hover-explanations', 'alt': 'Hover explanations on the Critics and Audience ratings', 'text': [
                    'I also added hover explanations to both Critics and Audience ratings. Since users may not know '
                    'what each score represents, these explanations make the rating systems easier to understand '
                    'without requiring them to leave the page.',
                ]},
            ],
        },
    ],
}

REFLECTION = {
    'n': '06', 'label': 'Reflection',
    'title': 'Reflections',
    'image': 'still-end-still',
    'text': [
        "This project turned out to be quite different from what I initially expected. During research, I became "
        "interested in a trade-off I hadn't anticipated: how can Rotten Tomatoes support its advertising business "
        "without compromising the experience people come for?",
        'The first time I visited the site, I was greeted by an ad for a shoe brand, completely unrelated to movies. '
        'It made me think about how irrelevant advertising can disrupt the consistency of an experience and, over '
        'time, affect how much users trust the platform.',
        'I came to believe that monetized content needs clear boundaries. In my redesign, I explored this through '
        'dedicated ad space and subtle visual distinctions, such as background colors and padding. These small changes '
        'help separate ads from editorial content without requiring advertising to disappear.',
        "Given more time, I'd like to explore where that boundary should be. For example, how much visual separation "
        "is enough? Could ad relevance be considered alongside placement? And how can we evaluate the impact of these "
        "choices on both user experience and ad performance?",
    ],
}
