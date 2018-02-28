images for conferences

{% for file in site.static_files %}
     * [{{ file.path }}]({{ site.baseurl }}{{ file.path }})
{% endfor %}
