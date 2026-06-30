class Selectors:

    PING_MY_URLS = {
        "url_input": "#furl",
        "submit_button_role": "Submit Now",
    }

    PINGOMATIC = {

        # Input Fields
        "blog_name": "input[name='title']",

        "homepage": "input[name='blogurl']",

        "rss_url": "input[name='rssurl']",

    }

    BULKLINK = {

    # Text Area
    "url_input": "textarea",

    # Select All buttons
    "search_all": "#search_all",
    "ping_all": "#ping_all",

    }

    WMTOOLS = {

    "url_input": "textarea",

    }

    PREPOSTSEO = {

    "url_input": "textarea",

    "next_button": "#stepOne",

    }

    SMALLSEO = {

    "url_input": "textarea",

    "submit_button": "button:has-text('Ping Now')",

    }

    HCAPTCHA = {

    "iframe": "iframe[src*='hcaptcha']",

    "checkbox": "#checkbox",

    "challenge": ".challenge-container",

    }

    DUPLICHECKER = {

    "url_input": "input[name='url']",

    "submit_button": "button:has-text('Ping URL Now')",

    }

    TURNSTILE = {

        "iframe": "iframe[src*='turnstile']",

    }

    PINGLER = {

    # Ad iframe
    "ad_iframe": "iframe",

    "pause_button": "button:has-text('Pause')",

    # Form
    "title_input": "input[placeholder='Title (keyword)']",

    "url_input": "input[placeholder='http://pingler.com']",

    "other_checkbox": "label:has-text('Other') input",

    "submit_button": "button:has-text('Ping!')",

    }