"""
Warning: contains a lot of opinions and experiences of the author. Proceed at your own risk!
"""

_RAW_MESSAGES = {
    """
    identifier-to-message hastable
    identifier is case insensitive and can be a multiple, split by "|" character
    note: all identifiers have to be unique (synonyms included) - duuuh
    """
    # python
    "python": "My favorite programming language <3",
    "fastapi": "this is made with fast api! :)",
    "flask": "My first intro to web APIs and it's great! Though fastapi is my to go alternative these days.",
    "celery": "ah old friend - lots of hate and love with this one",
    "pydantic": "love and hate relationship with this one - a must tool but the API is just so awkward.",
    "django": "it does everything! My favorite CMS system - big fan of model-view-template architecture!",
    "scrapy": "I've been #1 contributor on stackoverflow on this subject several times :) Absolutely lovely framework except that it's showing it's age a bit",
    "jupyter": "Distributing web-scrapers in notebooks makes for a cool ddos network!",
    "sqlalchemy": "Best DB orm imho except that optimizing batching is awfully complex at times. Also I wish it was more opinionated.",
    # "black": "",  # too broad :|
    # monitoring
    "prometheus": "the flame of stat tracking! My favorite part about it is that the server is scraping clients rather than other way around - so convenient ot manage",
    "grafana": "my favorite stat front-end! Combined with prometheus <3",
    # enemies
    "cloudflare": "my arch nemesis! Once I saw them sell a service that runs caesar cipher in js to obfuscate emails 😂",
    "captcha": "my arch nemesis - have you every tried to login to your spotify account in a shared IP internet cafe?",
    # ML stuff
    "machine learning": "I once wrote a giant AI broad crawler called shoggoth (the many-eyed monster from H.P. Lovecraft!)",
    "nlp": "this tool uses a bit of NLP. Check out the github source for more!",
    # DB stuff
    "elasticsearch": "fast text search! I've heard postgresql's full text search can perform really closely - would love to pit these two against each other!",
    "mysql|mariadb": "I prefer postgresql but for the most part both do the trick just the same!",
    "sqlite": "Convenient tiny database! My to-go when postgresql is not available and SQL is needed.",
    "sql": "I'm more of a nosql guy myself but I have to admit that SQL is slowly winning me over through modern ORM and postgresql",
    "nosql": "I love the philosophy that query computing should be done by code not query language!",
    "couchbase": "My first doc db - lots of love and hate with this one but it worked for the most part!",
    "redis": "honestly, my best friend for quick storage! This project uses redis as a cache as well!",
    # soft skills
    "remote": "I like working from coworking spaces or at my home setup as I can use mechanical keyboards without annoying people 😅",
    "communication|documentation|docs|mentor": "I love docs and technical writing in general! My favorite docstring style is numpy and auto doc platfom pdoc.",
    "education": "I love teaching people tech stuff. I have over 18k stackoverflow reputation and run a education platform on web-scraping and reverse-engineering at https://scrapecrow.com",
    # me.properties
    "thailand": "I've been staying in Thailand for few years now! Currently in Koh Tao trying to see a whale shark 🐋",
    "lithuania": "Hey, I'm from here! Grew up in Palanga and studied in Klaipeda :)",
    "finland": "I dive with a Finish center here in Koh Tao! 🍻",
    "estonia": "Lived there for a bit - lovely place! Tartu represent 💙",
    "japan": "Things just keep getting in a way of me visiting all the time :| One day!",
    "dogs": "I have rescue pup named Kobe (he's quite a jumper!)",
    # concepts
    "async": "Pop media doesn't show it but I bet robots would communicate asynchronously",
    "hacker": "Free Software Foundation supporter <3; I run arch btw. On a more serious note - I love hacking on everything. That's why I got into web-scraping and reverse-engineering and recently into 3D printing",
    "oss|foss|floss": "I run full libre machine! :) Checkout my <a href='https://github.com/granitosaurus'>github<a>!",
    "data science": "I prefer data hacker! Interactive shell on a dataset scratches that same hacking itch!",
    "task queue": "queues are fascinating! For big projects I prefer rabbitmq, smaller redis and recently I started dig into postgresql row locking as a queue which is really cool but I'm unsure how scallable it is!",
    # services
    "jsdelivr": "god bless these guys! 🙏",
    # languages
    "lua": "only used it in neovim scripts but it's pretty cool - would like to learn more!",
    "rust": "everyone's talking about it! Just waiting for an opportunity to get into it!",
    "nim": "love the language and love where it's going! Hadn't had the chance to make a big project using it just yet",
    "javascript": "it does the job I guess 😅",
    "typescript": "it's like javascript but with less hair pulling!",
    "python2": "🧟🐍!",
    "playwright": "when you're just too lazy to reverse-engineer fire up the most complex piece of software in the world! :)",
    # "go": "",  # TODO very board :|
    "ruby": "I actually switched to python from ruby back in college! Quite fond of both but Python won me over",
    # todo
    "php": "One time I was tasked writing a data aggregator using php. Not sure how that came to be but it almost worked! I've been purposefully avoiding it but I heard it's pretty workable these days!",
    "airflow": "the air goes right through it! (just like my knowledge of it 😆) I always wanted to give it a go though!",
    "saltstack": "heard a lot of mixed opinions but never got my hands on it just yet. Would love to give it a go!",
    "log management": "logs are awesome! I wrote some log processors myself which is generally not a great idea but it's a fun task!",
    # Toolsets
    "GNU": "The animal or one of the most important software projects ever made? I like both tho.",
    # webdev
    "react": "I wrote this in react first then though to myself - I can actually do it in vanilla JS! :)",
    "vue.js|vuejs": "I have more experience with React but I've heard loads of praises for this bad boy as well!",
    "bulma|bulma-css": "Use it on almost all of my projects!",
    "tailwind|tailwind-css": "I'm quite opposed to core principal of it but never tried it in a dynamic, fast-moving environment where, I heard, it shines!",
    "jquery": "xpath selectors as first class citizens is still awesome in 2021!",
    ## hardly know these
    "webflow": "ngl just looked it up: so that's what all the startup pages are using!",
    "openresty": "ngixn and lua - what a peculiar stack! How's the debugger? 🤔",
    # system
    "nginx": "rarely lets you down! Though I'm not a fan of the 'open core' licensing :|",
    "bash": "I ran away from bash to xonsh - python as a shell! Though unfortunately I do have to get back to bash once in a while and honestly, it's not that awful",
    "xonsh": "the best shell <3",
    # Deploy
    "github": '<a href="https://github.com/granitosaurus">check me out on github</a>. I kinda prefer gitlab tho 😅',
    "google cloud|gcloud": "this app is deployed on gcloud! god bless their free tier :P",
    "amazon-web-services|aws": "I prefer self hosting though aws is right there behind google cloud",
    "azure": "I prefer self hosting though I did spend my free 200$ credit on a badly optimized side project once - hey it's free!",
    "ci/cd|circleci|argocd": "As automation fan - this is one of the greatest devops inventions ever. My favorite being gitlab pipelines followed by quickly growing github actions!",
    "self-hosted": "cut the middleman! I love self-hosting as a free software enthusiast!",
    "devops": "I'm having trouble declining any sort of automation - automate everything!",
    "kubernetes": "containers made easy! After investing months to ease into them 😅",
    "nomad": "kubernetes made easy! Only got to play around with it few times but I really liked it!",
    "kafka": "I heard it might turn you into a big bug. It's the small sneaky ones that I'm afraid of.",
    "docker": "I run weird machines - so I love the idea of shipping my machine!",
    "docker-compose": "the sanity layer of docker <3",
    "linux|arch linux": "I run arch btw <3",
    "ansible": "automating the automation! Not my favorite but up there in top 3.",
    # employment
    "stock options|equity options": "best kind of motivation :)",
    "experiment": "",
    "international team": "big fan of international environments - it's great to have someone to chat with on those nights where you can't sleep and would rather get something done!",
}
# flatten raw message synonyms into a single layer
MESSAGES = {}
for k, v in _RAW_MESSAGES.items():
    if synonyms := k.split("|"):
        for syn in synonyms:
            MESSAGES[syn] = v
    else:
        MESSAGES[k] = v
