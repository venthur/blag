Title: Hello World!
Description: Hello there, this is the first blog post. You should read me first.
Date: 2023-01-01 12:00
Tags: blag, pygments


## Hello World

This is an example blog post. Internally, blag differentiates between **pages**
and **articles**. Intuitively, pages are simple pages and articles are blog
posts. The decision whether a document is a page or an article is made
depending on the presence of the `date` metadata element: Any document that
contains the `date` metadata element is an article, everything else a page.

This differentiation has consequences:

* blag uses different templates: `page.html` and `article.html`
* only articles are collected in the Atom feed
* only articles are aggregated in the tag pages

For more detailed information, please refer to the [documentation][doc]

[doc]: https://blag.readthedocs.io


### Syntax Highlighting

```python
def foo(bar):
    """This is a docstring.

    """
    # comment
    return bar
```

Syntax highlighting is done via [Pygments][pygments]. For code blocks, blag
generates the necessary CSS classes by default, which you can use to style your
code using CSS. It provides you with a default light- and dark theme, for more
information on how to generate a different theme, please refer to [Pygments'
documentation][pygments].

[pygments]: https://pygments.org


### Next Steps

* Adapt the files in `templates` to your needs
* Check out the files in `static` and modify as needed
* Add some content
* Change the [favicon.ico](favicon.ico)
