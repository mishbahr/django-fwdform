=============================
django-fwdform
=============================

.. image:: http://img.shields.io/travis/mishbahr/django-fwdform.svg?style=flat-square
    :target: https://travis-ci.org/mishbahr/django-fwdform/

.. image:: http://img.shields.io/pypi/v/django-fwdform.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-fwdform/
    :alt: Latest Version

.. image:: http://img.shields.io/pypi/dm/django-fwdform.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-fwdform/
    :alt: Downloads

.. image:: http://img.shields.io/pypi/l/django-fwdform.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-fwdform/
    :alt: License

.. image:: http://img.shields.io/coveralls/mishbahr/django-fwdform.svg?style=flat-square
  :target: https://coveralls.io/r/mishbahr/django-fwdform?branch=master

Simple and painless form processing for static sites.


Why?
----

I have several sites hosted on AWS S3 for pennies a month... and I didn't want to
pay $20 per month (per form) for processing contact forms!

**20+ domains powered by 1 Heroku app = Profit!**


Demo
----

Coming soon.

Features
--------

* Multi site support.
* Unlimited forms
* Unlimited submissions
* Spam Protection via Akismet.
* Submit forms with AJAX.
* REST API to manage forms.


Quickstart
----------

1. Install ``django-fwdform``::

    pip install django-fwdform

2. Add ``fwdform`` to ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'corsheaders',
        'fwdform',
        ...
    )

3. Sync database::

    python manage.py migrate


4. Add ``fwdform.urls`` to your project's urls module::

    urlpatterns = patterns(
        ...
        url(r'^', include('fwdform.urls', namespace='fwdform')),
        ...
    )



Dependencies
------------

This package requires ``django-cors-headers`` to be installed and configured correctly. When ``django-fwdform`` is installed using pip, ``django-cors-headers`` is automatically installed.

You will need to add corsheaders middleware class to ``MIDDLEWARE_CLASSES`` settings::

    MIDDLEWARE_CLASSES = (
        ...
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        ...
    )

Note that ``CorsMiddleware`` needs to come before Django's ``CommonMiddleware``.

For more information, see https://github.com/ottoyiu/django-cors-headers


Sample Form
-----------

::

    <form action="//example.com/send/<form_hash>/" method="POST">
        <input type="text" name="name" required="required"/>
        <input type="email" name="email" required="required" />
        <textarea name="message" rows="5"></textarea>
        <input type="submit" value="Send">
    </form>


Special Form Inputs
*******************

**_next**

By default, after submitting a form the user is shown the FwdForm "Thank You" page. You can provide an alternative URL for that page. ::

    <input type="hidden" name="_next" value="//example.com/thanks.html" />


**_subject**

This value is used for the email's subject::

    <input type="hidden" name="_subject" value="Contact Form" />

**_gotcha**

Add this "honeypot" field. If a value is provided, the submission will be silently ignored. The input should be hidden with CSS::

    <input type="text" name="_gotcha" style="display:none;" />

**name/email/message**

Span prevention via Akismet - Spam checker backend looks for these specially named form inputs::

    <input type="text" name="name" placeholder="Your Name">
    <input type="email" name="email" placeholder="Your Email">
    <textarea name="message" rows="5"></textarea>

Rest API
--------

Register a form, this returns a hashid for the newly created form::

    $ curl --data "name=Contact%20Form&recipients=conttact@example.com" http://example.com/<site_token>/
    {"hashid": "0rPGVlYZWqMRE8OebjoM1ogpmvNL23A9dxJzywQD"}

Update existing form config by passing a known ``hashid`` as a param::

    $ curl --data "recipients=hello@example.com&hashid=0rPGVlYZWqMRE8OebjoM1ogpmvNL23A9dxJzywQD" http://example.com/<site_token>/


AJAX Submission
---------------

You can use fwdform via AJAX. This even works cross-origin.

If you're using jQuery this can be done like so::

    $.ajax({
        url: $form.attr("action"),
        method: "POST",
        data: $form.serialize(),
        dataType: "json",
        headers: {"X-Requested-With": "XMLHttpRequest"},
    });
