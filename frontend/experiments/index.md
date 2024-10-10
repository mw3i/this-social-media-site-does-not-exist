---
layout: root.html
title: Experiments
pagination:
  data: collections.experiments
  size: 1000
  alias: experiment
---

<section class="section">
    <div class="container is-max-desktop">
        <div class="columns is-centered">
            <div class="column is-three-quarters">
                <div class="columns is-multiline">
                    {% for experiment in pagination.items %}
                    <!-- experiment Card -->
                    <div class="column is-full has-background-grey-darker my-5" style='border-radius: 15px;'>
                        <a href="{{ baseUrl }}/{{ experiment.url }}" class="card has-background-grey-darker">
                            <div class="card-content">
                                <p class="title has-text-white">{{ experiment.data.title }}</p>
                            </div>
                        </a>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</section>
