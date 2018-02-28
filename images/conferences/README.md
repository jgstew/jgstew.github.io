
{% for file in site.static_files %}
  {% if (file.extname | downcase) == ".png" %}
* [{{ file.path }}]({{ site.baseurl }}{{ file.path }})
  {% endif %}
{% endfor %}
