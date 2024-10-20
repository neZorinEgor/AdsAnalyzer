# Создание страницы, унаследованной от базовой

```html
{% extends 'components/base.html' %}

{% block title%}Тут будет title страницы{% endblock %}
{% block create     %}p-2 transition hover:bg-gray-200 rounded block text-lg text-black hover:text-black{% endblock %}
{% block my_backend %}p-2 transition hover:bg-gray-200 rounded block text-lg text-black hover:text-black{% endblock %}
{% block manual     %}p-2 transition hover:bg-gray-200 rounded block text-lg text-black hover:text-black{% endblock %}


{% block content %}
Тут будет информация в основном блоке
{% endblock %}
```